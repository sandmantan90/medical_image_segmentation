# experiment.py

import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from totalsegmentator.python_api import totalsegmentator
from pathlib import Path
from segmentation import save_combined_segmentation

### Loading and Processing Functions ###

def load_nifti(file_path):
    """
    Load a NIfTI file and return the image data.
    
    Args:
        file_path (str): Path to the .nii or .nii.gz file.
        
    Returns:
        np.ndarray: Image data as a NumPy array.
    """
    img = nib.load(file_path)
    return img.get_fdata()

def binarize_data(data, threshold=0.5):
    """
    Binarize the input data at the specified threshold.
    
    Args:
        data (np.ndarray): Input array.
        threshold (float): Threshold value for binarization.
        
    Returns:
        np.ndarray: Binarized data.
    """
    return (data > threshold).astype(np.float32)

### Dice Score Calculation ###

def dice_score(y_true, y_pred):
    """
    Calculate Dice score between two binary masks.
    
    Args:
        y_true (np.ndarray): Ground truth binary mask.
        y_pred (np.ndarray): Predicted binary mask.
        
    Returns:
        float: Dice score.
    """
    if y_true.sum() == 0 and y_pred.sum() == 0:
        return 1.0
    intersect = np.sum(y_true * y_pred)
    denominator = np.sum(y_true) + np.sum(y_pred)
    f1 = (2 * intersect) / (denominator + 1e-6)
    return f1

### Augmentation and Experimentation Functions ###

def apply_gaussian_blur(data, sigma):
    """
    Apply Gaussian blur to a 3D volume.
    
    Args:
        data (np.ndarray): 3D image data.
        sigma (float): Standard deviation for Gaussian kernel.
        
    Returns:
        np.ndarray: Blurred image data.
    """
    return gaussian_filter(data, sigma=sigma)

def run_totalsegmentator(input_data, output_dir):
    """
    Run TotalSegmentator on the blurred input data.
    
    Args:
        input_data (np.ndarray): Blurred 3D input data for segmentation.
        output_dir (Path): Directory to store segmentation output.
        
    Returns:
        np.ndarray: Segmented output as a NumPy array.
    """
    # Save the blurred image temporarily to run TotalSegmentator
    blurred_path = output_dir / "blurred_input.nii.gz"
    nib.save(nib.Nifti1Image(input_data, affine=np.eye(4)), str(blurred_path))
    
    # Run TotalSegmentator on the blurred input
    totalsegmentator(str(blurred_path), output=str(output_dir), fastest=True)
    

    data = save_combined_segmentation(output_dir)
    return data

def calculate_dice_vs_blur(gt_path, input_path, output_dir, blur_range=(0, 15), blur_steps=10):
    """
    Calculate Dice score for different levels of Gaussian blur on input data.
    
    Args:
        gt_path (str): Path to the ground truth NIfTI file.
        input_path (str): Path to the original input NIfTI file.
        output_dir (str): Directory to save temporary files.
        blur_range (tuple): Range of Gaussian blur sigma values to test.
        blur_steps (int): Number of blur levels to test.
        
    Returns:
        list: List of blur levels.
        list: List of corresponding Dice scores.
    """
    gt_data = binarize_data(load_nifti(gt_path))
    input_data = load_nifti(input_path)
    
    blur_levels = np.linspace(blur_range[0], blur_range[1], blur_steps)
    dice_scores = []
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for sigma in blur_levels:
        # Apply Gaussian blur to input data
        blurred_input = apply_gaussian_blur(input_data, sigma)
        
        # Run TotalSegmentator on the blurred input and get the segmented output
        segmented_output = run_totalsegmentator(blurred_input, output_dir)
        segmented_output = binarize_data(segmented_output)
        
        # Calculate Dice score and append to list
        dice = dice_score(gt_data, segmented_output)
        dice_scores.append(dice)
        print(f"Sigma: {sigma:.2f}, Dice Score: {dice:.4f}")
    
    return blur_levels, dice_scores

### Plotting Function ###

def plot_dice_vs_blur(blur_levels, dice_scores):
    """
    Plot Dice score vs. Gaussian blur level.
    
    Args:
        blur_levels (list): List of Gaussian blur sigma values.
        dice_scores (list): List of corresponding Dice scores.
    """
    plt.figure(figsize=(8, 6))
    plt.plot(blur_levels, dice_scores, marker='o', linestyle='-')
    plt.title("Dice Score vs. Gaussian Blur Level")
    plt.xlabel("Gaussian Blur Sigma")
    plt.ylabel("Dice Score")
    plt.grid()
    plt.show()

### Main Execution ###

def main():
    gt_path = r"C:\Users\admin\Downloads\Totalsegmentator_dataset_small_v201\s1403\segmentations\_combined_20241102_185803.nii"       # Update to your ground truth path
    input_path = r"C:\Users\admin\Downloads\Totalsegmentator_dataset_small_v201\s1403\ct.nii.gz"       # Update to your input CT path
    output_dir = 'output_directory_exp'       # Update to your desired output directory

    blur_levels, dice_scores = calculate_dice_vs_blur(gt_path, input_path, output_dir, blur_range=(0, 50), blur_steps=10)
    plot_dice_vs_blur(blur_levels, dice_scores)

if __name__ == "__main__":
    main()

import os
import numpy as np
from pathlib import Path
from totalsegmentator.python_api import totalsegmentator
from utils import load_nifti_file, save_combined_nifti, get_timestamp

def run_totalsegmentator(ct_path, output_directory, task = 'total'):
    """
    Run TotalSegmentator on the given CT file and store the output in a specific folder.
    
    Args:
        ct_path (str): Path to the CT scan.
        output_directory (str): Directory where the output segmentations will be stored.
    """
    
    # Run TotalSegmentator with the constructed output path
    totalsegmentator(ct_path, output=str(output_directory), task = task, fast=True)
    print(f"TotalSegmentator output saved to: {output_directory}")
    return output_directory

def combine_segmentations(output_directory):
    """
    Combine multiple segmentation NIfTI files into a single volume, assigning unique class labels to each.
    
    Args:
        output_directory (str): Directory where the NIfTI files are located.
        
    Returns:
        np.ndarray: Combined segmentation data as a NumPy array with unique class labels.
        np.ndarray: The affine transformation matrix from one of the NIfTI files.
    """
    # Get a list of all .nii files in the output directory
    nii_files = [f for f in os.listdir(output_directory) if f.endswith('.nii.gz')]
    
    # Load the first image to get the dimensions and affine matrix
    first_file_path = os.path.join(output_directory, nii_files[0])
    sample_data, affine = load_nifti_file(first_file_path)
    
    # Create an empty array to hold the combined segmentations (same shape as the first file)
    combined_data = np.zeros(sample_data.shape, dtype=np.uint8)
    
    # Assign unique labels for each organ (starting from 1)
    for idx, nii_file in enumerate(nii_files, start=1):
        file_path = os.path.join(output_directory, nii_file)
        data, _ = load_nifti_file(file_path)

        # Assume binary segmentation (0 = background, 1 = organ), assign unique label (idx) to the organ
        combined_data[data > 0] = idx
        
        print(f"Combined segmentation for {nii_file} with label {idx}.")
    
    return combined_data, affine


def save_combined_segmentation(output_path):
    combined_data, affine = combine_segmentations(output_path)
    combined_output_path = Path(output_path) / f"_combined_{get_timestamp()}.nii"
    save_combined_nifti(combined_data, affine, combined_output_path)
    return combined_data
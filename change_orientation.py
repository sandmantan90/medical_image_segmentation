import nibabel as nib
import numpy as np
from pathlib import Path

def load_nifti_file(file_path):
    """
    Load a NIfTI file and return the image data and affine matrix.
    
    Args:
        file_path (str): Path to the .nii file.
        
    Returns:
        tuple: A tuple containing the image data as a NumPy array and the affine matrix.
    """
    img = nib.load(file_path)
    data = img.get_fdata()
    affine = img.affine
    return data, affine

def flip_and_save_nifti(data, affine, output_directory, file_name_prefix):
    """
    Flip the NIfTI image data in different directions and save each version.
    
    Args:
        data (np.ndarray): Image data to flip.
        affine (np.ndarray): Affine matrix for NIfTI file.
        output_directory (str): Directory where flipped files will be saved.
        file_name_prefix (str): Prefix for each output file name.
    """
    output_dir = Path(output_directory)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Define flipping operations
    flip_operations = {
        "flip_x": np.flip(data, axis=0),
        "flip_y": np.flip(data, axis=1),
        "flip_z": np.flip(data, axis=2),
        "flip_xy": np.flip(np.flip(data, axis=0), axis=1),
        "flip_xz": np.flip(np.flip(data, axis=0), axis=2),
        "flip_yz": np.flip(np.flip(data, axis=1), axis=2),
        "flip_xyz": np.flip(np.flip(np.flip(data, axis=0), axis=1), axis=2),
    }

    # Save each flipped version as a new NIfTI file
    for flip_name, flipped_data in flip_operations.items():
        output_file = output_dir / f"{file_name_prefix}_{flip_name}.nii.gz"
        flipped_img = nib.Nifti1Image(flipped_data, affine)
        nib.save(flipped_img, str(output_file))
        print(f"Saved flipped image: {output_file}")

if __name__ == "__main__":
    # Path to the original mask file
    mask_file_path = r"C:\Users\admin\Desktop\KetanFiles\UCSD\FCRL-Lab\Total_segmentator\code\output_new\EARLIST_TO_LATEST_301_200_percent_segmentation_20241030_222607_combined_20241030_222607.nii"
    
    # Load the mask file
    mask_data, mask_affine = load_nifti_file(mask_file_path)
    
    # Output directory to save flipped images
    output_directory = "output_flipped_masks_20241030_222607"
    
    # Flip and save
    flip_and_save_nifti(mask_data, mask_affine, output_directory, "mask")

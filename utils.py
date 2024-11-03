import nibabel as nib
import yaml
from datetime import datetime
from pathlib import WindowsPath

def get_timestamp():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    return timestamp

def load_config(config_file):
    """
    Load the configuration file (config.yml).
    
    Args:
        config_file (str): Path to the config.yml file.
        
    Returns:
        dict: Dictionary containing all the configuration parameters.
    """
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

def load_nifti_file(file_path):
    """
    Load a NIfTI file and return the image data and the affine transformation.
    
    Args:
        file_path (str): Path to the .nii file.
        
    Returns:
        tuple: A tuple containing the image data as a NumPy array and the affine matrix.
    """
    img = nib.load(file_path)
    data = img.get_fdata()
    affine = img.affine
    return data, affine

def save_combined_nifti(combined_data, affine, output_path):
    """
    Save the combined segmentation data as a NIfTI file.
    
    Args:
        combined_data (np.ndarray): Combined segmentation data as a NumPy array.
        affine (np.ndarray): Affine transformation matrix for the NIfTI file.
        output_path (str): Path to save the combined NIfTI file.
    """
    combined_img = nib.Nifti1Image(combined_data, affine)
    nib.save(combined_img, output_path)
    print(f"Combined NIfTI file saved at {output_path}.")

def find_ct_files(base_directory):
    """
    Recursively find all 'ct.nii.gz' files in the base directory.

    Args:
        base_directory (Path): Path to the base directory.

    Returns:
        list: List of Paths to each 'ct.nii.gz' file found.
    """
    ct_files = []
    for ct_file in base_directory.rglob('*nii.gz'):
        ct_files.append(ct_file)
    return ct_files

def create_output_directory(ct_file: WindowsPath, parent_path: WindowsPath = None):
    """
    Create an output directory called 'TotalSegmentator' at the same level as the CT file.

    Args:
        ct_file (Path): Path to the 'ct.nii.gz' file.

    Returns:
        Path: Path to the created 'TotalSegmentator' folder.
    """
    # Get the current date and time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_folder_name = f"TotalSegmentator_{ct_file.parent.name}_{ct_file.stem}_seg_{timestamp}"
    if not parent_path:
        parent_path = ct_file.parent

    output_directory = parent_path / output_folder_name
    output_directory.mkdir(exist_ok=True)

    return output_directory


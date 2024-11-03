import numpy as np
import nibabel as nib
from scipy.ndimage import gaussian_filter
from skimage.transform import rescale
from pathlib import Path

def load_nifti(file_path):
    """
    Load a NIfTI file and return its data and affine.
    """
    img = nib.load(file_path)
    return img.get_fdata(), img.affine

def save_nifti(data, affine, output_path):
    """
    Save a 3D NumPy array as a NIfTI file.
    """
    img = nib.Nifti1Image(data, affine)
    nib.save(img, output_path)

def add_gaussian_noise(data, mean=0, std_dev=0.05):
    """
    Add Gaussian noise to the 3D image data.
    """
    max_pixel = data.max()
    lamda= .5
    noise = np.random.normal(mean, std_dev, data.shape)
    return data + max_pixel * noise * lamda

def blur_in_direction(data, sigma, axis):
    """
    Apply Gaussian blurring in a specific direction.
    """
    blurred_data = np.copy(data)
    gaussian_filter(data, sigma=sigma, output=blurred_data, mode='nearest', axes=axis)
    return blurred_data

def downsample(data, scale=(0.5, 1, 1)):
    """
    Downsample the 3D image by a specified scale factor.
    Scale factor should be a tuple for (depth, height, width).
    """
    return rescale(data, scale, anti_aliasing=True, preserve_range=True)

def augment_ct_volume(ct_file, output_dir):
    """
    Perform multiple augmentations on a 3D CT volume and save each one.
    """
    data, affine = load_nifti(ct_file)
    ct_name = Path(ct_file).stem
    output_dir = Path(output_dir) / f"{ct_name}_augmented"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Augmentation 1: Add Gaussian Noise
    noisy_data = add_gaussian_noise(data)
    save_nifti(noisy_data, affine, output_dir / f"{ct_name}_noisy.nii.gz")

    # Augmentation 2: Blur in SI direction (axis 0)
    si_blurred_data = blur_in_direction(data, sigma=2, axis=1)
    save_nifti(si_blurred_data, affine, output_dir / f"{ct_name}_blurred_SI.nii.gz")

    # Augmentation 3: Blur in other directions (axis 1 and 2)
    other_blurred_data = gaussian_filter(data, sigma=2, mode='nearest')  # Blur in AP direction
    save_nifti(other_blurred_data, affine, output_dir / f"{ct_name}_blurred_all.nii.gz")

    # Augmentation 4: Downsample to simulate fewer detectors
    downsampled_data = downsample(data, scale=(0.5, 1, 1))
    save_nifti(downsampled_data, affine, output_dir / f"{ct_name}_downsampled.nii.gz")

    print(f"Augmented data saved in {output_dir}")

# Main script
def main():
    ct_path = r"C:\Users\admin\Desktop\KetanFiles\UCSD\FCRL-Lab\Total_segmentator\dataset\TotalSegmentator\s1403\ct.nii.gz"  # Path to the original CT volume
    output_directory = "augmented_data"  # Output directory for augmented data
    augment_ct_volume(ct_path, output_directory)

if __name__ == "__main__":
    main()

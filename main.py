from segmentation import run_totalsegmentator, save_combined_segmentation
from utils import load_config, find_ct_files, create_output_directory
from pathlib import Path
from tqdm import tqdm


def main():
    # Load configuration from config.yml
    config = load_config('config.yml')
    
    # Run TotalSegmentator on the CT file
    ct_path = config['CT_PATH']
    base_output_directory = config['OUTPUT_DIRECTORY']
    output_directory = Path(base_output_directory)
    task = config['TASK']

    base_directory = Path(ct_path)

    # Step 1: Find all 'ct.nii.gz' files
    ct_files = find_ct_files(base_directory)
    print(f"Found {len(ct_files)} 'ct.nii.gz' files.")

    output_paths = []
    # Step 2: Run segmentation on each file with a progress bar
    for ct_file in tqdm(ct_files, desc="Processing CT files", unit="file"):
    
        # Create the output directory
        # Convert paths to pathlib.Path objects
        
        output_directory = create_output_directory(ct_file, parent_path = None)
        
        output_path = run_totalsegmentator(ct_file, output_directory, task)
        
        # Combine the segmentations
        combined_data = save_combined_segmentation(output_path)

        output_paths.append(output_path)
        print(f"Segmentation completed for {ct_file}")
        

if __name__ == "__main__":
    main()

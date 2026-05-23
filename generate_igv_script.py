import argparse
import time
import os
import re

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate IGV batch scripts for individual BAM files.")
    parser.add_argument('-b', '--bam-path', required=True, help="Path to the directory containing BAM files.")
    parser.add_argument('-s', '--snapshot-dir', required=True, help="Directory to save snapshots.")
    parser.add_argument('-g', '--genome', required=True, help="Path to the genome reference file.")
    parser.add_argument('-r', '--regions-file', required=True, help="Path to the file containing BAM regions.")
    parser.add_argument('-d', '--delay', type=int, default=2, help="Delay in seconds between processing each BAM file (default: 2 seconds).")

    args = parser.parse_args()

    # Ensure the igv directory exists
    igv_directory = os.path.join(args.bam_path, 'igv')
    if not os.path.exists(igv_directory):
        os.makedirs(igv_directory)
    print(f"IGV directory: {igv_directory}")

    # Read regions from external file
    sample_regions = {}
    try:
        with open(args.regions_file, 'r') as f:
            print("Reading regions file:")
            for line in f:
                line = line.strip()
                if line:
                    print(f"Processing line: '{line}'")  # Print each line for verification
                    # Split by any whitespace (space or tab)
                    parts = re.split(r'\s+', line)
                    print(f"Split parts: {parts}")  # Print split parts for debugging
                    if len(parts) == 2:
                        sample, region = parts
                        sample_regions[sample] = region
                    else:
                        print(f"Warning: Line format is incorrect: {line}")
    except FileNotFoundError:
        print(f"Error: Regions file {args.regions_file} not found.")
        return
    except Exception as e:
        print(f"Error reading regions file: {e}")
        return

    if not sample_regions:
        print("No valid sample-region pairs found. Exiting.")
        return

    print(f"Sample regions: {sample_regions}")

    # Generate individual IGV batch scripts for each BAM file
    for sample, region in sample_regions.items():
        sample_name = sample.split('.')[0]
        region_name = region.replace(":", "_").replace("-", "_")
        snapshot_name = f"{sample_name}_{region_name}.png"
        script_file = os.path.join(igv_directory, f"{sample_name}_script.igv")

        # Verify BAM file existence
        bam_file_path = os.path.join(args.bam_path, sample)
        if not os.path.isfile(bam_file_path):
            print(f"Warning: BAM file {sample} does not exist in {args.bam_path}")
            continue

        print(f"Generating script: {script_file}")

        try:
            with open(script_file, "w") as f:
                f.write("new\n")
                f.write(f"genome {args.genome}\n")
                f.write(f"snapshotDirectory {args.snapshot_dir}\n")
                f.write(f"load {bam_file_path}\n")
                f.write(f"goto {region}\n")
                f.write("pause 15\n")  # Pause for 15 seconds to allow rendering
                f.write(f"snapshot {snapshot_name}\n")
                f.write("unload\n")
                f.write("exit\n")
            
            print(f"Script written for {sample}")
        
        except Exception as e:
            print(f"Error writing script for {sample}: {e}")
        
        # Ensure that each script runs separately with the specified delay before moving to the next
        time.sleep(args.delay)

if __name__ == "__main__":
    main()

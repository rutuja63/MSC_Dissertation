import os
import sys

def process_gediMetric(hdf_folder, output_folder):
    # Check if the provided folder exists
    if not os.path.isdir(hdf_folder):
        print("Error: The specified HDF folder does not exist.")
        sys.exit(1)

    # Get a list of all HDF files in the folder
    hdf_files = [os.path.join(hdf_folder, file) for file in os.listdir(hdf_folder) if file.endswith(".h5")]

    # Loop through the HDF files and execute gediMetric for each file and write to respective text files
    for hdf_file in hdf_files:
        output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(hdf_file))[0])
        # Construct the gediMetric command
        command = f"gediMetric -input {hdf_file} -readHDFgedi -ground -varScale 3.5 -sWidth 0.8 -laiRes 5 -laiH 40  -outRoot {output_file}"

        # Execute gediMetric command using os.system()
        os.system(command)

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) !=3 :
        print("Usage: python process_hdf_files.py <hdf_folder>")
        sys.exit(1)

    # Get the folder path from the command-line argument
    hdf_folder = sys.argv[1]
    output_folder = sys.argv[2]
    # rhoc = float(sys.argv[3])


    process_gediMetric(hdf_folder, output_folder)

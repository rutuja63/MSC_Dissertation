import os
import sys

# Path to your input LAS file (same for all coordinate files)
input_list = "/exports/csce/datastore/geos/groups/MSCGIS/s2318635/working_repo/plots/LAS.txt"

def run_gediRat(coordinate_folder, output_folder):
    # Check if the provided folders exist
    if not os.path.isdir(coordinate_folder):
        print("Error: The specified coordinate folder does not exist.")
        sys.exit(1)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of all coordinate files in the folder
    coordinate_files = [os.path.join(coordinate_folder, file) for file in os.listdir(coordinate_folder) if file.endswith(".txt")]

    # Loop through the coordinate files and execute gediRat for each file
    for coord_file in coordinate_files:
        # Generate the output file path based on the coordinate file name
        output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(coord_file))[0] + ".h5")

        # Construct the gediRat command
        command = f"gediRat -inList '{input_list}' -listCoord '{coord_file}' -output '{output_file}' -hdf -ground -pSigma 0.1 -fSigma 2.75 -res 0.1 -checkCover"

        # Execute gediRat command using os.system()
        os.system(command)

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python process_coords.py <coordinate_folder> <output_folder>")
        sys.exit(1)

    # Get the folder paths from the command-line arguments
    coordinate_folder = sys.argv[1]
    output_folder = sys.argv[2]
#function to take the footprints of each 100 meter and siumulates a waveform using an ALS data and saves in one HDF file
    run_gediRat(coordinate_folder, output_folder)

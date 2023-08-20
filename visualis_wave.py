import numpy as np
import pandas as pd
import h5py
import os
import argparse
import matplotlib.pyplot as plt
import math

# filename='/exports/csce/datastore/geos/groups/MSCGIS/s2318635/240723/ICESAT-2/waves/testWave.7091328.21.txt'

# data=np.loadtxt(filename,usecols=(0,1,2,3),dtype=float,unpack=True,comments="#")
# print(data)

# plt.plot(data[1],data[0])


def plot_and_save_graph(input_file, output_folder):
    try:
        # Load data from the input file
        data = np.loadtxt(input_file, usecols=(0, 1, 2, 3), dtype=float, unpack=True, comments="#")
        
        # Check if the loaded data is empty
        if data.size == 0:
            print("Warning: Skipping file '{}' as it contains no data.".format(input_file))
            return

        # Extract filename without extension
        filename_without_extension = os.path.splitext(os.path.basename(input_file))[0]

        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Plot and save the graph
        plt.plot(data[1], data[0])
        plt.xlabel('number of photons')  # Set appropriate x-axis label
        plt.ylabel('Height in meters')  # Set appropriate y-axis label
        plt.title('Pseudowaveform')  # Set your graph title
        plt.savefig(os.path.join(output_folder, f"{filename_without_extension}.png"))
        plt.close()
    except Exception as e:
        print("Error occurred while processing file '{}': {}".format(input_file, e))
        print("Skipping this file and continuing with the next one.")

if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Plot and save graph from input text files in the folder.")
    parser.add_argument("input_folder", help="Path to the folder containing input text files.")
    parser.add_argument("output_folder", help="Path to the output folder where graphs will be saved.")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Get a list of all the text files in the input folder
    input_files = [f for f in os.listdir(args.input_folder) if f.endswith('.txt')]

    # Plot and save graph for each text file
    for input_file in input_files:
        input_file_path = os.path.join(args.input_folder, input_file)
        plot_and_save_graph(input_file_path, args.output_folder)


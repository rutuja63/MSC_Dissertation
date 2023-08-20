import os
import numpy as np
import matplotlib.pyplot as plt

#define fixed classnames
class_names = {
    0: 'noise',
    1: 'ground',
    2: 'canopy',
    3: 'top_canopy'
}

def plot_data_from_files(input_folder, output_folder):
    # List all the files in the input folder
    files = os.listdir(input_folder)

    # Filter only the text files
    txt_files = [file for file in files if file.endswith('.txt')]

    for filename in txt_files:
        input_file = os.path.join(input_folder, filename)
        print(f"Processing file: {input_file}")
        with open(input_file, 'r') as file:
            # Count the number of data rows (excluding the header)
            num_data_rows = sum(1 for line in file) - 1
            file.seek(0)  # Reset the file pointer to the beginning

            # Skip processing if the file has less than two rows (header + one data row)
            if num_data_rows <= 1:
                print(f"Invalid data format in {input_file}. Skipping.")
                continue

            try:
                lat, lon, height, classification = np.loadtxt(file, skiprows=1, unpack=True, dtype=float)
            except ValueError as e:
                print(f"Error loading data from {input_file}: {e}")
                continue

            # Handle the case of a single-row data separately
            if num_data_rows == 1:
                lat, lon, height, classification = [lat], [lon], [height], [classification]

            fig, ax = plt.subplots()
            for cls in np.unique(classification):
                lat_cls = lat[classification == cls]
                height_cls = height[classification == cls]
                label = class_names[int(cls)] if cls in class_names else f'Class {int(cls)}'
                ax.scatter(lat_cls, height_cls, label=label)

            ax.set_xlabel('Latitude')
            ax.set_ylabel('Elevation')
            ax.legend()

            # Get the output plot name without the .txt extension
            output_plot_name = os.path.splitext(filename)[0] + '.png'
            output_path = os.path.join(output_folder, output_plot_name)

            plt.savefig(output_path)
            plt.close()

            print(f"Plot saved as: {output_path}")

# Example usage of the function
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Plot data from text files in a folder.")
    parser.add_argument("input_folder", help="Path to the input folder containing text files.")
    parser.add_argument("output_folder", help="Path to the output folder for saving the plots.")

    args = parser.parse_args()

    plot_data_from_files(args.input_folder, args.output_folder)

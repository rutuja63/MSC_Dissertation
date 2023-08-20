import numpy as np
import matplotlib.pyplot as plt

def read_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    data = []
    for line in lines:
        parts = line.split()
        if len(parts) > 1:
            data.append([float(val) for val in parts[1:]])
    
    return np.array(data)

def plot_and_save(data1, data2, output_filename):
    plt.figure(figsize=(10, 6))
    for line1, line2 in zip(data1, data2):
        bins = np.arange(0, 20, 5)
        plt.plot(line1[0:4],bins, label='ICESat-2_PAVD')
        plt.plot(line2[0:4],bins, label='SIM_PAVD')
    
    plt.xlabel('PAVD values m^2/m^3')
    plt.ylabel('height intervals(meters)bins')
    plt.title('Comparison of PAVD  m^2/m^3at 100 meter segment level')
    plt.legend()
    plt.grid(True)
    plt.savefig(output_filename)
    plt.close()

# Replace these filenames with the actual paths to your text files
file1 = '/exports/csce/datastore/geos/groups/MSCGIS/s2318635/240723/LAI/REAL_LAI_matched_segments.txt'
file2 = '/exports/csce/datastore/geos/groups/MSCGIS/s2318635/240723/LAI/SIM_LAI_matched_segments.txt'

data1 = read_data(file1)
data2 = read_data(file2)

# Replace this with the path to the folder where you want to save the graphs
output_folder = '/exports/csce/datastore/geos/groups/MSCGIS/s2318635/240723/lai_plots/'

for i, (line1, line2) in enumerate(zip(data1, data2)):
    output_filename = f'{output_folder}graph_{i + 1}.png'
    plot_and_save([line1], [line2], output_filename)

print('Graphs saved successfully.')

import numpy as np
import os
import sys
import argparse


def calculate_segment_lai(file_path):
    '''function to calculate mean lai of each bin and creating array of it to write tp final lai file'''
    
    # file_path = '/exports/csce/datastore/geos/groups/MSCGIS/s2318635/240723/03sep19/gedisim/gedimetric/latlon.7089576.19.metric.txt'
      #extracting tlai columns
    data=np.loadtxt(file_path,usecols =(127,128,129,130,131,132,133,134,135),dtype=float,unpack=True,comments="#")

    # Calculate the mean  LAi across each columns for each individual array in the 'data' tuple, it will give 
    # mean of each lai bin and the resulting arry will be the LAI array for that segment

    # array of mean lai of each bin
    
    # bin_mean_lai = np.mean(data_values, axis = 1)
    # return (bin_mean_lai)
    if data.ndim <= 1 or data.shape[0] <= 1:
        print(f"Skipping {file_path}. Insufficient data to calculate mean LAI.")
        return None

    LAI_list = []
    #to scale PAVD calculate from G= 0.6 to pavd calculated using G= 0.5
    #data_values is scaler value variable
    data_values = data*(0.6/0.5)

    res=5
    for i in range(0, data_values.shape[0]):
        h=int((i+0.5)**res)
        thisLAI=np.mean(data_values[i,:])
        LAI_list.append(thisLAI)

    bin_mean_lai = np.array(LAI_list)
    return bin_mean_lai

    




def write_segment_lai(output_file, filename, bin_mean_lai):
    # This function writes the LAI values along with the filename to the output file
    if bin_mean_lai is not None:
        with open(output_file, 'a') as f:
            line = f"{filename} {' '.join(map(str, bin_mean_lai))}\n"
            f.write(line)
        print(f"Written to {output_file}")
    else:
        print(f"Skipping writing for {filename}. Insufficient data to calculate mean LAI.")




def get_cmdArgs():
    parser = argparse.ArgumentParser(description="Calculate mean LAI for all files in a folder.")
    parser.add_argument("input_folder", help="Path to the folder containing input text files.")
    parser.add_argument("output_file", help="Path to the output file to save the results.")
    cmdargs = parser.parse_args()
    return cmdargs



if __name__ == '__main__':


    cmd = get_cmdArgs()
    f=open(cmd.output_file,'w')
    line="#y0 lai" + "\n"
    f.write(line)
    f.close()


    for filename in os.listdir(cmd.input_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(cmd.input_folder, filename)
            print(file_path)
            
            bin_mean_lai = calculate_segment_lai(file_path)

           
            filename = os.path.splitext(filename)[0]
            print(filename)
            write_segment_lai(cmd.output_file, filename, bin_mean_lai)
            



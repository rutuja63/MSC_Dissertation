import numpy as np
import argparse 
from sys import path
from math import sqrt
import random
import re
import os

'''''script to find lAI, reference taken from Steven Hancocks's LAI finding code
 '''



def read_file(filename):
    # Define the parameters for np.loadtxt
    params = {
        "usecols": (0, 1, 2, 3),
        "dtype": float,
        "unpack": True,
        "comments": "#"
    }

    try:
        # Load the data from the file using np.loadtxt
        height, fullwave, ground, canopy = np.loadtxt(filename, **params)

        # Check if the data arrays are empty
        if height.size <= 1 or fullwave.size <= 1 or ground.size <= 1 or canopy.size <=1:
            print(f"Data arrays are empty for file: {filename}. Skipping further processing.")
            
            return None, None, None, None

    except (ValueError, IOError) as e:
        print(f"Error reading data from file: {filename}")
        print("Error message:", e)
        return None, None, None, None

    
    return height, fullwave, ground, canopy

def setOneZ(z):
    'set the height array'
    nBins = len(z)
    print("nBins", nBins)
    #taking the elevvation array from ASCII file where psudowaveforms are saved
    z = np.array(z)
    Res = float((z[-1]-z[0])/(nBins-1))
    print(Res)
    return nBins, z, Res


    
def find_lai(fullwave, ground,canopy, nBins, zG, Res, res, maxH, rhoRatio):
    '''find lai profile'''

    #allocate space 
    laibins = int(maxH/res+1)
    #calculate profile
    G =  0.5 #angular distibution
    totG = np.sum(ground)
    # totalphots = np.sum(fullwave)
    #total number of canopy photons
    totCan = np.sum(canopy)
    #Total number of photons detected aove the ground
    full_wave = totG + totCan
# cumulative array of photons detected in the canopy, it gives the profile of photons detected at every layer of height
    cumul = np.cumsum(fullwave)
# calculating gap
    gap = 1.0 - (cumul/(totCan+rhoRatio*totG))
    lngap = np.zeros(gap.shape, dtype = float)
    lngap[gap>0.0] = np.log(gap[gap>0.0])
# calculating raw LAI at every height at which the pseudowaveform has been digitised, using gap fraction
    rawLAI = np.zeros(nBins, dtype = float)
    for j in range (0,nBins-1):
        rawLAI[j] = (-1.0*(lngap[j+1] - lngap[j]))/G

    #coarsen to this resolution of 5 meter
    lai = np.zeros(laibins, dtype = float)
    for j in range(0,nBins):
        # calculating the bins of height at every 5 meters from ground
        h = zG[j]
        tBin = int(h/res)

        if((tBin>=0) & (tBin<laibins)):
            lai[tBin] = lai[tBin] + rawLAI[j]*Res/res  
    
    lai[lai<= 0]= 0

    return (lai)

# This function writes the LAI values along with the filename to the output file
def write_lai_to_file(output_file, filename, lai):
        
        if lai is None:
            print(f"Skipped writing to {output_file} for {filename} since LAI is None")
            return
            
        with open(output_file, 'a') as f:
            line = f"{filename} {' '.join(map(str, lai))}\n"
            f.write(line)
        print(f"Written to {output_file}")
       


def get_cmdArgs():
    parser = argparse.ArgumentParser(description="Calculate LAI profiles from ASCII files.")
    parser.add_argument("input_folder",type = str, default = 'exports/csce/datastore/geos/groups/MSCGIS/s2318635/bulkdata/21062023/trial/files/trialwaves',help="Path to the folder containing ASCII files.")
    parser.add_argument("output_file",type = str, default= 'exports/csce/datastore/geos/groups/MSCGIS/s2318635/bulkdata/21062023/trial/files/output_lai.txt', help="Path to the output ASCII file.")
    parser.add_argument("--res", type=int, default=5, help="Resolution value.")
    parser.add_argument("--maxH", type=int, default=70, help="Maximum height value.")
    parser.add_argument("--rhoRatio", type=float, help="canoopy, ground reflectance ratio.")
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
            height, fullwave, ground, canopy = read_file(file_path)
            if height is None or fullwave is None or ground is None or canopy is None:
                print(f"Error reading data from file: {filename}. Skipping further processing.")
                continue  # Move to the next file
            # Check if the canopy array is empty
            if np.sum(canopy) == 0:
                print(f"Canopy array is empty for file {filename}. Skipping LAI calculation.")
                lai = None  # Set lai to None to indicate that LAI is not calculated
            else:
                nBins, z, Res = setOneZ(height)
                print(nBins)
                print('z', z)
                print('Res', Res)
                lai = find_lai(fullwave, ground, canopy, nBins, height, Res, cmd.res, cmd.maxH, cmd.rhoRatio)
            
            file_name_split = filename.replace("testwave.", "").replace(".txt", "")
            
            # Write LAI to the output file
            write_lai_to_file(cmd.output_file, file_name_split, lai)
            
   
   
   
    
        
    
#python3 final_LAI.py --res 5 --maxH 40 /exports/csce/datastore/geos/groups/MSCGIS/s2318635/240723/ICESAT-2/waves /exports/csce/datastore/geos/groups/MSCGIS/s2318635/240723/test/LAI/test_LAI.txt






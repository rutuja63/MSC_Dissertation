"""script to filter the flight lines
 according to variables such as 
    cloud_cover, night_flag and orientation"""

import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import h5py
import argparse
os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"

def getCmdArgs():

    """command line fro all the ATL08 files for filtering"""

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", dest ="dirATL08",type = str, default = "/exports/csce/datastore/geos/groups/MSCGIS/s2318635/bulkdata/ATL08", help =" folder containing all ATL08 files")
    parser.add_argument("--output", dest = "dirtextfile",type = str, default = "/exports/csce/datastore/geos/groups/MSCGIS/s2318635/bulkdata/filtertext/", help = "directry for all the text files to save")
    cmdargs= parser.parse_args()
    return cmdargs

def reading_file(filename):
    f = h5py.File(filename, 'r')
        
    sc_orientation = np.asarray(f['orbit_info/sc_orient'])
        #  orientation = sc_orientation[:]
    print("orientation", sc_orientation)
    print(type(sc_orientation))
    print("orient_shape", sc_orientation.shape[0])

        #orient and msw
        #orient is in atl03
        # s = np.asarray(FILE_NAME['/orbit_info/sc_orient'], dtype = bool)
    msw = np.asarray(f['gt1l/land_segments/msw_flag'])
    print(msw)
    print("msw shape", msw.shape[0])
        #orientation of flight [0,1,2] meaning [backward, foward, transition]
        #when in forward mode weak beams are leading to strong beams and backward when strong beams are leading to weak beams
    

        #layer flag value 1= clouds or blowing snow, 0 = likely clear
    layer_flag = np.asarray(f['gt1l/land_segments/layer_flag'])
        #  orientation = sc_orientation[:]
    print("layer_flag", layer_flag)
    print(type(layer_flag))
    print("layershape", layer_flag.shape[0])
        #night flag 0 = day, 1= night
    night_flag = np.asarray(f['gt1l/land_segments/night_flag'])
    print("night_flag", night_flag)
    print(type(night_flag))
    print("night", night_flag.shape[0])
    f.close()
    return sc_orientation, msw, layer_flag, night_flag


        

if __name__ == '__main__':

    cmd= getCmdArgs()
    input_folder = cmd.dirATL08
    output_folder = cmd.dirtextfile

    #making list of all the files in directory 
    
    ATL08_files = [os.path.join(input_folder,f) for f in os.listdir(input_folder) if f.endswith('.h5')]
    for files in ATL08_files:
        filename = files
        name = os.path.splitext(os.path.basename(filename))[0]
        print(name)

    # filename = '/home/s2318635/Dissertation_Mdrive/Practise_data/ICESat-2/05092019/ATL08/5000004247536/229923700/ATL08_20190905101325_10590403_005_01.h5'
        orientation, MSW, cloud_flag, night_flag = reading_file(filename)
        # output_folder = '/home/s2318635/Dissertation_Mdrive/Practise_data/ICESat-2/05092019/ATL08/5000004247536/229923700/'
        # outName = os.path.join(output_folder , name +".txt")
        outName = output_folder + name + ".txt"
        f=open(outName,'w')
        line="#orientation "+str(orientation)+"\n"
        f.write(line)

        for i in range(0,MSW.shape[0]):
        
            line=str(MSW[i])+" "+str(cloud_flag[i])+" "+str(night_flag[i])+"\n"
            f.write(line)


        f.close()
    print("Written to",outName)


import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error,mean_squared_error
import scipy.stats 
from sklearn.metrics import r2_score 
import argparse 
import os


def remove_zeros_at_same_index(arr1, arr2):
    ''' Function to remove the zero value rows present in both the bins'''
    # Create new arrays to store the filtered values
    filtered_arr1 = []
    filtered_arr2 = []
    
    # Iterate through the arrays and only keep elements based on the conditions
    for val1, val2 in zip(arr1, arr2):
        if val1 != 0 or val2 != 0:
            filtered_arr1.append(val1)
            filtered_arr2.append(val2)
    
    return filtered_arr1, filtered_arr2


def calculate_metrics(sim, real, output_file):

    rmse = np.sqrt(mean_squared_error(sim,real))
    relative_rmse = (rmse/np.mean(sim))*100
    bias = np.mean(sim - real)   
    relative_bias = (bias/np.mean(sim)) *100
    mae = mean_absolute_error(sim, real)
    relative_MAE = (mae /np.mean(sim))*100
    # R_square = r2_score(sim, real)
    r_square = (scipy.stats.pearsonr(sim,real)[0])**2
    write_to_txt(i,rmse,r_square, relative_rmse, bias, relative_bias, mae, relative_MAE, output_file)



def write_to_txt(i,RMSE,r_square, relative_rmse, bias, relative_bias, MAE, relative_MAE, output_file):

    with open(output_file, 'a') as f:
        line = str(i)+" "+str(RMSE)+" "+ str(r_square) + " " + str(relative_rmse)+ " " + str(bias) + " " + str(relative_bias) + " " + str(MAE) + " " + str (relative_MAE) + " " +  "\n"
        f.write(line)
    print(f"Written to {output_file}")


def calculate_total(sim, real, output_file):
    #calculating total OAVD of a 100 meter segment 
    sim = np.sum(sim, axis =0)
    real= np.sum(real, axis =0)
    rmse = np.sqrt(mean_squared_error(sim,real))
    relative_rmse = (rmse/np.mean(sim))*100
    bias = np.mean(sim - real)   
    relative_bias = (bias/np.mean(sim)) *100
    mae = mean_absolute_error(sim, real)
    relative_MAE = (mae /np.mean(sim))*100
    # R_square = r2_score(sim, real)
    r_square = (scipy.stats.pearsonr(sim,real)[0])**2
    write_to_txt(i,rmse,r_square, relative_rmse, bias, relative_bias, mae, relative_MAE, output_file)
    print(sim.size)
    print(real.size)



def get_cmdArgs():
    parser = argparse.ArgumentParser(description="Accuracy asessment of PAVD.")
    parser.add_argument("input_file_sim",type = str,help="SIM_LAI_matched segment file for the rho ratio .")
    parser.add_argument("input_file_real",type = str, help="real_LAI mathced segment file with rho ratio")
    parser.add_argument("--output_file", type= str, help="output file of accuracy assessment for that rho ratio")
    cmdargs = parser.parse_args()
    return cmdargs





if __name__ == '__main__':
    
    cmd = get_cmdArgs()
    icesat2_real = cmd.input_file_real
    icesat_2_sim = cmd.input_file_sim
    # Load the text file using np.loadtxt()
    icesat_real = np.loadtxt(icesat2_real, unpack=True,dtype=float,delimiter=' ', usecols=(1,2,3,4,5,6,7))
    ALS_sim = np.loadtxt(icesat_2_sim, unpack=True,dtype=float,delimiter=' ', usecols=(1,2,3,4,5,6,7))
    output_file  = cmd.output_file
    with open(output_file, 'w') as f:
        line = "# i rmse,r_square, relative_rmse, bias, relative_bias, mae, relative_MAE " +"\n"
        f.write(line)
    num_rows = icesat_real.shape[0]
    for i in range (0, 6):

        simList, realList = remove_zeros_at_same_index(ALS_sim[i], icesat_real[i])
        sim = np.array(simList, dtype = float)
        real = np.array(realList, dtype = float)
        calculate_metrics(sim, real, output_file)

    with open(output_file, 'a') as f:
        line = "# total_PAVD for 100 meter segment " +"\n"
        f.write(line)
    calculate_total(ALS_sim, icesat_real, output_file)

    
    





# python3 accuracy1.py /exports/csce/datastore/geos/groups/MSCGIS/s2318635/240723/rhovariation/rho1.8/SIM_LAI_matched_segmentsrho1.8txt /exports/csce/datastore/geos/groups/MSCGIS/s2318635/240723/rhovariation/rho1.8/REAL_LAI_matched_segmentsrho1.8.txt --output_file /exports/csce/datastore/geos/groups/MSCGIS/s2318635/240723/rhovariation/rho1.8/accuracyrho1.8.txt
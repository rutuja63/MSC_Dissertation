import numpy as np
import pandas as pd
import h5py
import os
import argparse
import phoreal as pr
from phoreal.reader import get_atl03_struct
from phoreal.reader import get_atl_alongtrack
import matplotlib.pyplot as plt
import math
from pyproj import Proj, Transformer
import geopandas as gpd
from shapely.geometry import box
from shapely.geometry import Point



''' a script to run on h5 file of icesat-2 , in combination with functions from phoreal
  with angle finiding, creating segments and making pseudowaveform and saving all the outputs to text files
 '''

def calculate_angle(a):
    
''' The angle finding frunction for anIESat-2 flight line'''
    first_lat = a.lat_ph.iloc[0]
    first_lon = a.lon_ph.iloc[0]
    last_lat = a.lat_ph.iloc[-1]
    last_lon = a.lon_ph.iloc[-1]
    #inspects the flight line, is it ascending or descending 
    if first_lat < last_lat:
        direction = 'ascending'
    else:
        direction = 'desceding'
    print("direction", direction)

    if direction == 'ascending':
        first_lat = a.lat_ph.iloc[0]
        first_lon = a.lon_ph.iloc[0]
        last_lat = a.lat_ph.iloc[-1]
        last_lon = a.lon_ph.iloc[-1]

    else:
        first_lat = a.lat_ph.iloc[-1]
        first_lon = a.lon_ph.iloc[-1]
        last_lat = a.lat_ph.iloc[0]
        last_lon = a.lon_ph.iloc[0]

    print(first_lat, first_lon)
    print(last_lat, last_lon)
# calculate angle
    angle = math.atan2(last_lat - first_lat, last_lon - first_lon)
    print("angle :", angle)
    return angle


def reproject(inEPSG, outEPSG, a):
    ''' Function to reproject the Cordinates to the local projectiion of study area. '''

    lon = np.array(a.lon_ph)
    lat = np.array(a.lat_ph)
    transformer = Transformer.from_crs(
        "EPSG:" + str(inEPSG), "EPSG:"+str(outEPSG))
    x, y = transformer.transform(lat, lon)
    return x, y


def create_seg(a, stepsize, angle):
''' function to create a 100 meter segments of a flight line along the track'''
    longitude = np.array(a.lon_ph)
    latitude = np.array(a.lat_ph)
    print("lon", np.min(longitude))
    print("lat", np.min(latitude))

    x, y = reproject(4326, 32606, a)
    # ymin  = a.df['lon_ph'].iloc[0]
    # ymax = a.df['lon_ph'].iloc[-1]
    ymin = np.min(y)
    ymax = np.max(y)
    print(ymin, ymax)
    h = np.array(a.h_ph)
    cls = np.array(a.classification)
    # using the normalised height, height above ground
    norm_h = np.array(a.norm_h)
# creating a 100 meter step 
    step = stepsize * np.abs(np.sin(angle))

    y0 = ymin
    print(ymin, ymax, step)
    print(h.shape, y.shape)

    while y0 < ymax:
        y1 = (y0 + step)
        phots = norm_h[(y >= y0) & (y < y1)]
        if phots.size > 0:
         
            lat = y[(y >= y0) & (y < y1)]
            lon = x[(y >= y0) & (y < y1)]
            classification = cls[(y >= y0) & (y < y1)]
            # used a filter for height above ground to avoide the photons reflected from cloud
            #only using photons whose are belowe 50 meter
            h_norm = norm_h[(y >= y0) & (y < y1) & (norm_h < 50)]

            minZ = np.min(phots)
            maxZ = np.max(phots)
            
            print(minZ, maxZ)
            # resolution used to digitises the pseudowave
            res = 0.1  
            ranges = np.arange(minZ, maxZ+res, res)
            nPhot = phots.shape[0]

            # making histogram of all the photons making a pseudowave of all
            PWave = np.histogram(phots[(phots >= minZ) & (phots <= maxZ)], bins=ranges, range=(np.min(ranges), np.max(ranges)))

         
            # making a pseudowave of only ground photons
            PGWave = np.histogram(norm_h[(y >= y0) & (y < y1) & (cls == 1) & (norm_h>= minZ) & (norm_h<= maxZ)], bins=ranges, range=(np.min(ranges), np.max(ranges)))
            # making a pseudowave of only canopy photons
            canopy = np.histogram(norm_h[(y >= y0) & (y < y1) & (cls > 1) & (norm_h >= minZ) & (norm_h<= maxZ)], bins=ranges, range=(np.min(ranges), np.max(ranges)))

    
        # calling function to writing each segment to ascii file
            writeWave(y0, PWave, PGWave, nPhot, ranges, canopy)

            # calling function to write lat, long , classification and height to ascii file with same name as waves to compare
            writelon(y0, lat, lon, phots, classification, h)
        #Write results to ascii file for visualisation
            writelatlon(y0, lat, lon, phots)
        #adding the step size of 100 meter for the next segment.
        y0 += step


def writelatlon(y0, lat, lon, phots):
    '''write latlon for gediinput'''
    output_folder = "/exports/csce/datastore/geos/groups/MSCGIS/s2318635/240723/gedisim/gediinput"
  # create output folder if doesnt exist
    os.makedirs(output_folder, exist_ok=True)
    outName = os.path.join(output_folder, "latlon."+str(round(y0, 2))+".txt")
    f = open(outName, 'w')
    line = "lat lon "+"\n"
    f.write(line)
    for i in range(0, phots.shape[0]):
        line = str(np.round(lon[i], 5))+" "+str(np.round(lat[i], 5)) + "\n"
        f.write(line)
    f.close()
    print("Written to", outName)


def writelon(y0, lat, lon, phots, classification, height):
    '''Write results to ascii file for visualisation'''
    output_folder = "/exports/csce/datastore/geos/groups/MSCGIS/s2318635/240723/test/ICESAT-2/latlon"
    # create output folder if doesnt exist
    os.makedirs(output_folder, exist_ok=True)

    outName = os.path.join(output_folder, "latlon."+str(round(y0, 2))+".txt")
    f = open(outName, 'w')
    line = "lat lon height classification "+"\n"
    f.write(line)
    for i in range(0, phots.shape[0]):

        line = str(np.round(lat[i], 5))+" "+str(np.round(lon[i], 5))+" " + \
            str(phots[i])+" "+str(classification[i])+" "+str(height[i])+"\n"
        f.write(line)

    f.close()
    print("Written to", outName)


def writeWave(y0, Pwave, PGwave, nPhots, ranges, canopy):
    '''Write results to ascii file'''
    output_folder = "/exports/csce/datastore/geos/groups/MSCGIS/s2318635/240723/test/ICESAT-2/waves"
    # create output folder if doesnt exist
    os.makedirs(output_folder, exist_ok=True)

    outName = os.path.join(output_folder, "testWave."+str(round(y0, 2))+".txt")
    f = open(outName, 'w')
    line = "# nPhots "+str(nPhots)+"\n"
    f.write(line)

    for i in range(0, Pwave[0].shape[0]):
        z = (Pwave[1][i]+Pwave[1][i+1])/2
        line = str(z)+" "+str(Pwave[0][i])+" " + str(PGwave[0][i]) + " " + str(canopy[0][i]) + "\n"
        f.write(line)

    f.close()
    print("Written to", outName)


if __name__ == '__main__':

    # file_03 = "/home/s2318635/Dissertation_Mdrive/Practise_data/ICESat-2/bulk_data_files/ATL03/ATL03_20190903093027_10280403_006_02.h5"
    # file_08 = "/home/s2318635/Dissertation_Mdrive/Practise_data/ICESat-2/bulk_data_files/ATL08/ATL08_20190903093027_10280403_006_02.h5"
    # file_03 = "/home/s2318635/Dissertation_Mdrive/Practise_data/ICESat-2/ATL03/ATL03_20190912213302_11730405_006_02.h5"
    # file_08 = "/home/s2318635/Dissertation_Mdrive/Practise_data/ICESat-2/ATL08/ATL08_20190912213302_11730405_006_02.h5"
    # file_03 = "/home/s2318635/Dissertation_Mdrive/Practise_data/ICESat-2/ATL03/ATL03_20200802173335_05860803_006_01.h5"
    # file_08 = "/home/s2318635/Dissertation_Mdrive/Practise_data/ICESat-2/ATL08/ATL08_20200802173335_05860803_006_01.h5"
    file_03 = "/home/s2318635/Dissertation_Mdrive/Practise_data/ICESat-2/ATL03/ATL03_20210801001300_05861203_006_01.h5"
    file_08 = "/home/s2318635/Dissertation_Mdrive/Practise_data/ICESat-2/ATL08/ATL08_20210801001300_05861203_006_01.h5"
    gt = 'gt3r'
    atl03 = get_atl03_struct(file_03, gt, file_08)
    atl03.df = atl03.df[(atl03.df.lat_ph <= 65) & (atl03.df.lat_ph >= 62) & (atl03.df.classification > 0)]
    atl03.df = atl03.df.reset_index()
    atl03.df, atl03.rotationData = get_atl_alongtrack(atl03.df)
#clipping the flightline too study area
    atl03_gdf = gpd.GeoDataFrame(atl03.df, crs="EPSG:4326", geometry=[Point(xy) for xy in zip(atl03.df.lon_ph, atl03.df.lat_ph)])

    DEJU_boundry = "/exports/csce/datastore/geos/groups/MSCGIS/s2318635/neon_kml/full_boundry_deju/DEJU.shp"

    DEJU_gdf = gpd.read_file(DEJU_boundry)

    atl03_df = gpd.clip(atl03_gdf, DEJU_gdf)
    atl03_df.to_csv("/exports/csce/datastore/geos/groups/MSCGIS/s2318635/240723/01aug21/01aug21_gt3r_clipped.csv")
    #calculate angle
    a = calculate_angle(atl03_df)
    print(a)
#make 100 meter segments and save the waves for further processing
    create_seg(atl03_df, 100, a)

#!/usr/bin/env python3
#####################################################################################
# Program is used for processing *.dat displacement files generated by psgrn/pscmp  #
# Author: Lv Xiaoran                                                                #
# Created: January  2020                                                            #
#####################################################################################

import os
import sys
import argparse
import numpy as np
from osgeo import gdal, osr
######################################################################################
EXAMPLE = """example:
    process_psgrn+pscmp_datfiles.py $MODELOUT/pscmp/Bogd/model4/  
    process_psgrn+pscmp_datfiles.py $MODELOUT/pscmp/Bogd/model4/ --direction U 
    process_psgrn+pscmp_datfiles.py $MODELOUT/pscmp/Bogd/model4/ --direction U --date poseis-10y
    process_psgrn+pscmp_datfiles.py $MODELOUT/pscmp/Bogd/model4/ --direction U --date poseis-10y_20y --outdir $MODELOUT/pscmp/Bogd/model4/ 
"""


def create_parser():
    parser = argparse.ArgumentParser(description='Generate *.tiff files based on psgrn/pscmp *.dat files',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     epilog=EXAMPLE)

    parser.add_argument('inputdir', nargs=1, help='directory stored *.dat files. \n')
    
    parser.add_argument('--direction', dest='direction', nargs='?', default='all', help='direction of displacement. N: north-south' +
                                                                        'E: east-west; U: vertical; all: three directions.\n')
    
    parser.add_argument('--date', dest='date', nargs='?', help='select *.dat file or choose two time period to generate *.tiff.' + 
                                                                'examples for two time periods: poseis-10y_20y[poseis-date1_date2].\n')
    
    parser.add_argument('--outdir',dest='outdir',nargs='?',default=os.getenv('MODELOUT'), help='output directory')

    return parser

def cmd_line_parse(iargs=None):
    parser = create_parser()
    inps = parser.parse_args(args=iargs)  
    
    return inps    
    
def read_coseis_dat(dat_file):
    """read coseismic *.dat and transfer 1D data to 2D array"""
    # read dat file
    lat, lon, disp_north, disp_east, disp_down = np.loadtxt(dat_file,skiprows=1,dtype=np.float,usecols =(0, 1, 2, 3, 4),unpack=True)
    # transfer 1D to 2D array    
    lat_key = np.unique(lat)
    lat_num = lat_key.shape[0]
    lon_key = np.unique(lon)
    lon_num = lon_key.shape[0]
    # coverting 
    disp_n = np.flipud(np.transpose(disp_north.reshape(lon_num,lat_num)))
    disp_e = np.flipud(np.transpose(disp_east.reshape(lon_num,lat_num)))
    disp_d = np.flipud(np.transpose(disp_down.reshape(lon_num,lat_num)))
    return disp_n, disp_e, disp_d, lat_key, lon_key

def read_poseis_dat(dat_file,inps,disp_n_co,disp_e_co,disp_d_co):
    """read poseismic *.dat and transfer 1D data to 2D array"""
    #disp_n_co, disp_e_co, disp_d_co = read_coseis_dat('coseis.dat')
    # read dat file
    lat, lon, disp_north, disp_east, disp_down = np.loadtxt(dat_file,skiprows=1,dtype=np.float,usecols =(0, 1, 2, 3, 4),unpack=True)
    # transfer 1D to 2D array    
    lat_key = np.unique(lat)
    lat_num = lat_key.shape[0]
    lon_key = np.unique(lon)
    lon_num = lon_key.shape[0]
    # coverting 
    disp_n = np.flipud(np.transpose(disp_north.reshape(lon_num,lat_num)))
    disp_e = np.flipud(np.transpose(disp_east.reshape(lon_num,lat_num)))
    disp_d = np.flipud(np.transpose(disp_down.reshape(lon_num,lat_num)))
    # post-seismic displacment
    disp_n_post = disp_n - disp_n_co
    disp_e_post = disp_e - disp_e_co
    disp_d_post = disp_d - disp_d_co
    return disp_n_post, disp_e_post, disp_d_post, lat_key, lon_key

def geocode_direction(dat_file,disp_n,disp_e,disp_d,lat_key,lon_key,inps):

    if inps.direction == 'N':
        disp_name = 'north_south'
        geocode(dat_file,disp_n,disp_name,lat_key,lon_key,inps.outdir)
    if inps.direction == 'E':
        disp_name = 'east_west'
        geocode(dat_file,disp_e,disp_name,lat_key,lon_key,inps.outdir)  
    if inps.direction == 'U':
        disp_name = 'up'
        geocode(dat_file,disp_d,disp_name,lat_key,lon_key,inps.outdir)
    if inps.direction == 'all':
        disp_name = 'north_south'  
        geocode(dat_file,disp_n,disp_name,lat_key,lon_key,inps.outdir)   
        disp_name = 'east_west'
        geocode(dat_file,disp_e,disp_name,lat_key,lon_key,inps.outdir)   
        disp_name = 'up'
        geocode(dat_file,disp_d,disp_name,lat_key,lon_key,inps.outdir)


def geocode(dat_file,disp_data,disp_name,lat,lon,outdir):
    """geocode step"""
    # calculate geo information
    xmin, ymin, xmax, ymax = [np.nanmin(lon), np.nanmin(lat), np.nanmax(lon), np.nanmax(lat)]
    nrows, ncols = np.shape(disp_data)
    xres = (xmax - xmin) / float(ncols)
    yres = (ymax - ymin) / float(nrows)
    # output
    output_tif = outdir +'/' + dat_file + '_' + disp_name + '.tiff'
    geotransform = [xmin,xres,0,ymax,0,-yres]
    raster = gdal.GetDriverByName('GTiff').Create(output_tif,ncols,nrows,1,gdal.GDT_Float32)
    raster.SetGeoTransform(geotransform)
    srs=osr.SpatialReference()
    #srs.ImportFromEPSG(32638) #wgs84 UTM 38N
    srs.ImportFromEPSG(4326) #WGS 84 - WGS84 - World Geodetic System 1984, used in GPS
    raster.SetProjection(srs.ExportToWkt())
    raster.GetRasterBand(1).WriteArray(disp_data)
    raster.FlushCache()
    
def process_dat(inps):
    """process dat files according to requirements"""
    
    # read coseismic displacement
    disp_n_co, disp_e_co, disp_d_co, lat, lon = read_coseis_dat('coseis.dat')    
    
    if inps.date == None:
        # get all *.dat files
        path_list = os.listdir("".join(inps.inputdir))
        dat_name = []
        for filename in path_list:
            if os.path.splitext(filename)[1] == '.dat':
                dat_name.append(filename)
        dat_name.sort()
        # generate geocoded coseismic displacement
        geocode_direction('coseis.dat',disp_n_co,disp_e_co,disp_d_co,lat,lon,inps)
        # read *.dat file)
        # read post-seismic displacement
        for dat_file in dat_name[1:]:
            disp_n, disp_e, disp_d, lat, lon = read_poseis_dat(dat_file,inps,disp_n_co,disp_e_co,disp_d_co)
            geocode_direction(dat_file,disp_n,disp_e,disp_d,lat,lon,inps)
    elif inps.date.find('_') == -1:
        # not two time periods
        if inps.date != 'coseis.dat':
            disp_n, disp_e, disp_d, lat, lon = read_poseis_dat(inps.date,inps,disp_n_co,disp_e_co,disp_d_co)
            geocode_direction(inps.date,disp_n,disp_e,disp_d,lat,lon,inps)
        if inps.date == 'coseis.dat':
            geocode_direction('coseis.dat',disp_n_co,disp_e_co,disp_d_co,lat,lon,inps)
    else:
        # for two time periods
        date1 = inps.date.split('_')[0].split('-')[1] #10y
        date2 = inps.date.split('_')[1] #20y
        date1_file = 'poseis-' + date1 + '.dat'
        date2_file = 'poseis-' + date2 + '.dat'
        disp_n_1, disp_e_1, disp_d_1, lat, lon = read_coseis_dat(date1_file)
        disp_n_2, disp_e_2, disp_d_2, lat, lon = read_coseis_dat(date2_file)
        # disp between two time period should be date2-date1
        disp_n = disp_n_2 - disp_n_1
        disp_e = disp_e_2 - disp_e_1
        disp_d = disp_d_2 - disp_d_1
        geocode_direction(inps.date,disp_n,disp_e,disp_d,lat,lon,inps)
        
######################################################################################
def main(iargs=None):
    inps = cmd_line_parse(iargs)
   
    #whether outdir exists
    isExists = os.path.exists(inps.outdir)
    if not isExists:
        os.makedirs(inps.outdir)
    #go to *.dat directory
    os.chdir("".join(inps.inputdir))
    process_dat(inps)

   
######################################################################################
if __name__ == '__main__':
    main()

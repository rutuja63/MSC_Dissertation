import os
import argparse as ap
import numpy as np

from phoreal.reader import write_atl03_las
from phoreal.reader import get_atl03_struct
from phoreal.reader import get_atl08_struct


def parse_arguments() -> dict:
    '''Command line entry point'''
    parser = ap.ArgumentParser()
    '''Required arguments:'''
    parser.add_argument('-atl03', '--atl03_dir'
                        , required=True
                        , type=str
                        , help='Input ATL03 directory')

    parser.add_argument('-atl08', '--atl08_dir'
                        , required=True
                        , type=str
                        , help='Input ATL08 directory')
    
    parser.add_argument('-out', '--output_dir'
                        , required=True
                        , type=str
                        , help='las output file /directory/')

    parser.add_argument('-gt', '--gtXX'
                        , required=True
                        , type=str
                        , help='Alongtrack (gt1l, gt1r, gt2l, gt2r, gt3l, gt3r)')

    '''Optional arguments:'''
    parser.add_argument('-r', '--res'
                        , nargs='?'
                        , const=1
                        , type=int
                        , default=30
                        , help='Alongtrack resolution (m)')
    
    parser.add_argument('-ec', '--epsg_code'
                        , type=str
                        , default=None
                        , help='UTM Zone')
    
    args = parser.parse_args()
        # Using dict for readability and to work with logging more easily.
    arg_dict = {  'in_atl03'      : args.atl03_dir
                , 'in_atl08'      : args.atl08_dir
                , 'in_gt'         : args.gtXX
                , 'in_epsg'       : args.epsg_code
                , 'in_res'        : args.res
                , 'out_dir'       : args.output_dir }
    return arg_dict


def collect_processed_data(arg_dict) -> list:
    """
    Aggregate processed atl03 and atl08 files and create objects.
    
    Parameters:
        arg_dict (dict): dictionary of argparse command line inputs
    
    Returns:
        atl_data (list): list of atl03 objects
    """
    atl_data = []
    dataset_count = 0
    for data_file in os.listdir(arg_dict['in_atl03']):
        if data_file[:15] == 'processed_ATL03':
            atl03_file = os.path.join(arg_dict['in_atl03'], data_file)
        else:
            continue
            # atl08 file names are generated by modifying processed 
            # atl03 file names (identical minus 'atl03')
        atl08_file = os.path.join(arg_dict['in_atl08'], 'processed_ATL08' + data_file[15:])
            # Ensure that a matching atl08 file exists, ensure that both the atl03 and atl08
            # files contain data. Log and continue if not.
        try:
            if os.path.getsize(atl03_file) and os.path.getsize(atl08_file):
                atl03 = get_atl03_struct(atl03_file
                                         , arg_dict['in_gt']
                                         , atl08_file
                                         , epsg = arg_dict['in_epsg'])
                atl_data.append(atl03)                                                  
            else:
                print('The following file is empty: '
                      , atl03_file if not os.path.getsize(atl03_file) else atl08_file )
        except OSError:
            print('Missing the following atl file: '
                  , atl03_file if not os.path.isfile(atl03_file) else atl08_file)
    return atl_data

def main(arg_dict):
    atl_data = collect_processed_data(arg_dict)
    for atl03_object in atl_data:
        write_atl03_las(atl03_object, arg_dict['out_dir'])

if __name__ == '__main__':
    arg_dict = parse_arguments()
    main(arg_dict)    
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 6 2026

@author: Yuecheng XU
"""

import os
import pandas as pd

from .EplusEngine.EplusEngine import StaticEplusEngine as eplus
from .IDFEditHelper import read_idf_to_dict, write_dict_to_idf


def sim_geometry (va, sel, idf_path, epw_path):

    """
    This function is a top level function that run all simulations about modified geometry
    Args :
    ---------
    va: float
        Length or Height value
    sel: str
        selection of length or height by user
    idf path: str
        IDF file path
    epw path: str
        EPW file path

    Return:
    ---------
    heatings, coolings: tuple of lists
        Heating and cooling results
    """
    
    heatings = [] # a placeholder to save all heating energy results
    coolings = [] # a placeholder to save all cooling energy results 
    
    # Setup working directory and test folder for simulation outputs
    base_dir = os.getcwd() 
    test_dir = os.path.join(base_dir, "test")
    os.makedirs(test_dir, exist_ok=True)

    # Define temporary IDF file name and path for the modified model
    new_idf_name = "Changed_Model.idf"
    new_idf_save_path = os.path.join(test_dir, new_idf_name)

    # Convert relative paths to absolute paths for robust file access
    abs_idf_path = os.path.abspath(idf_path)
    abs_epw_path = os.path.abspath(epw_path)

    # Determine which geometric parameter to modify based on user selection
    if sel == "Length":
        # Modify window length in IDF and run EnergyPlus simulation
        os.makedirs("test", exist_ok=True)
        modify_l_in_idf(abs_idf_path, new_idf_save_path, va)
        eplus.run_eplus_model(
            idf_path = new_idf_save_path,
            output_dir = test_dir,
            weather_path = epw_path
            )
    elif sel == "Height":
        # Modify window height in IDF and run EnergyPlus simulation
        os.makedirs("test", exist_ok=True)
        modify_h_in_idf(abs_idf_path, new_idf_save_path, va)
        eplus.run_eplus_model(
            idf_path = new_idf_save_path,
            output_dir = test_dir,
            weather_path = abs_epw_path
            )        
    
    # Extract energy results from the simulation output files
    annual_heating, annual_cooling = get_energy_res(test_dir)
    heatings.append(annual_heating)
    coolings.append(annual_cooling)
    
    return heatings, coolings

    
            
def modify_l_in_idf (idf_path, new_idf_save_path, new_l):
    """
    This function reads a IDF file, modifies its Window Length, and saves it.
    It works by updating the X-coordinates of specific vertices in the 
    FenestrationSurface:Detailed object.
    
    Args:
    ----------
    idf_path : str
        Input IDF file path
    new_idf_save_path : str
        New IDF save path after modifying Length
    new_l : float
        New Length
    """
    
    # Load IDF content into a dictionary structure
    idf_dict_raw = read_idf_to_dict(idf_file_path = idf_path)
    
    # Extract the base X-coordinate from the first vertex of the window
    vertex1_x = float(idf_dict_raw ['FenestrationSurface:Detailed'][0][9].split('!')[0])
    
    # Calculate the new X-coordinate for vertices that define the width/length
    new_x_coordinate = vertex1_x + new_l
    
    # Preserve original comments while updating vertex values
    vertex3_x_comment = idf_dict_raw ['FenestrationSurface:Detailed'][0][15].split('!')[1]
    vertex4_x_comment = idf_dict_raw ['FenestrationSurface:Detailed'][0][18].split('!')[1]
    
    # Update X-coordinates for vertex 3 and vertex 4 to reflect new length
    idf_dict_raw['FenestrationSurface:Detailed'][0][15] = '!'.join([str(new_x_coordinate), vertex3_x_comment])
    idf_dict_raw['FenestrationSurface:Detailed'][0][18] = '!'.join([str(new_x_coordinate), vertex4_x_comment])
    
    # Save the modified dictionary back to a new IDF file
    write_dict_to_idf(idf_dict_raw, new_idf_save_path)


def modify_h_in_idf (idf_path, new_idf_save_path, new_h):
    """
    This function reads a IDF file, modifies its Window Height, and saves it.
    It works by updating the Z-coordinates of specific vertices in the 
    FenestrationSurface:Detailed object.
    
    Args:
    ----------
    idf_path : str
        Input IDF file path
    new_idf_save_path : str
        New IDF save path after modifying Height
    new_h : float
        New Height
    """
    
    # Load IDF content into a dictionary structure
    idf_dict_raw = read_idf_to_dict(idf_file_path = idf_path)
    
    # Extract the base Z-coordinate (height) from the second vertex
    vertex2_z = float(idf_dict_raw ['FenestrationSurface:Detailed'][0][14].split('!')[0])
    
    # Calculate the new Z-coordinate for vertices that define the height
    new_z_coordinate = vertex2_z + new_h
    
    # Preserve original comments while updating vertex values
    vertex1_z_comment = idf_dict_raw ['FenestrationSurface:Detailed'][0][11].split('!')[1]
    vertex4_z_comment = idf_dict_raw ['FenestrationSurface:Detailed'][0][20].split('!')[1]
    
    # Update Z-coordinates for vertex 1 and vertex 4 to reflect new height
    idf_dict_raw['FenestrationSurface:Detailed'][0][11] = '!'.join([str(new_z_coordinate), vertex1_z_comment])
    idf_dict_raw['FenestrationSurface:Detailed'][0][20] = '!'.join([str(new_z_coordinate), vertex4_z_comment])
    
    # Save the modified dictionary back to a new IDF file
    write_dict_to_idf(idf_dict_raw, new_idf_save_path)
    
    
def get_energy_res(result_dir):
    
    """
    This function reads the simulation result CSV file and extracts the 
    annual heating and cooling energy consumption in kWh.
    
    Args:
    -----
    result_dir: str
        Directory where simulation results are stored.

    Return:
    ------
    annual_heating: float
        Total annual heating energy (kWh).
    annual_cooling: float
        Total annual cooling energy (kWh).
    """

    # Construct path to the EnergyPlus standard CSV output
    res_csv_path = os.sep.join([result_dir, 'eplusout.csv'])
    
    # Read the simulation results into a pandas DataFrame
    res_df = pd.read_csv(res_csv_path)
    
    # Sum up the instantaneous heating/cooling rates (W) across all timesteps
    annual_heating_power = res_df['ZONE 1 IDEAL LOADS:Zone Ideal Loads Supply Air Total Heating Rate [W](TimeStep)'].sum()
    annual_cooling_power = res_df['ZONE 1 IDEAL LOADS:Zone Ideal Loads Supply Air Total Cooling Rate [W](TimeStep)'].sum() 
    
    # Conversion Logic:
    # 1. Convert Watts (W) to kiloWatts (kW) by dividing by 1000.
    # 2. Convert power to energy by multiplying by time (hours). 
    #    Since the timestep is 15 minutes, we multiply by 0.25 hours.
    annual_heating = annual_heating_power / 1000 * 0.25 
    annual_cooling = annual_cooling_power / 1000 * 0.25 
    
    return annual_heating, annual_cooling
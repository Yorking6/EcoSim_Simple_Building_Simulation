# -*- coding: utf-8 -*-
"""
Created on Tue Jan 6 2026

@author: Yuecheng XU
"""

import os
import pandas as pd

from .EplusEngine.EplusEngine import StaticEplusEngine as eplus
from .IDFEditHelper import read_idf_to_dict, write_dict_to_idf


def sim_resident (va, sel, idf_path, epw_path):

    """
    Top-level function to run energy simulations with modified occupant density and schedules.
    
    Args:
    ---------
    va: int
        Number of occupants (people) in this zone
    sel: str
        The specific occupancy schedule name selected by the user.
    idf_path: str
        Path to the original IDF model file.
    epw_path: str
        Path to the EPW file.

    Returns:
    ---------
    heatings, coolings: tuple of lists
        Lists containing the annual heating and cooling energy results (kWh).
    """
    
    heatings = [] # Placeholder to store heating energy results
    coolings = [] # Placeholder to store cooling energy results 
    
    # Initialize workspace and ensure test directory exists for outputs
    base_dir = os.getcwd() 
    test_dir = os.path.join(base_dir, "test")
    os.makedirs(test_dir, exist_ok=True)

    # Name and path for the temporary modified IDF model
    new_idf_name = "Changed_Model.idf"
    new_idf_save_path = os.path.join(test_dir, new_idf_name)

    # Use absolute paths to prevent issues with relative directory shifts
    abs_idf_path = os.path.abspath(idf_path)
    abs_epw_path = os.path.abspath(epw_path)

    # Update the IDF with new occupancy data and execute EnergyPlus
    os.makedirs("test", exist_ok=True)
    modify_resident_in_idf(abs_idf_path, new_idf_save_path, va, sel)
    eplus.run_eplus_model(
        idf_path = new_idf_save_path,
        output_dir = test_dir,
        weather_path = abs_epw_path
        )

    # Parse simulation output files to extract energy consumption
    annual_heating, annual_cooling = get_energy_res(test_dir)
    heatings.append(annual_heating)
    coolings.append(annual_cooling)
    
    return heatings, coolings

    
            
def modify_resident_in_idf (idf_path, new_idf_save_path, va, sel):
    """
    Modifies occupant-related objects in the IDF file.
    Specifically updates the 'People' count and synchronizes schedules across 
    People, Schedule:Compact, and ElectricEquipment objects.
    
    Args:
    ----------
    idf_path : str
        Source IDF file path.
    new_idf_save_path : str
        Target path for saving the modified IDF.
    va: str
        Target number of occupants (as a string to preserve IDF formatting).
    sel: str
        Target schedule name to apply.
    """
    
    # Read the IDF file into a dictionary for easy field manipulation
    idf_dict_raw = read_idf_to_dict(idf_file_path = idf_path)

    # Extract existing comments from the IDF fields to maintain file structure/documentation
    people_comment = idf_dict_raw ['People'][0][2].split('!')[1]
    schedule_compact_comment = idf_dict_raw ['Schedule:Compact'][4][0].split('!')[1]
    electric_equipment_comment = idf_dict_raw ['ElectricEquipment'][0][2].split('!')[1]
    
    # Update the schedule names to match the user's selection
    # Indices correspond to the 'Schedule Name' field in respective EnergyPlus objects
    idf_dict_raw['People'][0][2] = '!'.join([sel, people_comment])
    idf_dict_raw['Schedule:Compact'][4][0] = '!'.join([sel, schedule_compact_comment])
    idf_dict_raw['ElectricEquipment'][0][2] = '!'.join([sel, electric_equipment_comment])
    
    # Update the 'Number of People' field in the 'People' object
    people_number_comment = idf_dict_raw ['People'][0][4].split('!')[1]
    idf_dict_raw['People'][0][4] = '!'.join([va, people_number_comment])
    
    # Export the modified dictionary back to a valid IDF file
    write_dict_to_idf(idf_dict_raw, new_idf_save_path)


    
def get_energy_res(result_dir):
    
    """
    Parses EnergyPlus simulation results to calculate annual heating and cooling energy.
    
    Args:
    -----
    result_dir: str
        The directory where simulation output files (eplusout.csv) are stored.

    Returns:
    ------
    annual_heating: float
        Total annual heating energy (kWh).
    annual_cooling: float
        Total annual cooling energy (kWh).
    """

    # Define path to the EnergyPlus standard CSV output file
    res_csv_path = os.sep.join([result_dir, 'eplusout.csv'])
    
    # Read the results into a pandas DataFrame for analysis
    res_df = pd.read_csv(res_csv_path)
    
    # Calculate the sum of instantaneous heating and cooling rates (W) for the entire year
    annual_heating_power = res_df['ZONE 1 IDEAL LOADS:Zone Ideal Loads Supply Air Total Heating Rate [W](TimeStep)'].sum()
    annual_cooling_power = res_df['ZONE 1 IDEAL LOADS:Zone Ideal Loads Supply Air Total Cooling Rate [W](TimeStep)'].sum() 
    annual_heating = annual_heating_power / 1000 * 0.25 # Transfer heating power W into energy kwh (15min --> 0.25h)
    annual_cooling = annual_cooling_power / 1000 * 0.25 # Transfer cooling power W into energy kwh (15min --> 0.25h)
    
    return annual_heating, annual_cooling
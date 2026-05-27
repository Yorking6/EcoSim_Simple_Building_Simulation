# -*- coding: utf-8 -*-
"""
Created on Tue Jan 6 2026

@author: Yuecheng XU
"""

import os
import pandas as pd

from .EplusEngine.EplusEngine import StaticEplusEngine as eplus
from .IDFEditHelper import read_idf_to_dict, write_dict_to_idf


def sim_material (window_sel, wall_sel, idf_path, epw_path):

    """
    Main function to execute energy simulations based on user-selected materials.
    
    Args:
    ---------
    window_sel: str
        Window material type selected by user.
    wall_sel: str
        Wall construction type selected by user.
    idf_path: str
        Path to the base IDF model file.
    epw_path: str
        Path to the EPW file.

    Returns:
    ---------
    heatings, coolings: tuple of lists
        Lists containing calculated annual heating and cooling energy.
    """
    
    heatings = [] # Placeholder for heating energy results
    coolings = [] # Placeholder for cooling energy results 
    
    # Initialize workspace and output directories
    base_dir = os.getcwd() 
    test_dir = os.path.join(base_dir, "test")
    os.makedirs(test_dir, exist_ok=True)

    # Path for the temporary modified IDF file
    new_idf_name = "Changed_Model.idf"
    new_idf_save_path = os.path.join(test_dir, new_idf_name)

    # Ensure absolute paths for cross-platform reliability
    abs_idf_path = os.path.abspath(idf_path)
    abs_epw_path = os.path.abspath(epw_path)

    # Modify the IDF to reflect new material choices and trigger simulation
    os.makedirs("test", exist_ok=True)
    modify_type_in_idf(abs_idf_path, new_idf_save_path, window_sel, wall_sel)
    eplus.run_eplus_model(
        idf_path = new_idf_save_path,
        output_dir = test_dir,
        weather_path = abs_epw_path
        )

    # Extract and store simulation results
    annual_heating, annual_cooling = get_energy_res(test_dir)
    heatings.append(annual_heating)
    coolings.append(annual_cooling)
    
    return heatings, coolings

    
            
def modify_type_in_idf (idf_path, new_idf_save_path, window_sel, wall_sel):
    """
    Parses an IDF file and replaces construction types for walls and windows.
    
    Args:
    ----------
    idf_path : str
        Source IDF file path.
    new_idf_save_path : str
        Target path for the modified IDF.
    window_sel: str
        UI-friendly window type name.
    wall_sel: str
        UI-friendly wall type name.
    """
    
    # Load IDF content into a dictionary
    idf_dict_raw = read_idf_to_dict(idf_file_path = idf_path)
    
    def change_selction(window_type, wall_type):
        """
        Nested Functions for the use of modify_type_in_idf
        Parameters
        ----------
        window_type : str
            Select the new window type
        wall_type : str
            Select the new wall type
    
        Returns
        -------
        None.
    
        """
        new_wall_comment = idf_dict_raw ['BuildingSurface:Detailed'][0][2].split('!')[1]
        new_window_comment = idf_dict_raw ['BuildingSurface:Detailed'][0][2].split('!')[1]
        
        idf_dict_raw['BuildingSurface:Detailed'][0][2] = '!'.join([wall_type, new_wall_comment])
        idf_dict_raw['BuildingSurface:Detailed'][1][2] = '!'.join([wall_type, new_wall_comment])
        idf_dict_raw['BuildingSurface:Detailed'][2][2] = '!'.join([wall_type, new_wall_comment])
        idf_dict_raw['BuildingSurface:Detailed'][3][2] = '!'.join([wall_type, new_wall_comment])
        idf_dict_raw['FenestrationSurface:Detailed'][0][2] = '!'.join([window_type, new_window_comment])
        
        # Write modified data back to file
        write_dict_to_idf(idf_dict_raw, new_idf_save_path)
    
    # Map UI selections to internal IDF Construction names
    # Mapping for Double Pane Window (DoubleClear)
    if window_sel == "Double Pane Window":
        if wall_sel == "Light Timber Frame":
            change_selction("DoubleClear", "LightTimeberFrame")
        elif wall_sel == "Common Brick Wall":
            change_selction("DoubleClear", "CommonBrickWall")
        elif wall_sel == "Aerated Concrete":
            change_selction("DoubleClear", "AeratedConcrete")
        elif wall_sel == "High-Efficiency Insulated Wall":
            change_selction("DoubleClear", "High-EfficiencyInsulated")
    elif window_sel == "Double Pane Low-E Window":
        if wall_sel == "Light Timber Frame":
            change_selction("DoubleClear", "LightTimeberFrame")
        elif wall_sel == "Common Brick Wall":
            change_selction("DoubleClear", "CommonBrickWall")
        elif wall_sel == "Aerated Concrete":
            change_selction("DoubleClear", "AeratedConcrete")
        elif wall_sel == "High-Efficiency Insulated Wall":
            change_selction("DoubleClear", "High-EfficiencyInsulated")



def get_energy_res(result_dir):
    
    """
    Parses EnergyPlus simulation results to calculate annual heating and cooling energy.
    
    Args:
    -----
    result_dir: str
        The directory containing simulation output files (e.g., eplusout.csv).

    Returns:
    ------
    annual_heating: float
        Total annual heating energy in kWh.
    annual_cooling: float
        Total annual cooling energy in kWh.
    """

    # Locate the CSV output file from EnergyPlus
    res_csv_path = os.sep.join([result_dir, 'eplusout.csv'])
    
    # Load simulation results into a DataFrame
    res_df = pd.read_csv(res_csv_path)
    
    # Extract instantaneous heating and cooling rates (W) and sum them up
    annual_heating_power = res_df['ZONE 1 IDEAL LOADS:Zone Ideal Loads Supply Air Total Heating Rate [W](TimeStep)'].sum()
    annual_cooling_power = res_df['ZONE 1 IDEAL LOADS:Zone Ideal Loads Supply Air Total Cooling Rate [W](TimeStep)'].sum() 
    annual_heating = annual_heating_power / 1000 * 0.25 # Transfer heating power W into energy kwh (15min --> 0.25h)
    annual_cooling = annual_cooling_power / 1000 * 0.25 # Transfer cooling power W into energy kwh (15min --> 0.25h)
    
    return annual_heating, annual_cooling
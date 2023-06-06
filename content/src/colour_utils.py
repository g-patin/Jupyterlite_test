####### IMPORT PACKAGES #######

import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from IPython import get_ipython

'''
import colour
from colour.plotting import *
from colour.colorimetry import *
from colour.models import *
from colour import SDS_ILLUMINANTS

from ipywidgets import Layout, Button, Box, interact, interactive, fixed, interact_manual
import ipywidgets as wg
from IPython.display import display, clear_output

# self made packages
import acronyms
import class_interim


####### DEFINE GENERAL PARAMETERS #######

style = {"description_width": "initial"}
d65 = colour.CCS_ILLUMINANTS["cie_10_1964"]["D65"]

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": "Helvetica",
})
'''

####### THE FUNCTIONS #######


def tab_viewer(project = 'all'):
    """Graphical user interface to visualize the interim data of the reflectance measurements.

    Args:
        project (string)
        project_id number for which we want to see the results of the measurements. Default to 'all', it shows the results for all the projects.

    Returns:
        It returns a python widget object where the data are being show when individually selecting Id number.

    """    

    ####### LOAD THE DATABASE FILES ########

    
    folder = 'contents/data/RS/processed/'
    print(os.listdir(folder))
    
    '''
    folder_projects = '/home/gus/Documents/RCE/projects/'
    folder_DB = '/home/gus/Documents/RCE/data/databases/'

    Objects_DB_file = folder_DB + 'Objects_DB.csv'    
    Objects_DB = pd.read_csv(Objects_DB_file, index_col = 'object_Id')

    Projects_DB_file = folder_DB + 'Projects_DB.csv'
    Projects_DB = pd.read_csv(Projects_DB_file, index_col = 'project_Id')
  

    if project != 'all':
        projects = list(project)

    else:
        projects = Projects_DB.index


    ###### CREATE WIDGETS #######

    obj_proj = {}
        
    for p in projects:        
        name_folder = [x for x in os.listdir(folder_projects) if p in x][0]
        folder_interimdata = folder_projects + name_folder + '/data/interim/'
            
        subfolders = [ f.path.split('/')[-1] for f in os.scandir(folder_interimdata) if f.is_dir() ]
        if 'RS' in subfolders:
            folder_interimdata_RS = folder_interimdata + 'RS/'
            files = sorted([x for x in os.listdir(folder_interimdata_RS) if '.txt' in x])
                
            for file in files:
                Id = file.split('_')[2]
                obj_proj[Id] = p

    nbs_dropdown = wg.Dropdown(options = obj_proj.keys())

    output_data = wg.Output()
    #nbs_dropdown = wg.Dropdown(options = nbs)     


    ###### CREATE SAVE BUTTON #######
    
    wg_button = wg.Button(description='Save plot')
    box_button = wg.VBox([wg_button])
    output_button = wg.Output()  


    ##### CREATE THE CHANGE FUNCTION #####


    def Plot_data(Id):
        project = obj_proj[Id]
        itm = class_interim.itm(Id,project=project)   
        return itm.plot_data() 

   
    def values_change_Id(change):

        with output_data:
            output_data.clear_output(wait=True)
            Id = change.new         

            fig = Plot_data(Id)  
            
            def button(b):
                with output_button: 
                    fig.savefig('test.png')
                    print('Figure saved !') 

            wg_button.on_click(button)

            return fig
                
    nbs_dropdown.observe(values_change_Id, names='value')
    display(nbs_dropdown,output_data,wg.HBox([box_button, output_button]))
    '''





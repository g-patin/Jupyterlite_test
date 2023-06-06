####### IMPORT PACKAGES #######

import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from IPython import get_ipython

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


####### THE FUNCTIONS #######

def delta(ids, equations, data_type, reference='origin', plot=False):
        """Compute the colour differences between two or more colour measurements.

        Args:
           ids (string):
           A list of Id numbers written as a string, where each Id number refers to a reflectance measurement.
           eg: 'y.1000,y.1020,y.1450' or 'y.2007-y.2010'. The second example will calculate the colour difference between subsequent id numbers from y.2007 to y.2010 included.

           equations (list):
           A list of string that indicates the colour difference equations to be used. 
           eg: ['dE76', 'dE00', 'dE94', dR_VIS, 'dR']
           'dR' corresponds to the mean absolute difference between two reflectance spectral accross the entire spectrum (UV-VIS-NIR).
           'dR_VIS' is similar to 'dR' but only accross the visble spectrum (400 to 800 nm).

           data_type (string):
           It describes the kind of data being used. It can either be 'interim' or 'processed' data.

           reference (string, optional):
           It describes the reference data against which the colour difference should be calculated. It can either be 'origin' or 'mean'. The value 'origin' takes the first data as reference while 'mean' takes the Lab mean values of all data as reference. Default to 'origin'


        Returns:
            It returns a pandas dataframe where each column corresponds to colour difference according to the given equations.
        """

        if '-' in ids:
            letter_colour = ids.split('-')[0].split('.')[0]
            id_initial = np.int32(ids.split('-')[0].split('.')[1])
            id_final = np.int32(ids.split('-')[1].split('.')[1])

            id_nbs = range(id_initial,id_final+1,1)
            Ids = [f'{letter_colour}.{nb}' for nb in id_nbs] 

        else:
            Ids = ids.split(',')

        if data_type == 'interim':
            project = '1'
            path_files = [class_interim.itm(Id,project).get_path() for Id in Ids]

            Lab = [pd.read_csv(file, index_col = 'parameter')['value1'].loc[['L*','a*','b*']].astype('float').values for file in path_files]
            
            df_dE = pd.DataFrame({'Id':Ids})

            for eq in equations:
                dE = np.round(np.array([colour.delta_E(Lab[0], d, method=dicts.dE_colour[eq]) for d in Lab]),3)

                df_dE[eq] = dE
        
        if plot == True:

            df_dE.set_index('Id', inplace=True)
            sns.set()
            fs = 24
            
            df_dE.plot(figsize=(13,6))

            plt.xlim(0)
            plt.ylim(0)

            plt.xlabel('Id numbers',fontsize=fs)
            plt.ylabel('Colour difference', fontsize=fs)
            plt.xticks(fontsize=fs)
            plt.yticks(fontsize=fs)
            plt.legend(fontsize=fs)            

            plt.tight_layout()
            plt.show()

        return df_dE
  
       
def mean(project, objects='all', category='group', saving=True):
    """Function that calculates the mean and std values of several reflectance measurements.
    
    Args:
        ids (string):
        A list of Id numbers written as a string, where each Id number refers to a reflectance measurement.
        eg: 'y.1000,y.1020,y.1450' or 'y.2007-y.2010'. The second example will calculate the colour difference between subsequent id numbers from y.2007 to y.2010 included.

        saving (boolean):
        Whether to save the mean values or not. Default to 'True'.

    Returns:
        It returns a text file with mean and std values.
    """


    ####### RETRIEVE FOLDERS AND INTERIM FILES ########

    folder_projects = '/home/gus/Documents/RCE/projects/'
    name_folder = [x for x in os.listdir(folder_projects) if project in x][0]
    folder_interimdata = folder_projects + name_folder + '/data/interim/RS/'
    interim_files = sorted([x for x in os.listdir(folder_interimdata) if '.txt' in x])

    if objects == 'all':
        all_files = interim_files

    else:
        all_files = sorted([x for x in interim_files if objects in x])


    dic_categories = {'group': sorted(list(set([x.split('_')[3] for x in all_files]))),
                 'colour': sorted(list(set([x.split('_')[2].split('-')[1][:-2] for x in all_files]))),
                 'object': sorted(list(set([x.split('_')[2].split('-')[0] for x in all_files]))),
                 'project': [project]}

    
    
    categories = dic_categories[category]
    

    for cat in categories:
        
        files = [x for x in all_files if cat in x]
        N = len(files)       

        path_files = [class_interim.itm(file.split('_')[2],file.split('_')[1]).get_path() for file in files]

        df = pd.read_csv(path_files[0], index_col='parameter')
        object_Id = df.loc['object_Id']['value1']
        color = df.loc['color']['value1']
        
        LabCh_mean = np.round(np.mean([pd.read_csv(file, index_col = 'parameter')['value1'].loc[['x','y','L*','a*','b*','C*','h']].astype('float').values for file in path_files], axis = 0),3)
        LabCh_std = np.round(np.std([pd.read_csv(file, index_col = 'parameter')['value1'].loc[['x','y','L*','a*','b*','C*','h']].astype('float').values for file in path_files], axis = 0),3)
                
        sp_mean = np.round(np.mean([pd.read_csv(file, index_col = 'parameter').loc['[MEASUREMENT DATA]':][2:].iloc[:,0].astype('float') for file in path_files], axis = 0).flatten(),4)
        sp_std = np.round(np.std([pd.read_csv(file, index_col = 'parameter').loc['[MEASUREMENT DATA]':][2:].iloc[:,0].astype('float') for file in path_files], axis = 0).flatten(),4)
        
        df.iloc[:,1] = ''
        df.iloc[:,0][['x','y','L*','a*','b*','C*','h']] = LabCh_mean
        df.iloc[:,1][['x','y','L*','a*','b*','C*','h']] = LabCh_std

        if category == 'group' or category == 'colour':
            new_id = f'{object_Id}-{cat}'

        elif category == 'object':
            new_id = object_Id
        
        else:
            new_id = project            

        df.iloc[:,0]['Id'] = new_id
        df.iloc[:,0]['measurements_N'] = N

        df.iloc[:,0][df.loc['[MEASUREMENT DATA]':][2:].index] = sp_mean
        df.iloc[:,1][df.loc['[MEASUREMENT DATA]':][2:].index] = sp_std

        df.rename(columns={'value1':'value_mean', 'value2':'value_std'}, inplace=True)
        df.rename(index={'[SINGLE REFLECTANCE MEASUREMENT]':'[MULTI REFLECTANCE MEASUREMENT]'},inplace=True)

        if saving==True:

            colours = f'{color}s'            

            dic_fnames = {'group': path_files[0].replace(path_files[0].split('/')[-1].split('_')[2],f'{object_Id}').replace('interim','processed'),
                          'colour':path_files[0].replace(path_files[0].split('/')[-1].split('_')[2],f'{object_Id}').replace(path_files[0].split('/')[-1].split('_')[3],f'{colours}').replace('interim','processed'),
                          'object':path_files[0].replace(path_files[0].split('/')[-1].split('_')[2],f'{object_Id}').replace(path_files[0].split('/')[-1].split('_')[3],'object').replace('interim','processed'),
                          'project':path_files[0].replace(path_files[0].split('/')[-1].split('_')[2],f'{object_Id}').replace(path_files[0].split('/')[-1].split('_')[3],'project').replace('interim','processed')}            

            fname = dic_fnames[category]        
            df.to_csv(fname, index = True)
        else:
            return df

 

    











    '''
    if '-' in ids:
        letter_colour = ids.split('-')[0].split('.')[0]
        id_initial = np.int32(ids.split('-')[0].split('.')[1])
        id_final = np.int32(ids.split('-')[1].split('.')[1])

        id_nbs = range(id_initial,id_final+1,1)
        Ids = [f'{letter_colour}.{nb}' for nb in id_nbs] 

    else:
        Ids = ids.split(',')
    
    N = len(Ids)

    project = '1'
    path_files = [class_interim.itm(Id,project).get_path() for Id in Ids]

    df = pd.read_csv(path_files[0], index_col='parameter')

    LabCh_mean = np.round(np.mean([pd.read_csv(file, index_col = 'parameter')['value1'].loc[['x','y','L*','a*','b*','C*','h']].astype('float').values for file in path_files], axis = 0),3)
    LabCh_std = np.round(np.std([pd.read_csv(file, index_col = 'parameter')['value1'].loc[['x','y','L*','a*','b*','C*','h']].astype('float').values for file in path_files], axis = 0),3)
        
    sp = [pd.read_csv(file, index_col = 'parameter').loc['[MEASUREMENT DATA]':][2:].iloc[:,0].astype('float') for file in path_files]
    sp_mean = np.round(np.mean([pd.read_csv(file, index_col = 'parameter').loc['[MEASUREMENT DATA]':][2:].iloc[:,0].astype('float') for file in path_files], axis = 0).flatten(),4)
    sp_std = np.round(np.std([pd.read_csv(file, index_col = 'parameter').loc['[MEASUREMENT DATA]':][2:].iloc[:,0].astype('float') for file in path_files], axis = 0).flatten(),4)
      
    df.iloc[:,1] = ''
    df.iloc[:,0][['x','y','L*','a*','b*','C*','h']] = LabCh_mean
    df.iloc[:,1][['x','y','L*','a*','b*','C*','h']] = LabCh_std 
    
    df.iloc[:,0]['Id'] = ids
    df.iloc[:,0]['measurements_N'] = N

    df.iloc[:,0][df.loc['[MEASUREMENT DATA]':][2:].index] = sp_mean
    df.iloc[:,1][df.loc['[MEASUREMENT DATA]':][2:].index] = sp_std

    df.rename(columns={'value1':'value_mean', 'value2':'value_std'}, inplace=True)
    df.rename(index={'[SINGLE REFLECTANCE MEASUREMENT]':'[MULTI REFLECTANCE MEASUREMENT]'},inplace=True)

    if saving==True:        
        fname = path_files[0].replace(path_files[0].split('_')[1],f'{Ids[0]}-{Ids[-1]}').replace('interim','processed')
        df.to_csv(fname, index = True)

    else:
        return df
    '''


def tab_viewer(project = 'all'):
    """Graphical user interface to visualize the interim data of the reflectance measurements.

    Args:
        project (string)
        project_id number for which we want to see the results of the measurements. Default to 'all', it shows the results for all the projects.

    Returns:
        It returns a python widget object where the data are being show when individually selecting Id number.

    """    

    ####### LOAD THE DATABASE FILES ########

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






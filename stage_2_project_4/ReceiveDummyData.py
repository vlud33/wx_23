import glob 
import pandas as pd
import string
import time
import matplotlib.pyplot as plt
import numpy as np
import scipy

def get_r5im(num_indices):
    r5imArrays = []
    if num_indices < 10:
        files = glob.glob('./*.csv')
        for i in range (num_indices):
            selected_file = files[i]
            input_data = pd.read_csv(selected_file)
            dataframe = input_data.drop(columns = input_data.columns[0]).to_numpy()
            r5imArrays.append(dataframe[39])

    return r5imArrays


def get_blm(num_indices,num_of_blm):
    
    blmSums = []

    if num_indices < 10:
        files = glob.glob('./*.csv')
        for i in range (num_indices):
            selected_file = files[i]
            input_data = pd.read_csv(selected_file)
            dataframe = input_data.drop(columns = input_data.columns[0]).to_numpy()
            
            summed = sum(dataframe[:num_of_blm])
            blmSums.append(summed)         
            
    BLMfinalArray = blmSums
  
    return BLMfinalArray

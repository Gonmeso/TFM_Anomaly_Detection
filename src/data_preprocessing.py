import numpy as np
import pandas as pd
import os

DATA_PATH = '../data/'

files_list = [x for x in os.listdir(DATA_PATH) if 'cmd' in x]

for file_ in files_list:
    try:
        data = pd.read_csv(filepath_or_buffer=(DATA_PATH + file_),
                   sep='$',
                   engine='python',
                   header=None,
                   names=["Timestamp", "IP1", "Port1", "IP2", "Port2", "Entrypoint"])
        print(f"File {file_} loaded correctly!")
    except:
        print(f"File {file_} could not be correctly loaded")
        

import os
import logging
import numpy as np
import pandas as pd

DATA_PATH = '../data/'
LOGS_PATH = '../logs/'
logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename=(LOGS_PATH + 'preprocessing.log'),
                    filemode='w',
                    level=logging.DEBUG)

logging.info('Starting preproccessing.')

files_list = [x for x in os.listdir(DATA_PATH) if 'cmd' in x]

for file_ in files_list:
    try:
        data = pd.read_csv(filepath_or_buffer=(DATA_PATH + file_),
                   sep='\$\$',
                   engine='python',
                   header=None,
                   names=["Timestamp", "IP1", "Port1", "IP2", "Port2", "Entrypoint"],
                   usecols=[0, 1, 2, 3, 4, 5])

        logging.info(f"File {file_} loaded correctly!")

        data['IP1_N1'], data['IP1_N2'], data['IP1_N3'], data['IP1_Host'] = data['IP1'].str.split('.').str
        logging.debug(f'IP1 features created for file {file_}')

        data['IP2_N1'], data['IP2_N2'], data['IP2_N3'], data['IP2_Host'] = data['IP2'].str.split('.').str
        logging.debug(f'IP2 features created for file {file_}')

        data.to_csv((DATA_PATH + 'preprocessed/pre_' + file_),
                    sep=";",
                    header=True,
                    index=False)
        logging.info(f'Successfully saved preprocesed file: pre_{file_}')
        del data
    except Exception as e:
        logging.warning(f"File {file_} could not be correctly loaded")
        logging.error(f'{e}')

logging.info("Proccess finished")

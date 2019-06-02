import os
import sys
import json
import logging
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from autoencoder import Autoencoder

from preprocessing.helper.helpers import *

FILE_PATH = sys.argv[1]
CONFIG = sys.argv[2]
MODELS_PATH = 'models/'


def create_models_folder(models_path):
    current_time = datetime.now().strftime('%Y_%m_%d_%H_%M')
    folder = os.path.join(models_path, 'models_' + current_time)
    os.mkdir(folder)
    return folder


def read_config(filepath):
    with open(filepath) as f:
        config = json.load(f)
    forest_config = config['IsolationForest']
    autoencoder_config = config['Autoencoder']
    config['Data'] = FILE_PATH
    logging.info('Config loaded')
    return forest_config, autoencoder_config, config


def scale_data(data):
    data = StandardScaler().fit_transform(data)
    logging.info('Data scaled')
    return data


def create_isolation_forest(forest_config):
    isolation_forest = IsolationForest(**forest_config)
    return isolation_forest


def fit_save_forest(forest, data, model_folder):
    logging.info('Fitting data')
    forest.fit(data)
    logging.info('Model created. Starting save')
    with open(os.path.join(model_folder, 'IsolationForest.pkl'), 'wb') as f:
        pickle.dump(forest, f)
    logging.info('Model saved')


def write_config(config, model_folder):
    with open(os.path.join(model_folder, 'config.json'), 'w') as f:
        json.dump(config, f)
    logging.info('Config saved')


def main():
    folder_path = create_models_folder(MODELS_PATH)
    init_log(folder_path + '/', 'execution.log')
    logging.info('Process started')
    folder_name = folder_path.split('//')[-1]
    logging.info(f'Folder {folder_name} created')

    forest_conf, ae_conf, full_config = read_config(CONFIG)
    write_config(full_config, folder_path)

    logging.info('Loading data')
    data = read_tsv(FILE_PATH, index_col=[0])
    logging.info('Data loaded')
    data = scale_data(data)

    logging.info('Starting Isolation Forest')
    forest = create_isolation_forest(forest_conf)
    fit_save_forest(forest, data, folder_path)

    logging.info('Starting Autoencoder')
    ae = Autoencoder(data.shape[1])
    ae.init_layer_dims()
    ae.init_model()
    ae.fit_save(ae_conf, data, folder_path)
    logging.info('Process finished')

if __name__ == '__main__':
    main()

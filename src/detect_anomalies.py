import os
import sys
import json
import pickle
import logging
import numpy as np
import pandas as pd

from preprocessing.helper.helpers import *
from keras.models import load_model
from sklearn.preprocessing import StandardScaler


MODEL_PATH = sys.argv[1]


def get_data_filename(model_path):
    filepath = os.path.join(model_path, 'config.json')
    with open(filepath) as f:
        config = json.load(f)
    datapath = config['Data']
    logging.info(f'Data used: {datapath}')
    return datapath


def load_data(datapath):
    data = read_tsv(datapath, index_col=[0])
    logging.info('Data loaded')
    scaled_data = StandardScaler().fit_transform(data)
    logging.info('Data scaled')
    return data, scaled_data


def load_models(model_path):
    autoencoder = load_model(os.path.join(model_path, 'autoencoder.h5'))
    with open(os.path.join(MODEL_PATH, 'IsolationForest.pkl'), 'rb') as f:
        forest = pickle.load(f)
    logging.info('Models loaded')
    return autoencoder, forest


def get_anomalies(scaled_data, forest, autoencoder):
    logging.info('Detecting anomalies with Isolation Forest')
    forest_anomalies = forest.predict(scaled_data)
    logging.info('Number of anomalies found by Isolation Forest: '
                 f'{sum(forest_anomalies == -1)}')

    mse = np.mean(np.power(scaled_data - autoencoder.predict(scaled_data), 2),
                  axis=1)
    logging.info('Measuring reconstruction error in autoencoder')
    error = pd.DataFrame({'Recostruction_Error': mse,
                          'ae_anomaly': 0,
                          'is_anomaly': 0})

    idx = error.Recostruction_Error.nlargest(sum(forest_anomalies == -1)).index
    error['ae_anomaly'][idx] = -1

    idx = (error.ae_anomaly == -1) & (forest_anomalies == -1)
    error['is_anomaly'].loc[idx] = -1
    logging.info('The number of anomalies detected in the ensemble is: '
                 f'{sum(idx)}')

    return error['is_anomaly'].values


def main():
    init_log(MODEL_PATH, 'anomaly_detection.log')
    logging.info('Starting process')
    datapath = get_data_filename(MODEL_PATH)
    data, scaled = load_data(datapath)
    autoencoder, forest = load_models(MODEL_PATH)
    data['is_anomaly'] = get_anomalies(scaled, forest, autoencoder)
    data[data['is_anomaly'] == -1]\
        .to_csv(MODEL_PATH + 'detected_anomalies.csv',
                sep="\t",
                encoding='utf-8',
                header=True,
                index=True)
    logging.info('Anomalies saved')
    logging.info('Process finished')


if __name__ == '__main__':
    main()

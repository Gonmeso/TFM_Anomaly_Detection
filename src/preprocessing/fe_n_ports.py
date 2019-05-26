import os
import logging
import numpy as np
import pandas as pd
from helper.helpers import *
import matplotlib.pyplot as plt

from multiprocessing import Pool
from functools import partial

DATA_PATH = 'data/pcaps/csv/'
LOGS_PATH = 'logs/'
N_PROCESSES = 8


def count_unique_ports(x):
    return len(np.unique(x))


def extra_read(filepath, **kwargs):
    df = read_tsv(filepath, **kwargs)
    df['fileNum'] = filepath.split('/')[-1]
    return df


def create_port_count_window(data, ip_var, port_var, window='60s'):

    window_values = np.zeros(len(data))
    unique_values = data.loc[:, ip_var].unique()
    logging.info(f'Creating window for {port_var}')

    for unique in unique_values:
        idx = data.loc[:, ip_var] == unique
        window_values[idx] = data.loc[idx, port_var].rolling('60s').apply(
            count_unique_ports
            ).values

    logging.info(f'Window created for {port_var}')
    return window_values


def read_all_csv(data_path):
    logging.info('Getting file list')
    file_list = [DATA_PATH + c for c in get_file_list(data_path, 'csv')]
    pool = Pool(processes=N_PROCESSES)

    pool_read_tsv = partial(extra_read,
                            parse_dates=['Timestamp'],
                            )
    df_list = pool.map(pool_read_tsv, file_list)
    data = pd.concat(df_list)

    data.index = data['Timestamp']
    logging.info('All files loaded!')
    return data.sort_index()


def main():

    init_log(LOGS_PATH, 'fe_port_window.log', logging.INFO)
    logging.info('Starting Process!')
    names = get_file_list(DATA_PATH)
    data = read_all_csv(DATA_PATH)

    new_vars = ['Port1_last_1', 'Port2_last_1']

    for i, var in enumerate(new_vars):
        data[var] = create_port_count_window(data, f'IP{i+1}', f'Port{i+1}')

    for j in data['fileNum'].unique():
        save_to_tsv(data.loc[data['fileNum'] == j, ].drop('fileNum', axis=1),
                    DATA_PATH,
                    j)

    logging.info('Process finished')


if __name__ == '__main__':
    main()

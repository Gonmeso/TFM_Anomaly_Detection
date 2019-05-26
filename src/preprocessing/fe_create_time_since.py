import numpy as np 
import pandas as pd
import logging
import os
from time import time
from helper.helpers import *
from multiprocessing import Pool
from functools import partial

DATA_PATH = 'data/pcaps/csv/'
LOGS_PATH = 'logs/'
N_PROCESSES = 8


def to_seconds(x):
    return x.total_seconds()


def create_time_diff(data, var_list):

    for var in var_list:
        time_name = f'{var}_time_diff_per_value'
        logging.info(f'Starting {time_name}')
        unique_values = data[var].unique()
        data[time_name] = 0
        data[time_name] = data[time_name].astype('float64')

        for val in unique_values:
            idx = data[var] == val
            tmp = pd.DataFrame(data[idx]['Timestamp'])
            tmp = tmp.diff()
            data[time_name][idx] = tmp.iloc[:, 0].apply(to_seconds).values
        logging.info(f'{time_name} created!')

    return data


def create_diff_ip1_ip2(data, var_list):

    subset = data[var_list].drop_duplicates()
    col_ip_1 = subset[var_list[0]].values
    col_ip_2 = subset[var_list[1]].values
    time_name = 'IP1_IP2_time_diff_per_value'
    time_array = np.zeros(len(data))

    logging.info(f'Starting creation of {time_name}')
    logging.info(f'Total unique values: {len(col_ip_1)}')
    for ip_1, ip_2 in zip(col_ip_1, col_ip_2):
        start = time()
        idx = (data['IP1'] == ip_1) & (data['IP2'] == ip_2)
        tmp = data[idx, 'Timestamp']
        tmp = tmp.diff()
        time_array[idx] = tmp.iloc[:, 0].apply(to_seconds).values
        end = time()
        logging.debug(f'Time elapsed: {end - start}s')
    data[time_name] = time_array
    logging.info(f'{time_name} created!')

    return data


def execute(filename, path, var_list):

    filepath = os.path.join(path, filename)
    data = read_tsv(filepath, parse_dates=['Timestamp'])
    logging.info(f'{filename} loaded!')
    data = create_time_diff(data, var_list)
    data = create_diff_ip1_ip2(data, var_list)
    save_to_tsv(data, path, filename)
    logging.info(f'{filename} saved!')


def main():
    init_log(LOGS_PATH,
             'FE_last_connection.log',
             level=logging.INFO)
    logging.info('Process started!')

    var_list = ['IP1', 'IP2']
    files_list = get_file_list(DATA_PATH, 'csv')
    pool = Pool(processes=N_PROCESSES)
    execute_pool = partial(execute, path=DATA_PATH, var_list=var_list)

    pool.map(execute_pool, files_list)
    logging.info('Process finished!')

if __name__ == '__main__':
    main()

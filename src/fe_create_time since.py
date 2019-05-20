import numpy as np 
import pandas as pd
import logging
import os
from helper.helpers import *
from multiprocessing import Pool
from functools import partial

DATA_PATH = 'data/pcaps/csv/'
LOGS_PATH = 'logs/'
N_PROCESSES = 8


def to_seconds(x):
    return x.total_seconds()


def read_tsv(filepath):
    data = pd.read_csv(filepath,
                       sep='\t',
                       parse_dates=['Timestamp'])
    return data


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


def execute(filename, path, var_list):

    filepath = os.path.join(path, filename)
    data = read_tsv(filepath)
    logging.info(f'{filename} loaded!')
    data = create_time_diff(data, var_list)
    save_to_tsv(data, path, filename)
    logging.info(f'{filename} saved!')


def main():
    init_log(LOGS_PATH,
             'FE_last_connection.log',
             level=logging.INFO)
    logging.info('Process started!')

    var_list = ['IP1', 'IP2']
    files_list = get_file_list(DATA_PATH, 'csv')
    # execute(files_list[0], DATA_PATH, var_list)
    pool = Pool(processes=N_PROCESSES)
    execute_pool = partial(execute, path=DATA_PATH, var_list=var_list)

    pool.map(execute_pool, files_list)
    logging.info('Process finished!')

if __name__ == '__main__':
    main()

import os
import logging
from helper.helpers import *
import numpy as np
import pandas as pd

from multiprocessing import Pool
from functools import partial

DATA_PATH = 'data/pcaps/csv/'
LOGS_PATH = 'logs/'
N_PROCESSES = 8


def load_and_preprocess_data(path, filename, **kwargs):
    word_list = kwargs['word_list']
    params_dict = kwargs['split']
    read_params = kwargs['read_params']
    entrypoint = kwargs['Entrypoint']

    data = pd.read_csv(filepath_or_buffer=path + filename,
                       **read_params
                       )
    for ip in [x for x in data.columns if 'IP' in x.upper()]:
        data = pd.concat([data, split_ip(data[ip])], axis=1
                         )

    data = pd.concat([data, process_entrypoint(data[entrypoint],
                                               word_list,
                                               params_dict)], axis=1)

    return data


def split_ip(ip):
    df = pd.DataFrame()
    logging.info(f'Splitting {ip.name}.')
    for idx, col in enumerate(ip.str.split('.').str):
        df[f'{ip.name}_{idx}'] = col
    return df


def process_entrypoint(entrypoint, word_list, split_from_dict=None):
    features = pd.DataFrame()

    for word in word_list:
        features[f'is_{word}'] = entrypoint\
            .apply(lambda x: check_word(str(x), word))
        logging.info(f'is_{word} feature created')

    if split_from_dict:
        for splitter in split_from_dict:
            word = split_from_dict[splitter]['word']
            mode = split_from_dict[splitter]['mode']

            features[splitter] = entrypoint\
                .apply(lambda x: split_from_word(string_to_list(x),
                                                 word,
                                                 mode))
            logging.info(f'Feature {splitter} created.')

    return features


def execute(file_, path, **kwargs):
    try:
        logging.info('-'*20)
        logging.info(f'Preprocessing file {file_}')
        data = load_and_preprocess_data(path, file_, **kwargs)
        logging.info(f'Features created for {file_}')
        save_to_tsv(data, path, file_)
        logging.info(f'Successfully saved preprocesed file: {file_}')
    except Exception as e:
        logging.warning(f"File {file_} could not be processed")
        logging.error(f'{e}')


def main():

    init_log(LOGS_PATH, 'preprocessing.log')
    logging.info('Starting preprocessing.')
    pool = Pool(processes=N_PROCESSES)

    files_list = get_file_list(DATA_PATH, 'pcap')
    params = {'word_list': ['enable', 'sh', 'busybox'],
              'Entrypoint': 'Payload',
              'split': None,
              'read_params': {
                    'sep': '\t',
                    'header': None,
                    'names': [
                           "Timestamp",
                           "IP1",
                           "Port1",
                           "IP2",
                           "Port2",
                           "Length",
                           "Payload"
                           ]
                }
              }

    execute_pool = partial(execute, path=DATA_PATH, **params)
    pool.map(execute_pool, files_list)
    logging.info("Proccess finished")

if __name__ == '__main__':
    main()

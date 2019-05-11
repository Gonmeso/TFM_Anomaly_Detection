import os
import logging
from helper.helpers import *
import numpy as np
import pandas as pd

DATA_PATH = 'data/preprocessed/'
LOGS_PATH = 'logs/'


def load_and_preprocess_data(path, filename, **kwargs):
    word_list = kwargs['word_list']
    params_dict = kwargs['split']
    read_params = kwargs['read_params']

    data = pd.read_csv(filepath_or_buffer=path + filename,
                       **read_params
                       )
    data = pd.concat([data, split_ip(data['IP1'])], axis=1)
    data = pd.concat([data, split_ip(data['IP2'])], axis=1)
    data = pd.concat([data, process_entrypoint(data['Entrypoint'],
                                               word_list,
                                               params_dict)], axis=1)

    return data


def split_ip(ip):
    df = pd.DataFrame()
    logging.info(f'Splitting {ip.name}.')
    for idx, col in enumerate(ip.str.split('.').str):
        df[f'{ip.name}_{idx}'] = col
    return df


def process_entrypoint(entrypoint, word_list, split_from_dict):
    features = pd.DataFrame()

    for word in word_list:
        features[f'is_{word}'] = entrypoint\
            .apply(lambda x: check_word(x, word))
        logging.info(f'is_{word} feature created')

    for splitter in split_from_dict:
        word = split_from_dict[splitter]['word']
        mode = split_from_dict[splitter]['mode']

        features[splitter] = entrypoint\
            .apply(lambda x: split_from_word(string_to_list(x),
                                             word,
                                             mode))
        logging.info(f'Feature {splitter} created.')

    return features


def save_to_tsv(data, path, filename):

    data.to_csv(path + filename,
                sep="\t",
                encoding='utf-8',
                header=True,
                index=False)


def main():

    init_log(LOGS_PATH, 'preprocessing.log')
    logging.info('Starting preprocessing.')

    files_list = get_file_list(DATA_PATH)
    params = {'word_list': ['enable', 'sh'],
              'split': {
                'login': {'word': 'enable', 'mode': 'backward'},
                'commands': {'word': 'enable', 'mode': 'forward'}
                        },
              'read_params': {
                    'sep': '\$\$\$',
                    'engine': 'python',
                    'header': None,
                    'names': [
                           "Timestamp",
                           "IP1",
                           "Port1",
                           "IP2",
                           "Port2",
                           "Entrypoint"
                           ]
                }
              }

    for file_ in files_list:
        try:
            logging.info('-'*20)
            logging.info(f'Preprocessing file {file_}')
            data = load_and_preprocess_data(DATA_PATH, file_, **params)
            logging.info(f'Features created for {file_}')
            save_to_tsv(data, DATA_PATH, file_)
            logging.info(f'Successfully saved preprocesed file: {file_}')
        except Exception as e:
            logging.warning(f"File {file_} could not be processed")
            logging.error(f'{e}') 

    logging.info("Proccess finished")

if __name__ == '__main__':
    main()

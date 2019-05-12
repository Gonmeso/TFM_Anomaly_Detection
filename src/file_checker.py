import os
import logging
from helper.helpers import init_log, get_file_list

DATA_PATH = 'data/'
LOGS_PATH = 'logs/'


def get_csv(path, filename):
    with open(path + filename, 'r') as f:
        csv_file = f.readlines()
    return csv_file


def change_sep(csv_file, initial, new, ncol):
    for idx, line in enumerate(csv_file):
        data = line.split(initial, ncol)
        csv_file[idx] = new.join(data)
    return csv_file


def save_csv(dest_path, filename, csv_file):
    with open(dest_path + filename, 'w') as pre:
        pre.write(''.join(csv_file))


def main():
    init_log(LOGS_PATH, 'file_checker.log')
    logging.info('Starting file checker.')

    for file_ in get_file_list(DATA_PATH):
        logging.info(f'Checking {file_}')
        data = get_csv(DATA_PATH, file_)

        data = change_sep(csv_file=data,
                          initial='$$',
                          new='$$$',
                          ncol=5)
        logging.info('Separator replaced!')

        logging.info('Writing file.')
        save_csv(dest_path=DATA_PATH + 'preprocessed/pre_',
                 filename=file_,
                 csv_file=data)
    logging.info('Check finished.')

if __name__ == '__main__':
    main()

import os
import logging

DATA_PATH = '../data/'
LOGS_PATH = '../logs/'


logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename=(LOGS_PATH + 'file_checker.log'),
                    filemode='w',
                    level=logging.DEBUG)

logging.info('Starting file checker.')

files_list = [x for x in os.listdir(DATA_PATH) if 'cmd' in x]

for file_ in files_list:

    with open((DATA_PATH + file_), 'r') as f:
        csv_file = f.readlines()
        logging.info(f'Checking {file_}')

    for idx, line in enumerate(csv_file):
        data = line.split('$$', 5)
        csv_file[idx] = '$$$'.join(data)

    logging.info('Separator replaced!')

    with open(DATA_PATH + 'preprocessed/pre_' + file_, 'w') as pre:
        logging.info('Writing file.')
        pre.write(''.join(csv_file))

logging.info('Check finished.')

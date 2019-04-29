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

with open('check_results.csv', 'w') as results:

    for file_ in files_list:
        problematic_lines = []

        with open((DATA_PATH + file_), 'r') as f:
            csv_file = f.readlines()
            logging.info(f'Checking {file_}')

            for idx, line in enumerate(csv_file):
                n = len(line.split('$$'))
                if n > 6:
                    problematic_lines.append(idx)
                    logging.warning(f'Bad line found at {idx}')

        p_lines = [str(c) for c in problematic_lines]
        p_lines = ';'.join(p_lines)

        logging.info(f'Writing results for {file_}')
        results.write(','.join([file_, p_lines]) + '\n')

logging.info('Check finished.')

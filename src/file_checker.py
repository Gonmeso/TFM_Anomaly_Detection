import os
import logging
from helper.helpers import init_log

DATA_PATH = '../data/'
LOGS_PATH = '../logs/'


# logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s',
#                     datefmt='%d/%m/%Y %H:%M:%S',
#                     filename=(LOGS_PATH + 'file_checker.log'),
#                     filemode='w',
#                     level=logging.DEBUG)

def get_file_list(path):
    file_list = [x for x in os.listdir(path) if 'cmd' in x]
    file_list.sort()
    return file_list


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
# files_list = [x for x in os.listdir(DATA_PATH) if 'cmd' in x]

# for file_ in files_list:

#     with open((DATA_PATH + file_), 'r') as f:
#         csv_file = f.readlines()
#         logging.info(f'Checking {file_}')

#     for idx, line in enumerate(csv_file):
#         data = line.split('$$', 5)
#         csv_file[idx] = '$$$'.join(data)

#     logging.info('Separator replaced!')

#     with open(DATA_PATH + 'preprocessed/pre_' + file_, 'w') as pre:
#         logging.info('Writing file.')
#         pre.write(''.join(csv_file))

# logging.info('Check finished.')

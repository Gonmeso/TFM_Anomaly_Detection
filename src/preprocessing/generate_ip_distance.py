import os
import logging
import numpy as np
import pandas as pd
from helper.helpers import *

from multiprocessing import Pool
from functools import partial


DATA_PATH = 'data/pcaps/csv/'
LOGS_PATH = 'logs/'
N_PROCESSES = 8


def number_to_bin(num):
    return format(int(num), 'b').zfill(8)


def ip_to_bin(ip):
    bin_num = ''.join([number_to_bin(x) for x in ip.split('.')])
    return bin_num


# https://www.imperva.com/blog/clustering-app-attacks-with-machine-learning-part-2-calculating-distance/
def ip_distance(ip1, ip2):
    ip1 = ip_to_bin(ip1)
    ip2 = ip_to_bin(ip2)
    counter = 0
    for x, y in zip(ip1, ip2):
        result = bool(int(x)) != bool(int(y))
        if result:
            break
        else:
            counter += 1
    distance = (32 - counter)/32
    return distance


def execute(filename, path, ip_list):
    data = read_tsv(path + filename)
    logging.info(f'{filename} loaded successfully')
    data['IP_distance'] = data[ip_list].apply(lambda x: ip_distance(x[0], x[1]), axis=1)
    logging.info(f'{filename}: feature IP_distance created successfully')
    save_to_tsv(data, path, filename)
    logging.info(f'{filename} successfully saved at {path}')


def main():
    init_log(LOGS_PATH,
             'FE_IP_distance.log',
             level=logging.INFO)
    logging.info('Process started!')

    ip_list = ['IP1', 'IP2']
    files_list = get_file_list(DATA_PATH, 'csv')
    pool = Pool(processes=N_PROCESSES)
    execute_pool = partial(execute, path=DATA_PATH, ip_list=ip_list)

    pool.map(execute_pool, files_list)
    logging.info('Process finished!')

if __name__ == '__main__':
    main()

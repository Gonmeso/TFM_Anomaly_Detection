import logging
import sys
import numpy as np
import pandas as pd
from helper.helpers import *

from multiprocessing import Pool
from functools import partial

DATA_PATH = 'data/pcaps/csv/'
LOGS_PATH = 'logs/'
DST_PATH = 'data/final/'
N_PROCESSES = 8
TIME_WINDOW = sys.argv[1]


def read_all_csv(data_path):
    logging.info('Getting file list')
    file_list = [data_path + c for c in get_file_list(data_path, 'csv')]
    pool = Pool(processes=N_PROCESSES)

    pool_read_tsv = partial(read_tsv,
                            parse_dates=['Timestamp'],
                            )
    df_list = pool.map(pool_read_tsv, file_list)
    data = pd.concat(df_list)
    logging.info('Dropping unnecessary variables')
    data = data.drop([
        'Payload',
        'IP1_0', 'IP2_0',
        'IP1_1', 'IP2_1',
        'IP1_2', 'IP2_2',
        'IP1_3', 'IP2_3',
        ], axis=1)

    data = data.set_index('Timestamp')
    logging.info('All files loaded!')
    return data.sort_index()


def resample_data(data, group):
    return data.groupby(group).resample(TIME_WINDOW)


def aggregate_data(resampled_data, state):

    resample_avg = resampled_data.mean().unstack().add_prefix(state + '_avg_')
    logging.info('Avg done')
    resample_sum = resampled_data.sum().unstack().add_prefix(state + '_sum_')
    logging.info('Sum done')
    resample_std = resampled_data.std().unstack().add_prefix(state + '_std_')
    logging.info('Std done')
    resample_count = resampled_data.count().unstack()\
        .add_prefix(state + 'source_count_')
    logging.info('Count done')
    # resample_max = resampled_data.max().unstack()\
    #     .add_prefix(state + 'source_max_')
    # logging.info('Max done')
    # resample_min = resampled_data.min().unstack()\
    #     .add_prefix(state + 'source_min_')
    # logging.info('Min done')

    resampled_data = pd.concat([
        resample_avg,
        resample_sum,
        resample_std,
        resample_count,
        # resample_max,
        # resample_min,
    ], axis=1)

    resampled_data = pd.concat([
        resampled_data,
        host_to_bin(resampled_data.index)
        ], axis=1)
    logging.info(f'Renaming {state} index')
    resampled_data.index = resampled_data.index.map(lambda x: x + state)

    if state is 'source':
        resampled_data['is_src'] = 1
    else:
        resampled_data['is_src'] = 0

    return resampled_data


def get_host(x):
    x = x.split('.')[-1]
    x = format(int(x), 'b').zfill(8)
    return list(x)


def host_to_bin(ips):
    idx = ips
    ips = pd.Series(ips)
    ips = ips.apply(get_host)
    ips = pd.DataFrame(ips.tolist(),
                       columns=['host' + str(i) for i in range(8)],
                       index=idx)
    logging.info('Host to binary done')
    return ips


def generate_dataset(data):

    logging.info('Starting first resample')
    resampled_1 = resample_data(data, 'IP1')
    logging.info('Resample one generated, starting aggregation')
    resampled_1 = aggregate_data(resampled_1, 'source')
    logging.info('Resample one aggregated')
    logging.info('Starting second resample')
    resampled_2 = resample_data(data, 'IP2')
    logging.info('Resample two generated, starting aggregation')
    resampled_2 = aggregate_data(resampled_2, 'dst')
    logging.info('Resample two aggregated')

    del data
    logging.info('Concatenating resamples')
    data = pd.concat([
        resampled_1,
        resampled_2
    ])
    logging.info('Full dataset generated!')

    data = data.fillna(0)

    return data


def main():
    init_log(LOGS_PATH, 'create_dataset.log')
    logging.info('Process started!')
    data = read_all_csv(DATA_PATH)
    data = generate_dataset(data)
    save_to_tsv(data, DST_PATH, f'final_dataset_{TIME_WINDOW}.csv')
    logging.info('File saved!')
    logging.info('Process finished!')


if __name__ == '__main__':
    main()

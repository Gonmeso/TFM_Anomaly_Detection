import os
import logging
import pandas as pd
import matplotlib.pyplot as plt

PRE_PATH = '../../data/preprocessed/'
LOGS_PATH = '../../logs/'
PLOTS_PATH = '../plots/'
TIMES = ['1min', '30s', '10s']

logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename=(LOGS_PATH + 'complete_graph.log'),
                    filemode='w',
                    level=logging.INFO)

logging.info('Starting process.')

files_list = [x for x in os.listdir(PRE_PATH) if 'cmd' in x]
files_list.sort()

data = pd.DataFrame()

for file_ in files_list:

    try:
        logging.info(f'Reading file {file_}')
        tmp = pd.read_csv(PRE_PATH + file_, sep='\t', usecols=[0, 1])
    except:
        continue
    tmp = tmp.set_index('Timestamp')
    tmp.index = pd.to_datetime(tmp.index)

    for time in TIMES:
        logging.info(f'Generating resample of {time}')
        df = pd.DataFrame(tmp.resample(time).count())
        df['time'] = time
        data = pd.concat([data, df])

del tmp, df

fig, ax = plt.subplots(nrows=len(TIMES)+1, figsize=(15, 10*len(TIMES)+1))
# fig_1, ax_1 = plt.subplots(nrows=len(TIMES)+1, figsize=(15, 10*len(TIMES)+1))

logging.info('Plotting graph.')
for idx, time in enumerate(TIMES):
    tmp = data[data['time'] == time].drop('time', axis=1)
    ax[idx].plot(tmp)
    # ax_1[idx].hist(tmp, bins=50)
    ax[len(TIMES)].plot(tmp, alpha=0.7)
    # ax_1[len(TIMES)].hist(tmp, bins=50, alpha=0.7)

    ax[idx].set_title(f'Plot with {time} interval')
    # ax_1[idx].set_title(f'Hist with {time} interval')

ax[len(TIMES)].set_title(f'Plot with all intervals')
# ax_1[en(TIMES)].set_title(f'Hist with all intervals')


logging.info('Saving graphs.')
fig.savefig(PLOTS_PATH + 'complete_plot.png')
fig_1.savefig(PLOTS_PATH + 'complete_hist.png')
logging.info('Process finished')

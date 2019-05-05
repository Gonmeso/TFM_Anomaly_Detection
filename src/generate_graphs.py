import os
import logging
import pandas as pd
import matplotlib.pyplot as plt

PRE_PATH = '../data/preprocessed/'
LOGS_PATH = '../logs/'
PLOTS_PATH = './plots/'

logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename=(LOGS_PATH + 'generate_graphs.log'),
                    filemode='w',
                    level=logging.INFO)

if not os.path.exists(PLOTS_PATH):
    logging.warning("Plots directory does not exist")
    logging.info("Creating plots dir")
    os.mkdir(PLOTS_PATH)

logging.info('Starting graphs.')

files_list = [x for x in os.listdir(PRE_PATH) if 'cmd' in x]

for file_ in files_list:
    try:
        logging.info('-'*20)

        df = pd.read_csv((PRE_PATH + file_), sep=';', usecols=[0])
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df = df['Timestamp'].value_counts().sort_index()

        logging.info(f"File {file_} loaded")

        year = df.index.year.unique().values[0]
        str_template = "{year}-{month}-{day} {hour}:{minute}:{second}"

        for month in df.index.month.unique().values:

            fig, ax = plt.subplots(nrows=6, ncols=4, figsize=(24, 16))
            plt.tight_layout()

            for day in df.index.day.unique():

                for hour in range(24):
                    init = str_template.format(
                        year=year,
                        month=month,
                        day=day,
                        hour=hour,
                        minute='00',
                        second='00'
                    )

                    end = str_template.format(
                        year=year,
                        month=month,
                        day=day,
                        hour=hour,
                        minute='59',
                        second='59'
                    )
                    if not df[init:end].empty:
                        logging.info("Plotting graph for interval"
                                     f"{hour}-{hour + 1} @ day {day}")
                        df[init:end].plot(
                            ax=ax[hour % 6][hour//6], x='index', y='Timestamp'
                            )
                    else:
                        logging.warning("No data for interval "
                                        f"{hour}-{hour + 1} @ day {day}")

                plt.savefig(
                    PLOTS_PATH + file_ + '_' + str(month) + '_hourly_plots.png'
                    )
                logging.info(f"Graph for {file_} created")
    except Exception as e:
        logging.error(str(e))

logging.info("Process finished")

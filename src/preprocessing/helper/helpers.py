import os
import logging
import pandas as pd
from ast import literal_eval


def check_word(str_cmd_list, word):
    if word in str_cmd_list:
        return 1
    else:
        return 0


def split_from_word(cmd_list, word, mode):
    if word in cmd_list:
        idx = cmd_list.index(word)
        if mode == 'forward':
            subset = cmd_list[idx:]
        elif mode == 'backward':
            subset = cmd_list[:idx]
    else:
        subset = cmd_list if mode == 'backward' else list()
    return subset


def string_to_list(string):
    return literal_eval(string)


def init_log(logs_path, name, level=logging.DEBUG):
    return logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s',
                               datefmt='%d/%m/%Y %H:%M:%S',
                               filename=(logs_path + name),
                               filemode='w',
                               level=level)


def get_file_list(path, word='cmd'):
    file_list = [x for x in os.listdir(path) if word in x]
    file_list.sort()
    return file_list


def save_to_tsv(data, path, filename):

    data.to_csv(path + filename,
                sep="\t",
                encoding='utf-8',
                header=True,
                index=False)


def read_tsv(filepath, **kwargs):
    data = pd.read_csv(filepath,
                       sep='\t',
                       **kwargs)
    return data

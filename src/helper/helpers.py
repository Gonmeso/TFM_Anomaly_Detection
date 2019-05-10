import logging
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
        subset = cdm_list if mode == 'backward' else list()
    return cmd_list


def string_to_list(string):
    return literal_eval(string)


def init_log(logs_path, name):
    return logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s',
                               datefmt='%d/%m/%Y %H:%M:%S',
                               filename=(logs_path + name),
                               filemode='w',
                               level=logging.DEBUG)

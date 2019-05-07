from ast import literal_eval


def check_word(str_cmd_list, word):
    if word in str_cmd_list:
        return 1
    else:
        return 0


def split_from_word(cmd_list, word):
    if word in cmd_list:
        idx = cmd_list.index(word)
        previous = cmd_list[:idx]
        post = cmd_list[idx:]
        return (previous, post)
    else:
        return (cmd_list, [])


def string_to_list(string):
    return literal_eval(string)

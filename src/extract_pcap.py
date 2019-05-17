import logging
from helper.helpers import *
from scapy.all import *
from datetime import datetime as dt

from multiprocessing import Pool
from functools import partial


LOGS_PATH = 'logs/'
PCAP_PATH = 'data/pcaps/subsets/'
DST_PATH = 'data/pcaps/csv/'
N_PROCESSES = 9


def get_packet_length(pkg):
    return str(pkg[IP].len)


def get_source_ip(pkg):
    return str(pkg[IP].src)


def get_dst_ip(pkg):
    return str(pkg[IP].dst)


def get_source_port(pkg):
    return str(pkg[TCP].sport)


def get_dst_port(pkg):
    return str(pkg[TCP].dport)


def get_timestamp(pkg):
    time = dt.fromtimestamp(pkg.len)
    return str(time)


def get_payload(pkg):
    if hasattr(pkg.payload, 'load'):
        payload = str(pkg.payload.load)
        # payload = payload.replace('\n', ';')
        # payload = payload.replace('\x00', '')
    else:
        payload = ''
    return payload


def extract_features(pkg):
    if IP and TCP in pkg:
        row = []
        row.append(get_timestamp(pkg))
        row.append(get_source_ip(pkg))
        row.append(get_source_port(pkg))
        row.append(get_dst_ip(pkg))
        row.append(get_dst_port(pkg))
        row.append(get_packet_length(pkg))
        row.append(get_payload(pkg))
        return '\t'.join(row)
    else:
        pass


def save_csv_from_list(row_list, filename, path):
    with open(path + filename + '.csv', 'w+') as f:
        f.write('\n'.join(row_list))
    logging.info(f'File {filename} saved at {path}')


def generate_fe_file(data):
    row_list = []
    for pkg in data:
        data_str = extract_features(pkg)
        if data_str is None:
            continue
        row_list.append(data_str)
    return row_list


def execute(filename, src_path, dst_path):
    data = PcapReader(src_path + filename)
    logging.info(f'File {filename} loaded from {src_path}')
    csv = generate_fe_file(data)
    save_csv_from_list(csv, filename, dst_path)


def main():
    init_log(LOGS_PATH, 'pcap_extraction.log', level=logging.INFO)
    logging.info('Starting extraction')
    pool = Pool(processes=N_PROCESSES)

    files_list = get_file_list(PCAP_PATH, 'pcap')

    execute_pool = partial(execute, src_path=PCAP_PATH, dst_path=DST_PATH)
    pool.map(execute_pool, files_list)
    logging.info("Proccess finished")

if __name__ == '__main__':
    main()

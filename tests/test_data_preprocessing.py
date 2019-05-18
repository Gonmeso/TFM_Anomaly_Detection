import pytest
from data_preprocessing import *

DEFAULT_DF = pd.DataFrame({
    'IP': '192.168.1.1',
    'Entrypoint': "['login', 'enable', 'sh', 'login']",
}, index=[0])

ENTRYPOINT_PARAMS = {'ssh': {'word': 'sh', 'mode': 'backward'}}

PROCESS_PARAMS = {'word_list': ['enable'],
                  'Entrypoint': 'Entrypoint',
                  'split': ENTRYPOINT_PARAMS,
                  'read_params': {
                    'sep': ';',
                }
          }


def test_load_and_preprocess_data(tmpdir):
    DEFAULT_DF.to_csv(tmpdir + 'test.csv', sep=';', header=True, index=False)
    df = load_and_preprocess_data(tmpdir, 'test.csv', **PROCESS_PARAMS)
    assert df.shape == (1, 8)
    assert (df.columns == ['IP', 'Entrypoint', 'IP_0',
                           'IP_1', 'IP_2', 'IP_3',
                           'is_enable', 'ssh']).all()


def test_split_ip():
    r = split_ip(DEFAULT_DF['IP'])
    assert (r.values == ['192', '168', '1', '1']).all()


def test_process_entrypoint():
    r = process_entrypoint(
        DEFAULT_DF['Entrypoint'],
        ['enable'],
        ENTRYPOINT_PARAMS
    )
    assert r.is_enable.values == 1
    assert r.ssh.values[0] == ['login', 'enable']


def test_save_to_tsv(tmpdir):
    save_to_tsv(DEFAULT_DF, tmpdir, 'test.tsv')
    df = pd.read_csv(tmpdir + 'test.tsv', sep='\t')
    assert (DEFAULT_DF == df).all().all()

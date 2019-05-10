import os
import pytest
from file_checker import *

TEST_CSV = ['test$word$noneed']
EXPECTED_CHANGE = ['test//word$noneed']


def test_get_file_list(tmpdir):
    with open(os.path.join(tmpdir, 'cmd.txt'), 'w') as f:
        f.write('test')
    assert get_file_list(tmpdir) == ['cmd.txt']


def test_get_csv(tmpdir):
    with open(os.path.join(tmpdir, 'cmd.txt'), 'w') as f:
        f.write('test')
    assert get_csv(tmpdir, '/cmd.txt')[0] == 'test'


def test_change_sep():
    assert change_sep(TEST_CSV, '$', '//', 1) == EXPECTED_CHANGE


def test_save_csv(tmpdir):
    save_csv(tmpdir, '/test.txt', TEST_CSV)
    f = open(tmpdir + '/test.txt')
    assert f.readlines() == TEST_CSV

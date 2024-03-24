import pytest

from pandaspgs import read_scoring_file
import os
import shutil

home_path = os.path.expanduser('~') + os.sep + 'pandaspgs_home'


def test_read_scoring_file():
    shutil.rmtree(home_path, ignore_errors=True)
    df1 = read_scoring_file(pgs_id='PGS000737')
    df2 = read_scoring_file(pgs_id='PGS000737', grch='GRCh38')
    shutil.rmtree(home_path, ignore_errors=True)
    assert df1.size == 3*14 and df2.size == 3*12
    with pytest.raises(Exception):
        read_scoring_file(pgs_id='PGS000xxxx')


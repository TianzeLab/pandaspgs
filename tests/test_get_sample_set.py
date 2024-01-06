import numpy

from pandaspgs.get_sample_set import get_sample_sets
from pandas import DataFrame, json_normalize, set_option, Series

set_option('display.max_columns', None)
set_option('display.width', 1000)
set_option('display.colheader_justify', 'center')
set_option('display.precision', 3)



def test_get_sample_sets():
    filter_by_id = get_sample_sets()
    assert len(filter_by_id) == 9112
    assert len(filter_by_id ^ filter_by_id[0]) == 9111
    assert len(filter_by_id[range(2)]) == 2
    assert len(filter_by_id[1:3]) == 2
    assert len(filter_by_id['PSS011331']) == 1
    assert len(filter_by_id[0] + filter_by_id[1]) == 2
    assert len(filter_by_id - filter_by_id[1]) == 9111
    assert len(filter_by_id[0] & filter_by_id) == 1
    assert len(filter_by_id | filter_by_id[0]) == 9112
    assert len(filter_by_id[0:506] | filter_by_id[506]) == 507



import numpy

from pandaspgs.get_performance import get_performances
from pandas import DataFrame, json_normalize, set_option, Series

set_option('display.max_columns', None)
set_option('display.width', 1000)
set_option('display.colheader_justify', 'center')
set_option('display.precision', 3)



def test_get_sample_sets():
    filter_by_id = get_performances()
    assert len(filter_by_id) == 18078
    assert len(filter_by_id ^ filter_by_id[0]) == 18077
    assert len(filter_by_id[range(2)]) == 2
    assert len(filter_by_id[1:3]) == 2
    assert len(filter_by_id['PPM000001']) == 1
    assert len(filter_by_id[0] + filter_by_id[1]) == 2
    assert len(filter_by_id - filter_by_id[1]) == 18077
    assert len(filter_by_id[0] & filter_by_id) == 1
    assert len(filter_by_id | filter_by_id[0]) == 18078
    assert len(filter_by_id[0:506] | filter_by_id[506]) == 507
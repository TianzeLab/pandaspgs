from pandaspgs.get_cohort import get_cohorts
from pandaspgs.client import clear_cache


def test_get_publications():
    filter_by_id = get_cohorts()
    assert len(filter_by_id) == 1252
    assert len(filter_by_id ^ filter_by_id[0]) == 1251
    assert len(filter_by_id[range(2)]) == 2
    assert len(filter_by_id[1:3]) == 2
    assert len(filter_by_id['AGP']) == 1
    assert len(filter_by_id[0] + filter_by_id[1]) == 2
    assert len(filter_by_id - filter_by_id[1]) == 1251
    assert len(filter_by_id[0] & filter_by_id) == 1
    assert len(filter_by_id | filter_by_id[0]) == 1252
    assert len(filter_by_id[0:506] | filter_by_id[506]) == 507

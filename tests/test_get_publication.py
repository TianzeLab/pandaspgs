from pandaspgs.get_publication import get_publications
from pandaspgs.client import clear_cache

def test_get_publications():
    filter_by_id = get_publications(pgp_id='PGP000001')
    assert len(filter_by_id) == 1
    filter_by_pgs_id = get_publications(pgs_id='PGS000001')
    assert len(filter_by_pgs_id) == 1
    filter_by_pmid = get_publications(pmid=25855707)
    assert len(filter_by_pmid) == 1
    filter_by_author = get_publications(author='Mavaddat')
    assert len(filter_by_author) == 6
    filter_by_all = get_publications(pgs_id='PGS000001', pgp_id='PGP000001', pmid=25855707, author='Mavaddat')
    assert len(filter_by_all) == 1
    filter_by_none = get_publications()
    clear_cache('publication')
    clear_cache('all')
    assert len(filter_by_none) == 461

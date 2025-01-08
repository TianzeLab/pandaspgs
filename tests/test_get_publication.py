from pandaspgs.get_publication import get_publications
from pandaspgs.client import clear_cache, reinit_cache
from pandaspgs.get_trait import get_traits
import pandaspgs.client as client

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
    clear_cache('Publication')
    clear_cache('All')
    assert len(filter_by_none) == 689
    assert len(filter_by_none ^ filter_by_id) == 688
    assert len(filter_by_none[range(2)]) == 2
    assert len(filter_by_none[1:3]) == 2
    assert filter_by_none['PGP000001'] == filter_by_id
    assert len(filter_by_id + filter_by_pgs_id) == 2
    assert len(filter_by_none - filter_by_id) == 688
    assert len(filter_by_none & filter_by_id) == 1
    assert len(filter_by_id | filter_by_pgs_id) == 1
    assert filter_by_id == filter_by_pgs_id
    assert len(filter_by_none[0:506] | filter_by_none[506]) == 507


def test_pub_cache():
    pub = get_publications()
    traits = get_traits()
    reinit_cache(field='Publication', maxsize=10, ttl=10)
    assert client.publication_cache.maxsize == 10
    assert client.trait_cache.maxsize > 10
    pub = get_publications()
    traits = get_traits()
    reinit_cache(field='All', maxsize=10, ttl=10)
    pub = get_publications()
    traits = get_traits()
    assert client.publication_cache.maxsize == 10
    assert client.trait_cache.maxsize == 10

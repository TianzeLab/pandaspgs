from pandaspgs.client import get_data


def test_get_data():
    r1 = get_data('https://www.pgscatalog.org/rest/publication/search?pgs_id=PGS000001')
    assert len(r1) == 1
    r2 = get_data('https://www.pgscatalog.org/rest/publication/PGP000001')
    assert len(r2) == 1
    r3 = get_data('https://www.pgscatalog.org/rest/publication/all')
    assert len(r3) == 455
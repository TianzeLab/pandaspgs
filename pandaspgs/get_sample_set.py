from typing import List, Dict
from pandaspgs.client import get_sample_set


def get_sample_sets(pss_id: str = None, pgs_id: str = None, pgp_id: str = None, pmid: int = None, cached=True) -> List[Dict]:
    if pss_id is None and pgs_id is None and pgp_id is None and pmid is None:
        return get_sample_set('https://www.pgscatalog.org/rest/sample_set/all', cached=cached)
    by_id = None
    by_other = None
    if pss_id is not None:
        by_id = get_sample_set('https://www.pgscatalog.org/rest/sample_set/%s' % pss_id, cached=cached)
    if pgs_id is not None or pmid is not None or pgp_id is not None:
        query_str = []
        if pgs_id is not None:
            query_str.append('pgs_id=%s' % pgs_id)
        if pmid is not None:
            query_str.append('pmid=%d' % pmid)
        if pgp_id is not None:
            query_str.append('pgp_id=%s' % pgp_id)
        by_other = get_sample_set('https://www.pgscatalog.org/rest/sample_set/search?%s' % '&'.join(query_str))
    if pss_id is None:
        return by_other
    if pgs_id is None and pmid is None and pgp_id is None:
        return by_id
    other_set = set()
    id_dict = {}
    for single in by_id:
        id_dict[single['id']] = single
    ppm_id_set = id_dict.keys()
    for single in by_other:
        other_set.add(single['id'])
    intersection = ppm_id_set & other_set
    result = []
    for id in intersection:
        result.append(id_dict[id])
    return result
from pandaspgs.client import get_performance
from pandaspgs.performancemetric import PerformanceMetrics


def get_performances(ppm_id: str = None, pgs_id: str = None, pgp_id: str = None, pmid: int = None,
                     cached=True, mode: str = 'Fat') -> PerformanceMetrics:
    if ppm_id is None and pgs_id is None and pgp_id is None and pmid is None:
        return PerformanceMetrics(get_performance('https://www.pgscatalog.org/rest/performance/all', cached=cached),
                                  mode)
    by_id = None
    by_other = None
    if ppm_id is not None:
        by_id = get_performance('https://www.pgscatalog.org/rest/performance/%s' % ppm_id, cached=cached)
    if pgs_id is not None or pmid is not None or pgp_id is not None:
        query_str = []
        if pgs_id is not None:
            query_str.append('pgs_id=%s' % pgs_id)
        if pmid is not None:
            query_str.append('pmid=%d' % pmid)
        if pgp_id is not None:
            query_str.append('pgp_id=%s' % pgp_id)
        by_other = get_performance('https://www.pgscatalog.org/rest/performance/search?%s' % '&'.join(query_str),
                                   cached=cached)
    if ppm_id is None:
        return PerformanceMetrics(by_other, mode)
    if pgs_id is None and pmid is None and pgp_id is None:
        return PerformanceMetrics(by_id, mode)
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
    return PerformanceMetrics(result, mode)


a = get_performances(ppm_id='PPM000001')

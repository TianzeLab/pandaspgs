from typing import List, Dict
from pandaspgs.client import get_publication


def get_publications(pgs_id: str = None, pgp_id: str = None, pmid: int = None, author: str = None, cached=True) -> List[
    Dict]:
    if pgs_id is None and pgp_id is None and pmid is None and author is None:
        return get_publication('https://www.pgscatalog.org/rest/publication/all', cached=cached)
    by_id = None
    by_other = None
    if pgp_id is not None:
        by_id = get_publication('https://www.pgscatalog.org/rest/publication/%s' % pgp_id, cached=cached)
    if pgs_id is not None or pmid is not None or author is not None:
        query_str = []
        if pgs_id is not None:
            query_str.append('pgs_id=%s' % pgs_id)
        if pmid is not None:
            query_str.append('pmid=%d' % pmid)
        if author is not None:
            query_str.append('author=%s' % author)
        by_other = get_publication('https://www.pgscatalog.org/rest/publication/search?%s' % '&'.join(query_str))
    if pgp_id is None:
        return by_other
    if pgs_id is None and pmid is None and author is None:
        return by_id
    other_set = set()
    id_dict = {}
    for single in by_id:
        id_dict[single['id']] = single
    pgp_id_set = id_dict.keys()
    for single in by_other:
        other_set.add(single['id'])
    intersection = pgp_id_set & other_set
    result = []
    for id in intersection:
        result.append(id_dict[id])
    return result

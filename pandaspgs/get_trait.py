from typing import List, Dict
from pandaspgs.client import get_trait_category, get_trait

def get_trait_categories(cached=True) -> List[Dict]:
    return get_trait_category('https://www.pgscatalog.org/rest/trait_category/all', cached)


def get_traits(trait_id: str = None, term: str = None, exact: bool = None, cached=True) -> List[Dict]:
    if trait_id is None and term is None and exact is None:
        return get_trait('https://www.pgscatalog.org/rest/trait/all?include_child_associated_pgs_ids=1', cached=cached)
    elif term is None and exact is not None:
        raise Exception("exact is available only if term is not None")
    elif trait_id is not None:
        by_other=get_trait('https://www.pgscatalog.org/rest/trait/%s?include_children=0'%trait_id, cached=cached)
        if term is None:
            return by_other
        else:
            by_pgs_id = get_trait("https://www.pgscatalog.org/rest/trait/search?include_children=0&term=%s"%term, cached=cached)
        other_set = set()
        pgs_id_dict = {}
        for single in by_pgs_id:
            pgs_id_dict[single['id']] = single
        pgs_id_set = pgs_id_dict.keys()
        for single in by_other:
            other_set.add(single['id'])
        intersection = pgs_id_set & other_set
        result = []
        for id in intersection:
            result.append(pgs_id_dict[id])
        return result
    else:
        return get_trait("https://www.pgscatalog.org/rest/trait/search?include_children=0&term=%s"%term, cached=cached)


def get_child_traits(trait_id: str = None, cached=True) -> List[Dict]:
    pass





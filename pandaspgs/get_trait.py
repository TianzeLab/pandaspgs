from typing import List, Dict

from pandas import DataFrame

from pandaspgs.client import get_trait_category, get_trait
from pandaspgs.trait import Trait

from pandas import DataFrame, Series, json_normalize, set_option
import numpy

def get_trait_categories(cached=True) -> List[Dict]:
    return get_trait_category('https://www.pgscatalog.org/rest/trait_category/all', cached)


def get_traits(trait_id: str = None, term: str = None, exact: bool = None, cached=True) -> Trait:
    if exact is not None:
        if exact:
            num = "1"
        else:
            num = "0"

    if trait_id is None and term is None and exact is None:
        return Trait(get_trait('https://www.pgscatalog.org/rest/trait/all?include_child_associated_pgs_ids=1'
                               , cached=cached))
    elif term is None and exact is not None:
        raise Exception("exact is available only if term is not None")
    elif trait_id is not None:
        by_other = get_trait('https://www.pgscatalog.org/rest/trait/%s?include_children=0' % trait_id
                             , cached=cached)
        if term is None:
            return Trait(by_other)
        else:
            if exact is not None:
                by_pgs_id = get_trait(
                    "https://www.pgscatalog.org/rest/trait/search?include_children=0&term=%s&exact=%s" % (term, num),
                    cached=cached)
            else:
                by_pgs_id = get_trait("https://www.pgscatalog.org/rest/trait/search?include_children=0&term=%s" % term,
                                      cached=cached)
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
        if exact is not None:
            return Trait(get_trait(
                "https://www.pgscatalog.org/rest/trait/search?include_children=0&term=%s&exact=%s" % (term, num),
                cached=cached))
        else:
            return Trait(get_trait("https://www.pgscatalog.org/rest/trait/search?include_children=0&term=%s" % term,
                                   cached=cached))


def get_child_traits(trait_id: str = None, cached=True) -> Trait:
    return Trait(get_trait('https://www.pgscatalog.org/rest/trait/%s?include_children=1' % trait_id, cached=cached))


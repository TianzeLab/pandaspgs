from typing import List, Dict
from pandaspgs.client import get_trait_category


def get_trait_categories(cached=True) ->  List[Dict]:
    return get_trait_category('https://www.pgscatalog.org/rest/trait_category/all',cached)
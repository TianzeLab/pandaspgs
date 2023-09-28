from typing import List, Dict
from pandaspgs.client import get_trait_category, get_trait


def get_trait_categories(cached=True) -> List[Dict]:
    return get_trait_category('https://www.pgscatalog.org/rest/trait_category/all', cached)


def get_traits(trait_id: str = None, term: str = None, exact: bool = None, cached=True) -> List[Dict]:
    pass


def get_child_traits(trait_id: str = None, cached=True) -> List[Dict]:
    pass

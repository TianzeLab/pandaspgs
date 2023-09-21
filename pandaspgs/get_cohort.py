from typing import List, Dict
from pandaspgs.client import get_cohort


def get_cohorts(cohort_symbol: str = None, cached=True) -> List[Dict]:
    if cohort_symbol is None:
        return get_cohort('https://www.pgscatalog.org/rest/cohort/all', cached=cached)
    by_id = None
    if cohort_symbol is not None:
        by_id = get_cohort('https://www.pgscatalog.org/rest/cohort/%s' % cohort_symbol, cached=cached)
    return by_id

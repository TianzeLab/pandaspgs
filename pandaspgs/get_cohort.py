from pandaspgs.client import get_cohort
from pandaspgs.cohort import Cohort


def get_cohorts(cohort_symbol: str = None, cached=True, mode: str = 'Fat') -> Cohort:
    if cohort_symbol is None:
        return Cohort(get_cohort('https://www.pgscatalog.org/rest/cohort/all', cached=cached), mode)
    by_id = None
    if cohort_symbol is not None:
        by_id = get_cohort('https://www.pgscatalog.org/rest/cohort/%s' % cohort_symbol, cached=cached)
    return Cohort(by_id, mode)

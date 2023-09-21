from typing import List, Dict
from pandaspgs.client import get_release
import re


def get_releases(date: str = 'latest', cached=True) -> List[Dict]:
    if date == 'all':
        return get_release('https://www.pgscatalog.org/rest/releases/all', cached=cached)
    if date == 'latest':
        return get_release('https://www.pgscatalog.org/rest/releases/rest/release/current', cached=cached)
    if date is None:
        raise Exception("Date can't be None.")
    if re.match('\\d{4}-\\d{2}-\\d{2}$', date) is None:
        raise Exception('The format of the date must be YYYY-MM-DD.')
    return get_release('https://www.pgscatalog.org/rest/releases/rest/release/%s' % date, cached=cached)

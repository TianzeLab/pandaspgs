from typing import List, Dict
from pandaspgs.client import get_release
from pandaspgs.release import Release
import re


def get_releases(date: str = 'latest', cached=True, mode: str = 'Fat') -> Release:
    if date == 'all':
        return Release(get_release('https://www.pgscatalog.org/rest/release/all', cached=cached), mode)
    if date == 'latest':
        return Release(get_release('https://www.pgscatalog.org/rest/release/current', cached=cached), mode)
    if date is None:
        raise Exception("Date can't be None.")
    if re.match('\\d{4}-\\d{2}-\\d{2}$', date) is None:
        raise Exception('The format of the date must be YYYY-MM-DD.')
    return Release(get_release('https://www.pgscatalog.org/rest/release/%s' % date, cached=cached), mode)


print(get_releases(date="2024-01-26").raw_data)

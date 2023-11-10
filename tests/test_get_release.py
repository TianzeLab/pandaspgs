from pandaspgs.get_release import get_releases


def test_get_releases():
    current = get_releases()
    all_release = get_releases(date='all')
    some_release = get_releases(date='2023-10-17')
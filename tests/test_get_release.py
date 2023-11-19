from pandaspgs.get_release import get_releases


def test_get_releases():
    current = get_releases()
    assert len(current) == 1
    all_release = get_releases(date='all')
    assert len(all_release) == 72
    some_release = get_releases(date='2023-10-17')
    assert len(some_release) == 1
    assert len(all_release[1:3]) == 2
    assert len(all_release[2]) == 1
    assert len(all_release['2023-10-17']) == 1
    assert len(all_release[range(2)]) == 2
    assert len(all_release ^ all_release[0]) == 71
    assert len(all_release[0] + all_release[1]) == 2
    assert len(all_release - all_release[0]) == 71
    assert len(all_release & all_release[1]) == 1
    assert len(all_release[0] | all_release[1]) == 2

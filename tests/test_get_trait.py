from pandaspgs.get_trait import get_trait_categories


def test_get_trait_categories():
    categories = get_trait_categories()
    assert len(categories) == 18

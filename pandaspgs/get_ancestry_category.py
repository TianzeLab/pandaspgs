from pandaspgs.client import get_ancestry_category
from pandaspgs.ancestrycategory import AncestryCategory


def get_ancestry_categories(cached=True, mode: str = 'Fat') -> AncestryCategory:
    return AncestryCategory(get_ancestry_category('https://www.pgscatalog.org/rest/ancestry_categories/',
                                                  cached=cached), mode)


a = get_ancestry_categories()
print(a.categories)
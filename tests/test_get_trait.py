from pandaspgs.get_trait import get_trait_categories
from pandaspgs.get_trait import get_traits

def test_get_trait_categories():
    categories = get_trait_categories()
    assert len(categories) == 18

def test_get_traits():
    filter_get_trait=get_traits(trait_id='EFO_0000305')
    assert len(filter_get_trait) == 1
    filter_get_trait_a = get_traits(trait_id='EFO_0001645')
    assert len(filter_get_trait_a) == 1
    filter_get_trait_b = get_traits(term='Alzheimer')
    assert len(filter_get_trait_b) == 4
    filter_get_trait_c = get_traits(term='Neurological disorder')
    assert len(filter_get_trait_c) == 103
    filter_get_trait_d = get_traits(trait_id="EFO_0005782",term='Neurological disorder')
    assert len(filter_get_trait_d) == 1
    filter_get_trait_e = get_traits()
    assert len(filter_get_trait_e) == 1183
    filter_get_trait_f = get_traits(term='Alzheimer',exact=False)
    assert len(filter_get_trait_f) == 4
    filter_get_trait_g = get_traits(trait_id="EFO_0005782", term='Neurological disorder',exact=False)
    assert len(filter_get_trait_g) == 1









from pandaspgs import Cohort
from pandaspgs.ancestry_category import AncestryCategory
from pandaspgs.performance import PerformanceMetric
from pandaspgs.publication import Publication
from pandaspgs.release import Release
from pandaspgs.sample_set import SampleSet
from pandaspgs.score import Score
from pandaspgs.trait import Trait
from pandaspgs.trait_category import TraitCategory


def bind(
        a: AncestryCategory | Cohort | PerformanceMetric | Publication | Release | SampleSet | Score | Trait | TraitCategory,
        b: AncestryCategory | Cohort | PerformanceMetric | Publication | Release | SampleSet | Score | Trait | TraitCategory) -> AncestryCategory | Cohort | PerformanceMetric | Publication | Release | SampleSet | Score | Trait | TraitCategory:
    """
    Binds together PGS objects of the same object. Note that bind() preserves duplicates whereas union() does not.

    Args:
        a: An object of the pandasPGS custom class.
        b: An object of the same type as a.

    Returns:
        An object of the same type as a.
    ```python
    from pandaspgs.get_cohort import get_cohorts
    from pandaspgs.set_operation import bind


    a = get_cohorts(cohort_symbol='100-plus')
    b = get_cohorts(cohort_symbol='23andMe')
    c = bind(a,b)
    ```

    """
    return a + b

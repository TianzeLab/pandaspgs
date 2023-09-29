from pandas import DataFrame, Series, json_normalize, set_option
import numpy

set_option('display.max_columns', None)
set_option('display.width', 1000)
set_option('display.colheader_justify', 'center')
set_option('display.precision', 3)


class Trait:
    def __init__(self, data:list=[], mode: str = "Fat"):
        if data is None:
            data = []
        if data is None:
            data = []
        if mode == "Thin":
            return
        if mode not in ['Thin', "Fat"]:
            raise Exception("Mode must be Fat or Thin")
        self.raw_data = data
        if data is None or len(data) == 0:
            self.efo_traits = DataFrame(
                columns=["id", "label", "description", "url", "trait_categories", "trait_synonyms",
                         "trait_mapped_terms", "associated_pgs_ids", "child_associated_pgs_ids"])
            return
        self.efo_traits: DataFrame = json_normalize(data, max_level=2)


    def __len__(self):
        return len(self.efo_traits)

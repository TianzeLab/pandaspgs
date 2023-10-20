# mode为Fat, trait在Thin模式基础上, 还有以下属性:EFO_traits, trait_categories, trait_synonyms, trait_mapped_terms,
# associated_pgs_ids, child_associated_pgs_ids. 这些属性的类型都为DataFrame, 各个DataFrame的列名和他们的关联参考PPT

from pandas import DataFrame, Series, json_normalize, set_option
import numpy

set_option('display.max_columns', None)
set_option('display.width', 1000)
set_option('display.colheader_justify', 'center')
set_option('display.precision', 3)


class Trait:
    def __init__(self, data: list = [], mode: str = "Fat"):
        if data is None:
            data = []
        if mode not in ['Thin', "Fat"]:
            raise Exception("Mode must be Fat or Thin")
        self.raw_data = data
        self.mode = mode
        if mode == "Thin":
            return
        if data is None or len(data) == 0:
            self.EFO_traits = DataFrame(
                columns=['id', 'label', 'description', 'url'])
            self.trait_categories = DataFrame(
                columns=['trait _id', 'trait_category'])
            self.trait_synonyms = DataFrame(columns=['trait_id', 'trait_synonym'])
            self.trait_mapped_terms = DataFrame(columns=['trait_id', 'trait_mapped_term'])
            self.associated_pgs_ids = DataFrame(columns=['trait_id', 'associated_pgs_id'])
            self.child_associated_pgs_ids = DataFrame(columns=['trait_id', 'child_associated_pgs_id'])
            return
        self.EFO_traits = json_normalize(data=data, max_level=1).drop(
            columns=['trait_categories', 'trait_synonyms', 'trait_mapped_terms',
                     'associated_pgs_ids', 'child_associated_pgs_ids'])
        if data[0]['trait_categories'] is not []:
            self.trait_categories = json_normalize(data=data, record_path=['trait_categories'], meta=['id'])
            self.trait_categories.columns = ['trait_category', 'trait_id']
        else:
            self.trait_categories = DataFrame(
                columns=['trait _id', 'trait_category'])
        if data[0]['trait_synonyms'] is not []:
            self.trait_synonyms = json_normalize(data=data, record_path=['trait_synonyms'], meta=['id'])
            self.trait_synonyms.columns = ['trait_synonym', 'trait_id']
        else:
            self.trait_synonyms = DataFrame(columns=['trait_id', 'trait_synonym'])
        if data[0]['trait_mapped_terms'] is not []:
            self.trait_mapped_terms = json_normalize(data=data, record_path=['trait_mapped_terms'], meta=['id'])
            self.trait_mapped_terms.columns = ['trait_mapped_term', 'trait_id']
        else:
            self.trait_mapped_terms = DataFrame(columns=['trait_id', 'trait_mapped_term'])
        if data[0]['associated_pgs_ids'] is not []:
            self.associated_pgs_ids = json_normalize(data=data, record_path=['associated_pgs_ids'], meta=['id'])
            self.associated_pgs_ids.columns = ['associated_pgs_id', 'trait_id']
        else:
            self.associated_pgs_ids = DataFrame(columns=['trait_id', 'associated_pgs_id'])
        if data[0]['child_associated_pgs_ids'] is not []:
            self.child_associated_pgs_ids = json_normalize(data=data, record_path=['child_associated_pgs_ids'], meta=['id'])
            self.child_associated_pgs_ids.columns = ['child_associated_pgs_id', 'trait_id']
        else:
            self.child_associated_pgs_ids = DataFrame(columns=['trait_id', 'child_associated_pgs_id'])
        return

    def __len__(self):
            return len(self.EFO_traits)



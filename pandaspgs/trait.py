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
        datas = json_normalize(data=data, max_level=1).drop(columns=['id', 'label', 'description', 'url'])
        datas['trait_categories'] = datas['trait_categories'].map(lambda x: x == [])
        datas['trait_synonyms'] = datas['trait_synonyms'].map(lambda x: x == [])
        datas['trait_mapped_terms'] = datas['trait_mapped_terms'].map(lambda x: x == [])
        datas['associated_pgs_ids'] = datas['associated_pgs_ids'].map(lambda x: x == [])
        datas['child_associated_pgs_ids'] = datas['child_associated_pgs_ids'].map(lambda x: x == [])
        self.EFO_traits = json_normalize(data=data, max_level=1).drop(
            columns=['trait_categories', 'trait_synonyms', 'trait_mapped_terms',
                     'associated_pgs_ids', 'child_associated_pgs_ids'])
        if not datas['trait_categories'].all():
            self.trait_categories = json_normalize(data=data, record_path=['trait_categories'], meta=['id'])
            self.trait_categories.columns = ['trait_category', 'trait_id']
        else:
            self.trait_categories = DataFrame(
                columns=['trait _id', 'trait_category'])
        if not datas['trait_synonyms'].all():
            self.trait_synonyms = json_normalize(data=data, record_path=['trait_synonyms'], meta=['id'])
            self.trait_synonyms.columns = ['trait_synonym', 'trait_id']
        else:
            self.trait_synonyms = DataFrame(columns=['trait_id', 'trait_synonym'])
        if not datas['trait_mapped_terms'].all():
            self.trait_mapped_terms = json_normalize(data=data, record_path=['trait_mapped_terms'], meta=['id'])
            self.trait_mapped_terms.columns = ['trait_mapped_term', 'trait_id']
        else:
            self.trait_mapped_terms = DataFrame(columns=['trait_id', 'trait_mapped_term'])
        if not datas['associated_pgs_ids'].all():
            self.associated_pgs_ids = json_normalize(data=data, record_path=['associated_pgs_ids'], meta=['id'])
            self.associated_pgs_ids.columns = ['associated_pgs_id', 'trait_id']
        else:
            self.associated_pgs_ids = DataFrame(columns=['trait_id', 'associated_pgs_id'])
        if not datas['child_associated_pgs_ids'].all():
            self.child_associated_pgs_ids = json_normalize(data=data, record_path=['child_associated_pgs_ids'],
                                                           meta=['id'])
            self.child_associated_pgs_ids.columns = ['child_associated_pgs_id', 'trait_id']
        else:
            self.child_associated_pgs_ids = DataFrame(columns=['trait_id', 'child_associated_pgs_id'])
        return

    def __str__(self):
        if self.mode == 'Fat':
            return ("Trait is running in fat mode. It has 6 DataFrames with hierarchical dependencies.\nEFO_traits: "
                    "%d rows\n|\n -associated_pgs_ids: %d rows\n|\n -child_associated_pgs_ids:"
                    "%d rows\n|\n -trait_categories: %d rows\n|\n -trait_mapped_terms: %d rows\n|\n -trait_synonyms:"
                    " %d rows" % (
                    len(self.EFO_traits), len(self.associated_pgs_ids), len(self.child_associated_pgs_ids),
                    len(self.trait_categories), len(self.trait_mapped_terms)
                    , len(self.trait_synonyms)))
        if self.mode == 'Thin':
            return ('Trait is running in thin mode. It has 1 list that contains the raw data.\nraw_data: a list of '
                    'size x.')

    def __getitem__(self, item):
        if isinstance(item, str) or isinstance(item, int):
            arr = [item]
        elif isinstance(item, list) or isinstance(item, tuple) or isinstance(item, range):
            arr = item
        elif isinstance(item, slice):
            start, stop, step = item.indices(len(self))
            arr = list(range(start, stop, step))
        else:
            raise TypeError('Invalid argument type：{}'.format(type(item)))
        raw_data = self.raw_data
        raw_data_dict = {}
        for j in raw_data:
            raw_data_dict[j['id']] = j
        sub_set = []
        for i in arr:
            if isinstance(i, str):
                sub_set.append(raw_data_dict[i])
            elif isinstance(i, int):
                sub_set.append(raw_data[i])
            else:
                raise TypeError('Invalid item type: {}'.format(type(i)))
        return Trait(sub_set, self.mode)

    def __add__(self, other):
        if self.mode == other.mode:
            return Trait(self.raw_data + other.raw_data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __sub__(self, other):
        if self.mode == other.mode:
            self_key_set = set()
            self_dict = {}
            other_key_set = set()
            for i in self.raw_data:
                self_key_set.add(i['id'])
                self_dict[i['id']] = i
            for j in other.raw_data:
                other_key_set.add(j['id'])
            sub_key = self_key_set - other_key_set
            data = []
            for k in sub_key:
                data.append(self_dict[k])
            return Trait(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __and__(self, other):
        if self.mode == other.mode:
            self_key_set = set()
            self_dict = {}
            other_key_set = set()
            for i in self.raw_data:
                self_key_set.add(i['id'])
                self_dict[i['id']] = i
            for j in other.raw_data:
                other_key_set.add(j['id'])
            sub_key = self_key_set & other_key_set
            data = []
            for k in sub_key:
                data.append(self_dict[k])
            return Trait(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __or__(self, other):
        if self.mode == other.mode:
            and_dict = {}
            for i in self.raw_data:
                and_dict[i['id']] = i
            for j in other.raw_data:
                and_dict[j['id']] = j
            data = list(and_dict.values())
            return Trait(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __xor__(self, other):
        if self.mode == other.mode:
            self_key_set = set()
            and_dict = {}
            other_key_set = set()
            for i in self.raw_data:
                self_key_set.add(i['id'])
                and_dict[i['id']] = i
            for j in other.raw_data:
                other_key_set.add(j['id'])
                and_dict[j['id']] = j
            sub_key = self_key_set ^ other_key_set
            data = []
            for k in sub_key:
                data.append(and_dict[k])
            return Trait(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __eq__(self, other):
        if self is None or other is None:
            return self is None and other is None
        return self.raw_data == other.raw_data and self.mode == other.mode

    def __len__(self):
        return len(self.raw_data)

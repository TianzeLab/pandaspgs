from pandas import DataFrame, Series, json_normalize, set_option
import numpy

set_option('display.max_columns', None)
set_option('display.width', 1000)
set_option('display.colheader_justify', 'center')
set_option('display.precision', 3)


class Release:
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
            self.releases = ['date', 'score_count', 'performance_count', 'publication_count', 'notes']
            self.released_score_ids = ['release_date', 'released_score_id']
            self.released_publication_ids = ['release_date', 'released_publication']
            self.released_performance_ids = ['release_date', 'released_performance_id']
            return
        datas = json_normalize(data=data, max_level=1)
        datas['released_score_ids'] = datas['released_score_ids'].map(lambda x: x == [])
        datas['released_publication_ids'] = datas['released_publication_ids'].map(lambda x: x == [])
        datas['released_performance_ids'] = datas['released_performance_ids'].map(lambda x: x == [])
        self.releases = json_normalize(data=data, max_level=1).drop(
            columns=['released_score_ids', 'released_publication_ids', 'released_performance_ids'])
        if not datas['released_score_ids'].all():
            self.released_score_ids = json_normalize(data=data, record_path=['released_score_ids'], meta=['date'])
            self.released_score_ids.columns = ['released_score_id', 'release_date']
        else:
            self.released_score_ids = DataFrame(
                columns=['released_score_id', 'release_date'])
        if not datas['released_publication_ids'].all():
            self.released_publication_ids = json_normalize(data=data, record_path=['released_publication_ids'],
                                                           meta=['date'])
            self.released_publication_ids.columns = ['released_publication_id', 'release_date']
        else:
            self.released_publication_ids = DataFrame(columns=['released_publication_id', 'release_date'])
        if not datas['released_performance_ids'].all():
            self.released_performance_ids = json_normalize(data=data, record_path=['released_performance_ids'],
                                                           meta=['date'])
            self.released_performance_ids.columns = ['released_performance_id', 'release_date']
        else:
            self.released_performance_ids = DataFrame(columns=['released_performance_id', 'release_date'])
        return

    def __str__(self):
        if self.mode == 'Fat':
            return ("Trait is running in fat mode. It has 4 DataFrames with hierarchical dependencies.\n-releases: "
                    "%d rows\n|\n -released_score_ids: %d rows\n|\n -released_publication_ids:"
                    "%d rows\n|\n -released_performance_ids: %d rows" % (
                        len(self.releases), len(self.released_score_ids), len(self.released_publication_ids),
                        len(self.released_performance_ids)))
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
            raw_data_dict[j['date']] = j
        sub_set = []
        for i in arr:
            if isinstance(i, str):
                sub_set.append(raw_data_dict[i])
            elif isinstance(i, int):
                sub_set.append(raw_data[i])
            else:
                raise TypeError('Invalid item type: {}'.format(type(i)))
        return Release(sub_set, self.mode)

    def __add__(self, other):
        if self.mode == other.mode:
            return Release(self.raw_data + other.raw_data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __sub__(self, other):
        if self.mode == other.mode:
            self_key_set = set()
            self_dict = {}
            other_key_set = set()
            for i in self.raw_data:
                self_key_set.add(i['date'])
                self_dict[i['date']] = i
            for j in other.raw_data:
                other_key_set.add(j['date'])
            sub_key = self_key_set - other_key_set
            data = []
            for k in sub_key:
                data.append(self_dict[k])
            return Release(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __and__(self, other):
        if self.mode == other.mode:
            self_key_set = set()
            self_dict = {}
            other_key_set = set()
            for i in self.raw_data:
                self_key_set.add(i['date'])
                self_dict[i['date']] = i
            for j in other.raw_data:
                other_key_set.add(j['date'])
            sub_key = self_key_set & other_key_set
            data = []
            for k in sub_key:
                data.append(self_dict[k])
            return Release(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __or__(self, other):
        if self.mode == other.mode:
            and_dict = {}
            for i in self.raw_data:
                and_dict[i['date']] = i
            for j in other.raw_data:
                and_dict[j['date']] = j
            data = list(and_dict.values())
            return Release(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __xor__(self, other):
        if self.mode == other.mode:
            self_key_set = set()
            and_dict = {}
            other_key_set = set()
            for i in self.raw_data:
                self_key_set.add(i['date'])
                and_dict[i['date']] = i
            for j in other.raw_data:
                other_key_set.add(j['date'])
                and_dict[j['date']] = j
            sub_key = self_key_set ^ other_key_set
            data = []
            for k in sub_key:
                data.append(and_dict[k])
            return Release(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __eq__(self, other):
        if self is None or other is None:
            return self is None and other is None
        return self.raw_data == other.raw_data and self.mode == other.mode

    def __len__(self):
        return len(self.raw_data)

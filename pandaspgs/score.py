from pandas import DataFrame, json_normalize, set_option, Series
from pandas import concat

set_option('display.max_columns', None)
set_option('display.width', 1000)
set_option('display.colheader_justify', 'center')
set_option('display.precision', 3)
import numpy


class Score:
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
            self.scores = DataFrame(
                columns=['id'
                         'name'
                         'ftp_scoring_file'
                         'ftp_harmonized_scoring_files.GRCh37.positions'
                         'ftp_harmonized_scoring_files.GRCh38.positions'
                         'publication.id'
                         'publication.title'
                         'publication.doi'
                         'publication.PMID'
                         'publication.journal'
                         'publication.firstauthor'
                         'publication.date_publication'
                         'matches_publication'
                         'trait_reported'
                         'trait_additional'
                         'method_name'
                         'method_params'
                         'variants_number'
                         'variants_interactions'
                         'variants_genomebuild'
                         'weight_type'
                         'date_release'
                         'license'
                         ])
            self.samples_variants = DataFrame(
                columns=['id'
                         'score_id'
                         'sample_number'
                         'sample_cases'
                         'sample_controls'
                         'sample_percent_male'
                         'sample_age.estimate_type'
                         'sample_age.estimate'
                         'sample_age.interval.type'
                         'sample_age.interval.lower'
                         'sample_age.interval.upper'
                         'sample_age.variability_type'
                         'sample_age.variability'
                         'sample_age.unit'
                         'phenotyping_free'
                         'followup_time.estimate_type'
                         'followup_time.estimate'
                         'followup_time.interval.type'
                         'followup_time.interval.lower'
                         'followup_time.interval.upper'
                         'followup_time.variability_type'
                         'followup_time.variability'
                         'followup_time.unit'
                         'ancestry_broad'
                         'ancestry_free'
                         'ancestry_country'
                         'ancestry_additional'
                         'source_GWAS_catalog'
                         'source_PMID'
                         'source_DOI'
                         'cohorts_additional'
                         ])
            self.samples_variants_cohorts = DataFrame(
                columns=['score_id'
                         'sample_id'
                         'name_short'
                         'name_full'
                         'name_others'])
            self.trait_efo = DataFrame(
                columns=['score_i'
                         'id'
                         'label'
                         'description'
                         'url'
                         ])
            self.samples_training = DataFrame(
                columns=['id'
                         'score_id'
                         'sample_number'
                         'sample_cases'
                         'sample_controls'
                         'sample_percent_male'
                         'sample_age.estimate_type'
                         'sample_age.estimate'
                         'sample_age.interval.type'
                         'sample_age.interval.lower'
                         'sample_age.interval.upper'
                         'sample_age.variability_type'
                         'sample_age.variability'
                         'sample_age.unit'
                         'phenotyping_free'
                         'followup_time.estimate_type'
                         'followup_time.estimate'
                         'followup_time.interval.type'
                         'followup_time.interval.lower'
                         'followup_time.interval.upper'
                         'followup_time.variability_type'
                         'followup_time.variability'
                         'followup_time.unit'
                         'ancestry_broad'
                         'ancestry_free'
                         'ancestry_country'
                         'ancestry_additional'
                         'source_GWAS_catalog'
                         'source_PMID'
                         'source_DOI'
                         'cohorts_additional'
                         ])
            self.samples_training_cohorts = DataFrame(
                columns=['score_id'
                         'sample_id'
                         'name_short'
                         'name_full'
                         'name_others'
                         ])
            self.ancestry_distribution = DataFrame(
                columns=['score_id'
                         'stage'
                         'dist'
                         'count'
                         'multi'])
            return
        datas = json_normalize(data=data, max_level=1)
        datas['samples_variants'] = datas['samples_variants'].map(lambda x: x == [])
        datas['samples_training'] = datas['samples_training'].map(lambda x: x == [])
        datas['trait_efo'] = datas['trait_efo'].map(lambda x: x == [])
        datas['ancestry_distribution.eval'] = datas['ancestry_distribution.eval'].map(lambda x: x == [])
        datas['ancestry_distribution.gwas'] = datas['ancestry_distribution.gwas'].map(lambda x: x == [])
        self.scores = json_normalize(data=data, max_level=1).drop(
            columns=['samples_variants', 'samples_training',
                     'trait_efo', 'ancestry_distribution.eval', 'ancestry_distribution.gwas'])
        self.scores['ftp_harmonized_scoring_files.GRCh38.positions'] = self.scores[
            'ftp_harmonized_scoring_files.GRCh38'].map(
            lambda x: x['positions'])
        self.scores['ftp_harmonized_scoring_files.GRCh37.positions'] = self.scores[
            'ftp_harmonized_scoring_files.GRCh37'].map(
            lambda x: x['positions'])
        if not datas['samples_variants'].all():
            self.samples_variants = json_normalize(data=data, record_path=['samples_variants'], meta=['id'])
            self.samples_variants['score_id'] = self.samples_variants['id']
            self.samples_variants['id'] = Series(data=range(0, len(self.samples_variants)))
            cohort = self.samples_variants[['id', 'score_id', 'cohorts']].copy()
            self.samples_variants = self.samples_variants.drop(columns=['cohorts'])
            cohort['sample_id'] = cohort['id']
            cohort['cohorts'] = cohort['cohorts'].apply(lambda x: x if len(x) > 0 else numpy.nan)
            cohort = cohort.dropna()
            cohort = cohort.explode('cohorts')
            if len(cohort) == 0:
                self.samples_variants_cohorts = DataFrame(
                    columns=['score_id'
                             'sample_id'
                             'name_short'
                             'name_full'
                             'name_others'])
            else:
                cohort[['name_short', 'name_full', 'name_others']] = cohort['cohorts'].apply(
                    lambda x: Series(data=[x['name_short'], x['name_full'], x['name_others']]))
                cohort = cohort.drop(columns=['id', 'cohorts'])
            self.samples_variants_cohorts = cohort

        else:
            self.samples_variants = DataFrame(
                columns=['id'
                         'score_id'
                         'sample_number'
                         'sample_cases'
                         'sample_controls'
                         'sample_percent_male'
                         'sample_age.estimate_type'
                         'sample_age.estimate'
                         'sample_age.interval.type'
                         'sample_age.interval.lower'
                         'sample_age.interval.upper'
                         'sample_age.variability_type'
                         'sample_age.variability'
                         'sample_age.unit'
                         'phenotyping_free'
                         'followup_time.estimate_type'
                         'followup_time.estimate'
                         'followup_time.interval.type'
                         'followup_time.interval.lower'
                         'followup_time.interval.upper'
                         'followup_time.variability_type'
                         'followup_time.variability'
                         'followup_time.unit'
                         'ancestry_broad'
                         'ancestry_free'
                         'ancestry_country'
                         'ancestry_additional'
                         'source_GWAS_catalog'
                         'source_PMID'
                         'source_DOI'
                         'cohorts_additional'
                         ])
            self.samples_variants_cohorts = DataFrame(
                columns=['score_id'
                         'sample_id'
                         'name_short'
                         'name_full'
                         'name_others'])
        if not datas['samples_training'].all():
            self.samples_training = json_normalize(data=data, record_path=['samples_training'], meta=['id'])
            self.samples_training['score_id'] = self.samples_training['id']
            self.samples_training['id'] = Series(data=range(0, len(self.samples_training)))
            cohort = self.samples_training[['id', 'score_id', 'cohorts']].copy()
            self.samples_training = self.samples_training.drop(columns=['cohorts'])
            cohort['sample_id'] = cohort['id']
            cohort['cohorts'] = cohort['cohorts'].apply(lambda x: x if len(x) > 0 else numpy.nan)
            cohort = cohort.dropna()
            cohort = cohort.explode('cohorts')
            if len(cohort) == 0:
                self.samples_variants_cohorts = DataFrame(
                    columns=['score_id'
                             'sample_id'
                             'name_short'
                             'name_full'
                             'name_others'])
            cohort[['name_short', 'name_full', 'name_others']] = cohort['cohorts'].apply(
                lambda x: Series(data=[x['name_short'], x['name_full'], x['name_others']]))
            cohort = cohort.drop(columns=['id', 'cohorts'])
            self.samples_training_cohorts = cohort

        else:
            self.samples_training = DataFrame(
                columns=['id'
                         'score_id'
                         'sample_number'
                         'sample_cases'
                         'sample_controls'
                         'sample_percent_male'
                         'sample_age.estimate_type'
                         'sample_age.estimate'
                         'sample_age.interval.type'
                         'sample_age.interval.lower'
                         'sample_age.interval.upper'
                         'sample_age.variability_type'
                         'sample_age.variability'
                         'sample_age.unit'
                         'phenotyping_free'
                         'followup_time.estimate_type'
                         'followup_time.estimate'
                         'followup_time.interval.type'
                         'followup_time.interval.lower'
                         'followup_time.interval.upper'
                         'followup_time.variability_type'
                         'followup_time.variability'
                         'followup_time.unit'
                         'ancestry_broad'
                         'ancestry_free'
                         'ancestry_country'
                         'ancestry_additional'
                         'source_GWAS_catalog'
                         'source_PMID'
                         'source_DOI'
                         'cohorts_additional'
                         ])
            self.samples_training_cohorts = DataFrame(
                columns=['score_id'
                         'sample_id'
                         'name_short'
                         'name_full'
                         'name_others'
                         ])
        for i in range(len(data)):
            data[i]['id1'] = data[i]['id']
        if not datas['trait_efo'].all():
            self.trait_efo = json_normalize(data=data, record_path=['trait_efo'], meta=['id1'])
            self.trait_efo['score_id'] = self.trait_efo['id1']
            self.trait_efo = self.trait_efo.drop(columns=['id1'])
        else:
            self.trait_efo = DataFrame(
                columns=['score_i'
                         'id'
                         'label'
                         'description'
                         'url'])
        if not datas['ancestry_distribution.gwas'].all() or not datas['ancestry_distribution.gwas.'].all():
            a = json_normalize(data=data, max_level=1)
            dva = a[['id', 'ancestry_distribution.eval']].copy()
            dva['stage'] = 'eval'
            dva['ancestry_distribution'] = dva['ancestry_distribution.eval']
            dva = dva.drop(columns=['ancestry_distribution.eval'])
            eva = a[['id', 'ancestry_distribution.gwas']].copy()
            eva['stage'] = 'gwas'
            eva['ancestry_distribution'] = eva['ancestry_distribution.gwas']
            eva = eva.drop(columns=['ancestry_distribution.gwas'])
            b = concat([dva, eva])
            b['score_id'] = b['id']
            b = b.dropna()
            b.index = range(len(b))
            for i in range(len(b['ancestry_distribution'])):
                if not ('multi' in b['ancestry_distribution'][i]):
                    b['ancestry_distribution'][i]['multi'] = None

            b[['dist', 'count', 'multi']] = b['ancestry_distribution'].apply(
                lambda x: Series(data=[x['dist'], x['count'], x['multi']]))
            b = b.drop(columns=['id', 'ancestry_distribution'])
            self.ancestry_distribution = b




        else:
            self.ancestry_distribution = DataFrame(
                columns=['score_id'
                         'stage'
                         'dist'
                         'count'
                         'multi'])

        if 'publication' in self.scores.columns:
            self.scores.drop(columns=['pubication'])
            self.scores = self.scores.reindex(
                columns=self.scores.columns.tolist() + ['publication.id'
                                                        'publication.title'
                                                        'publication.doi'
                                                        'publication.PMID'
                                                        'publication.journal'
                                                        'publication.firstauthor'
                                                        'publication.date_publication'])
        if 'samples_age' in self.samples_variants.columns:
            self.samples_variants.drop(columns=['samples_age'])
            self.samples_variants = self.samples_variants.reindex(
                columns=self.samples_variants.columns.tolist() + ['sample_age.estimate_type'
                                                                  'sample_age.estimate'
                                                                  'sample_age.interval.type'
                                                                  'sample_age.interval.lower'
                                                                  'sample_age.interval.upper'
                                                                  'sample_age.variability_type'
                                                                  'sample_age.variability'
                                                                  'sample_age.unit']
            )
        if 'followup_time' in self.samples_variants.columns:
            self.samples_variants.drop(columns=['followup_time'])
            self.samples_variants = self.samples_variants.reindex(
                columns=self.samples_variants.columns.tolist() + ['followup_time.estimate_type'
                                                                  'followup_time.estimate'
                                                                  'followup_time.interval.type'
                                                                  'followup_time.interval.lower'
                                                                  'followup_time.interval.upper'
                                                                  'followup_time.variability_type'
                                                                  'followup_time.variability'
                                                                  'followup_time.unit'])
        if 'samples_age' in self.samples_training.columns:
            self.samples_training.drop(columns=['samples_age'])
            self.samples_training = self.samples_training.reindex(
                columns=self.samples_training.columns.tolist() + ['sample_age.estimate_type'
                                                                  'sample_age.estimate'
                                                                  'sample_age.interval.type'
                                                                  'sample_age.interval.lower'
                                                                  'sample_age.interval.upper'
                                                                  'sample_age.variability_type'
                                                                  'sample_age.variability'
                                                                  'sample_age.unit']
            )
        if 'followup_time' in self.samples_training.columns:
            self.samples_training.drop(columns=['followup_time'])
            self.samples_training = self.samples_training.reindex(
                columns=self.samples_training.columns.tolist() + ['followup_time.estimate_type'
                                                                  'followup_time.estimate'
                                                                  'followup_time.interval.type'
                                                                  'followup_time.interval.lower'
                                                                  'followup_time.interval.upper'
                                                                  'followup_time.variability_type'
                                                                  'followup_time.variability'
                                                                  'followup_time.unit'])
        return

    def __str__(self):
        if self.mode == 'Fat':
            return ("Score is running in fat mode. It has 7 DataFrames with hierarchical dependencies.\n"
                    "scores:%d rows\n|\n -samples_varients: %d rows\n  |\n   -samples_variants_cohorts: %d rows\n|\n "
                    "-samples_training: %d rows"
                    "\n|\n  -samples_training_cohorts: %d rows"
                    "\n|\n -trait_efo: %d rows"
                    "\n|\n -ancestry_distribution: %d rows" % (
                        len(self.scores), len(self.samples_variants), len(self.samples_variants_cohorts),
                        len(self.samples_training), len(self.samples_training_cohorts), len(self.trait_efo),
                        len(self.ancestry_distribution)))
        if self.mode == 'Thin':
            return ('Score is running in thin mode. It has 1 list that contains the raw data.\n raw_data: '
                    'a list of size %d.' % len(self.raw_data))

    def __repr__(self):
        return self.__str__()

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
        return Score(sub_set, self.mode)

    def __add__(self, other):
        if self.mode == other.mode:
            return Score(self.raw_data + other.raw_data, self.mode)
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
            return Score(data, self.mode)
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
            return Score(data, self.mode)
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
            return Score(data, self.mode)
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
            return Score(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __eq__(self, other):
        if self is None or other is None:
            return self is None and other is None
        return self.raw_data == other.raw_data and self.mode == other.mode

    def __len__(self):
        return len(self.raw_data)
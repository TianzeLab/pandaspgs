from pandas import DataFrame, json_normalize, set_option, Series

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
        # ['id', 'name', 'ftp_scoring_file', 'matches_publication', 'samples_variants', 'samples_training',
        #  'trait_reported', 'trait_additional', 'trait_efo', 'method_name', 'method_params', 'variants_number',
        #  'variants_interactions', 'variants_genomebuild', 'weight_type', 'date_release', 'license',
        #  'ftp_harmonized_scoring_files.GRCh37', 'ftp_harmonized_scoring_files.GRCh38', 'publication.id',
        #  'publication.title', 'publication.doi', 'publication.PMID', 'publication.journal', 'publication.firstauthor',
        #  'publication.date_publication', 'ancestry_distribution.eval', 'ancestry_distribution.gwas']
        datas['samples_variants'] = datas['samples_variants'].map(lambda x: x == [])
        datas['performance_metrics.effect_sizes'] = datas['performance_metrics.effect_sizes'].map(lambda x: x == [])
        datas['performance_metrics.class_acc'] = datas['performance_metrics.class_acc'].map(lambda x: x == [])
        datas['performance_metrics.othermetrics'] = datas['performance_metrics.othermetrics'].map(lambda x: x == [])
        self.performance_metrics = json_normalize(data=data, max_level=1).drop(
            columns=['sampleset.samples', 'performance_metrics.effect_sizes',
                     'performance_metrics.class_acc',
                     'performance_metrics.othermetrics'])
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
            cohort[['name_short', 'name_full', 'name_others']] = cohort['cohorts'].apply(
                lambda x: Series(data=[x['name_short'], x['name_full'], x['name_others']]))
            cohort = cohort.drop(columns=['id', 'cohorts'])
            self.samples_variants_cohorts = cohort

        else:
            self.samples_variants = DataFrame(
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
            self.samples_variants_cohorts = DataFrame(
                columns=['score_id'
                         'sample_id'
                         'name_short'
                         'name_full'
                         'name_others'])
        if not datas['samples_variants'].all():
            self.samples_training = json_normalize(data=data, record_path=['samples_training'], meta=['id'])
            self.samples_training['score_id'] = self.samples_training['id']
            self.samples_training['id'] = Series(data=range(0, len(self.samples_training)))
            cohort = self.samples_training[['id', 'score_id', 'cohorts']].copy()
            self.samples_training = self.samples_training.drop(columns=['cohorts'])
            cohort['sample_id'] = cohort['id']
            cohort['cohorts'] = cohort['cohorts'].apply(lambda x: x if len(x) > 0 else numpy.nan)
            cohort = cohort.dropna()
            cohort = cohort.explode('cohorts')
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
            
        if not datas['performance_metrics.effect_sizes'].all():
            self.effect_sizes = json_normalize(data=data, record_path=['performance_metrics', 'effect_sizes'],
                                               meta=['id'])
            self.effect_sizes['performance_metric_id'] = self.effect_sizes['id']
            self.effect_sizes = self.effect_sizes.drop(columns=['id'])
        else:
            self.effect_sizes = DataFrame(
                columns=['performance_metric_id', 'name_long', 'name_short', 'estimate', 'ci_lower', 'ci_upper', 'se'])
        if not datas['performance_metrics.class_acc'].all():
            self.class_acc = json_normalize(data=data, record_path=['performance_metrics', 'class_acc'], meta=['id'])
            self.class_acc['performance_metric_id'] = self.class_acc['id']
            self.class_acc = self.class_acc.drop(columns=['id'])
        else:
            self.class_acc = DataFrame(
                columns=['performance_metric_id', 'name_long', 'name_short', 'estimate', 'ci_lower', 'ci_upper', 'se'])
        if not datas['performance_metrics.othermetrics'].all():
            self.othermetrics = json_normalize(data=data, record_path=['performance_metrics', 'othermetrics'],
                                               meta=['id'])
            self.othermetrics['performance_metric_id'] = self.othermetrics['id']
            self.othermetrics = self.othermetrics.drop(columns=['id'])
        else:
            self.othermetrics = DataFrame(
                columns=['performance_metric_id', 'name_long', 'name_short', 'estimate', 'ci_lower', 'ci_upper', 'se'])
        if 'publication' in self.performance_metrics.columns:
            self.performance_metrics.drop(columns=['pubication'])
            self.performance_metrics = self.performance_metrics.reindex(
                columns=self.performance_metrics.columns.tolist() + ['publication.title',
                                                                     'publication.doi', 'publication.PMID',
                                                                     'publication.journal',
                                                                     'publication.firstauthor',
                                                                     'publication.date_publication'])
        if 'sample_age' in self.samples:
            self.samples.drop(columns=['samples_age'])
            self.samples = self.samples.reindex(
                columns=self.samples.columns.tolist() + ['sample_age.estimate_type', 'sample_age.estimate',
                                                         'sample_age.interval.type', 'sample_age.interval.lower',
                                                         'sample_age.interval.upper',
                                                         'sample_age.variability_type', 'sample_age.variability',
                                                         'sample_age.unit']
            )
        if 'followup_time' in self.samples:
            self.samples.drop(columns=['followup_time'])
            self.samples = self.samples.reindex(
                columns=self.samples.columns.tolist() + ['followup_time.estimate_type', 'followup_time.estimate',
                                                         'followup_time.interval.type', 'followup_time.interval.lower',
                                                         'followup_time.interval.upper',
                                                         'followup_time.variability_type', 'followup_time.variability',
                                                         'followup_time.unit'])
        return

    def __str__(self):
        if self.mode == 'Fat':
            return ("PerformanceMetric is running in fat mode. It has 6 DataFrames with hierarchical dependencies.\n"
                    "performance_metrics:"
                    "%d rows\n|\n -samples: %d rows\n  |\n   -cohorts: %d rows\n|\n -effect_sizes: %d rows"
                    "\n|\n -class_acc: %d rows"
                    "\n|\n -othermetrics: %d rows" % (
                        len(self.performance_metrics), len(self.samples), len(self.cohorts),
                        len(self.effect_sizes), len(self.class_acc), len(self.othermetrics)))
        if self.mode == 'Thin':
            return ('PerformanceMetrics is running in thin mode. It has 1 list that contains the raw data.\nraw_data: '
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
        return PerformanceMetrics(sub_set, self.mode)

    def __add__(self, other):
        if self.mode == other.mode:
            return PerformanceMetrics(self.raw_data + other.raw_data, self.mode)
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
            return PerformanceMetrics(data, self.mode)
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
            return PerformanceMetrics(data, self.mode)
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
            return PerformanceMetrics(data, self.mode)
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
            return PerformanceMetrics(data, self.mode)
        else:
            raise Exception("Please input the same mode")

    def __eq__(self, other):
        if self is None or other is None:
            return self is None and other is None
        return self.raw_data == other.raw_data and self.mode == other.mode

    def __len__(self):
        return len(self.raw_data)

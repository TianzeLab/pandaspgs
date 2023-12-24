import numpy

from pandaspgs.get_sample_set import get_sample_sets
from pandas import DataFrame, json_normalize, set_option, Series

set_option('display.max_columns', None)
set_option('display.width', 1000)
set_option('display.colheader_justify', 'center')
set_option('display.precision', 3)


def test_get_sample_sets():
    all_ss=get_sample_sets()
    df=json_normalize(data=all_ss, record_path=['samples'],meta='id')
    df['sample_set_id']=df['id']
    df['id']=Series(data=range(0,len(df)))
    cohort=df[['id','sample_set_id','cohorts']].copy()
    df=df.drop(columns=['cohorts'])

    cohort['sample_id']=cohort['id']
    cohort['cohorts']=cohort['cohorts'].apply(lambda x: x if len(x) > 0 else numpy.nan)
    cohort = cohort.dropna()
    cohort = cohort.explode('cohorts')
    cohort[['name_short','name_full','name_others']] = cohort['cohorts'].apply(lambda x: Series(data=[x['name_short'], x['name_full'], x['name_others']]))



    cohort=cohort.drop(columns=['id','cohorts'])
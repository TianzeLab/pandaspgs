import os
import sys
import re

import requests
from pandas import DataFrame, read_table, Series
from requests.adapters import HTTPAdapter

from pandaspgs import get_scores

s = requests.Session()
s.mount('https://', HTTPAdapter(max_retries=5))
home_path = os.path.expanduser('~') + os.sep + 'pandaspgs_home'


def read_scoring_file(pgs_id: str = None, grch: str = 'GRCh37') -> DataFrame:
    """
    Download a scoring file and convert it to a DataFrame. The directory of the downloaded file is $HOME/pandaspgs_home.

    Args:
        pgs_id: Polygenic Score ID.
        grch: GRCh37 or GRCh38.

    Returns:
        A DataFrame.

    ```Python
    from pandaspgs import read_scoring_file

    df = read_scoring_file(pgs_id='PGS000737')
    ```
    """
    if pgs_id is None:
        raise Exception("pgs_id can't be None.")
    raw_score_data = get_scores(pgs_id=pgs_id).raw_data
    if len(raw_score_data) != 1:
        raise Exception("Unable to find the link to download. Please check the pgs_id.")
    url = raw_score_data[0]['ftp_harmonized_scoring_files'][grch]['positions']
    match_obj = re.match('.*/(.*)', url)
    file_name = match_obj.group(1)
    os.makedirs(home_path, exist_ok=True)

    with s.get(url, timeout=60, stream=True) as r:
        online_size = r.headers.get('content-length', 0)
        local_size = 0
        if os.path.exists(home_path + os.sep + file_name):
            local_size = os.path.getsize(home_path + os.sep + file_name)
        if local_size > 0 and (int(online_size) == local_size):
            sys.stdout.write('[SKIP]: %s has been downloaded in %s\n' % (file_name, home_path))
        else:
            r.raise_for_status()
            with open(home_path + os.sep + file_name, 'wb') as f:
                i = 0
                for chunk in r.iter_content(chunk_size=1024):
                    i += 1024
                    sys.stdout.write('%s downloading: %.2f MB\r' % (file_name, i / 1024 / 1024))
                    f.write(chunk)
            sys.stdout.write('%s(%.2f MB) has been downloaded in %s\n' % (file_name, i / 1024 / 1024, home_path))

    df = read_table(home_path + os.sep + file_name, comment='#', compression='gzip')
    return df


def genotype_weighted_score(s: Series) -> DataFrame:
    genotype = [s['effect_allele'] + '/' + s['effect_allele'], s['effect_allele'] + '/' + s['other_allele'],
                s['other_allele'] + '/' + s['other_allele']]
    weighted_score = [2 * s['effect_weight'], 1 * s['effect_weight'], 0 * s['effect_weight']]
    data = {s['rsID'] + "_genotype": genotype, s['rsID'] + "_weighted_score": weighted_score}
    return DataFrame(data=data)

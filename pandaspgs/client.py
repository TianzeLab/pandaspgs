import requests
import json
import progressbar
from typing import List, Dict
from requests.adapters import HTTPAdapter
from cachetools import TTLCache

fields = ['Score','Publication','Trait','Trait_category','Performance','Cohort','Sample_set','Release']
fields_and_all = ['All', 'Score','Publication','Trait','Trait_category','Performance','Cohort','Sample_set','Release']
publication_cache = TTLCache(maxsize=1024, ttl=60 * 60)
score_cache = TTLCache(maxsize=1024, ttl=60 * 60)
trait_cache = TTLCache(maxsize=1024, ttl=60 * 60)
trait_category_cache = TTLCache(maxsize=1024, ttl=60 * 60)
performance_cache = TTLCache(maxsize=1024, ttl=60 * 60)
cohort_cache = TTLCache(maxsize=1024, ttl=60 * 60)
sample_set_cache = TTLCache(maxsize=1024, ttl=60 * 60)
release_cache = TTLCache(maxsize=1024, ttl=60 * 60)


def get_publication(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=publication_cache, cached=cached)


def get_score(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=score_cache, cached=cached)


def get_trait(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=trait_cache, cached=cached)


def get_trait_category(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=trait_category_cache, cached=cached)


def get_performance(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=performance_cache, cached=cached)


def get_cohort(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=cohort_cache, cached=cached)


def get_sample_set(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=sample_set_cache, cached=cached)


def get_release(url: str, cached=True) -> List[Dict]:
    return get_data(url, cache_impl=release_cache, cached=cached)


def clear_cache(field: str = 'All'):
    if field not in fields_and_all:
        raise Exception('The field must one of %s' % str(fields_and_all))
    if field == 'All':
        for s in fields:
            eval(s.lower() + '_cache.clear()')
    else:
        eval(field.lower()+'_cache.clear()')


def get_data(url: str, cache_impl=None, cached=True) -> List[Dict]:
    with requests.Session() as s:
        s.mount('https://', HTTPAdapter(max_retries=5))
        if url in cache_impl and cached:
            r = cache_impl[url]
        else:
            r = s.get(url)
            cache_impl[url] = r
        if r.status_code == 200:
            parsed_data = json.loads(r.text)
            if parsed_data.get('results') is not None:
                results_list = parsed_data.get('results')
                if parsed_data.get('next') is not None:
                    bar = progressbar.ProgressBar(max_value=parsed_data.get('count')).start()
                    progress = 50
                    bar.update(progress)
                    next_url = parsed_data.get('next')
                    while next_url is not None:
                        if next_url in cache_impl and cached:
                            r = cache_impl[next_url]
                        else:
                            r = s.get(next_url)
                            cache_impl[next_url] = r
                        parsed_data = json.loads(r.text)
                        results_list.extend(parsed_data.get('results'))
                        progress = progress + parsed_data.get('size')
                        bar.update(progress)
                        next_url = parsed_data.get('next')
                    bar.finish()
                return results_list
            else:
                return [parsed_data]
        elif r.status_code == 404:
            return []
        else:
            raise Exception('The request for %s failed: response code was %d' % (url, r.status_code))


def ask_yes_no_question(question: str) -> str:
    yes_no_answer = ""
    while yes_no_answer != "YES" and yes_no_answer != "NO":
        yes_no_answer = input(question).upper()
    return yes_no_answer

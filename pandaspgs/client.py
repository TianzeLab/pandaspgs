import requests
import json
import progressbar
from typing import List, Dict
from requests.adapters import HTTPAdapter
from cachetools import TTLCache

cache = TTLCache(maxsize=1024, ttl=10)


def get_data(url: str, interactive: bool = True) -> List[Dict]:

    with requests.Session() as s:
        s.mount('https://', HTTPAdapter(max_retries=5))
        if url in cache:
            r = cache[url]
        else:
            r = s.get(url)
            cache[url] = r
        if r.status_code == 200:
            parsed_data = json.loads(r.text)
            if parsed_data.get('results') is not None:
                results_list = parsed_data.get('results')
                if parsed_data.get('next') is not None:
                    if parsed_data.get('count') > 50 * 100 and interactive:
                        answer = ask_yes_no_question(
                            "You are about to download to many data from the PGS Catalog.\r\nThis might take several "
                            "minutes.\r\nDo you still want to proceed? (Yes or No)")
                        if answer == "NO":
                            return []
                    bar = progressbar.ProgressBar(max_value=parsed_data.get('count')).start()
                    progress = 50
                    bar.update(progress)
                    next_url = parsed_data.get('next')
                    while next_url is not None:
                        if next_url in cache:
                            r = cache[next_url]
                        else:
                            r = s.get(next_url)
                            cache[next_url] = r
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
            print('The request for %s failed: response code was %d' % (url, r.status_code))


def ask_yes_no_question(question: str) -> str:
    yes_no_answer = ""
    while yes_no_answer != "YES" and yes_no_answer != "NO":
        yes_no_answer = input(question).upper()
    return yes_no_answer

import re
from datetime import date, datetime, timedelta

import requests
import httplib2
import unidecode
from collections import defaultdict

from fujgold.HTMLParser import MyHTMLParser
from fujgold.config import CONFIG

REQUEST_STRING = CONFIG['FIO']['REQUEST_STRING']
FUJGOLD_NAME = 'fujgold'

def format_request_range(previous, current):
    current = datetime.strftime(current, '%d.%m.%Y')
    previous = datetime.strftime(previous, '%d.%m.%Y')
    print('Parsing data between %s - %s' % (previous, current))
    return previous, current


def transform_name_canonical(x):
    x = unidecode.unidecode(x.lower())
    x = x.replace('.', '')
    x = x.split(' ')
    x = sorted(x)
    x = ' '.join(x)
    return x

def expand_symbol(name_string, symbol):
    candidates = set()
    if symbol in name_string:
        candidates.update(set(name_string.split(symbol)))
        additions = []
        for c in candidates:
            new_c = expand_candidates(c)
            additions.extend(new_c)

        candidates.update(additions)

        candidates.add(name_string.replace(symbol, ''))

    return candidates

def expand_candidates(name_string):
    candidates = set()
    candidates.update(expand_symbol(name_string, ','))
    candidates.update(expand_symbol(name_string, '/'))
    candidates.update(expand_symbol(name_string, '-'))
    candidates.update(expand_symbol(name_string, 'frisbee'))

    candidates = set(x.strip() for x in candidates)

    return candidates

def recognize_name(item, known_names):
    all_possibilities = item.copy()

    expanded_possibilities = [expand_candidates(x) for x in all_possibilities]

    all_possibilities += [x for sublist in expanded_possibilities for x in sublist if isinstance(sublist, set)]

    # if FUJGOLD_NAME in transfer note, skip
    if FUJGOLD_NAME in all_possibilities:
        return None

    name = [transform_name_canonical(x) for x in all_possibilities if transform_name_canonical(x) in known_names]

    if len(name) > 1:
        name = list(set(name))


    if len(name) == 1:
        name = name[0]
    elif len(name) > 1:
        print(name)
#         raise RuntimeError('ambiguous name')
        print('log: ambiguous name', name)
        name = None
    else:
        name = item[3]
#         print("name doesn't match any known name, using: %s" % name)

    return name

def parse_fio_page(request_result_text):
    parser = MyHTMLParser()
    parser.feed(request_result_text)
    res = parser.res.copy()
    parser.close()
    parser.reset()
    return res

def process_payments(parsed_page, sheet_names):
    payments = defaultdict(lambda: list())

    for item in parsed_page[3:]:
        if len(item) >= 4:
            item_date = item[0]

            amount = item[1][:-4]
            amount = amount.replace(',', '.')
            amount = re.sub(r"\s+", "", amount)
            try:
                amount = float(amount)
            except:
                print('failed to parse amount')
                print(item)
                continue
            if amount > 0:
                name = recognize_name(item, sheet_names)
                if name is not None:
                    payments[name] = [amount] + payments[name]

    return payments

def get_request(previous, current):
    previous, current = format_request_range(previous, current)
    request_string = REQUEST_STRING % (previous, current)
    print(request_string)
    return requests.get(request_string)

def process_payments_range(previous, current, sheet_names):
    req = get_request(previous, current)
    parsed_page = parse_fio_page(req.text)
    return process_payments(parsed_page, sheet_names)
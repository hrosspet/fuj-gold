import re
from datetime import date, datetime, timedelta

import requests
import unidecode
from io import StringIO
from collections import defaultdict
import pandas as pd

from fujgold.config import CONFIG

REQUEST_STRING = CONFIG["FIO"]["REQUEST_STRING"]
FUJGOLD_NAME = "fujgold"
FIO_TIME_FORMAT = "%Y-%m-%d"


COL_POZNAMKA = "Zpráva pro příjemce"
COL_OBJEM = "Objem"
COL_INDEX = "ID pohybu"


def format_request_range(previous, current):
    current = datetime.strftime(current, FIO_TIME_FORMAT)
    previous = datetime.strftime(previous, FIO_TIME_FORMAT)
    print("Parsing data between %s - %s" % (previous, current))
    return previous, current


def get_request(previous, current):
    previous, current = format_request_range(previous, current)
    request_string = REQUEST_STRING % (previous, current)
    return requests.get(request_string)


def process_transactions(response, sheet_names):
    data = StringIO(response.text)
    transactions_df = (
        pd.read_csv(data, skiprows=12, delimiter=";", decimal=",")
        .set_index(COL_INDEX)
        .sort_index()
        .dropna(subset=[COL_POZNAMKA])
    )
    transactions_df[COL_POZNAMKA] = (
        transactions_df[COL_POZNAMKA]
        .apply(unidecode.unidecode)  # get rid of weird czech symbols
        .apply(str.lower)  # transform to lowercase
    )

    # deprecated transformations (they wouldn't help here, because the new names in the sheet don't obey these rules)
    # .apply(lambda x: x.split(" ")) # split to words
    # .apply(sorted) # sort words alphabetically
    # .apply(" ".join) # merge words into the name

    # select only incoming transactions
    transactions_df = transactions_df[transactions_df[COL_OBJEM] > 0]

    # filter transactions by known names
    transactions_df = transactions_df[transactions_df[COL_POZNAMKA].isin(set(sheet_names))]

    return transactions_df


def format_payments(transactions_df, sheet_names):
    payments = defaultdict(list)
    payments.update(transactions_df.groupby(COL_POZNAMKA)[COL_OBJEM].apply(list).to_dict())
    payments = [payments[x] for x in sheet_names]
    return payments


def process_payments_range(previous, current, sheet_names):
    response = get_request(previous, current)

    try:
        transactions_df = process_transactions(response, sheet_names)
    except pd.errors.EmptyDataError:
        transactions_df = pd.DataFrame(columns=[COL_POZNAMKA, COL_OBJEM])

    # format the transactions for the spreadsheet
    payments = format_payments(transactions_df, sheet_names)

    return payments

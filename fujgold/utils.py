from datetime import datetime, timedelta
from fujgold.google_tools import (
    get_google_api,
    read_spreadsheet_values,
    write_values,
    write_date,
)
from fujgold.fio_tools import process_payments_range
from fujgold.config import CONFIG

START_DATE = CONFIG["START_DATE"]

SHEET_OFFSET = 1


def get_sheet_names(spreadsheet_values):
    return [x[0] for x in spreadsheet_values[SHEET_OFFSET:] if x[0]]


def get_name_to_row_dict(names):
    return dict(zip(names, range(len(names))))


def update_fuj_gold(last_update=None):
    current = datetime.utcnow()

    if "END_DATE" in CONFIG:
        current = datetime.strptime(CONFIG["END_DATE"], "%d.%m.%Y")

    service = get_google_api()

    # fetch old spreadsheet values
    spreadsheet_values = read_spreadsheet_values(service)

    # extract names
    sheet_names = get_sheet_names(spreadsheet_values)

    # writing to new table since START_DATE
    last_update = datetime.strptime(START_DATE, "%d.%m.%Y") + timedelta(days=1)

    # fetch & process new payments
    payments = process_payments_range(last_update, current, sheet_names)

    # # write values
    write_values(service, payments, len(payments), SHEET_OFFSET)
    write_date(service)

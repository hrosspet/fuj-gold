from datetime import datetime, timedelta
from fujgold.google_tools import get_google_api, read_spreadsheet_values, write_values, write_date
from fujgold.fio_tools import process_payments_range
from fujgold.config import CONFIG

START_DATE = CONFIG['START_DATE']


def get_sheet_names(spreadsheet_values):
    return [x[0] for x in spreadsheet_values[3:len(spreadsheet_values):2]]


def get_name_to_row_dict(names):
    return {x: (i * 2 + 1) for i,x in enumerate(names)}


def update_fuj_gold(last_update=None):
    current = datetime.utcnow()

    service = get_google_api()

    # fetch old spreadsheet values
    spreadsheet_values = read_spreadsheet_values(service)

    # extract names
    sheet_names = get_sheet_names(spreadsheet_values)
    name_to_row = get_name_to_row_dict(sheet_names)

    # fetch & process new payments

    # writing to new table since START_DATE
    last_update = datetime.strptime(START_DATE, '%d.%m.%Y') + timedelta(days=1)
    last_update

    payments = process_payments_range(last_update, current, sheet_names)

    vals = [x[3:] for x in spreadsheet_values[3:]]

    # update values
    for name, values in payments.items():
        if name in name_to_row:
            row = name_to_row[name]
            vals[row] = values

        else:
            print('unmatched payment: %s,' % name, values)

    # write values
    write_values(service, vals, len(name_to_row))
    write_date(service)
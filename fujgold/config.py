CONFIG = {
    'START_DATE': '05.03.2019',
    # 'END_DATE': '05.03.2018', # currently unused, but could be used as an upper limit
    'GOOGLE': {
        'SCOPES': 'https://www.googleapis.com/auth/spreadsheets',
        'CLIENT_SECRET_FILE': 'client_secret.json',
        'APPLICATION_NAME': 'Google Sheets API Python Quickstart',
        'SHEET_NAME': 'Transfers bank',
        'SPREADSHEET_ID': '1VIoZOvYjZXpy3AzO1E6yj-yNyBBzXywep8frB9pR7DY'
    },
    'FIO': {
        'REQUEST_STRING': 'https://www.fio.cz/ib2/transparent?a=2800359168&f=%s&t=%s'
    }
}

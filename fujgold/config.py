CONFIG = {
    "START_DATE": "28.03.2020",
    # 'END_DATE': '05.03.2018', # currently unused, but could be used as an upper limit
    "GOOGLE": {
        "SCOPES": "https://www.googleapis.com/auth/spreadsheets",
        "CLIENT_SECRET_FILE": "client_secret.json",
        "APPLICATION_NAME": "Google Sheets API Python Quickstart",
        "SHEET_NAME": "Transfers bank",
        "SPREADSHEET_ID": "1X659l4t3YtHc7dDkGLlbKQSLy6ZHFdrSGu0VIc-YuPc",
    },
    "FIO": {
        "REQUEST_STRING": "https://www.fio.cz/ib2/transparent?a=2800359168&f=%s&t=%s"
    },
}

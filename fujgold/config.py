CONFIG = {
    "START_DATE": "16.06.2021",
    # 'END_DATE': '05.03.2018', # currently unused, but could be used as an upper limit
    "GOOGLE": {
        "SCOPES": "https://www.googleapis.com/auth/spreadsheets",
        "CLIENT_SECRET_FILE": "client_secret.json",
        "APPLICATION_NAME": "Google Sheets API Python Quickstart",
        "SHEET_NAME": "Transfers bank",
        "SPREADSHEET_ID": "1Sj5i_CXAWDOBF0UjRAhaTuArKetiWWE0NoaKNeTc1Y0",
    },
    "FIO": {
        "REQUEST_STRING": "https://www.fio.cz/ib_api/rest/periods/oUTFke1wvtFXzbZ9kHNpe1wbdCxyWaqFInxBFcFzAXLFzFVjkSOJZGs4Gu3VaePH/%s/%s/transactions.csv"
    },
}

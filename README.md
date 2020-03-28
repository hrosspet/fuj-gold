# Fuj-gold

The purpose of this library is to automate the accounting of our team [FUJ](https://www.facebook.com/FUJprague/) finances. It scrapes the incoming transactions from our transparent [account](https://ib.fio.cz/ib/transparent?a=2800359168) once per day and writes them to our accounting table in google sheets, where everybody can see their balance, past transactions and payment calendar for future events.

# Development

0. `git clone https://github.com/hrosspet/fuj-gold.git`
1. `cd fuj-gold`
2. `pip install -r requirements.txt`
3. `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`
4. `pip install -e .`

Python 3.5+ required.

## Setup access for Google API:

You need to get OAuth key:

    - Follow step 1 from https://developers.google.com/sheets/api/quickstart/python
    - rename it to "client_secret.json" and copy it in this folder
    - run __main__.py
    - note: it stores credentials in ~/.credentials/sheets.googleapis.com-python-quickstart.json

## Set up new year

### New sheets

- Copy the main spreadsheet (currently [this one](https://docs.google.com/spreadsheets/d/1X659l4t3YtHc7dDkGLlbKQSLy6ZHFdrSGu0VIc-YuPc/))
- Copy the helper spreadsheet (currently [this one](https://docs.google.com/spreadsheets/d/10iFRKNpic7PGpsk4hl7Al4yzPDQr6SP4iZXW-92vTT8/edit))
- Change the spreadsheet id in the main sheet, Teammates, in the cell A1, in the `importRange` function to the new helper sheet id (currently `10iFRKNpic7PGpsk4hl7Al4yzPDQr6SP4iZXW-92vTT8`)
- Do the same for Attendance sheet
- Do the same for Events sheet, except for here it's in the cell C2
- Rename the first sheet to current year (just a cosmetic issue)
- Clear all the values in Transfers bank and Transfers manual
- Clear all the Attendance values in the helper sheet
- Update the values in Teammates in the helper sheet according to this year's paushál
- Copy the balance column from previous year to the column `Last year`
- Reload the whole sheet to update all values
- Update the date in the cell saying "Příchozí platby počínaje" in `Transfers bank` to the current date

### Change config in code

- In the file config.py change the value of `SPREADSHEET_ID` to the new id of the main spreadsheet (currently `1X659l4t3YtHc7dDkGLlbKQSLy6ZHFdrSGu0VIc-YuPc`)
- In the file config.py change the value of `START_DATE` to the same value as in the last step of the updating of sheets
- Test it by running `python __main__.py` to see whether the script correctly writes new transfers into the sheet `Transfers bank`
- deploy the script on the server

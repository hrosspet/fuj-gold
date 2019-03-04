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
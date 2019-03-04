import os
import httplib2
from oauth2client import client
from datetime import datetime, timedelta

from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient import discovery

from fujgold.config import CONFIG

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json

SCOPES = CONFIG['GOOGLE']['SCOPES']
CLIENT_SECRET_FILE = CONFIG['GOOGLE']['CLIENT_SECRET_FILE']
APPLICATION_NAME = CONFIG['GOOGLE']['APPLICATION_NAME']

SHEET_NAME = CONFIG['GOOGLE']['SHEET_NAME']
SPREADSHEET_ID = CONFIG['GOOGLE']['SPREADSHEET_ID']


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.

    [copied from https://developers.google.com/sheets/api/quickstart/python]
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_google_api():
    """Takes care of authentification of google sheets API"""
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    return service


def read_spreadsheet(service, spreadsheet_id, sheet_name):
    return service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                               range=sheet_name, valueRenderOption='FORMULA').execute()['values']

def write_spreadsheet(service, spreadsheet_id, sheet_name, data):
    service.spreadsheets().values().update(spreadsheetId=spreadsheet_id,
                                               range=sheet_name,
                                               body={'values': data},
#                                                valueInputOption='RAW').execute()
                                               valueInputOption='USER_ENTERED').execute()


def read_spreadsheet_values(service):
    return read_spreadsheet(service, SPREADSHEET_ID, SHEET_NAME)


def write_values(service, new_values, names_len):
    offset = 4
    write_range = SHEET_NAME + ('!D%d:Z%d' % (offset, offset + 2 * names_len))
#     print(write_range)
    write_spreadsheet(service, SPREADSHEET_ID, write_range, new_values)

def write_date(service):
    write_range = SHEET_NAME + '!A2'
    val = datetime.utcnow() + timedelta(hours=1)
    val = val.strftime('%Y-%m-%d %H:%M:%S')
    val = [[val]]
    write_spreadsheet(service, SPREADSHEET_ID, write_range, val)

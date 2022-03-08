from googleapiclient.discovery import build
from google.oauth2 import service_account
import json


class Sheets:
    def __init__(self):
        with open('ids.json') as f:
            self.__ids__ = json.load(f)
        self.__scopes__ = ['https://www.googleapis.com/auth/spreadsheets']
        self.__serviceAccount__ = 'credentials.json'
        self.__sheetId__ = self.__ids__['sheet_id']

        self.__creds__ = service_account.Credentials.from_service_account_file(
            self.__serviceAccount__, scopes=self.__scopes__)
        self.__service__ = build('sheets', 'v4', credentials=self.__creds__)
        self.__sheet__ = self.__service__.spreadsheets()

    def __insertData__(self, data, range_):
        self.__sheet__.values().append(spreadsheetId=self.__sheetId__,
                                       range=range_,
                                       valueInputOption='USER_ENTERED',
                                       insertDataOption='INSERT_ROWS',
                                       body={'values': data}).execute()

    def __updateData__(self, data, range_):
        self.__sheet__.values().update(spreadsheetId=self.__sheetId__,
                                       range=range_,
                                       valueInputOption='USER_ENTERED',
                                       body={'values': data}).execute()

    def readSheet(self, sheetRange):
        res = self.__sheet__.values().get(spreadsheetId=self.__sheetId__,
                                          range=sheetRange).execute()
        values = res.get('values', [])
        return values

    def insertRow(self, data, range_):
        self.__insertData__([data], range_)

    def updateRow(self, data, range_):
        self.__updateData__([data], range_)

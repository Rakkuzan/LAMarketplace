from googleapiclient.discovery import build
from google.oauth2 import service_account
import json


class Sheets:
    def __init__(self):
        with open('ids.json') as f:
            self.ids = json.load(f)
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
        self.serviceAccount = 'credentials.json'
        self.sheetId = self.ids['sheet_id']

        self.creds = service_account.Credentials.from_service_account_file(
            self.serviceAccount, scopes=self.scopes)
        self.service = build('sheets', 'v4', credentials=self.creds)
        self.sheet = self.service.spreadsheets()

    def readSheet(self, sheetRange):
        res = self.sheet.values().get(spreadsheetId=self.sheetId,
                                      range=sheetRange).execute()
        values = res.get('values', [])
        print(values)


import gspread
from oauth2client.service_account import ServiceAccountCredentials

class MeridianSync:

    def __init__(self, sheet_name):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open(sheet_name).sheet1

    def fetch(self):
        rows = self.sheet.get_all_records()
        data = {}
        for r in rows:
            data[r["Indicator"]] = [r["v1"], r["v2"], r["v3"]]
        return data

    def write(self, value):
        self.sheet.update_acell("G2", value)

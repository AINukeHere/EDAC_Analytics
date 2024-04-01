import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials

RANK_TYPE_POST = 0
RANK_TYPE_COMMENT = 1
RANK_TYPE_LIKE = 2
RANK_TYPE_VISIT = 3

worksheetName_map = {
    RANK_TYPE_POST:'카페 멤버 게시글 순위',
    RANK_TYPE_COMMENT:'카페 멤버 댓글 순위',
    RANK_TYPE_LIKE:'카페 멤버 좋아요 순위',
    RANK_TYPE_VISIT:'카페 멤버 방문 순위',
}

class GoogleSpreadSheetWriter():
    def __init__(self):
        # 구글 API 사용을 위한 상수들
        self.scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        self.key_file_name = 'expanded-symbol-367617-03f470c1d316.json'
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.key_file_name, self.scope)
        self.spreadsheetList = {}

    def writeRankData(self, year, month, rankType, data):
        if not year in self.spreadsheetList:
            gspread_file_name = f'NaverCafe_Analytics_{year}'
            self.spreadsheetList[year] = gspread.authorize(self.credentials).open(gspread_file_name)
        worksheet = None
        sheetName = worksheetName_map[rankType]
        try:
            worksheet = self.spreadsheetList[year].worksheet(sheetName)
        except gspread.WorksheetNotFound:
            worksheet = self.spreadsheetList[year].add_worksheet(sheetName,110*11+102, 18)
        gspread.Spreadsheet.add_worksheet
        if month < 1 or 12 < month:
            print('month must be between 1 and 12. ')
            return False

        idxOffset = 110 * (month - 1) + 1
        cellIdx = f'A{idxOffset}'
        worksheet.update(cellIdx, data)
        return True
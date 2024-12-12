import os, time
from subprocess import Popen, PIPE
import shutil, glob

class DataDownloader():
    def __init__(self, year:int, month:int, weekDimStart:tuple):
        '''
        example: DataDownloader(2023,10,(2023,09,26))
        :param year: 년
        :param month: 월
        :param weekDimStart: 분석하고자하는 주의 시작 날짜
        '''
        self.analyticsYear = year
        self.analyticsMonth = month

        self.analyticsWeekDimStartYear=weekDimStart[0]
        self.analyticsWeekDimStartMonth=weekDimStart[1]
        self.analyticsWeekDimStartDay=weekDimStart[2]

        self.subprocessList = []
        self.chrome='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'

    def DownloadAll(self):
        # 23 = 내가만든유즈맵 26 = 타인제작유즈맵 326 = 맞히기유즈맵
        for boardID in (23,26,326):
            self.__download_each_day(boardID)
            self.__download_each_week(boardID)
            self.__download_each_month(boardID)
        self.__download_member_rank_month()
        self.__download_inflow_rank_month()

        time.sleep(10)

    def __getMonthEndDay(self, year, month):
        endDay=30
        if month in (1,3,5,7,8,10,12):
            endDay=31
        elif month == 2:
            if year % 4 == 0 and year % 100 != 0:
                endDay = 29
            else:
                endDay = 28
        return endDay
    # 일간
    def __download_each_day(self, boardID):
        endDay=30
        if self.analyticsMonth in (1,3,5,7,8,10,12):
            endDay = 31
        elif self.analyticsMonth == 2:
            if self.analyticsYear % 4 == 0 and self.analyticsYear % 100 != 0:
                endDay = 29
            else:
                endDay = 28

        print(f'endDay : {endDay}')

        for day in range(1, endDay+1):
            print(f'boardID:{boardID}, day:{day}')
            downloadURL = f'https://cafe.stat.naver.com/download/cafe/17046257/rank/articleCv?service=CAFE&timeDimension=DATE&startDate={self.analyticsYear}-{self.analyticsMonth:02d}-{day:02d}&selectedBoardId={boardID}'
            cmd = f'\"{self.chrome}\" "{downloadURL}"'
            print(cmd)
            
            ps = Popen([self.chrome,downloadURL],stdout=PIPE, stderr=PIPE)
            self.subprocessList.append(ps)
            # subprocess.check_call(cmd)
            time.sleep(1)
    # 주간
    def __download_each_week(self, boardID):
        
        curYear=self.analyticsWeekDimStartYear
        curMonth=self.analyticsWeekDimStartMonth
        curDay=self.analyticsWeekDimStartDay
        curMonthEndDay = self.__getMonthEndDay(curYear, curMonth)
        while curMonth < self.analyticsMonth or (curMonth == self.analyticsMonth and curDay + 6 <= curMonthEndDay):
            print(f'{curYear}, {curMonth}, {curDay}')
            downloadURL = f'https://cafe.stat.naver.com/download/cafe/17046257/rank/articleCv?service=CAFE&timeDimension=WEEK&startDate={curYear}-{curMonth:02d}-{curDay:02d}&selectedBoardId={boardID}'
            cmd = f'"{self.chrome}" "{downloadURL}"'
            print(cmd)
            ps = Popen([self.chrome,downloadURL],stdout=PIPE, stderr=PIPE)
            self.subprocessList.append(ps)
            # subprocess.check_call(cmd)
            time.sleep(2)
            curDay += 7
            if curDay > curMonthEndDay:
                curMonth += 1
                curDay -= curMonthEndDay
            if curMonth > 12:
                curYear += 1
                curMonth -= 12
            if curMonth > self.analyticsMonth or (curMonth == self.analyticsMonth and curDay + 6 > curMonthEndDay):
                break
            curMonthEndDay = self.__getMonthEndDay(curYear, curMonth)
    # 월간
    def __download_each_month(self, boardID):
        downloadURL = f'https://cafe.stat.naver.com/download/cafe/17046257/rank/articleCv?service=CAFE&timeDimension=MONTH&startDate={self.analyticsYear}-{self.analyticsMonth:02d}-01&selectedBoardId={boardID}'
        cmd = f'"{self.chrome}" "{downloadURL}"'
        print(cmd)
        ps = Popen([self.chrome,downloadURL],stdout=PIPE, stderr=PIPE)
        self.subprocessList.append(ps)
        # subprocess.check_call(cmd)
        time.sleep(2)
    # 멤버순위
    def __download_member_rank_month(self):
        # 방뭇횟수
        downloadURL = f'https://cafe.stat.naver.com/download/cafe/17046257/rank/memberVisit?service=CAFE&timeDimension=MONTH&startDate={self.analyticsYear}-{self.analyticsMonth:02d}-01&memberId=%%EB%%A9%%A4%%EB%%B2%%84'
        cmd = f'"{self.chrome}" "{downloadURL}"'
        print(cmd)
        ps = Popen([self.chrome,downloadURL],stdout=PIPE, stderr=PIPE)
        self.subprocessList.append(ps)
        # subprocess.check_call(cmd)
        time.sleep(1)
        # 게시글 수
        downloadURL = f'https://cafe.stat.naver.com/download/cafe/17046257/rank/memberCreate?service=CAFE&timeDimension=MONTH&startDate={self.analyticsYear}-{self.analyticsMonth:02d}-01&memberId=%%EB%%A9%%A4%%EB%%B2%%84'
        cmd = f'"{self.chrome}" "{downloadURL}"'
        print(cmd)
        ps = Popen([self.chrome,downloadURL],stdout=PIPE, stderr=PIPE)
        self.subprocessList.append(ps)
        # subprocess.check_call(cmd)
        time.sleep(1)
        # 댓글 수
        downloadURL = f'https://cafe.stat.naver.com/download/cafe/17046257/rank/memberComment?service=CAFE&timeDimension=MONTH&startDate={self.analyticsYear}-{self.analyticsMonth:02d}-01&memberId=%%EB%%A9%%A4%%EB%%B2%%84'
        cmd = f'"{self.chrome}" "{downloadURL}"'
        print(cmd)
        ps = Popen([self.chrome,downloadURL],stdout=PIPE, stderr=PIPE)
        self.subprocessList.append(ps)
        # subprocess.check_call(cmd)
        time.sleep(1)
        # 좋아요 수
        downloadURL = f'https://cafe.stat.naver.com/download/cafe/17046257/rank/memberLiked?service=CAFE&timeDimension=MONTH&startDate={self.analyticsYear}-{self.analyticsMonth:02d}-01&memberId=%%EB%%A9%%A4%%EB%%B2%%84'
        cmd = f'"{self.chrome}" "{downloadURL}"'
        print(cmd)
        ps = Popen([self.chrome,downloadURL],stdout=PIPE, stderr=PIPE)
        self.subprocessList.append(ps)
        # subprocess.check_call(cmd)
        time.sleep(1)
    # 유입분석
    def __download_inflow_rank_month(self):
        # 전체 게시판 검색 유입
        
        memberIdList=[
            None,   # 방문자 전체
            0,      # 비멤버
            1,      # 커패회원1
            110,    # 카페회원2
            120,    # 우수회원1
            130,    # 우수회원2
            140,    # 감사회원
            150     # VIP 회원
        ]
        for memberId in memberIdList:
            downloadURL = f'https://cafe.stat.naver.com/download/cafe/17046257/user/referer/search?service=CAFE&timeDimension=MONTH&startDate={self.analyticsYear}-{self.analyticsMonth:02d}-01'
            if memberId is not None:
                downloadURL += f'&memberId={memberId}'
            cmd = f'"{self.chrome}" "{downloadURL}"'
            print(cmd)
            ps = Popen([self.chrome,downloadURL],stdout=PIPE, stderr=PIPE)
            self.subprocessList.append(ps)
            # subprocess.check_call(cmd)
            time.sleep(2)

    def ClearSubProcess(self):
        for ps in self.subprocessList:
            print("terminate()")
            ps.terminate()

    def MoveAll(self):
        desktopPath = os.path.join(os.path.expanduser('~'),'Desktop')

        destPath = './data/usemap_rank/week/'
        if not os.path.exists(destPath):
            os.makedirs(destPath)
        for srcPath in glob.glob(os.path.join(desktopPath, '카페통계_게시글순위_조회수_주간*.xlsx')):
            shutil.move(srcPath, destPath)

        destPath = './data/usemap_rank/day/'
        if not os.path.exists(destPath):
            os.makedirs(destPath)
        for srcPath in glob.glob(os.path.join(desktopPath, '카페통계_게시글순위_조회수_일간*.xlsx')):
            shutil.move(srcPath, destPath)

        destPath = './data/usemap_rank/month/'
        if not os.path.exists(destPath):
            os.makedirs(destPath)
        for srcPath in glob.glob(os.path.join(desktopPath, '카페통계_게시글순위_조회수_월간*.xlsx')):
           shutil.move(srcPath, destPath)

        destPath = f'./data/member_rank/{self.analyticsYear}/'
        if not os.path.exists(destPath):
            os.makedirs(destPath)
        for srcPath in glob.glob(os.path.join(desktopPath, '카페통계_멤버순위*.xlsx')):
            shutil.move(srcPath, destPath)

        destPath = f'./data/inflow_rank/'
        if not os.path.exists(destPath):
            os.makedirs(destPath)
        for srcPath in glob.glob(os.path.join(desktopPath, '카페통계_유입분석_검색유입_월간*.xlsx')):
            shutil.move(srcPath, destPath)

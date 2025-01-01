import os, time
from DataDownloader import DataDownloader
from MapDictionary import category_map, 유즈맵
from analytics import *
analyzer = Analyzer()

year = 2024
month = 12
weekDimStart = (2024,11,25)

# if True:
if False:
    print('start download')
    time.sleep(2)
    ### 네이버 카페 통계 데이터 다운로드 및 이동
    downloader = DataDownloader(year=year,month=month,weekDimStart=weekDimStart)
    downloader.DownloadAll()
    input('ready to move?')
    downloader.ClearSubProcess()
    print('move xlsx files')
    downloader.MoveAll()

    ### 멤버 순위 관리 및 통계
    analyzer.upload_member_rank_data(year)
    
    ### 유즈맵 순위 관리 및 통계
    joinMeList=['day', 'week', 'month']
    analyzer.analytics_UsemapRank_preprocess(joinMeList=joinMeList)
    
    ### 유입분석
    analyzer.analytics_inflow_preprocess()

# if False: # usemap rank analyze
if True:
    if True: # 일반 통계글 작성용
    # if False:
        joinMeList=['month','day']
        for joinMe in joinMeList:
            analyzer.analytics_UsemapRank_historical(
                joinMeList=[joinMe], 
                regexTest=f'.*(내가 만든|타인 제작).*{year}-{month:02d}.*',
                category_map=유즈맵,
                # autoDetect= False)
                autoDetect= True)
    else: # historical visulaizer
        analyzer.analytics_UsemapRank_historical(
            joinMeList=['week'], 
            regexTest=f'.*(내가 만든|타인 제작).*2024-.*',
            category_map=유즈맵,
            # autoDetect= False,
            autoDetect= True,
            bHistoricalWebSource=True,
            bUseMaxValue = False)

### 유입분석
analyzer.analytics_inflow(year, month, category_map)
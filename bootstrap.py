import os, time
from DataDownloader import DataDownloader
from MapDictionary import category_map, 유즈맵
from analytics import *
analyzer = Analyzer()

year = 2024
month = 5
weekDimStart = (2024,4,29)
# if True:
if False:
    ### 네이버 카페 통계 데이터 다운로드 및 이동
    downloader = DataDownloader(year=year,month=month,weekDimStart=weekDimStart)
    downloader.DownloadAll()
    print('move xlsx files')
    downloader.MoveAll()


    ### 멤버 순위 관리 및 통계
    analyzer.upload_member_rank_data(year)
    # analyzer.analytics_member_1year(2024)
    # analyzer.analytics_member_1year(2023)
    # analyzer.analytics_member_1year(2022) 
    # analyzer.analytics_member_1year(2021) 
    # exit()
    
    ### 유즈맵 순위 관리 및 통계
    # joinMeList=['day']
    # joinMeList=['week']
    # joinMeList=['month']
    joinMeList=['day', 'week', 'month']
    analyzer.analytics_UsemapRank_preprocess(joinMeList=joinMeList)

# joinMeList=['day']
# joinMeList=['month']
# joinMeList=['week']
# joinMeList=['day', 'week', 'month']
    
if False: # usemap rank analyze
# if True:
    ### web visualize option
    bHistoricalWebSource = False
    if not bHistoricalWebSource:
        joinMeList=['month','day']
        for joinMe in joinMeList:
            analyzer.analytics_UsemapRank_historical(
                joinMeList=[joinMe], 
                regexTest=f'.*(내가 만든|타인 제작).*{year}-{month:02d}.*',
                category_map=유즈맵,
                # autoDetect= False)
                autoDetect= True)
    else:
        # historical visulaizer
        analyzer.analytics_UsemapRank_historical(
            joinMeList=['day'], 
            regexTest=f'.*(내가 만든|타인 제작).*2023-.*',
            category_map=유즈맵,
            # autoDetect= False,
            autoDetect= True,
            bHistoricalWebSource=True)
    
    


### 유입분석
# analyzer.analytics_inflow_preprocess()
analyzer.analytics_inflow(year, month, category_map)
# analyzer.analytics_inflow_new_for_historical('유입분석_검색유입', ["month"], category_map)
# analyzer.analytics_inflow('카페 내 검색', 'week', category_map)
# analyzer.analytics_inflow_new_for_historical('유입분석_카페내검색', ["month", "week"], category_map)
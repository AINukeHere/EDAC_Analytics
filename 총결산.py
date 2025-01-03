
from analytics import *
from MapDictionary import 유즈맵
year = 2024
analyzer = Analyzer()
# analyzer.analytics_member_1year(year)
analyzer.analytics_UsemapRank_historical(
    joinMeList=['day'], 
    regexTest=f'.*(내가 만든|타인 제작).*{year}-.*',
    category_map=유즈맵,
    autoDetect= True,
    useValueMethod='each')
    # useValueMethod='acc')
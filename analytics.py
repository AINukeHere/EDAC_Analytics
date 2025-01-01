import pandas as pd
from GoogleSpreadSheetWriter import *
import os, re
from tqdm import tqdm


class Analyzer():
    def __init__(self):
        self.writer = GoogleSpreadSheetWriter()

    def splitPeriod(self, date):
        res = re.findall('(.*)년 (.*)월 (.*)일', date)[0]
        year = int(res[0])
        month = int(res[1])
        day = int(res[2])
        return year, month, day

    def analytics_board(self, includeMe):
        dataDir = os.path.join('data','board_rank')
        flist = os.listdir(dataDir)
        searchinflow = [f for f in flist if includeMe in f]

        result_columns_list = []
        dataFrame_excels = []
        for fname in searchinflow:
            print(fname)
            fPath = os.path.join(dataDir, fname)
            ed = pd.read_excel(fPath, engine = 'openpyxl')
            dataFrame_excels.append(ed)

            values = ed.values[6:,1:]
            for row in values:
                if isinstance(row[0], str):
                    searchWord = row[0]
                    category_name = searchWord

                    if category_name in result_columns_list:
                        continue
                    result_columns_list.append(category_name)

        print(result_columns_list)
        result_columns_list.insert(0, '기간')
        data_result = [result_columns_list]

        for ed in dataFrame_excels:
            period = ed.columns.values[1]
            new_row = [0]*len(result_columns_list)
            new_row[0] = period
            
            values = ed.values[6:,1:]
            for row in values:
                if isinstance(row[0], str):
                    boardName = row[0]
                    postCount = row[1]
                    
                    category_name = boardName

                    idx = result_columns_list.index(category_name)
                    new_row[idx] += int(postCount.replace(',',''))
            data_result.append(new_row)
        # print(data_result)
        result= pd.DataFrame(data_result)
        result = result.transpose()
        result.to_clipboard(index=False, header=None)
        print('클립보드에 복사되었습니다.')
    
    def analytics_inflow(self, reqYear, reqMonth, category_map = None):
        #TODO 멤버 + 비멤버 + 전체 자동 병합 구현
        dataDir = os.path.join('data', 'inflow_rank', 'preprocess')
        flist = os.listdir(dataDir)

        wordList = []
        wordToIdx = {}
        result_columns_list = [['검색어', '멤버', '비멤버', '전체 방문자']]
        dataFrame_excels = []
        for fname in flist:
            fPath = os.path.join(dataDir, fname)
            ed = pd.read_excel(fPath, engine = 'openpyxl', header=None)
            res = re.findall('전체 게시판_검색 유입_(.*)_(.*)-(.*)-(.*)\.', fname)[0]
            검색한사람 = str(res[0])
            year = int(res[1])
            month = int(res[2])
            day = int(res[3])
            if reqYear != year or reqMonth != month:
                continue
            countIdx = -1
            if 검색한사람 in ('카페회원I', '카페회원II', '우수회원I', '우수회원II', '감사회원', 'VIP 회원'):
                countIdx = 0
            elif 검색한사람 == '방문자 전체':
                countIdx = 2
            elif 검색한사람 == '비멤버':
                countIdx = 1
            assert countIdx != -1
            # dataFrame_excels.append([ed, f'{year}-{month:02d}-{day:02d}']) # dataFrame, period
            for row in ed.values:
                if isinstance(row[0], str):
                    searchWord = row[0]
                    searchCount = int(str(row[1]).replace(',','').replace('.',''))
                    if searchWord == '기타':
                        pass
                    if not searchWord in wordToIdx:
                        wordToIdx[searchWord] = len(wordList)
                        wordList.append([searchWord, [0,0,0]]) # 멤버, 비멤버, 전체 방문자
                    listIdx = wordToIdx[searchWord]
                    wordList[listIdx][1][countIdx] += searchCount

        # for wordCounts in wordList:
        #     if wordCounts[1][2] == 0:
        #         wordCounts[1][2] = wordCounts[1][0] + wordCounts[1][1]
        #     else:
        #         if wordCounts[1][1] == 0:
        #             wordCounts[1][1] = wordCounts[1][2] - wordCounts[1][0]
        #         elif wordCounts[1][0] == 0:
        #             wordCounts[1][0] = wordCounts[1][2] - wordCounts[1][1]

        wordList.sort(key=lambda x:x[1][0]+x[1][1],reverse=True)

        for wordCounts in wordList:
            result_columns_list.append([wordCounts[0],wordCounts[1][0],wordCounts[1][1],wordCounts[1][2]])
        print(result_columns_list)

        for item in result_columns_list:
            for i in range(1, 4):
                if item[i] == 0:
                    item[i] = ''
        result= pd.DataFrame(result_columns_list)
        # result = result.transpose()
        result.to_excel(f'{reqYear}년 {reqMonth}월 검색 유입 통계.xlsx', index=False, header=None)


    def analytics_inflow_preprocess(self):
        ed_list = []
        board_period_dict = {} # 중복 데이터 검사용
        dataDir = os.path.join('data', 'inflow_rank')
        outputDir = os.path.join(dataDir, 'preprocess')
        moveToDir = os.path.join(dataDir, '원본')        
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        flist = os.listdir(dataDir)
        for fname in flist:
            fPath = os.path.join(dataDir, fname)
            if os.path.isdir(fPath):
                continue
            ed = pd.read_excel(fPath, engine = 'openpyxl')
            ed_list.append(ed)

            period = ed.columns.values[1]
            boardType = ed.values[3][1] # 게시판 이름
            dataTitle = ed.values[4][1] # 검색 유입 or 카페 내 검색
            조사대상 = ed.values[5][1] # 방문자 전체 or 멤버 전체, 비멤버
            data_unique_key = f'{boardType}_{dataTitle}_{조사대상}_{period}'
            if data_unique_key in board_period_dict:
                raise Exception(f'동일한 데이터: {data_unique_key}\n{fname} == {board_period_dict[data_unique_key]}')
            board_period_dict[data_unique_key] = fname
    
        ed_list.sort(key=lambda x : x.columns.values[1])
        for ed in ed_list:
            period = ed.columns.values[1]
            startDate = period.split('~')[0] # 시작날짜 
            year, month, day = self.splitPeriod(startDate)
            _date = f'{year}-{month}-{day}'


            values = ed.values[8:,:]
            boardType = ed.values[3][1] # 게시판 이름
            dataTitle = ed.values[4][1] # 검색 유입 or 카페 내 검색
            조사대상 = ed.values[5][1] # 방문자 전체 or 멤버 전체, 비멤버

            result= pd.DataFrame(values)
            filename = f'{boardType}_{dataTitle}_{조사대상}_{_date}.xlsx'
            outputPath = os.path.join(outputDir, filename)
            # print(outputPath)
            result.to_excel(outputPath, index=False, header=None)
        os.system(f'move {dataDir}\\*.xlsx {moveToDir}')

    # bUseMaxValue: 바 그래프 가시화할때 날짜별 최대 조회수로 순위를 매김
    def analytics_UsemapRank_historical(self, joinMeList, regexTest=None, category_map = {}, autoDetect=False, 
                                        bHistoricalWebSource=False, bUseMaxValue=False):
        data_stack = {} # 여러 게시판들의 동일기간 데이터 합치기용
        ed_list = []
        typeDict = {}
        board_period_dict = {} # 중복 데이터 검사용
        nextType = 0
        for joinMe in joinMeList:
            dataDir = os.path.join('data', 'usemap_rank', joinMe, 'preprocess')
            flist = os.listdir(dataDir)
            for fname in flist:
                fPath = os.path.join(dataDir, fname)
                if os.path.isdir(fPath):
                    continue
                if regexTest is not None:
                    if re.search(regexTest, fname) is None:
                        continue
                print(fname)
                ed = pd.read_excel(fPath, engine = 'openpyxl')
                ed_list.append([fname, ed])

                if fname in board_period_dict:
                    raise Exception(f'{fname}')
                board_period_dict[fname] = True
        
        ed_list.sort(key=lambda x : x[0])
        for ed_item in ed_list:
            fname = ed_item[0]
            ed = ed_item[1]
            res = re.findall('.*_(.*)\\.xlsx', fname)
            _date = res[0]
            print(_date)

            if not _date in data_stack:
                data_stack[_date] = {}
            curCsvDict = data_stack[_date]

            for row in ed.values:
                map_name = row[1]
                map_name = map_name.lstrip()
                foundList = re.findall('^(\[.*?\])',map_name)
                if len(foundList) > 0:
                    removeNum = len(foundList[0])
                    map_name = map_name[removeNum:]
                map_name = map_name.lstrip()
                foundList = re.findall('^(\(.*?\))',map_name)
                if len(foundList) > 0:
                    removeNum = len(foundList[0])
                    map_name = map_name[removeNum:]
                map_name = map_name.lstrip()
                if map_name.startswith('EUD'):
                    map_name = map_name[3:]
                map_name = map_name.lstrip()
                view_count = row[5]
                if map_name == '삭제된 게시글 입니다.':
                    continue
                if '' == map_name:
                    pass
                _name = map_name
                if category_map is not None:
                    for category_name in category_map:
                        for category_joinValue in category_map[category_name]:
                            if category_joinValue in map_name:
                                _name = category_name
                if _name in ['기타', '맞히기 관련']:#, '메운디 관련']:
                    continue
                if not _name in typeDict:
                    typeDict[_name] = nextType
                    nextType += 1
                _type = typeDict[_name]
                _value = 0
                if type(view_count) == int:
                    _value = view_count
                else:
                    _value = int(view_count.replace(',',''))
                if not _name in curCsvDict:
                    curCsvDict[_name] = [_type, _value,0]
                else:
                    curCsvDict[_name][1] += _value


        if bHistoricalWebSource:
            # historical 만 출력
            data_result = [['name','type','value','date']] # csv 데이터

            # 최고 조회수만 갱신해서 그걸로 결과 보여주기
            if bUseMaxValue:
                max_values = {}
                for i,keyDate in enumerate(data_stack):
                    curCsvDict = data_stack[keyDate]
                    for _name in curCsvDict:
                        data = curCsvDict[_name]
                        # 최초로 나오거나 기존 최대치보다 크면 저장
                        if not _name in max_values or max_values[_name] < data[1]:
                            max_values[_name] = data[1]
                    sorted_max_values = sorted(max_values, key=lambda x:max_values[x], reverse=True)
                    if (i % 7) == 0:
                        for k,_name in enumerate(sorted_max_values):
                            if k > 50:
                                break
                            data_result.append([
                                _name, typeDict[_name], max_values[_name], keyDate])
            else:
                for keyDate in data_stack:
                    curCsvDict = data_stack[keyDate]
                    for _name in curCsvDict:
                        data = curCsvDict[_name]
                        data_result.append([
                            _name, data[0], data[1], keyDate])

            # for _name in all_csv_data:
            #     data_result.append(all_csv_data[_name])
        else:
            # 모든 파일에서 각각의 맵에 대한 조회수 총합
            all_csv_data = {}
            for csvDictKey in data_stack:
                csvDict = data_stack[csvDictKey]
                for _name in csvDict:
                    _type = csvDict[_name][0]
                    _value = int(csvDict[_name][1])
                    _date = csvDictKey
                    if not _name in all_csv_data:
                        all_csv_data[_name] = [_name, _type, _value, _date]
                    else:
                        all_csv_data[_name][2] += _value
                        all_csv_data[_name][3] += f', {_date}'
            # historical + 꾸준한 조회수를 받은 (날짜가 많은) 건지 데이터 추가
            data_result = [['name','type','value','date count', 'date']] # csv 데이터
            for _name in all_csv_data:
                data_result.append([
                    all_csv_data[_name][0],
                    all_csv_data[_name][1],
                    all_csv_data[_name][2],
                    all_csv_data[_name][3].count(',')+1,
                    all_csv_data[_name][3]
                    ])

        result= pd.DataFrame(data_result)
        if bHistoricalWebSource:
            outputFileName = f'output_{joinMeList}.csv'
            result.to_csv(outputFileName, index=False, header=None)
        else:
            outputFileName = f'output_{joinMeList}.xlsx'
            result.to_excel(outputFileName, index=False, header=None)

        ### 디버깅 or 단순출력
        sorted_data = data_result[1:]
        sorted_data.sort(key=lambda x: x[0]) # name 에 대해서 정렬
        # sorted_data.sort(key=lambda x: x[2]) # value 에 대해서 정렬
        b중복제거 = True
        의심목록=[]
        if b중복제거:
            중복제거 = []
            priv_map_name = None
            for _data in tqdm(sorted_data):
                if _data[1] in 중복제거:
                    continue
                중복제거.append(_data[1])
                # print(_data)
                cur_map_name = _data[0]
                if priv_map_name is not None:
                    minRange = min(len(priv_map_name),len(cur_map_name))
                    equal_count = 0
                    for i in range(minRange):
                        if priv_map_name[i] == cur_map_name[i]:
                            equal_count += 1
                        else:
                            break
                    if autoDetect and equal_count >= 5:
                        의심목록.append((priv_map_name,cur_map_name))
                        # print(f'EQUAL_COUNT : {equal_count}')
                        # print(f'    {priv_map_name}')
                        # print(f'    {cur_map_name}')
                        # input('continue?')
                priv_map_name = _data[0]
        else:
            for _data in sorted_data:
                print(_data)
        
        for map_name in tqdm(의심목록):
            print(f'    {map_name[0]}')
            print(f'    {map_name[1]}')
            print()
      
    def analytics_UsemapRank_preprocess(self, joinMeList):
        for joinMe in joinMeList:
            ed_list = []
            board_period_dict = {} # 중복 데이터 검사용
            dataDir = os.path.join('data', 'usemap_rank', joinMe)
            outputDir = os.path.join(dataDir, 'preprocess')
            moveToDir = os.path.join(dataDir, '원본')
            if not os.path.exists(outputDir):
                os.makedirs(outputDir)
            flist = os.listdir(dataDir)
            for fname in flist:
                fPath = os.path.join(dataDir, fname)
                if os.path.isdir(fPath):
                    continue
                ed = pd.read_excel(fPath, engine = 'openpyxl')
                ed_list.append(ed)

                period = ed.columns.values[1]
                boardType = ed.values[3][1]
                board_period_str = f'{boardType}_{period}'
                # print(f'{fPath}-> {board_period_str}')
                if board_period_str in board_period_dict:
                    print(f'동일한 데이터: {board_period_str}\n{fname} == {board_period_dict[board_period_str]}')
                    continue
                board_period_dict[board_period_str] = fname
        
            ed_list.sort(key=lambda x : x.columns.values[1])
            for ed in ed_list:
                period = ed.columns.values[1]
                startDate = period.split('~')[0] # 시작날짜 
                res = re.findall('(.*)년 (.*)월 (.*)일', startDate)[0]
                year = int(res[0])
                month = int(res[1])
                day = int(res[2])
                _date = f'{year}-{month:02d}-{day:02d}'


                values = ed.values[7:,:]
                boardType = ed.values[3][1]
                memberType = ed.values[4][1]
                if memberType != "방문자 전체":
                    print(f'{memberType} is not 방문자 전체 {fname}')


                result= pd.DataFrame(values)
                filename = f'{boardType}_{_date}.xlsx'
                outputPath = os.path.join(outputDir, filename)
                print(outputPath)
                result.to_excel(outputPath, index=False, header="dummy")
            os.system(f'move {dataDir}\\*.xlsx {moveToDir}')
        
    ### 멤버 순위 관련
    # 멤버 순위 데이터 구글 스프레드 시트에 업로드
    def upload_member_rank_data(self, year):
        dataDir = os.path.join('data','member_rank', str(year))
        filenamelist = os.listdir(dataDir)
        written_list = {}
        moveToDir = os.path.join(dataDir,'uploaded')
        if not os.path.exists(moveToDir):
            os.system(f'mkdir {moveToDir}')

        for fname in filenamelist:
            fPath = os.path.join(dataDir,fname)
            if os.path.isdir(fPath):
                continue
            fPath = os.path.join(dataDir, fname)
            ed = pd.read_excel(fPath, engine = 'openpyxl')
            ed = ed.fillna('nan')
            # ed['Unnamed: 4'] = ed['Unnamed: 4'].astype(int)
            dataPeriod = ed.columns[1]
            groupList = re.findall('([0-9]*)년 ([0-9]*)월', dataPeriod)
            year = int(groupList[0][0])
            month = int(groupList[0][1])

            data = ed.values[5:,:]
            head = [f'{year}년 {month}월','','','','']
            data = data.tolist()
            for i in range(1,len(data)):
                data[i][4] = int(data[i][4])
            data.insert(0, head)

            rankType = None
            if '작성게시글수' in fname:
                rankType = RANK_TYPE_POST
            elif '받은좋아요수' in fname:
                rankType = RANK_TYPE_LIKE
            elif '작성댓글수' in fname:
                rankType = RANK_TYPE_COMMENT
            elif '방문횟수' in fname:
                rankType = RANK_TYPE_VISIT
            else:
                raise Exception(f'Unknown data category name. fname={fname}')

            work_name = f'{year}.{month} {worksheetName_map[rankType]}'
            if work_name in written_list:
                raise Exception(f"데이터 충돌 {work_name}")
            else:
                written_list[work_name] = True
            ret = self.writer.writeRankData(year, month, rankType, data)
            print(work_name, ret)

            os.system(f'move {fPath} {moveToDir}')
    # 특정 년도 전체 순위
    def analytics_member_1year(self, year):
        dataDir = os.path.join('data','member_rank', str(year), 'uploaded')
        filenamelist = os.listdir(dataDir)
        member_rank_dict = {
            '작성댓글수':[],
            '작성게시글수':[],
            '받은좋아요수':[],
            '방문횟수':[]
        }
        for fname in filenamelist:
            fPath = os.path.join(dataDir,fname)
            if os.path.isdir(fPath):
                continue
            fPath = os.path.join(dataDir, fname)
            ed = pd.read_excel(fPath, engine = 'openpyxl')
            ed = ed.fillna('nan')
            for rank_type in member_rank_dict:
                if rank_type in fname:
                    curRankList = member_rank_dict[rank_type]
                    for i in range(6,len(ed.values)):
                        memberName = ed.values[i][1]
                        if memberName == '탈퇴한 회원입니다.':
                            continue
                        score = int(ed.values[i][4])
                        for item in curRankList:
                            if item[0] == memberName:
                                item[1] += score
                                break
                        else:
                            curRankList.append([memberName,score])

        for rank_type in member_rank_dict:
            curRankListTop100 = member_rank_dict[rank_type]
            curRankListTop100.sort(key=lambda x : x[1])
            curRankListTop100.reverse()
            curRankListTop100=curRankListTop100[:100]

            # 1등 확정
            curRankListTop100[0].insert(0, 1)
            rank = 1
            sameScoreCount = 0
            for i in range(1, len(curRankListTop100)):
                prevItem = curRankListTop100[i-1]
                curItem = curRankListTop100[i]
                if prevItem[2] == curItem[1]:
                    sameScoreCount += 1
                else:
                    rank += 1 + sameScoreCount
                    sameScoreCount = 0
                curItem.insert(0,rank)
            curDF = pd.DataFrame(curRankListTop100)
            curDF.to_excel(f'{year}년 {rank_type} 통계.xlsx', index=False, header=['순위','닉네임',rank_type])


    
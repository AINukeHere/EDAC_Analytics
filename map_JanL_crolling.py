import os

self_made_headMap={
    235:'캠페인',
    369:'디펜스',
    370:'대전',
    371:'RPG',
    372:'블러드',
    373:'미니게임',
    374:'컴까기',
    375:'서바이벌',
    376:'컨트롤',
    395:'리듬게임',
    397:'퍼즐',
    399:'밀리기반',
    401:'기타',
    403:'디플로메시',
    407:'키우기',
    409:'어드벤처',
    411:'공포',
    412:'영상',
    413:'탈출',
    414:'오펜스',
    415:'병맛',
    421:'추리',
    423:'슈팅',
    425:'AOS',
    428:'레이싱',
}
made_by_other_headMap={
    378:'캠페인',
    379:'디펜스',
    380:'대전',
    381:'RPG',
    382:'블러드',
    383:'미니게임',
    384:'컴까기',
    385:'서바이벌',
    377:'컨트롤',
    396:'리듬게임',
    398:'퍼즐',
    400:'밀리기반',
    402:'기타',
    404:'디플로메시',
    408:'키우기',
    410:'어드벤처',
    416:'공포',
    417:'영상',
    418:'탈출',
    419:'오펜스',
    420:'병맛',
    422:'추리',
    424:'슈팅',
    426:'AOS',
    427:'호환요청',
    429:'레이싱'
}
chrome = r'"C:\Program Files\Google\Chrome\Application\chrome.exe"'

headMapMap={
    23:self_made_headMap,
    26:made_by_other_headMap,
}
import time
for menuid in headMapMap:
    headMap = headMapMap[menuid]
    input()
    time.sleep(1)
    for headid in headMap:
        url = f'https://cafe.naver.com/edac?iframe_url=/ArticleList.nhn%3Fsearch.clubid=17046257%26search.menuid={menuid}%26search.boardtype=L%26userDisplay=50%26search.headid={headid}'
        cmd = f'{chrome} {url}'
        os.system(cmd)
        time.sleep(1)

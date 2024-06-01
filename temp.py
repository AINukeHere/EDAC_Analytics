

import subprocess

chrome='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
for memberId in range(1000):
    downloadURL = f'https://cafe.stat.naver.com/download/cafe/17046257/user/referer/search?service=CAFE&timeDimension=MONTH&startDate=2024-04-01&memberId={memberId}'
    cmd = f'"{chrome}" "{downloadURL}"'
    print(cmd)
    subprocess.check_call(cmd)
    if memberId % 10 == 0:
        input()
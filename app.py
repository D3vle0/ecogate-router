#!/usr/bin/python3
import requests
import json
import sys

cookies = {
    'LiT': 'U',
    'LiU': '0',
    'loginChk': 'N',
    'mdd': '100',
    'patches': '0',
    'uid': 'aef00de0ffcfaeaeadc',
    'language': 'ko',
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'text/plain, */*; q=0.01',
    'Accept-Language': 'ko-KR,ko;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Host': '192.168.255.1',
    'Origin': 'http://192.168.255.1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
    'Connection': 'keep-alive',
    'Referer': 'http://192.168.255.1/basic/3g.html?random=1631007152543',
    'Content-Length': '21',
    'X-Requested-With': 'XMLHttpRequest',
}

data = {
  'page': 'getDataUsageInfo'
}
if len(sys.argv) == 1:
    response = requests.post('http://192.168.255.1/cgi-bin/meco_web_cgi', headers=headers, cookies=cookies, data=data)
    print("🚀 Ecogate Router Data Usage Viewer")
    print(f"{int((json.loads(response.text))['lgdatainfo']['mdatause'])/1000} MB used this month")
else:
    if sys.argv[1] in ["-h", "--help"]:
        print("이 프로그램은 mobileeco 사에서 생산한 ecogate (LG U+ Mobile Router)\n휴대용 라우터의 데이터 사용량을 확인할 수 있는 프로그램입니다.\n")
        print("made by Devleo\n\nhttps://github.com/d3vle0")
#!/usr/bin/python3
import requests
import json
import sys
import socket

ROUTER_IP_ADDR = "192.168.255.1"
URL = f"http://{ROUTER_IP_ADDR}/cgi-bin/meco_web_cgi"

cookies = {
    "LiT": "U",
    "LiU": "0",
    "loginChk": "N",
    "mdd": "100",
    "patches": "0",
    "uid": "aef00de0ffcfaeaeadc",
    "language": "ko",
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "text/plain, */*; q=0.01",
    "Accept-Language": "ko-KR,ko;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Host": ROUTER_IP_ADDR,
    "Origin": ROUTER_IP_ADDR,
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
    "Connection": "keep-alive",
    "Referer": f"http://{ROUTER_IP_ADDR}/basic/3g.html?random=1631007152543",
    "Content-Length": "21",
    "X-Requested-With": "XMLHttpRequest",
}

def getHostname(i):
    if i["ip_addr"] == "0.0.0.0":
        return socket.gethostname()
    return i['hostname']

if len(sys.argv) == 1:
    response = requests.post(URL, headers=headers, cookies=cookies, data={"page": "getDataUsageInfo"})
    print("🚀 Ecogate Router Info Viewer\n")
    print(f"🔥 Data Usage: {int((json.loads(response.text))['lgdatainfo']['mdatause'])/1000} MB")
    response = requests.post(URL, headers=headers, cookies=cookies, data={"page": "getLanInfo"})
    if len(json.loads(response.text)["wifi2Ghz"]["conn_client"]["conn_list"]) <= 1:
        print(f"💻 Connected Host: ", end="")
    else:
        print(f"💻 Connected Hosts: ", end="")
    print(", ".join(map(getHostname, json.loads(response.text)["wifi2Ghz"]["conn_client"]["conn_list"])))
    response = requests.post(URL, headers=headers, cookies=cookies, data={"page": "getWWanInfo"})
    print(f"⏰ Uptime: {json.loads(response.text)['info']['h']}h {json.loads(response.text)['info']['m']}m {json.loads(response.text)['info']['s']}s")
    # d 추가할것
    response = requests.post(URL, headers=headers, cookies=cookies, data={"page": "getIndicatorInfo"})
    print(f"🔋 Battery: {json.loads(response.text)['info']['disp_bat_per']}%")
else:
    if sys.argv[1] in ["-h", "--help"]:
        print("이 프로그램은 mobileeco 사에서 생산한 ecogate (LG U+ Mobile Router)\n휴대용 라우터의 연결 정보를 확인할 수 있는 프로그램입니다.\n")
        print("made by Devleo\n\nhttps://github.com/d3vle0")
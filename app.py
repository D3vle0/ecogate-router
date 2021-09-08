#!/usr/bin/python3
import requests
import json
import sys
from dotenv import load_dotenv
import os
import socket
from termcolor import colored
from getpass import getpass

ROUTER_IP_ADDR = "192.168.255.1"
URL = f"http://{ROUTER_IP_ADDR}/cgi-bin/meco_web_cgi"
load_dotenv(verbose=True)

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
    if i["ip_addr"] == "0.0.0.0" and i["mac_addr"] == os.getenv("MY_MAC_ADDR"):
        return socket.gethostname()
    return i['hostname']

if len(sys.argv) == 1:
    response = requests.post(URL, headers=headers, cookies=cookies, data={"page": "getDataUsageInfo"})
    print(colored("🚀 Ecogate Router Info Viewer\n", "green"))
    print("===== Basic Information =====")
    print(f"🔥 Data Usage: {int((json.loads(response.text))['lgdatainfo']['mdatause'])/1000} MB")
    response = requests.post(URL, headers=headers, cookies=cookies, data={"page": "getLanInfo"})
    if len(json.loads(response.text)["wifi2Ghz"]["conn_client"]["conn_list"]) <= 1:
        print(f"💻 Connected Host: ", end="")
    else:
        print(f"💻 Connected Hosts: ", end="")
    print(", ".join(map(getHostname, json.loads(response.text)["wifi2Ghz"]["conn_client"]["conn_list"])))
    response = requests.post(URL, headers=headers, cookies=cookies, data={"page": "getWWanInfo"})
    uptime_hour = int(json.loads(response.text)['info']['h'])
    if uptime_hour > 8:
        print(colored(f"⏰ Uptime: {str(uptime_hour)}h {json.loads(response.text)['info']['m']}m {json.loads(response.text)['info']['s']}s", "red"))
    elif uptime_hour >= 5:
        print(colored(f"⏰ Uptime: {str(uptime_hour)}h {json.loads(response.text)['info']['m']}m {json.loads(response.text)['info']['s']}s", "yellow"))
    else:
        print(colored(f"⏰ Uptime: {str(uptime_hour)}h {json.loads(response.text)['info']['m']}m {json.loads(response.text)['info']['s']}s", "green"))
    # d 추가할것
    response = requests.post(URL, headers=headers, cookies=cookies, data={"page": "getIndicatorInfo"})
    battery = int(json.loads(response.text)['info']['disp_bat_per'])
    if int(json.loads(response.text)['info']['disp_bat_level']) == 5:
        print(colored("⚡️ Charging", "cyan"))
    else:
        if battery >= 60:
            print(colored(f"🔋 Battery: {battery}%\n", "green"))
        elif battery >= 30 and battery < 60:
            print(colored(f"🔋 Battery: {battery}%\n", "yellow"))
        else:
            print(colored(f"🔋 Battery: {battery}%\n", "red"))
    response = requests.post(URL, headers=headers, cookies=cookies, data={"page": "getWWanInfo"})
    print("===== Network =====")
    print(f"📨 Public IP Addr: {json.loads(response.text)['info']['public_ip']}")
    print(f"1️⃣  Primary DNS: {json.loads(response.text)['info']['primary_dns']}")
    print(f"2️⃣  Secondary DNS: {json.loads(response.text)['info']['secondary_dns']}")
    response = requests.post(URL, headers=headers, cookies=cookies, data={"page": "getLanInfo"})
    print(f"🔌 MAC Addr: {json.loads(response.text)['lan']['macAddr']}")

else:
    if sys.argv[1] in ["-h", "--help"]:
        print("이 프로그램은 mobileeco 사에서 생산한 ecogate (LG U+ Mobile Router)\n휴대용 라우터의 연결 정보를 확인할 수 있는 프로그램입니다.\n")
        print("argv[1]: -h, --help - 도움말 표시")
        print("argv[1]: -p, --password - 와이파이 비밀번호 표시")
        print("argv[1]: null - 프로그램 실행")
        print("made by Devleo\n\nhttps://github.com/d3vle0")
    if sys.argv[1] in ["-p", "--password"]:
        print(colored("🚀 Ecogate Router Info Viewer\n", "green"))
        password = getpass("Input Password: ")
        print(os.environ["HOME"])
        # export 환경변수를 영구적으로 등록하는 명령어 알아야함
        if password == os.environ["ROUTER_PASS"]:
            response = requests.post(URL, headers=headers, cookies=cookies, data={"page": "netWirelessInfo"})
            print(f"📌 SSID: {json.loads(response.text)['wifi2Ghz']['ssid']}")
            print(f"🔐 PW: {json.loads(response.text)['wifi2Ghz']['wpa_passphrase']}")
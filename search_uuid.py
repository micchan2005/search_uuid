import sys
from tetpyclient import RestClient
import json
import re
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()

API_ENDPOINT="https://<Your Cluster's FQDN>"

rc = RestClient(API_ENDPOINT,credentials_file='credentials.json', verify=False)

resp = rc.get('/sensors')
sensor = resp.json()

result = sensor['results']
w_num = len(result)

def getuuid_ip(ipaddr):
    i_num = 0
    for a in range(w_num):
        ints = result[i_num]['interfaces']
        ip_num = len(ints)
        x = 0
        for b in range(ip_num):
            if ints[x]['ip'] == ipaddr:
                return(result[i_num]['uuid'])
            x += 1
        i_num += 1

def getuuid_host(hostname):
    i_num = 0
    for c in range(w_num):
        if result[i_num]['host_name'] == hostname:
            return(result[i_num]['uuid'])
        i_num += 1

def main():
    while True:
        print('IPアドレスとホスト名どちらで検索したいか選択して下さい')
        print('1: IPアドレス')
        print('2: ホスト名')
        x = input('1 か 2 どちらかを入力して下さい:')
        x = int(x)

        if x == 1:
            while True:
                ip = input('対象のIPアドレスを入力してください： ')
                ip = str(ip)
                pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
                test = pat.match(ip)
                if test:
                    print('入力を受け付けました')
                    break
                else:
                    print('入力が正しくありません')

            uuid = getuuid_ip(ip)
            print('uuidは: ' + uuid + ' です。')
            break

        if x == 2:
            while True:
                hostname = input('対象のホスト名を入力して下さい：')
                hostname = str(hostname)
                if hostname:
                    print('入力を受け付けました')
                    break
                else:
                    print('入力が正しくありません')
            uuid = getuuid_host(hostname)
            print('uuidは: ' + uuid + ' です。')
            break


if __name__ == '__main__':
    main()

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

IP_data = []
# 忽略https安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def getfile():
    file_data = open('./save/result.txt', 'r')
    for i in file_data.readlines():
        i = i.replace("\n", "")
        i = i.split(":")
        IP_data.append(i)
    file_data.close()


def request_test(IP_test):
    url = "http://" + IP_test[0]
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            f = open('./save/过滤后资产.txt', 'a')
            f.write(IP_test[0] + ':' + IP_test[1])
            print("test:" + IP_test[0] + "返回值:200")
    except Exception as e:
        print("请求失败")


if __name__ == '__main__':
    getfile()
    for i in range(0, len(IP_data)):
        request_test(IP_data[i])

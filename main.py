import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import base64
import yaml

# 忽略https安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 结果
result = []


# 获取配置信息
def getFofaconfig():
    file = open("config/fofaConfig.yaml", 'r', encoding='utf-8')
    file_date = file.read()  # 配置文件数据保存到变量中
    file.close()
    # 处理配置文件
    Userdata = yaml.load(file_date, Loader=yaml.FullLoader)
    return Userdata


def IptoHostname(result):
    url =[]
    j = 1
    for i in result['results']:
        url.append(str(i[1]+':'+i[2]))
    print(url)



def getTarget():
    useremail = str(getFofaconfig().get('email'))
    userkey = str(getFofaconfig().get('key'))
    # fofa获取站点
    Search = getFofaconfig().get('Search')
    select = base64.b64encode(Search.encode('UTF-8'))
    select = str(select, 'UTF-8')
    fofa_url = "https://fofa.so/api/v1/search/all?email=" + useremail + "&key=" + userkey + "&qbase64=" + select
    try:
        res = requests.get(fofa_url)
        result = json.loads(res.text)
        IptoHostname(result)
        count = 0
        with open('save/result.txt', 'w') as targets:
            for i in result['results']:
                targets.write(i[1] + ':' + i[2] + '\n')
                print(i[1])
                count += 1
            print("搜索结果有" + str(count) + "条，已保存")


    except Exception as e:
        print(e)


getTarget()

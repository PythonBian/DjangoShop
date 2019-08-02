#coding:utf-8
import json
import requests

url = "https://oapi.dingtalk.com/robot/send?access_token=2d33d53383aaae6199e81d569c31d5d2f8e872b9e2d61c31a636ae31b8c108f4"

headers = {
    "Content-Type": "application/json",
    "Chartset": "utf-8"
}

requests_data = {
    "msgtype": "text",
    "text":{
        "content": "我就是我, 是不一样的烟火"
    },
    "at":{
        "atMobiles":[
        ],
    },
    "isAtAll": True
}

sendData = json.dumps(requests_data)
response = requests.post(url,headers = headers,data=sendData)
content = response.json()
print(content)
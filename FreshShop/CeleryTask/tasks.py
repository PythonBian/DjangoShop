#coding:utf-8
from __future__ import absolute_import
import json
import requests

from FreshShop.celery import app #在安装成功celery框架之后，django新生成的模块

@app.task #将taskExample转换为一个任务
def taskExample():
   print('send email ok!')
   return 'send email ok!'

@app.task
def add(x=1, y=2):
   return x+y


@app.task
def DingTalk():
   url = "https://oapi.dingtalk.com/robot/send?access_token=2d33d53383aaae6199e81d569c31d5d2f8e872b9e2d61c31a636ae31b8c108f4"

   headers = {
       "Content-Type": "application/json",
       "Chartset": "utf-8"
   }

   requests_data = {
       "msgtype": "text",
       "text":{
           "content": "又是一个美好的晚上，你们写作业了吗？bug改了吗？工资发了吗，信用卡还了吗，房子买了吗？"
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
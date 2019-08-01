#coding:utf-8
# import requests
#
# url = "http://106.ihuyi.com/webservice/sms.php?method=Submit"
#
# account = "C85050877"
# password = "9c14def972fa00acf877b04cc827fa8a"
# mobile = "13331153360"
# content = "您的验证码是：201981。请不要把验证码泄露给其他人。"
# #定义请求的头部
# headers = {
#     "Content-type": "application/x-www-form-urlencoded",
#     "Accept": "text/plain"
# }
# #定义请求的数据
# data = {
#     "account": account,
#     "password": password,
#     "mobile": mobile,
#     "content": content,
# }
# #发起数据
# response = requests.post(url,headers = headers,data=data)
#     #url 请求的地址
#     #headers 请求头部
#     #data 请求的数据
#
# print(response.content.decode())
import json
import requests

url = "https://open.ucpaas.com/ol/sms/sendsms"

sid = ""
token = ""
appid = ""
templateid = ""
param = "0506"
mobile = ""

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json;charset=utf-8'
}
#定义请求的数据
data = {
    "sid": sid,
    "token": token,
    "appid": appid,
    "templateid": templateid,
    "param": param,
    "mobile": mobile,
}
#发起数据
response = requests.post(url,headers = headers,data=json.dumps(data))
    #url 请求的地址
    #headers 请求头部
    #data 请求的数据

print(response.json())

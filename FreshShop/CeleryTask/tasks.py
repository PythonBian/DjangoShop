from __future__ import absolute_import
from FreshShop.celery import app #�ڰ�װ�ɹ�celery���֮��django�����ɵ�ģ��

@app.task #��taskExampleת��Ϊһ������
def taskExample():
   print('send email ok!')

@app.task
def add(x=1, y=2):
   return x+y
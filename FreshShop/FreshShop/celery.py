from __future__ import absolute_import,unicode_literals
import os
from celery import Celery
from django.conf import settings

# ����celeryִ�еĻ�������,ִ��django��Ŀ�������ļ�
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CeleryTask.settings")

#����celeryӦ��
app = Celery('art_project') #celeryӦ�õ�����
app.config_from_object('django.conf:settings') #���ص������ļ�

#����ڹ��̵�Ӧ���д�����tasks.pyģ�飬��ôCeleryӦ�þͻ��Զ�ȥ�������������񡣱����������һ����#����django�л�ʵʱ�ؼ���������
app.autodiscover_tasks(lambda :settings.INSTALLED_APPS)
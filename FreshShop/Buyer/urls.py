from django.urls import path,include
from Buyer.views import *
urlpatterns = [
    path("login/", login),
    path("logout/", logout),
    path("register/", register),
    path("index/", index),
    path("goods_list/", goods_list),
]

urlpatterns+=[
    path("base/", base),
    path("pay_order/", pay_order),
    path("pay_result/", pay_result),
]
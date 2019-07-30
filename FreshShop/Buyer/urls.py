from django.urls import path,include
from Buyer.views import *
urlpatterns = [
    path("login/", login),
    path("logout/", logout),
    path("register/", register),
    path("index/", index),
    path("goods_list/", goods_list),
    path("goods_detail/", goods_detail),
    path("place_order/", place_order),
    path(r'cart/', cart),  # 订单列表
    path(r'add_cart/', add_cart),  # 订单列表
]

urlpatterns+=[
    path("base/", base),
    path("pay_order/", pay_order),
    path("pay_result/", pay_result),
]
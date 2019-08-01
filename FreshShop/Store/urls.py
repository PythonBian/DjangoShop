from django.urls import path,re_path
from Store.views import *

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('index/', index),
    path('logout/', logout),
    re_path('^$', index),
    path('register_store/', register_store),
    path('add_goods/', add_goods),
    re_path(r'list_goods/(?P<state>\w+)', list_goods),#商品列表页
    re_path(r'^goods/(?P<goods_id>\d+)',goods),
    re_path(r'update_goods/(?P<goods_id>\d+)', update_goods),
    re_path(r'set_goods/(?P<state>\w+)/', set_goods), #设置商品状态
    path(r'list_goods_type/', list_goods_type),  # 设置商品状态
    path(r'delete_goods_type/', delete_goods_type),  # 设置商品状态
    path(r'order_list/', order_list) # 订单列表
]

urlpatterns += [
    path('base/', base),
    path('Test/', CookieTest),
    path(r'agl/', ajax_goods_list),  # 订单列表
    path(r'get_add/', get_add)  # 订单列表
]














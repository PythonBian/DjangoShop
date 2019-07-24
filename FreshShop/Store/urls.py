from django.urls import path,re_path
from Store.views import *

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('index/', index),
    re_path('^$', index),
    path('register_store/', register_store),
    path('add_goods/', add_goods),
    path('list_goods/', list_goods),
    re_path(r'^goods/(?P<goods_id>\d+)',goods),
    re_path(r'update_goods/(?P<goods_id>\d+)', update_goods)
]

urlpatterns += [
    path('base/', base),
    path('Test/', CookieTest)
]

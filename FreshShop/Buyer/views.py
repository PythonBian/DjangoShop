from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect

from Buyer.models import *
from Store.views import set_password
from Store.models import *

def loginValid(fun):
    def inner(request,*args,**kwargs):
        c_user = request.COOKIES.get("username")
        s_user = request.session.get("username")
        if c_user and s_user and c_user == s_user:
            return fun(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/Buyer/login/")
    return inner

def register(request):
    if request.method == "POST":
        #获取前端post请求的数据
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        email = request.POST.get("email")
        #将数据存入数据库
        buyer = Buyer()
        buyer.username = username
        buyer.password = set_password(password)
        buyer.email = email
        buyer.save()
        #跳转到login页面
        return HttpResponseRedirect("/Buyer/login/")
    return render(request,"buyer/register.html")

def login(request):
    if request.method == "POST":
        #获取数据
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        if username and password:
            #判断用户是否存在
            user = Buyer.objects.filter(username=username).first()
            if user:
                #密码加密比对
                web_password = set_password(password)
                if user.password == web_password:
                    response = HttpResponseRedirect("/Buyer/index/")
                    #校验的登陆
                    response.set_cookie("username",user.username)
                    request.session["username"] = user.username
                    #方便其他查询
                    response.set_cookie("user_id",user.id)
                    return response
    return render(request,"buyer/login.html")

@loginValid
def index(request):
    goods_type_list = GoodsType.objects.all()
    print(goods_type_list)
    return render(request,"buyer/index.html",locals())

def logout(request):
    response = HttpResponseRedirect("/Buyer/login/")
    #删除所有的请求携带的cookie
    for key in request.COOKIES:
        response.delete_cookie(key)
    #删除session
    del request.session["username"]
    return response

def base(request):
    return render(request,"buyer/base.html")

# Create your views here.









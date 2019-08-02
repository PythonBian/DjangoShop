import hashlib
from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect

from Store.models import *
from Buyer.models import *

def loginValid(fun):
    def inner(request,*args,**kwargs):
        c_user = request.COOKIES.get("username")
        s_user = request.session.get("username")
        if c_user and s_user and c_user == s_user:
            return fun(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/Store/login/")
    return inner

def set_password(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result

def register(request):
    """
    register注册
    返回注册页面
    进行注册数据保存
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            seller = Seller()
            seller.username = username
            seller.password = set_password(password)
            seller.nickname = username
            seller.save()
            return HttpResponseRedirect("/Store/login/")
    return render(request,"store/register.html")

def login(request):
    """
    登陆功能，如果登陆成功，跳转到首页
    如果失败，跳转到登陆页
    """
    #加载登陆页面，下发页面校验cookie校验登陆请求从登陆页面发起
    response = render(request,"store/login.html")
    response.set_cookie("login_from","login_page")
    #处理登陆
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            #校验的是用户名是否存在
            user = Seller.objects.filter(username = username).first()
            if user:
                web_password = set_password(password)
                #校验请求是否来源于登陆页面
                cookies = request.COOKIES.get("login_from")
                # 校验密码是否正确
                if user.password == web_password and cookies == "login_page":
                    response = HttpResponseRedirect("/Store/index/")
                    # 校验是否登陆
                    response.set_cookie("username",username)
                    request.session["username"] = username

                    #cookie提供用户id方便其他功能查询
                    response.set_cookie("user_id", user.id)

                    #校验是否有店铺
                    store = Store.objects.filter(user_id=user.id).first()  # 再查询店铺是否存在
                    if store:
                        response.set_cookie("has_store", store.id) #将店铺id设置为cookie值
                    else:
                        response.set_cookie("has_store", "") #没有就为空 ""代表空
                    return response
    return response

@loginValid
def index(request):
    """
    添加检查账号是否有店铺的逻辑
    """
    #查询当前用户是谁
    return render(request,"store/index.html")

@loginValid
def register_store(request):
    type_list = StoreType.objects.all()
    if request.method == "POST":
        post_data = request.POST #接收post数据
        store_name = post_data.get("store_name")
        store_descripton = post_data.get("store_descripton")
        store_phone = post_data.get("store_phone")
        store_money = post_data.get("store_money")
        store_address = post_data.get("store_address")

        user_id =int(request.COOKIES.get("user_id")) #通过cookie来得到user_id
        type_lists = post_data.getlist("type") #通过request.post得到类型，但是是一个列表

        store_logo = request.FILES.get("store_logo") #通过request.FILES得到

        #保存非多对多数据
        store = Store()
        store.store_name = store_name
        store.store_descripton = store_descripton
        store.store_phone = store_phone
        store.store_money = store_money
        store.store_address = store_address
        store.user_id = user_id
        store.store_logo = store_logo #django1.8之后图片可以直接保存
        store.save() #保存，生成了数据库当中的一条数据
        #在生成的数据当中添加多对多字段。
        for i in type_lists: #循环type列表，得到类型id
            store_type = StoreType.objects.get(id = i) #查询类型数据
            store.type.add(store_type) #添加到类型字段，多对多的映射表
        store.save() #保存数据
        #数据保存成功之后，跳转到主页
        response = HttpResponseRedirect("/Store/index/")
        #下发cookie证明当前用户有店铺
        response.set_cookie("has_store", store.id)
        return response
    return render(request, "store/register_store.html", locals())

@loginValid
def add_goods(request):
    """
    负责添加商品
    """
    goods_type_list = GoodsType.objects.all()
    if request.method == "POST":
        #获取post请求
        goods_name = request.POST.get("goods_name")
        goods_price = request.POST.get("goods_price")
        goods_number = request.POST.get("goods_number")
        goods_description = request.POST.get("goods_description")
        goods_date = request.POST.get("goods_date")
        goods_safeDate = request.POST.get("goods_safeDate")
        goods_type = request.POST.get("goods_type")
        #使用cookie当中的店铺id
        goods_store = request.COOKIES.get("has_store")
        goods_image = request.FILES.get("goods_image")
        #开始保存数据
        goods = Goods()
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        goods.goods_image = goods_image
        goods.goods_type = GoodsType.objects.get(id = int(goods_type))
        goods.store_id = Store.objects.get(id = int(goods_store))
        goods.save()
        return HttpResponseRedirect("/Store/list_goods/up/")
    return render(request,"store/add_goods.html",locals())

@loginValid
def list_goods(request,state):
    """
    商品的列表页
    :param request:
    :param state: 商品状态
        up    在售
        down  下架
    """
    if state == "up":
        state_num = 1
    else:
        state_num = 0
    #获取两个关键字
    keywords = request.GET.get("keywords","") #查询关键词
    page_num = request.GET.get("page_num",1) #页码
    #查询店铺
    store_id = request.COOKIES.get("has_store")
    store = Store.objects.get(id=int(store_id))
    if keywords: #判断关键词是否存在
        goods_list = store.goods_set.filter(goods_name__contains=keywords,goods_under=state_num)#完成了模糊查询

    else: #如果关键词不存在，查询所有
        goods_list = store.goods_set.filter(goods_under=state_num)
    #分页，每页3条
    paginator = Paginator(goods_list,3)
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    #返回分页数据
    return render(request,"store/goods_list.html",{"page":page,"page_range":page_range,"keywords":keywords,"state":state})

@loginValid
def goods(request,goods_id):
    goods_data = Goods.objects.filter(id = goods_id).first()
    return render(request,"store/goods.html",locals())

@loginValid
def update_goods(request,goods_id):
    goods_data = Goods.objects.filter(id=goods_id).first()
    if request.method == "POST":
        # 获取post请求
        goods_name = request.POST.get("goods_name")
        goods_price = request.POST.get("goods_price")
        goods_number = request.POST.get("goods_number")
        goods_description = request.POST.get("goods_description")
        goods_date = request.POST.get("goods_date")
        goods_safeDate = request.POST.get("goods_safeDate")
        goods_image = request.FILES.get("goods_image")
        # 开始修改数据
        goods = Goods.objects.get(id = int(goods_id)) #获取当前商品
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        if goods_image: #如果有上传图片再发起修改
            goods.goods_image = goods_image
        goods.save()
        return HttpResponseRedirect("/Store/goods/%s/"%goods_id)
        # 保存多对多数据
    return render(request, "store/update_goods.html", locals())

@loginValid
def add_goods_type(request):
    pass

@loginValid
def list_goods_type(request):
    goods_type_list = GoodsType.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        picture = request.FILES.get("picture")

        goods_type = GoodsType()
        goods_type.name = name
        goods_type.description = description
        goods_type.picture = picture
        goods_type.save()
    return render(request,"store/goods_type_list.html",locals())

@loginValid
def delete_goods_type(request):
    id = int(request.GET.get("id"))
    goods = GoodsType.objects.get(id = id)
    goods.delete()
    return HttpResponseRedirect("/Store/list_goods_type/")


def base(request):
    return render(request,"store/base.html")



# Create your views here.


def CookieTest(request):
    #查询拥有指定商品的所有店铺
    goods = Goods.objects.get(id = 1)
    # store_list = goods.store_id.all()
    # store_list = goods.store_id.filter()
    # store_list = goods.store_id.get()
    #查询指定店铺拥有的所有商品
    # store = Store.objects.get(id = 17)
    #goods是多对多表的名称的小写_set是固定写法
    # store.goods_set.get()
    # store.goods_set.filter()
    # store.goods_set.all()

    response = render(request,"store/Test.html",locals())
    response.set_cookie("valid",'')
    return response

def set_goods(request,state):
    if state == "up":
        state_num = 1
    else:
        state_num = 0
    id = request.GET.get("id") #get获取id
    referer = request.META.get("HTTP_REFERER") #返回当前请求的来源地址
    if id:
        goods = Goods.objects.filter(id = id).first() #获取指定id的商品
        if state == "delete":
            goods.delete()
        else:
            goods.goods_under = state_num #修改状态
            goods.save() #保存
    return HttpResponseRedirect(referer) #跳转到请求来源页

def order_list(request):
    store_id = request.COOKIES.get("has_store")
    order_list = OrderDetail.objects.filter(order_id__order_status=2,goods_store=store_id)
    return render(request,"store/order_list.html",locals())


def logout(request):
    response = HttpResponseRedirect("/Store/login/")
    for key in request.COOKIES:#获取当前所有cookie
        response.delete_cookie(key)
    return response

from rest_framework import viewsets,mixins

from Store.serializers import *
from django_filters.rest_framework import DjangoFilterBackend #导入过滤器

#当前部分还是为了自习接口的查询逻辑
class UserViewSet(viewsets.ModelViewSet):
    """
    查询所有的商品，并且实现了分页
    """
    queryset = Goods.objects.all() #具体返回的数据
    serializer_class = UserSerializer #指定过滤的类
    #filter_class = GoodsFilter
    filter_backends = [DjangoFilterBackend] #采用哪个过滤器
    filterset_fields = ['goods_name',"goods_price"] #进行查询的字段

class TypeViewSet(viewsets.ModelViewSet):
    """
    返回具体查询的内容
    """
    queryset = GoodsType.objects.all()
    serializer_class = GoodsTypeSerializer

def ajax_goods_list(request):
    return render(request,"store/ajax_goods_list.html")

from django.core.mail import send_mail
def sendMail(request):
    send_mail("邮件主题","邮件内容","from_email",["to_email"],fail_silently=False)

from CeleryTask.tasks import add
from django.http import JsonResponse,HttpResponse

def get_add(request):
    add.delay(2,3)
    return JsonResponse({"statue":200})

# def small_white_views(request):
#     print("我是小白视图")
#     raise TypeError("我就不想好好的")
#     return HttpResponse("我是小白视图")

def small_white_views(request):
    # print("我是小白视图")

    rep = HttpResponse("I am rep")
    rep.render = lambda : HttpResponse("hello world")
    return rep

# def small_white_views(request):
#     # print("我是小白视图")
#     def hello():
#         return HttpResponse("hello world")
#     rep = HttpResponse("I am rep")
#     rep.render = hello
#     return rep

# def small_white_views(request):
#     print("我是小白视图")
#     def render():
#         print("hello world")
#         return HttpResponse("98k")
#     rep = HttpResponse("od")
#     rep.render = render
#     return rep
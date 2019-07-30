import time

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect

from Buyer.models import *
from Store.views import set_password
from Store.models import *

from alipay import AliPay

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
    """
    前台首页
    """
    result_list = [] #定义一个容器用来存放结果
    goods_type_list = GoodsType.objects.all() #查询所有的类型
    for goods_type in goods_type_list: #循环类型
        goods_list = goods_type.goods_set.values()[:4] #查询前4条
        if goods_list: #如果类型对应的值
            goodsType = {
                "id": goods_type.id,
                "name": goods_type.name,
                "description": goods_type.description,
                "picture": goods_type.picture,
                "goods_list": goods_list
            } #构建输出结果
             #查询类型当中有数据的数据
            result_list.append(goodsType) #有数据的类型放入result_list
    return render(request,"buyer/index.html",locals())

@loginValid
def goods_list(request):
    """
    前台列表页
    :param reuqest:
    :return:
    """
    goodsList = []
    type_id = request.GET.get("type_id")
    #获取类型
    goods_type = GoodsType.objects.filter(id = type_id).first()
    if goods_type:
        #查询所有上架的产品
        goodsList = goods_type.goods_set.filter(goods_under=1)

    return render(request,"buyer/goods_list.html",locals())


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

def goods_detail(request):
    goods_id = request.GET.get("goods_id")
    if goods_id:
        goods = Goods.objects.filter(id = goods_id).first()
        if goods:
            return render(request,"buyer/detail.html",locals())
    return HttpResponse("没有您指定的商品")

def setOrderId(user_id,goods_id,store_id):
    """
    设置订单编号
    时间+用户id+商品的id+商铺+id
    """
    strtime = time.strftime("%Y%m%d%H%M%S",time.localtime())
    return strtime+user_id+goods_id+store_id

def place_order(request):
    if request.method == "POST":
        #post数据
        count = int(request.POST.get("count"))
        goods_id = request.POST.get("goods_id")
        #cookie的数据
        user_id = request.COOKIES.get("user_id")
        #数据库的数据
        goods = Goods.objects.get(id = goods_id)
        store_id = goods.store_id.id
        price = goods.goods_price

        order = Order()
        order.order_id = setOrderId(str(user_id),str(goods_id),str(store_id))
        order.goods_count = count
        order.order_user = Buyer.objects.get(id = user_id)
        order.order_price = count*price
        order.order_status = 1
        order.save()

        order_detail = OrderDetail()
        order_detail.order_id = order
        order_detail.goods_id = goods_id
        order_detail.goods_name = goods.goods_name
        order_detail.goods_price = goods.goods_price
        order_detail.goods_number = count
        order_detail.goods_total = count*goods.goods_price
        order_detail.goods_store = store_id
        order_detail.goods_image = goods.goods_image
        order_detail.save()

        detail = [order_detail]

        return render(request,"buyer/place_order.html",locals())
    else:
        return HttpResponse("非法请求")

def pay_result(request):
    """
    支付宝支付成功自动用get请求返回的参数
    #编码
    charset=utf-8
    #订单号
    out_trade_no=10002
    #订单类型
    method=alipay.trade.page.pay.return
    #订单金额
    total_amount=1000.00
    #校验值
    sign=enBOqQsaL641Ssf%2FcIpVMycJTiDaKdE8bx8tH6shBDagaNxNfKvv5iD737ElbRICu1Ox9OuwjR5J92k0x8Xr3mSFYVJG1DiQk3DBOlzIbRG1jpVbAEavrgePBJ2UfQuIlyvAY1fu%2FmdKnCaPtqJLsCFQOWGbPcPRuez4FW0lavIN3UEoNGhL%2BHsBGH5mGFBY7DYllS2kOO5FQvE3XjkD26z1pzWoeZIbz6ZgLtyjz3HRszo%2BQFQmHMX%2BM4EWmyfQD1ZFtZVdDEXhT%2Fy63OZN0%2FoZtYHIpSUF2W0FUi7qDrzfM3y%2B%2BpunFIlNvl49eVjwsiqKF51GJBhMWVXPymjM%2Fg%3D%3D&trade_no=2019072622001422161000050134&auth_app_id=2016093000628355&version=1.0&app_id=2016093000628355
    #订单号
    trade_no=2019072622001422161000050134
    #用户的应用id
    auth_app_id=2016093000628355
    #版本
    version=1.0
    #商家的应用id
    app_id=2016093000628355
    #加密方式
    sign_type=RSA2
    #商家id
    seller_id=2088102177891440
    #时间
    timestamp=2019-07-26
    """

    return render(request,"buyer/pay_result.html",locals())

def pay_order(request):

    money = request.GET.get("money") #获取订单金额
    order_id = request.GET.get("order_id") #获取订单id
    alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6M7zHSmJhDrrfKt7eYapbbGhdth72wcws74vLQamlzIpCuLLTaJFUkva0fVlwAwl0l9DZotLSORKxxIORhzslOxtwGnQ+staKJUEe2AhLVu/v5jRTIuVPVFm7qgWXD/H3vNF9kL9jFCl1REvgc207xe0r1rk41cQFAodWmJEp+0pcKq6UzAi8ZNhnjbSQjOE1WbMDIb+lgXQdDlk/Bp5w2W7wNJ6oAISejruKAOvCSnbk1WRUYUDPXxbJakhqBoozrni8R5LKEQ/MJAs9ztCi3h3RKdAhaOqgaTwrR52fCqolaCl0JTUZu0YNIqUdeo3MbnqC95HIK82N0h6oL9mWwIDAQAB
    -----END PUBLIC KEY-----"""

    app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
    MIIEpgIBAAKCAQEA6M7zHSmJhDrrfKt7eYapbbGhdth72wcws74vLQamlzIpCuLLTaJFUkva0fVlwAwl0l9DZotLSORKxxIORhzslOxtwGnQ+staKJUEe2AhLVu/v5jRTIuVPVFm7qgWXD/H3vNF9kL9jFCl1REvgc207xe0r1rk41cQFAodWmJEp+0pcKq6UzAi8ZNhnjbSQjOE1WbMDIb+lgXQdDlk/Bp5w2W7wNJ6oAISejruKAOvCSnbk1WRUYUDPXxbJakhqBoozrni8R5LKEQ/MJAs9ztCi3h3RKdAhaOqgaTwrR52fCqolaCl0JTUZu0YNIqUdeo3MbnqC95HIK82N0h6oL9mWwIDAQABAoIBAQCoKOO+SsSD+LMkKBFWJIi5LTc9yv0bpkPtcRBOa6FlUNwIeuzytKVx3ky+n4zRfXTMUfczWKYWjp/czxP0XOweXfCgrU4/+Sa0bX8BRtxwEPeeA1oa+i/gTK4W8N7F32QVjI8aZCUUdyRxlKpGDjoFAZCHoRX3iGmar/unz5db2zfYx1XvelzP8B10XCBg9E8Efid587ud6g+FfaC+YbSfH9I6bE3cGcGF4Vr3/iDK7StvjaPJflGl/zZKkjakrhglJWa5k4yqfgwjqxnOT6FR1r4kMm59p62D2MsmAdn6WXRk3iEGLfXOhTRA8TuzKD/KX9NhqRWkVSoLMGGU6MqBAoGBAPwkt00FvmvL+M0F84Dl5qcdTg6jYbB8T/Jp1+rJHDA/4jboZwxd9NuChiks+IWhQASUYp8aedjaJShm+xgwzOZGbNrD3gk3asQMqfdReRiW8/dnOGi2r3Q5vyR7yFxLITLsBjh44CYPxJNmoX01mx84Wwpg3/t01K4pFGL+aVahAoGBAOxehq5CDbMnexPDycP1lBwyp8TGlocO+5xkDzi94IQ9Pam3Gp/CiPXx3F9ZBvuKg3SGTamBPVsOvs0yNjv119Px0pjuPIkenkhUN7s56rQhXBSvj1dDAceSkYlxoY28bHa4gS781i1/6CkNhW4kvVsgUgwlOzxb9qlStWyFSGd7AoGBAKyA3htG87lCSkzSZn7oSv5IMVAYfUxGMFgUC9Gol61292hDZcTzPwMy8GCZUMnzwR2g+zwI3BX9YPCcS+uH75cX1X9yA6VgkZ3hYCNBTU0CcZTwvIn/elhU7a2jNjfWercg/TyDji7cGMwTqiZEl4UrhDW8g2DA1IT2u+jiT+UhAoGBAOuIUdpo9a/VIp6SVYaQOvNSQr0hSjPw6SZwyn43Lvd28vAgBka2GbZCON9GHmAfKVi+z7qdjx8idVyRsVtUYanP6ZP8qZPVT9IxIYvObaLrLw9p1YMVwTs2QRHdiidrYAV5WzkQNvgF4biuwYv8zjd04G072GgQF52oTiKCOaDrAoGBANg3xbUhpWAKqSLRTnTKzxikBZdfpHPgC7S9fAHumYBp4m252nJCQORh/TA/E0GVSxE+tqih98EGvbWqck+yhYTaxqcO2pRmrnFT0xizHKfjJsmMkuzxKY6FOL3SrZv2Kj0KhSuW0KmkpCSF5Yw2dbHvuHCh56c2ttPhVQUDV5eO
    -----END RSA PRIVATE KEY-----"""

    # 实例化支付应用
    alipay = AliPay(
        appid="2016093000628355",
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2"
    )

    # 发起支付请求
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,  # 订单号
        total_amount=str(money),  # 支付金额
        subject="生鲜交易",  # 交易主题
        return_url="http://127.0.0.1:8000/Buyer/pay_result/",
        notify_url="http://127.0.0.1:8000/Buyer/pay_result/"
    )

    order = Order.objects.get(order_id = order_id)
    order.order_status = 2
    order.save()

    return HttpResponseRedirect("https://openapi.alipaydev.com/gateway.do?" + order_string)

def add_cart(request):
    result = {"state": "error","data":""}
    if request.method == "POST":
        count = int(request.POST.get("count"))
        goods_id = request.POST.get("goods_id")
        goods = Goods.objects.get(id = int(goods_id))

        user_id = request.COOKIES.get("user_id")

        cart = Cart()
        cart.goods_name = goods.goods_name
        cart.goods_price = goods.goods_price
        cart.goods_total = goods.goods_price*count
        cart.goods_number = count
        cart.goods_picture = goods.goods_image
        cart.goods_id = goods.id
        cart.goods_store = goods.store_id.id
        cart.user_id = user_id
        cart.save()
        result["state"] = "success"
        result["data"] = "商品添加成功"
    else:
        result["data"] = "请求错误"
    return JsonResponse(result)

def cart(request):
    user_id = request.COOKIES.get("user_id")
    goods_list = Cart.objects.filter(user_id = user_id)
    return render(request,"buyer/cart.html",locals())


# Create your views here.









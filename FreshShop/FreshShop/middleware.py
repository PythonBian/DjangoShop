#coding:utf-8
from django.utils.deprecation import MiddlewareMixin #中间件的元类，所有自定义的中间件都是基于当前类进行重写的
from django.http import HttpResponse
import os
import datetime
from FreshShop.settings import BASE_DIR

class MiddlewareTest(MiddlewareMixin):
    def process_response(self,request,response):
        """
        :param request:
        :param response:
        """
        response.set_cookie("hhh","111")
        return response

# class MiddlewareTest(MiddlewareMixin):
#     def process_template_response(self,request,response):
#         print("I am response")
#         return response

# class MiddlewareTest(MiddlewareMixin):
#     def process_exception(self,request,exception):
#         """
#         """
#         now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         level = "Error"
#         content = str(exception)
#         log_result = "%s [%s] %s \n"%(now,level,content)
#         file_path = os.path.join(BASE_DIR,"error.log")
#         with open(file_path,"a") as f:
#             f.write(log_result)
#         print(exception)


# class MiddlewareTest(MiddlewareMixin):
#     def process_view(self,request,view_func,view_args,view_kwargs):
#         """
#         """
#         print(view_func.__name__)

# class MiddlewareTest(MiddlewareMixin):
#     def process_request(self,request):
#         """
#         :param request: 视图没有处理的请求
#         """
#         username = request.GET.get("username")
#         if username and username=="lb":
#             return HttpResponse("404")


# class MiddlewareTest1(MiddlewareMixin):
#     def process_request(self,request):
#         """
#         :param request: 视图没有处理的请求
#         """
#         print("这是process_request1")
#
#     def process_response(self,request,response):
#         """
#         request 视图没有处理的请求
#         view_func 视图函数
#         view_args 视图函数的参数，元组格式
#         view_kwargs 视图函数的参数，字典格式
#         """
#         print("这是process_response1")
#         return response
#
# class MiddlewareTest2(MiddlewareMixin):
#     def process_request(self,request):
#         """
#         :param request: 视图没有处理的请求
#         """
#         print("这是process_request2")
#
#     def process_response(self,request,response):
#         """
#         request 视图没有处理的请求
#         view_func 视图函数
#         view_args 视图函数的参数，元组格式
#         view_kwargs 视图函数的参数，字典格式
#         """
#         print("这是process_response2")
#         return response


# class MiddlewareTest(MiddlewareMixin):
#     def process_request(self,request):
#         """
#         :param request: 视图没有处理的请求
#         """
#         print("这是process_request")
#
#     def process_view(self,request,view_func,view_args,view_kwargs):
#         """
#         request 视图没有处理的请求
#         view_func 视图函数
#         view_args 视图函数的参数，元组格式
#         view_kwargs 视图函数的参数，字典格式
#         """
#         print("这是process_view")
#     def process_exception(self,request,exception):
#         """
#         :param request: 视图处理中的请求
#         :param exception: 错误
#         """
#         print("这是process_exception")
#     def process_template_response(self,request,response):
#         """
#         :param request: 视图处理完成的请求
#         :param response: 视图处理完成的响应
#         """
#         print("这是process_template_response")
#         return response
#
#     def process_response(self,request,response):
#         """
#         :param request: 视图处理完成的请求
#         :param response: 视图处理完成的响应
#         """
#         print("这是process_response")
#         return response

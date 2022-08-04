from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

"""
前端：
    拼接一个url，然后给发起请求
    
后端：
    1. 接收UUID
    2. 生成图片验证码和图片二进制，通过redis把图片验证码保存起来
    3. 返回图片二进制
    
    路由：
        采用get方式
"""


# Create your views here.
class ImageCodeView(View):
    """获取验证码图片，保存UUID"""

    def get(self, request, uuid):
        # 导入captcha包
        from libs.captcha.captcha import captcha
        text, image = captcha.generate_captcha()

        # 通过redis把图片验证码保存起来
        from django_redis import get_redis_connection
        # 1. 建立redis链接
        redis_cli = get_redis_connection("code")
        # 2. 执行redis语句
        redis_cli.setex(uuid, 300, text)
        # 用HttpResponse返回图片二进制
        # content_type 的语法是  ： 大类/小类
        return HttpResponse(content=image,content_type="image/png")

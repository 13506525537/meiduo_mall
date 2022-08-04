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
        request.session['uuid'] = uuid
        request.session.set_expiry(300)




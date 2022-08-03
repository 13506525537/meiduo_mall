import json
import re

from django.views import View
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from apps.users.models import User

# Create your views here.
"""
需求分析： 根据页面，从上到下，从左到右，分析哪些功能需要和后端配合完成
    依赖：
        1. 经验
        2. 关注类似网站
登录页面接口：
    1. 校验用户名
    2. 校验手机号
    3. 给到验证码图片
    4. 发送短信
    5. 提交注册
数据库字段设计：
    1. id
    2. username
    3. password
    4. phone
    5. email
    6. email_state
    7. is_delete

"""


class UsernameCount(View):
    """检测用户名是否重复
         如果数据库查询结果数等于0，说明没注册，
         如果大于1说明有注册
         url : usernames/<username>/count
         响应：JSON  {code:0/1, count:0/1, msg:ok)
     """

    def get(self, request, username):
        # 1. 接受用户名并判断,可以放到转化器里
        # if not re.match("[a-zA-Z0-9_-]{5,20}", username):
        #     response = {
        #         'code': 200,
        #         'msg': '用户名不符合要求'
        #     }
        #     return JsonResponse(response)
        count = User.objects.filter(username=username).count()
        if count == 0:
            response = {
                'code': 0,
                'count': count,
                'msg': 'ok'
            }
            return JsonResponse(response)
        else:
            response = {
                'code': 1,
                'count': count,
                'msg': '用户已存在'
            }
            return JsonResponse(response)

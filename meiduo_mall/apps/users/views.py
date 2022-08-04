import json
import random
import re

from django.views import View
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from apps.users.models import User
from django_redis import get_redis_connection
from utils.SendMessage import send_message

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


class MobilesCheck(View):
    """
        校验手机号是否重复

    """
    pass


class UserRegister(View):
    """
    1. 接受请求
    2. 验证数据
        1. 用户名，密码，确认密码，手机号，是否统一协议 都要有
        2. 用户名满足限制，且不能重复
        3. 密码满足规则
        4. 确认密码和密码一致
        5. 手机号满足规则且手机号不能重复
        6. 需要同意协议
    3，数据入库
    4. 响应  JSON{code:0, msg:"ok"}
    5. 路由 POST register/

    """

    def post(self, request):
        # 1.获取到的是二进制，需要解码，并转成json格式
        bodystr = request.body.decode()
        body = json.loads(bodystr)

        # 2.获取各个值
        username = body.get('username')
        password = body.get('password')
        password2 = body.get('password2')
        mobile = body.get('mobile')
        allow = body.get('allow')

        # all([XXX,XXX])
        # all里的元素只要是None或False，all就返回False
        if not all([username, password, password2, mobile, allow]):
            response = {
                'code': 400,
                'msg': '参数不全'
            }
            return JsonResponse(response)

        # 校验用户名
        if not re.match('[a-zA-Z0-9_-]{5,20}', username):
            response = {
                'code': 400,
                'msg': '传入用户名不符合规则'
            }
            return JsonResponse(response)
        # 校验密码
        if len(password) < 8 or len(password) > 20:
            response = {
                'code': 400,
                'msg': '传入密码不符合规则'
            }
            return JsonResponse(response)

        if password != password2:
            response = {
                'code': 400,
                'msg': '两次密码不一致'
            }
            return JsonResponse(response)

        if not re.match('^1[345789]\d{9}$', mobile):
            response = {
                'code': 400,
                'msg': '您输入的手机号不正确'
            }
            return JsonResponse(response)

        if not allow:
            response = {
                'code': 400,
                'msg': '您输入的手机号不正确'
            }
            return JsonResponse(response)

        # 校验用户名重复
        count = User.objects.filter(username=username).count()
        if count > 0:
            response = {
                'code': 1,
                'msg': '用户名重复'
            }
            return JsonResponse(response)

        count = User.objects.filter(mobile=mobile).count()
        if count > 0:
            response = {
                'code': 1,
                'msg': '手机号重复'
            }
            return JsonResponse(response)
        # 方法一 密码未加密
        # user = User(username=username, password=password, mobile=mobile)
        # user.save()

        # 方法二
        user = User.objects.create_user(username=username, password=password, mobile=mobile)
        # 设置session
        # response.session['username']=username

        # django自带的方法
        from django.contrib.auth import login

        login(request, user)  # login函数会自动是设置session

        response = {
            'code': 0,
            'msg': 'ok'
        }
        return JsonResponse(response)


"""
1. 注册成功即表示已经登录，实现保持
2. 注册成功后不表示登录，用户单独登录
实现保持的方式：
    1. 设置cookie 
    2. 设置session
"""

"""
发送短信逻辑分析
前端：
    url = this.host + '/sms_codes/' + this.mobile + '/' + '?image_code=' + this.image_code + '&image_code_id=' + this.image_code_id
    方式 get 两个参数： image_code, image_code_id
后端:
    1. 获取手机号
    2. 校验image_code 和 image_code_id
    3. 发送短信 (目前使用云联容)
    4. 返回验证码内容给前端
    

"""


class SendMessageView(View):
    """发送短信类"""

    def get(self, request, mobile):
        # 获取参数中的值
        req = request.GET
        image_code = req.get('image_code')
        image_code_id = req.get('image_code_id')

        # 链接redis
        res_cli = get_redis_connection('code')
        # 查询UUID的缓存
        result = res_cli.get(image_code_id)
        if result:
            result = result.decode()
        # 校验验证码
        # print(image_code,image_code_id,result)
        if image_code.lower() != result.lower():
            response = {
                'code': 1,
                'msg': '图片验证码错误'
            }
            return JsonResponse(response)
        # 用random产生一个四位随机数
        seeds = '1234567890'
        mobile_code = []
        for i in range(4):
            num = random.choice(seeds)
            mobile_code.append(num)
        mobile_code = "".join(mobile_code)

        resp = send_message(1, mobile, (mobile_code, 3))
        print(mobile_code,resp)
        return HttpResponse(resp)


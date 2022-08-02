from django.shortcuts import render

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
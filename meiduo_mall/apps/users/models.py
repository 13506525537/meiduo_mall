from django.db import models

# Create your models here.
"""
定义用户表
数据库字段设计：
    1. id
    2. username
    3. password
    4. phone
    5. email
    6. email_state
    7. is_delete
"""

# 1. 自定义模型
# class User(models.Model):
#     username = models.CharField(max_length=32, unique=True)
#     password = models.CharField(max_length=20)
#     phone = models.CharField(max_length=11, unique=True)
#     email = models.CharField(max_length=32, null=True)
#     email_state = models.BooleanField(default=False) # False 是未校验  Ture是校验
#     is_delete = models.BooleanField(default=False)  # False 是未删除 True 是删除
#
#     class Meta:
#         db_table = 'user'
#         verbose_name = 'user'

# 2. 使用django自带的用户模型
# 这个用户模型有密码加密和密码验证
from django.contrib.auth.models import AbstractUser

# 用户组和用户权限只能关联一个用户表，
# 我们自己定义了一个用户表，系统还有一个用户表，这个时候就会出现问题
# 解决方案： 让我们的模型替换系统的User就可以
# 继承系统模型，重写phone
class User(AbstractUser):
    phone = models.CharField(max_length=11, unique=True)

    class Meta:
        db_table = 'tb_user'
        verbose_name = 'tb_user'

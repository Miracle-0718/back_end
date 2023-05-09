from django.db import models

# Create your models here.
class User(models.Model):
    '''
    用户表
    '''
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)


class RecImg(models.Model):
    '''
    存放未识别的图片
    '''
    id = models.AutoField(primary_key=True)
    image = models.ImageField('未识别',upload_to="unRecImg",null=True) # 使用ImageField upload_to必不可少
    text = models.CharField(max_length=200)
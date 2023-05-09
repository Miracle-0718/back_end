from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from guwen.model import RecImg,User

import json
import time
# my function
from rec.rec import img_detect,img_rec,convet_fan2jian
from trans.trans1 import text_trans

def test(request):
    if request.method == "GET":
        return HttpResponse('hhh')

@api_view(['POST'])
def upload_img(request):
    if request.method == 'POST':
        # print(request.FILES)
        name = request.data['name'] # 提取文件的key
        img = request.FILES[name] # 提取文件本身
        rec = RecImg() #创建对象
        rec.image.save(name,img) # 将文件存储到数据库中  格式：model.column.save(name,file)
        id = rec.id #获取id
        if RecImg.objects.filter(id=id)[0].image is not None:
            return HttpResponse('success')
        return HttpResponse('fail')

@api_view(['POST'])
def rec_img(request):
    if request.method == 'POST':
        img_name = request.data['name']
        t1 = time.time()
        text, score = img_rec(img_name)
        t2 = time.time()
        rec = RecImg.objects.get(image='unRecImg/'+img_name)  # 先查询
        rec.text = text  # 在内存中修改
        rec.save()  # 将修改保存到数据库
        res={}
        res['time'] = (t2 - t1)*1000
        res['text'] = text
        res['score'] = score
        json_str = json.dumps(res, ensure_ascii=False)
        return HttpResponse(json_str)

@api_view(['POST'])
def convert_zh(request):
    if request.method == 'POST':
        text = request.data['text']
        return HttpResponse(convet_fan2jian(text))

@api_view(['POST'])
def trans_text(request):
    if request.method == 'POST':
        text = request.data['text']
        results = text_trans(text)
        res = {}
        res['results'] = results
        json_str = json.dumps(res, ensure_ascii=False)
        return HttpResponse(json_str)

@api_view(['POST'])
def signIn(request):
    response={}
    try:
        input_name =request.data['name'].replace('\"','') #对请求里的数据先消除转义符号
        input_psw = request.data['password'].replace('\"','')
        result = list(User.objects.filter(username=input_name,password=input_psw).values())
        if result == []:
            response['user'] = ''
            response['msg'] = 'fail'
        else:
            response['user'] = result[0]
            response['msg'] = 'success'
    except  Exception as e:
        response['msg'] = str(e)
    return JsonResponse(response,json_dumps_params={'ensure_ascii': False}) #另一种返回JSON数据的方法

@api_view(['POST'])
def signUp(request):
    response={}
    name = request.data['name']
    password = request.data['password']
    phone = request.data['phone']
    res = {}
    try:
        if 'email' in request.data:
            email = request.data['email']
            u = User.objects.create(username=name, password=password, phone=phone,email=email)
        else:
            u = User.objects.create(username=name, password=password, phone=phone)
        u.save()
        res['msg'] = 'success'
    except  Exception as e:
        res['msg'] = str(e)
    return JsonResponse(res,json_dumps_params={'ensure_ascii': False}) #另一种返回JSON数据的方法

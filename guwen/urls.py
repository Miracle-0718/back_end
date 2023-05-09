from django.urls import path
from guwen import views

urlpatterns = [
    path('test/', views.test),
    path('uploadImg/', views.upload_img),
    path('recImg/', views.rec_img),
    path('convertText/', views.convert_zh),
    path('transText/', views.trans_text),
    path('signIn/', views.signIn),
    path('signUp/', views.signUp),
]
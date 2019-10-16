from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    # 登录
    path('login/', views.user_login, name='login'),
    # 登出
    path('logout', views.user_logout, name='logout'),
]
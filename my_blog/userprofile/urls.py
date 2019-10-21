from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    # 登录
    path('login/', views.user_login, name='login'),
    # 登出
    path('logout', views.user_logout, name='logout'),
    # 注册
    path('register/', views.user_register, name="register"),
    # 删除用户
    path('delete/<int:id>', views.user_delete, name='delete'),
    # 编辑用户
    path('edit/<int:id>/', views.profile_edit, name="edit"),
]
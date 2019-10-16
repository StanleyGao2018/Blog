from django import forms
from django.contrib.auth.models import User

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

# 用户注册表单
class UserRegisterForm(forms.ModelForm):
    # 复写密码
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            
    
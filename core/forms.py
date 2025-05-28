from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'zen-form-control',
            'placeholder': '请输入您的邮箱地址'
        })
    )
    
    birth_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'class': 'zen-form-control',
            'type': 'datetime-local'
        }),
        label='出生时间'
    )
    
    birth_place = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'zen-form-control',
            'placeholder': '请输入出生地点'
        }),
        label='出生地点'
    )    
    gender = forms.ChoiceField(
        required=False,
        choices=[('', '请选择'), ('male', '男'), ('female', '女')],
        widget=forms.Select(attrs={
            'class': 'zen-form-control'
        }),
        label='性别'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'zen-form-control',
            'placeholder': '请输入用户名（4-20个字符）'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'zen-form-control',
            'placeholder': '请输入密码（至少8个字符）'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'zen-form-control',
            'placeholder': '请再次输入密码'
        })
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # 创建用户档案
            UserProfile.objects.create(
                user=user,
                birth_date=self.cleaned_data.get('birth_date'),
                birth_place=self.cleaned_data.get('birth_place'),
                gender=self.cleaned_data.get('gender')
            )
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['birth_date', 'birth_place', 'gender']
        widgets = {
            'birth_date': forms.DateTimeInput(attrs={
                'class': 'zen-form-control',
                'type': 'datetime-local'
            }),
            'birth_place': forms.TextInput(attrs={
                'class': 'zen-form-control',
                'placeholder': '请输入出生地点'
            }),
            'gender': forms.Select(attrs={
                'class': 'zen-form-control'
            })
        }
        labels = {
            'birth_date': '出生时间',
            'birth_place': '出生地点',
            'gender': '性别'
        }

#!/usr/bin/env python3
"""
测试验证码流程
"""

import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fatemaster.settings')
sys.path.append('/Users/Zhuanz/Documents/LX-Ai')
django.setup()

from core.models import SMSVerification
from core.sms import generate_verification_code
import json

def test_verification_flow():
    """测试验证码完整流程"""
    print("=== 验证码流程测试 ===")
    
    # 测试手机号
    test_phone = "13800138000"
    
    print(f"1. 测试手机号: {test_phone}")
    
    # 生成验证码
    code = generate_verification_code()
    print(f"2. 生成的验证码: {code}")
    
    # 保存到数据库
    verification = SMSVerification.objects.create(
        phone_number=test_phone,
        code=code
    )
    print(f"3. 保存到数据库，ID: {verification.id}")
    
    # 查询验证码记录
    records = SMSVerification.objects.filter(phone_number=test_phone)
    print(f"4. 该手机号的验证码记录数: {records.count()}")
    
    # 获取最新的验证码
    latest = records.order_by('-created_at').first()
    if latest:
        print(f"5. 最新验证码: {latest.code}, 创建时间: {latest.created_at}")
        print(f"6. 是否已使用: {latest.is_used}")
        print(f"7. 是否有效: {latest.is_valid()}")
        print(f"8. 过期时间: {latest.expire_at}")
    
    # 测试验证过程
    from core.forms import CustomUserCreationForm
    
    print("\n=== 表单验证测试 ===")
    
    form_data = {
        'username': 'testuser123',
        'phone_number': test_phone,
        'verification_code': code,
        'password1': 'testpass123456',
        'password2': 'testpass123456'
    }
    
    form = CustomUserCreationForm(data=form_data)
    print(f"表单是否有效: {form.is_valid()}")
    
    if not form.is_valid():
        print("表单错误:")
        for field, errors in form.errors.items():
            print(f"  {field}: {errors}")
    
    print("\n=== 数据库状态 ===")
    all_records = SMSVerification.objects.all().order_by('-created_at')[:5]
    for record in all_records:
        print(f"手机号: {record.phone_number}, 验证码: {record.code}, 时间: {record.created_at}")
    
if __name__ == "__main__":
    test_verification_flow()

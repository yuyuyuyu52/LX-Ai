#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试登录用户的AI模式
创建一个测试用户并模拟登录状态来测试AI功能
"""

import requests
import json
import time

def create_test_user_and_login():
    """创建测试用户并获取登录会话"""
    print("🔑 创建测试用户并登录...")
    
    # 获取CSRF token
    session = requests.Session()
    csrf_url = "http://127.0.0.1:8001/login/"  # 修正登录URL
    
    try:
        # 获取登录页面和CSRF token
        response = session.get(csrf_url)
        if response.status_code != 200:
            print(f"❌ 无法访问登录页面: {response.status_code}")
            return None
            
        # 从cookie中获取CSRF token
        csrf_token = session.cookies.get('csrftoken')
        if not csrf_token:
            print("❌ 无法获取CSRF token")
            return None
        
        print(f"✅ 获取CSRF token: {csrf_token[:10]}...")
        
        # 创建测试用户（如果还不存在）
        from django.contrib.auth.models import User
        from core.models import UserProfile
        import os
        import django
        
        # 设置Django环境
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fatemaster.settings')
        django.setup()
        
        # 创建或获取测试用户
        username = 'ai_test_user'
        password = 'test123456'
        email = 'aitest@example.com'
        
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': 'AI测试',
                'last_name': '用户'
            }
        )
        
        if created:
            user.set_password(password)
            user.save()
            print(f"✅ 创建新用户: {username}")
        else:
            print(f"✅ 使用现有用户: {username}")
        
        # 创建或更新用户档案为VIP
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'is_vip': True,
                'ai_usage_count': 0,
                'daily_usage_count': 0
            }
        )
        
        if not profile.is_vip:
            profile.is_vip = True
            profile.save()
            print("✅ 设置用户为VIP")
        
        # 登录
        login_data = {
            'username': username,
            'password': password,
            'csrfmiddlewaretoken': csrf_token
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': csrf_url,
            'X-CSRFToken': csrf_token
        }
        
        login_response = session.post(csrf_url, data=login_data, headers=headers)
        
        if login_response.status_code == 200 or login_response.status_code == 302:
            print("✅ 用户登录成功")
            return session, csrf_token
        else:
            print(f"❌ 登录失败: {login_response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ 创建用户和登录过程失败: {str(e)}")
        return None

def test_ai_with_logged_in_user():
    """测试登录用户的AI模式"""
    print("🤖 测试登录用户的AI增强分析")
    print("=" * 80)
    
    # 创建用户并登录
    auth_result = create_test_user_and_login()
    if not auth_result:
        print("❌ 无法获取登录会话，跳过AI测试")
        return
    
    session, csrf_token = auth_result
    
    # 测试AI模式
    url = "http://127.0.0.1:8001/divination/api/bazi/"
    
    test_data = {
        "birth_time": "1990-01-01 子时",
        "gender": "男",
        "birth_place": "北京",
        "ai_mode": True
    }
    
    headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf_token,
        'Referer': 'http://127.0.0.1:8001/divination/bazi/'
    }
    
    print(f"📡 发送AI增强请求（已登录用户）...")
    print(f"🎯 AI模式: 启用")
    print(f"👤 用户: ai_test_user (VIP)")
    print("-" * 40)
    
    try:
        start_time = time.time()
        response = session.post(url, json=test_data, headers=headers, timeout=120)
        end_time = time.time()
        
        print(f"⏱️  请求耗时: {end_time - start_time:.2f}秒")
        print(f"📊 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 请求成功")
            print("-" * 40)
            
            print("📋 响应数据分析:")
            print(f"  - 成功状态: {data.get('success', False)}")
            print(f"  - AI增强: {data.get('ai_enhanced', False)}")
            print(f"  - 分析长度: {len(data.get('analysis', ''))}字符")
            
            if data.get('ai_enhanced', False):
                print("🎉 AI模式成功激活！")
                analysis = data.get('analysis', '')
                print(f"📝 AI增强分析长度: {len(analysis)}字符")
                print(f"📄 分析内容预览:")
                print("-" * 20)
                print(analysis[:500] + "..." if len(analysis) > 500 else analysis)
                print("-" * 20)
                print("✅ AI服务正常工作！")
            else:
                print("⚠️  AI模式未激活（即使用户已登录）")
                print("   - 可能原因: VIP权限、AI服务异常等")
                
        else:
            print(f"❌ 请求失败: HTTP {response.status_code}")
            try:
                error_data = response.json()
                print(f"错误详情: {error_data}")
            except:
                print(f"错误内容: {response.text}")
    
    except requests.exceptions.Timeout:
        print("⏰ 请求超时（可能AI正在处理中）")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    print("=" * 80)

if __name__ == "__main__":
    print("🚀 开始登录用户AI模式测试")
    print("注意：将创建测试用户并设置为VIP来测试AI功能")
    print()
    
    test_ai_with_logged_in_user()
    
    print("✅ 测试完成")
    print()
    print("📋 如果看到AI增强分析内容和AI服务调试输出，说明AI功能正常工作")

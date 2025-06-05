#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的AI测试脚本 - 直接通过Django创建用户和会话
"""

import os
import sys
import django
import requests
import json
import time
from datetime import datetime

def setup_django():
    """设置Django环境"""
    # 添加项目路径
    sys.path.insert(0, '/Users/Zhuanz/Documents/LX-Ai')
    
    # 设置Django设置模块
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fatemaster.settings')
    
    # 初始化Django
    django.setup()

def create_test_user():
    """创建测试用户"""
    from django.contrib.auth.models import User
    from core.models import UserProfile
    
    print("🔑 创建测试用户...")
    
    # 用户信息
    username = 'ai_test_user'
    password = 'test123456'
    email = 'aitest@example.com'
    
    try:
        # 删除现有用户（如果存在）
        try:
            existing_user = User.objects.get(username=username)
            existing_user.delete()
            print(f"🗑️  删除现有用户: {username}")
        except User.DoesNotExist:
            pass
        
        # 创建新用户
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name='AI测试',
            last_name='用户'
        )
        
        # 创建用户档案并设置为VIP
        profile = UserProfile.objects.create(
            user=user,
            membership='vip',  # 使用正确的字段名
            ai_usage_count=0
        )
        
        print(f"✅ 创建测试用户成功: {username}")
        print(f"🎯 VIP状态: {profile.is_vip()}")
        print(f"🤖 可使用AI: {profile.can_use_ai()}")
        
        return user
        
    except Exception as e:
        print(f"❌ 创建用户失败: {str(e)}")
        return None

def simulate_login(username, password):
    """模拟用户登录并获取会话"""
    print("🔐 模拟用户登录...")
    
    session = requests.Session()
    
    try:
        # 获取登录页面和CSRF token
        login_url = "http://127.0.0.1:8001/login/"
        response = session.get(login_url)
        
        if response.status_code != 200:
            print(f"❌ 无法访问登录页面: {response.status_code}")
            return None
        
        # 获取CSRF token
        csrf_token = session.cookies.get('csrftoken')
        if not csrf_token:
            print("❌ 无法获取CSRF token")
            return None
        
        print(f"✅ 获取CSRF token: {csrf_token[:10]}...")
        
        # 提交登录表单
        login_data = {
            'username': username,
            'password': password,
            'csrfmiddlewaretoken': csrf_token
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': login_url,
            'X-CSRFToken': csrf_token
        }
        
        login_response = session.post(login_url, data=login_data, headers=headers)
        
        # 检查登录是否成功（通常会重定向）
        if login_response.status_code in [200, 302]:
            print("✅ 登录成功")
            
            # 验证登录状态 - 访问需要登录的页面
            profile_url = "http://127.0.0.1:8001/profile/"
            profile_response = session.get(profile_url)
            
            if profile_response.status_code == 200 and 'ai_test_user' in profile_response.text:
                print("✅ 登录验证成功")
                return session, csrf_token
            else:
                print(f"⚠️  登录验证失败: {profile_response.status_code}")
                return session, csrf_token  # 仍然尝试使用会话
        else:
            print(f"❌ 登录失败: {login_response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ 登录过程失败: {str(e)}")
        return None

def test_ai_with_logged_user():
    """测试已登录用户的AI功能"""
    print("\n🤖 测试AI增强分析（已登录用户）")
    print("=" * 80)
    
    # 设置Django环境
    setup_django()
    
    # 创建测试用户
    user = create_test_user()
    if not user:
        print("❌ 无法创建测试用户，停止测试")
        return
    
    # 模拟登录
    session_data = simulate_login('ai_test_user', 'test123456')
    if not session_data:
        print("❌ 无法获得登录会话，停止测试")
        return
    
    session, csrf_token = session_data
    
    # 测试AI分析
    print("\n🔬 开始AI分析测试...")
    print("-" * 40)
    
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
    
    print(f"📡 发送AI增强请求...")
    print(f"👤 用户: ai_test_user (VIP)")
    print(f"🎯 AI模式: 启用")
    
    try:
        start_time = time.time()
        print("⏰ 开始请求...")
        
        response = session.post(url, json=test_data, headers=headers, timeout=120)
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        print(f"⏱️  请求完成，耗时: {elapsed:.2f}秒")
        print(f"📊 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 请求成功")
            print("-" * 40)
            
            # 分析响应
            success = data.get('success', False)
            ai_enhanced = data.get('ai_enhanced', False)
            analysis = data.get('analysis', '')
            
            print("📋 响应分析:")
            print(f"  - 成功状态: {success}")
            print(f"  - AI增强: {ai_enhanced}")
            print(f"  - 分析长度: {len(analysis)}字符")
            
            if ai_enhanced and len(analysis) > 500:
                print("🎉 AI模式成功激活！")
                print(f"📝 AI增强分析预览:")
                print("-" * 20)
                preview = analysis[:400] + "..." if len(analysis) > 400 else analysis
                print(preview)
                print("-" * 20)
                print("✅ AI功能正常工作！")
                
                # 检查分析质量
                if "AI增强" in analysis or len(analysis) > 800:
                    print("🌟 分析质量: 高质量AI增强分析")
                else:
                    print("⚠️  分析质量: 可能是基础分析")
                    
            elif ai_enhanced:
                print("⚠️  AI模式激活但内容较短，可能存在问题")
                print(f"📄 分析内容: {analysis[:200]}...")
            else:
                print("❌ AI模式未激活")
                print("   - 可能原因: 用户权限、AI服务故障等")
                
        else:
            print(f"❌ 请求失败: HTTP {response.status_code}")
            try:
                error_data = response.json()
                print(f"错误详情: {error_data}")
            except:
                print(f"错误内容: {response.text[:200]}...")
    
    except requests.exceptions.Timeout:
        print("⏰ 请求超时（AI处理时间较长）")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    print("=" * 80)

if __name__ == "__main__":
    print("🚀 AI功能完整测试")
    print("📝 此测试将创建VIP用户并完整测试AI增强分析功能")
    print()
    
    test_ai_with_logged_user()
    
    print("\n✅ 测试完成")
    print("\n📋 检查要点:")
    print("1. 查看Django控制台是否有AI调试输出")
    print("2. 确认AI增强分析的内容长度和质量")
    print("3. 验证提示词是否正确发送到DeepSeek-R1")

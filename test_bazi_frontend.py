#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
八字分析前端问题测试
模拟前端请求，测试整个流程
"""

import os
import sys
import time
import django

# 添加项目路径到Python路径
sys.path.append('/Users/Zhuanz/Documents/LX-Ai')

# 设置Django设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fatemaster.settings')

# 初始化Django
django.setup()

import json
from datetime import datetime
from django.test import Client
from django.contrib.auth.models import User
from core.models import UserProfile

def test_bazi_page_access():
    """测试八字分析页面访问"""
    print("=" * 60)
    print("测试八字分析页面访问")
    print("=" * 60)
    
    client = Client()
    
    try:
        response = client.get('/divination/bazi/')
        print(f"页面访问状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ 八字分析页面访问正常")
            # 检查页面是否包含关键元素
            content = response.content.decode('utf-8')
            if 'baziForm' in content:
                print("✓ 页面包含八字表单")
            if 'ai_mode' in content.lower():
                print("✓ 页面包含AI模式选项")
        else:
            print(f"✗ 页面访问失败: {response.status_code}")
            
    except Exception as e:
        print(f"✗ 页面访问异常: {e}")

def test_guest_bazi_analysis():
    """测试游客八字分析"""
    print("\n" + "=" * 60)
    print("测试游客八字分析（普通模式）")
    print("=" * 60)
    
    client = Client()
    
    # 模拟前端发送的数据格式
    test_data = {
        'birth_time': '1990-01-01 子时',
        'gender': 'male',
        'birth_place': '北京',
        'ai_mode': False
    }
    
    print(f"请求数据: {test_data}")
    
    try:
        start_time = time.time()
        
        response = client.post(
            '/divination/api/bazi/',
            data=json.dumps(test_data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'  # 模拟AJAX请求
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"响应时间: {response_time:.2f}秒")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                
                if result.get('success'):
                    print("✓ 游客八字分析成功")
                    print(f"  - 八字结果: {result.get('bazi')}")
                    print(f"  - 分析文本长度: {len(result.get('analysis', ''))}字符")
                    print(f"  - AI增强: {result.get('ai_enhanced', False)}")
                    print(f"  - 详细信息: {result.get('detail_info')}")
                    
                    # 检查分析内容质量
                    analysis = result.get('analysis', '')
                    if '八字排盘' in analysis:
                        print("✓ 包含八字排盘信息")
                    if '五行统计' in analysis:
                        print("✓ 包含五行统计")
                    if '性格特点' in analysis:
                        print("✓ 包含性格分析")
                else:
                    print(f"✗ API返回失败: {result.get('error')}")
                    
            except json.JSONDecodeError as e:
                print(f"✗ 响应JSON解析失败: {e}")
                print(f"原始响应: {response.content[:500]}")
        else:
            print(f"✗ HTTP请求失败: {response.status_code}")
            print(f"错误内容: {response.content}")
            
    except Exception as e:
        print(f"✗ 测试异常: {e}")
        import traceback
        traceback.print_exc()

def test_registered_user_bazi():
    """测试注册用户八字分析"""
    print("\n" + "=" * 60)
    print("测试注册用户八字分析")
    print("=" * 60)
    
    # 创建普通用户（非VIP）
    try:
        user = User.objects.create_user(
            username='testuser_normal',
            email='normal@test.com',
            password='testpass123'
        )
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.membership = 'free'  # 确保是免费用户
        profile.save()
        print(f"✓ 创建普通用户: {user.username}")
    except Exception as e:
        print(f"✗ 创建用户失败: {e}")
        return
    
    client = Client()
    login_success = client.login(username='testuser_normal', password='testpass123')
    
    if not login_success:
        print("✗ 用户登录失败")
        user.delete()
        return
    
    print("✓ 用户登录成功")
    
    # 测试普通模式
    test_data = {
        'birth_time': '1985-05-15 午时',
        'gender': 'female',
        'birth_place': '上海',
        'ai_mode': False
    }
    
    try:
        print("\n测试普通用户的普通模式...")
        response = client.post(
            '/divination/api/bazi/',
            data=json.dumps(test_data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✓ 普通用户普通模式成功")
                print(f"  - 会保存记录: {result.get('ai_enhanced', False)}")
            else:
                print(f"✗ 普通模式失败: {result.get('error')}")
        
        # 测试AI模式（应该被拒绝）
        print("\n测试普通用户的AI模式（应该被拒绝）...")
        test_data['ai_mode'] = True
        
        response = client.post(
            '/divination/api/bazi/',
            data=json.dumps(test_data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        if response.status_code == 200:
            result = response.json()
            if not result.get('success'):
                print(f"✓ AI模式正确被拒绝: {result.get('error')}")
            else:
                print("⚠️  AI模式应该被拒绝但却成功了")
                
    except Exception as e:
        print(f"✗ 测试异常: {e}")
    
    # 清理
    try:
        user.delete()
        print("✓ 清理普通用户")
    except Exception as e:
        print(f"⚠️  清理用户失败: {e}")

def test_vip_user_ai_mode():
    """测试VIP用户AI模式"""
    print("\n" + "=" * 60)
    print("测试VIP用户AI增强模式")
    print("=" * 60)
    
    # 创建VIP用户
    try:
        user = User.objects.create_user(
            username='testuser_vip',
            email='vip@test.com',
            password='testpass123'
        )
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.membership = 'vip'
        profile.save()
        print(f"✓ 创建VIP用户: {user.username}")
    except Exception as e:
        print(f"✗ 创建VIP用户失败: {e}")
        return
    
    client = Client()
    login_success = client.login(username='testuser_vip', password='testpass123')
    
    if not login_success:
        print("✗ VIP用户登录失败")
        user.delete()
        return
    
    print("✓ VIP用户登录成功")
    
    # 测试AI增强模式
    test_data = {
        'birth_time': '1992-08-20 辰时',
        'gender': 'male',
        'birth_place': '广州',
        'ai_mode': True
    }
    
    try:
        print("\n测试VIP用户AI增强模式...")
        start_time = time.time()
        
        response = client.post(
            '/divination/api/bazi/',
            data=json.dumps(test_data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"AI模式响应时间: {response_time:.2f}秒")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✓ VIP用户AI模式成功")
                print(f"  - AI增强标识: {result.get('ai_enhanced')}")
                
                analysis = result.get('analysis', '')
                if len(analysis) > 500:  # AI增强的分析应该更详细
                    print("✓ AI增强分析内容丰富")
                else:
                    print("⚠️  AI增强分析可能不够详细")
                    
                # 检查是否有AI增强特征
                if 'AI增强' in analysis or '深度分析' in analysis:
                    print("✓ 包含AI增强特征")
                else:
                    print("⚠️  可能未启用AI增强")
                    
            else:
                print(f"✗ VIP AI模式失败: {result.get('error')}")
        else:
            print(f"✗ VIP AI模式HTTP错误: {response.status_code}")
                
    except Exception as e:
        print(f"✗ VIP AI模式测试异常: {e}")
        import traceback
        traceback.print_exc()
    
    # 清理
    try:
        user.delete()
        print("✓ 清理VIP用户")
    except Exception as e:
        print(f"⚠️  清理VIP用户失败: {e}")

def test_edge_cases():
    """测试边界情况"""
    print("\n" + "=" * 60)
    print("测试边界情况和错误处理")
    print("=" * 60)
    
    client = Client()
    
    # 测试空数据
    print("1. 测试空数据请求...")
    try:
        response = client.post(
            '/divination/api/bazi/',
            data=json.dumps({}),
            content_type='application/json'
        )
        if response.status_code == 200:
            result = response.json()
            if not result.get('success'):
                print(f"✓ 空数据正确拒绝: {result.get('error')}")
            else:
                print("⚠️  空数据应该被拒绝")
    except Exception as e:
        print(f"✗ 空数据测试异常: {e}")
    
    # 测试无效时间格式
    print("\n2. 测试无效时间格式...")
    invalid_data = {
        'birth_time': '无效时间',
        'gender': 'male',
        'birth_place': '北京',
        'ai_mode': False
    }
    
    try:
        response = client.post(
            '/divination/api/bazi/',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        if response.status_code == 200:
            result = response.json()
            if not result.get('success'):
                print(f"✓ 无效时间格式正确拒绝: {result.get('error')}")
            else:
                print("⚠️  无效时间格式应该被拒绝")
    except Exception as e:
        print(f"✗ 无效时间测试异常: {e}")
    
    # 测试未来时间
    print("\n3. 测试未来时间...")
    future_data = {
        'birth_time': '2030-01-01 子时',
        'gender': 'female',
        'birth_place': '北京',
        'ai_mode': False
    }
    
    try:
        response = client.post(
            '/divination/api/bazi/',
            data=json.dumps(future_data),
            content_type='application/json'
        )
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("⚠️  未来时间应该被前端验证拒绝（后端未限制）")
            else:
                print(f"✓ 未来时间被拒绝: {result.get('error')}")
    except Exception as e:
        print(f"✗ 未来时间测试异常: {e}")

if __name__ == "__main__":
    print("八字分析前端问题全面测试")
    print("=" * 60)
    
    # 1. 页面访问测试
    test_bazi_page_access()
    
    # 2. 游客分析测试
    test_guest_bazi_analysis()
    
    # 3. 注册用户测试
    test_registered_user_bazi()
    
    # 4. VIP用户AI模式测试  
    test_vip_user_ai_mode()
    
    # 5. 边界情况测试
    test_edge_cases()
    
    print("\n" + "=" * 60)
    print("前端测试完成")
    print("=" * 60)
    print("\n如果普通模式正常但AI模式有问题，主要检查：")
    print("1. AI服务配置和API密钥")
    print("2. 网络连接和超时设置")
    print("3. 会员权限验证逻辑")
    print("4. 前端JavaScript的错误处理")

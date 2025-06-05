#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
八字分析页面问题诊断
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

def test_bazi_api_basic():
    """测试八字API基本功能"""
    print("=" * 50)
    print("八字API基本功能测试")
    print("=" * 50)
    
    client = Client()
    
    # 准备测试数据
    test_data = {
        'birth_time': '1990-01-01 子时',
        'gender': 'male',
        'birth_place': '北京',
        'ai_mode': False
    }
    
    print(f"测试数据: {test_data}")
    
    try:
        # 测试普通模式
        print("\n1. 测试普通模式...")
        response = client.post(
            '/divination/api/bazi/',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"响应内容: {result}")
                
                if result.get('success'):
                    print("✓ 普通模式测试成功")
                    print(f"✓ 八字结果: {result.get('bazi')}")
                    print(f"✓ 分析长度: {len(result.get('analysis', ''))}字符")
                else:
                    print(f"✗ API返回错误: {result.get('error')}")
            except json.JSONDecodeError:
                print(f"✗ 响应不是有效JSON: {response.content}")
        else:
            print(f"✗ HTTP错误: {response.status_code}")
            print(f"响应内容: {response.content}")
            
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()

def test_bazi_api_with_user():
    """测试登录用户的八字API"""
    print("\n" + "=" * 50)
    print("登录用户八字API测试")
    print("=" * 50)
    
    # 创建测试用户
    try:
        user = User.objects.create_user(
            username='testuser_bazi',
            email='test@example.com',
            password='testpass123'
        )
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.is_vip = True
        profile.save()
        print(f"✓ 创建测试用户: {user.username}")
    except Exception as e:
        print(f"✗ 创建用户失败: {e}")
        return
    
    client = Client()
    client.login(username='testuser_bazi', password='testpass123')
    
    # 测试AI模式
    test_data = {
        'birth_time': '1990-01-01 子时',
        'gender': 'male',
        'birth_place': '北京',
        'ai_mode': True
    }
    
    print(f"测试数据: {test_data}")
    
    try:
        print("\n2. 测试AI增强模式...")
        start_time = time.time()
        
        response = client.post(
            '/divination/api/bazi/',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"响应时间: {response_time:.2f}秒")
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                if result.get('success'):
                    print("✓ AI增强模式测试成功")
                    print(f"✓ AI增强标识: {result.get('ai_enhanced')}")
                    print(f"✓ 分析长度: {len(result.get('analysis', ''))}字符")
                    print(f"✓ 分析预览: {result.get('analysis', '')[:200]}...")
                else:
                    print(f"✗ API返回错误: {result.get('error')}")
            except json.JSONDecodeError:
                print(f"✗ 响应不是有效JSON: {response.content}")
        else:
            print(f"✗ HTTP错误: {response.status_code}")
            print(f"响应内容: {response.content}")
    
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 清理测试数据
    try:
        user.delete()
        print("✓ 清理测试用户")
    except Exception as e:
        print(f"⚠️  清理用户失败: {e}")

def test_bazi_calculator():
    """测试八字计算器"""
    print("\n" + "=" * 50)
    print("八字计算器测试")
    print("=" * 50)
    
    try:
        from core.bazi_calculator import bazi_calculator
        from divination.views import parse_chinese_time
        
        # 测试时间解析
        test_time = "1990-01-01 子时"
        print(f"测试时间解析: {test_time}")
        
        parsed_time = parse_chinese_time(test_time)
        print(f"✓ 解析结果: {parsed_time}")
        
        # 测试八字计算
        print("\n测试八字计算...")
        bazi_result = bazi_calculator.calculate_bazi(parsed_time, '男')
        
        print(f"✓ 八字计算成功")
        print(f"✓ 八字结果: {bazi_result['bazi_string']}")
        print(f"✓ 生肖: {bazi_result['shengxiao']}")
        print(f"✓ 五行统计: {bazi_result['wuxing_count']}")
        
    except Exception as e:
        print(f"✗ 八字计算器测试失败: {e}")
        import traceback
        traceback.print_exc()

def test_middleware_and_decorators():
    """测试中间件和装饰器"""
    print("\n" + "=" * 50)
    print("中间件和装饰器测试")
    print("=" * 50)
    
    try:
        from core.decorators import check_usage_limit, membership_info
        print("✓ 装饰器导入成功")
        
        # 测试视图函数
        from divination.views import bazi_api
        print("✓ 视图函数导入成功")
        
        # 测试中间件
        from core.middleware import MembershipMiddleware
        print("✓ 中间件导入成功")
        
    except Exception as e:
        print(f"✗ 中间件/装饰器测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("八字分析页面问题诊断")
    print("=" * 50)
    
    # 基本API测试
    test_bazi_api_basic()
    
    # 用户API测试
    test_bazi_api_with_user()
    
    # 八字计算器测试
    test_bazi_calculator()
    
    # 中间件测试
    test_middleware_and_decorators()
    
    print("\n" + "=" * 50)
    print("诊断完成")
    print("=" * 50)

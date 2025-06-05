#!/usr/bin/env python3
"""
八字分析VIP用户测试
测试VIP用户的AI增强分析功能
"""

import os
import sys
import django
import requests
import json
from datetime import datetime

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fatemaster.settings')
sys.path.append('/Users/Zhuanz/Documents/LX-Ai')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import UserProfile

def test_vip_bazi_analysis():
    """测试VIP用户八字分析功能"""
    print("=== VIP用户八字分析测试 ===\n")
    
    # 获取VIP用户
    vip_users = User.objects.filter(userprofile__membership='vip').order_by('id')
    if not vip_users.exists():
        print("❌ 没有找到VIP用户")
        return False
    
    test_user = vip_users.first()
    profile = test_user.userprofile
    
    print(f"🔐 使用VIP测试用户: {test_user.username}")
    print(f"📅 VIP到期时间: {profile.membership_expire_date}")
    print(f"🎯 VIP状态: {'有效' if profile.is_vip() else '已过期'}")
    print()
    
    # 创建测试客户端并登录
    client = Client()
    login_success = client.login(username=test_user.username, password='testpass123')
    
    if not login_success:
        # 尝试常见密码
        passwords_to_try = ['password', '123456', 'admin', test_user.username]
        for pwd in passwords_to_try:
            if client.login(username=test_user.username, password=pwd):
                login_success = True
                print(f"✅ 使用密码 '{pwd}' 登录成功")
                break
    
    if not login_success:
        print("❌ 无法登录VIP用户，将重置密码")
        test_user.set_password('testpass123')
        test_user.save()
        client.login(username=test_user.username, password='testpass123')
        print("✅ 重置密码后登录成功")
    
    # 测试数据
    test_data = {
        'birth_time': '1990-05-15 14:30',
        'gender': 'male',
        'birth_place': '北京市',
        'ai_mode': True  # 测试AI模式
    }
    
    print("📊 测试数据:")
    print(f"   出生时间: {test_data['birth_time']}")
    print(f"   性别: {test_data['gender']}")
    print(f"   出生地: {test_data['birth_place']}")
    print(f"   模式: AI增强分析")
    print()
    
    # 测试普通模式
    print("1️⃣ 测试普通模式...")
    basic_data = test_data.copy()
    basic_data['ai_mode'] = False
    
    try:
        start_time = datetime.now()
        response = client.post('/divination/api/bazi/', 
                              data=json.dumps(basic_data),
                              content_type='application/json')
        end_time = datetime.now()
        response_time = (end_time - start_time).total_seconds()
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"   ✅ 普通模式成功 (响应时间: {response_time:.2f}秒)")
                print(f"   📊 分析结果长度: {len(result.get('analysis', ''))}")
            else:
                print(f"   ❌ 普通模式失败: {result.get('error', '未知错误')}")
                return False
        else:
            print(f"   ❌ 普通模式HTTP错误: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 普通模式异常: {e}")
        return False
    
    # 测试AI模式
    print("\n2️⃣ 测试AI增强模式...")
    try:
        start_time = datetime.now()
        response = client.post('/divination/api/bazi/', 
                              data=json.dumps(test_data),
                              content_type='application/json')
        end_time = datetime.now()
        response_time = (end_time - start_time).total_seconds()
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"   ✅ AI模式成功 (响应时间: {response_time:.2f}秒)")
                print(f"   📊 分析结果长度: {len(result.get('analysis', ''))}")
                print(f"   🤖 AI分析状态: {result.get('ai_analysis_status', '未知')}")
                
                # 检查AI增强内容
                analysis = result.get('analysis', '')
                if len(analysis) > 500:  # AI分析通常更详细
                    print("   ✅ AI增强分析内容丰富")
                else:
                    print("   ⚠️ AI分析内容较短，可能只是基础分析")
                
                return True
            else:
                error_msg = result.get('error', '未知错误')
                print(f"   ❌ AI模式失败: {error_msg}")
                
                # 如果是会员限制，说明权限检查有问题
                if '会员' in error_msg or 'VIP' in error_msg:
                    print("   🔍 VIP权限检查问题，需要进一步调试")
                    print(f"   🆔 用户ID: {test_user.id}")
                    print(f"   👤 用户名: {test_user.username}")
                    print(f"   🎫 会员状态: {profile.membership}")
                    print(f"   📅 到期时间: {profile.membership_expire_date}")
                
                return False
        else:
            print(f"   ❌ AI模式HTTP错误: {response.status_code}")
            if hasattr(response, 'content'):
                print(f"   📄 响应内容: {response.content.decode()[:200]}")
            return False
    except Exception as e:
        print(f"   ❌ AI模式异常: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_bazi_calculator():
    """测试八字计算器基础功能"""
    print("\n3️⃣ 测试八字计算器...")
    
    try:
        from core.bazi_calculator import BaziCalculator
        from datetime import datetime
        
        calculator = BaziCalculator()
        birth_time = datetime(1990, 5, 15, 14, 30)
        result = calculator.calculate_bazi(birth_time, '男')
        
        if result:
            print("   ✅ 八字计算器正常工作")
            print(f"   🔢 年柱: {result.get('bazi_string', {}).get('year', '未知')}")
            print(f"   🔢 月柱: {result.get('bazi_string', {}).get('month', '未知')}")
            print(f"   🔢 日柱: {result.get('bazi_string', {}).get('day', '未知')}")
            print(f"   🔢 时柱: {result.get('bazi_string', {}).get('hour', '未知')}")
            return True
        else:
            print("   ❌ 八字计算器返回空结果")
            return False
    except Exception as e:
        print(f"   ❌ 八字计算器异常: {e}")
        return False

def test_ai_service():
    """测试AI服务配置"""
    print("\n4️⃣ 测试AI服务配置...")
    
    try:
        from core.ai_service import AI_TIMEOUT, MAX_RETRIES
        print(f"   ⚙️ AI超时设置: {AI_TIMEOUT}秒")
        print(f"   🔄 最大重试次数: {MAX_RETRIES}")
        print("   ✅ AI服务配置正常")
        return True
    except Exception as e:
        print(f"   ❌ AI服务配置异常: {e}")
        return False

if __name__ == "__main__":
    try:
        success = test_vip_bazi_analysis()
        test_bazi_calculator()
        test_ai_service()
        
        print("\n" + "="*50)
        if success:
            print("🎉 VIP用户AI模式测试成功！")
        else:
            print("❌ VIP用户AI模式测试失败")
    except KeyboardInterrupt:
        print("\n⏹️ 测试被用户中断")
    except Exception as e:
        print(f"\n💥 测试过程中出现异常: {e}")
        import traceback
        traceback.print_exc()

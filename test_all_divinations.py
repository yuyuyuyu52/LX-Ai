#!/usr/bin/env python3
"""
全面测试占卜功能
包括八字分析、梅花易数、每日运势等的AI和普通模式
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

def test_bazi_analysis():
    """测试八字分析功能"""
    print("1️⃣ 测试八字分析...")
    
    # 获取VIP用户
    vip_users = User.objects.filter(userprofile__membership='vip')
    if not vip_users.exists():
        print("   ❌ 没有VIP用户，跳过AI模式测试")
        return False
    
    test_user = vip_users.first()
    client = Client()
    client.force_login(test_user)
    
    # 测试数据
    test_data = {
        'birth_time': '1990-05-15 14:30',
        'gender': 'male',
        'birth_place': '北京市',
        'ai_mode': False  # 先测试普通模式
    }
    
    try:
        # 普通模式测试
        start_time = datetime.now()
        response = client.post('/divination/api/bazi/', 
                              data=json.dumps(test_data),
                              content_type='application/json')
        end_time = datetime.now()
        response_time = (end_time - start_time).total_seconds()
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"   ✅ 普通模式成功 (响应时间: {response_time:.2f}秒)")
                
                # 测试AI模式
                test_data['ai_mode'] = True
                start_time = datetime.now()
                response = client.post('/divination/api/bazi/', 
                                      data=json.dumps(test_data),
                                      content_type='application/json')
                end_time = datetime.now()
                ai_response_time = (end_time - start_time).total_seconds()
                
                if response.status_code == 200:
                    ai_result = response.json()
                    if ai_result.get('success'):
                        print(f"   ✅ AI模式成功 (响应时间: {ai_response_time:.2f}秒)")
                        print(f"   📊 分析长度对比: 普通{len(result.get('analysis', ''))} vs AI{len(ai_result.get('analysis', ''))}")
                        return True
                    else:
                        print(f"   ❌ AI模式失败: {ai_result.get('error', '未知错误')}")
                        return False
                else:
                    print(f"   ❌ AI模式HTTP错误: {response.status_code}")
                    return False
            else:
                print(f"   ❌ 普通模式失败: {result.get('error', '未知错误')}")
                return False
        else:
            print(f"   ❌ 普通模式HTTP错误: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 测试异常: {e}")
        return False

def test_meihua_analysis():
    """测试梅花易数功能"""
    print("\n2️⃣ 测试梅花易数...")
    
    # 获取VIP用户
    vip_users = User.objects.filter(userprofile__membership='vip')
    if not vip_users.exists():
        print("   ❌ 没有VIP用户，跳过AI模式测试")
        return False
    
    test_user = vip_users.first()
    client = Client()
    client.force_login(test_user)
    
    # 测试数据
    test_data = {
        'question': '测试事业发展如何',
        'ai_mode': False  # 先测试普通模式
    }
    
    try:
        # 普通模式测试
        start_time = datetime.now()
        response = client.post('/divination/api/meihua/', 
                              data=json.dumps(test_data),
                              content_type='application/json')
        end_time = datetime.now()
        response_time = (end_time - start_time).total_seconds()
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"   ✅ 普通模式成功 (响应时间: {response_time:.2f}秒)")
                print(f"   🔮 主卦: {result.get('main_gua', {}).get('name', '未知')}")
                print(f"   🔄 变卦: {result.get('bian_gua', {}).get('name', '未知')}")
                
                # 测试AI模式
                test_data['ai_mode'] = True
                start_time = datetime.now()
                response = client.post('/divination/api/meihua/', 
                                      data=json.dumps(test_data),
                                      content_type='application/json')
                end_time = datetime.now()
                ai_response_time = (end_time - start_time).total_seconds()
                
                if response.status_code == 200:
                    ai_result = response.json()
                    if ai_result.get('success'):
                        print(f"   ✅ AI模式成功 (响应时间: {ai_response_time:.2f}秒)")
                        print(f"   📊 分析长度对比: 普通{len(result.get('analysis', ''))} vs AI{len(ai_result.get('analysis', ''))}")
                        return True
                    else:
                        print(f"   ❌ AI模式失败: {ai_result.get('error', '未知错误')}")
                        return False
                else:
                    print(f"   ❌ AI模式HTTP错误: {response.status_code}")
                    return False
            else:
                print(f"   ❌ 普通模式失败: {result.get('error', '未知错误')}")
                return False
        else:
            print(f"   ❌ 普通模式HTTP错误: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 测试异常: {e}")
        return False

def test_daily_fortune():
    """测试每日运势功能"""
    print("\n3️⃣ 测试每日运势...")
    
    # 获取VIP用户
    vip_users = User.objects.filter(userprofile__membership='vip')
    if not vip_users.exists():
        print("   ❌ 没有VIP用户，跳过AI模式测试")
        return False
    
    test_user = vip_users.first()
    client = Client()
    client.force_login(test_user)
    
    # 测试数据
    test_data = {
        'zodiac': '龙',
        'date': '2025-06-05',
        'ai_mode': False  # 先测试普通模式
    }
    
    try:
        # 普通模式测试
        start_time = datetime.now()
        response = client.post('/divination/api/daily-fortune/', 
                              data=json.dumps(test_data),
                              content_type='application/json')
        end_time = datetime.now()
        response_time = (end_time - start_time).total_seconds()
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"   ✅ 普通模式成功 (响应时间: {response_time:.2f}秒)")
                print(f"   🌟 综合运势: {result.get('overall_score', '未知')}")
                
                # 测试AI模式
                test_data['ai_mode'] = True
                start_time = datetime.now()
                response = client.post('/divination/api/daily-fortune/', 
                                      data=json.dumps(test_data),
                                      content_type='application/json')
                end_time = datetime.now()
                ai_response_time = (end_time - start_time).total_seconds()
                
                if response.status_code == 200:
                    ai_result = response.json()
                    if ai_result.get('success'):
                        print(f"   ✅ AI模式成功 (响应时间: {ai_response_time:.2f}秒)")
                        print(f"   📊 分析长度对比: 普通{len(result.get('analysis', ''))} vs AI{len(ai_result.get('analysis', ''))}")
                        return True
                    else:
                        print(f"   ❌ AI模式失败: {ai_result.get('error', '未知错误')}")
                        return False
                else:
                    print(f"   ❌ AI模式HTTP错误: {response.status_code}")
                    return False
            else:
                print(f"   ❌ 普通模式失败: {result.get('error', '未知错误')}")
                return False
        else:
            print(f"   ❌ 普通模式HTTP错误: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 测试异常: {e}")
        return False

def test_ai_service_directly():
    """直接测试AI服务"""
    print("\n4️⃣ 直接测试AI服务...")
    
    try:
        from core.ai_service import AIService, AI_TIMEOUT, MAX_RETRIES, ARK_API_AVAILABLE
        
        print(f"   📋 AI配置:")
        print(f"      超时时间: {AI_TIMEOUT}秒")
        print(f"      重试次数: {MAX_RETRIES}")
        print(f"      API可用性: {ARK_API_AVAILABLE}")
        
        if not ARK_API_AVAILABLE:
            print("   ⚠️ ARK API不可用，AI功能受限")
            return False
        
        ai_service = AIService()
        
        # 测试简单的AI调用
        start_time = datetime.now()
        try:
            result = ai_service.enhance_bazi_analysis(
                {"year": "庚午", "month": "壬午", "day": "丙戌", "hour": "乙未"},
                "这是一个基础分析测试",
                {"birth_time": "1990-05-15 14:30", "gender": "男", "birth_place": "北京"}
            )
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds()
            
            print(f"   ✅ AI服务测试成功 (响应时间: {response_time:.2f}秒)")
            print(f"   📝 返回内容长度: {len(result)}字符")
            return True
        except Exception as e:
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds()
            print(f"   ❌ AI服务测试失败 (耗时: {response_time:.2f}秒)")
            print(f"   🔍 错误信息: {str(e)}")
            return False
    except Exception as e:
        print(f"   ❌ AI服务导入失败: {e}")
        return False

def test_system_overview():
    """系统概览测试"""
    print("\n5️⃣ 系统概览...")
    
    try:
        # 用户统计
        total_users = User.objects.count()
        vip_users = User.objects.filter(userprofile__membership='vip').count()
        print(f"   👥 总用户数: {total_users}")
        print(f"   💎 VIP用户数: {vip_users}")
        
        # 占卜记录统计
        from core.models import DivinationRecord
        total_records = DivinationRecord.objects.count()
        ai_records = DivinationRecord.objects.filter(ai_enhanced=True).count()
        print(f"   📊 总占卜记录: {total_records}")
        print(f"   🤖 AI增强记录: {ai_records}")
        
        return True
    except Exception as e:
        print(f"   ❌ 系统统计失败: {e}")
        return False

if __name__ == "__main__":
    print("=== 全面占卜功能测试 ===\n")
    
    results = {
        'bazi': test_bazi_analysis(),
        'meihua': test_meihua_analysis(), 
        'daily_fortune': test_daily_fortune(),
        'ai_service': test_ai_service_directly(),
        'system': test_system_overview()
    }
    
    print("\n" + "="*50)
    print("📋 测试结果汇总:")
    
    success_count = 0
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {test_name.ljust(15)}: {status}")
        if result:
            success_count += 1
    
    print(f"\n🎯 总体通过率: {success_count}/{len(results)} ({success_count/len(results)*100:.1f}%)")
    
    if success_count == len(results):
        print("🎉 所有测试通过！系统运行正常！")
    else:
        print("⚠️ 部分测试失败，需要进一步调试")

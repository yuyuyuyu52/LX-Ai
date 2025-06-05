#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细的AI调试测试脚本
测试AI模式的完整流程，包括权限检查和AI调用
"""

import requests
import json
import time

def test_ai_mode_detailed():
    """测试AI模式的详细流程"""
    print("🔍 开始详细的AI模式调试测试")
    print("=" * 80)
    
    # 测试参数
    url = "http://127.0.0.1:8001/divination/api/bazi/"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    # 测试数据
    test_data = {
        "birth_time": "1990-01-01 子时",
        "gender": "男",
        "birth_place": "北京",
        "ai_mode": True  # 启用AI模式
    }
    
    print(f"📡 发送请求到: {url}")
    print(f"📋 请求数据: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
    print(f"🎯 AI模式: {'启用' if test_data['ai_mode'] else '禁用'}")
    print("-" * 40)
    
    try:
        # 发送请求
        start_time = time.time()
        response = requests.post(url, json=test_data, headers=headers, timeout=120)
        end_time = time.time()
        
        print(f"⏱️  请求耗时: {end_time - start_time:.2f}秒")
        print(f"📊 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 请求成功")
            print("-" * 40)
            
            # 分析响应数据
            print("📋 响应数据分析:")
            print(f"  - 成功状态: {data.get('success', False)}")
            print(f"  - AI增强: {data.get('ai_enhanced', False)}")
            print(f"  - 分析长度: {len(data.get('analysis', ''))}")
            print(f"  - 八字数据: {data.get('bazi', {})}")
            
            # 检查AI增强状态
            if data.get('ai_enhanced', False):
                print("🤖 AI模式已激活")
                analysis = data.get('analysis', '')
                print(f"📝 分析内容长度: {len(analysis)}字符")
                print(f"📄 分析内容预览:")
                print("-" * 20)
                print(analysis[:300] + "..." if len(analysis) > 300 else analysis)
            else:
                print("⚠️  AI模式未激活")
                if data.get('success', False):
                    print("   - 可能原因: 用户权限不足或VIP状态异常")
                else:
                    print(f"   - 错误信息: {data.get('error', '未知错误')}")
            
            # 检查详细信息
            if 'detail_info' in data:
                detail = data['detail_info']
                print(f"📊 详细信息:")
                print(f"  - 生肖: {detail.get('shengxiao', '未知')}")
                print(f"  - 五行统计: {detail.get('wuxing_count', {})}")
                print(f"  - 格局: {detail.get('geju', '未知')}")
            
        else:
            print(f"❌ 请求失败: HTTP {response.status_code}")
            try:
                error_data = response.json()
                print(f"错误详情: {error_data}")
            except:
                print(f"错误内容: {response.text}")
    
    except requests.exceptions.Timeout:
        print("⏰ 请求超时")
    except requests.exceptions.ConnectionError:
        print("🔌 连接错误 - 请确保Django服务器正在运行")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    print("=" * 80)

def test_without_ai():
    """测试不使用AI模式"""
    print("🔍 测试普通模式（无AI）")
    print("=" * 80)
    
    url = "http://127.0.0.1:8001/divination/api/bazi/"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    test_data = {
        "birth_time": "1990-01-01 子时",
        "gender": "男",
        "birth_place": "北京",
        "ai_mode": False  # 禁用AI模式
    }
    
    try:
        response = requests.post(url, json=test_data, headers=headers, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 普通模式请求成功")
            print(f"📝 分析长度: {len(data.get('analysis', ''))}字符")
            print(f"🤖 AI增强: {data.get('ai_enhanced', False)}")
        else:
            print(f"❌ 普通模式请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 普通模式测试失败: {str(e)}")
    
    print("=" * 80)

if __name__ == "__main__":
    print("🚀 开始AI模式详细调试测试")
    print("注意：请确保Django开发服务器正在运行在 http://127.0.0.1:8001")
    print()
    
    # 先测试普通模式
    test_without_ai()
    
    # 再测试AI模式
    test_ai_mode_detailed()
    
    print("✅ 测试完成")
    print()
    print("📋 调试说明:")
    print("1. 如果AI模式未激活，请检查用户是否有VIP权限")
    print("2. 查看Django控制台是否有AI调试输出")
    print("3. 确认AI服务的调试打印是否出现")

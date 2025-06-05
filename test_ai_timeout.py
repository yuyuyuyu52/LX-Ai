#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI超时问题诊断测试
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

from core.ai_service import ai_service, ARK_API_AVAILABLE

def test_ai_service_basic():
    """测试AI服务基本功能"""
    print("=" * 50)
    print("AI服务基本诊断测试")
    print("=" * 50)
    
    print(f"1. Ark API可用性: {ARK_API_AVAILABLE}")
    print(f"2. AI服务API密钥: {ai_service.api_key[:10]}..." if ai_service.api_key else "未设置")
    print(f"3. AI模型: {ai_service.model}")
    print(f"4. 超时设置: {ai_service.__class__.__module__}.AI_TIMEOUT")
    
    # 检查模块导入
    try:
        from volcenginesdkarkruntime import Ark
        print("5. volcenginesdkarkruntime导入: ✓")
    except ImportError as e:
        print(f"5. volcenginesdkarkruntime导入: ✗ ({e})")
    
    print("\n" + "=" * 50)

def test_simple_ai_call():
    """测试简单AI调用"""
    print("测试简单AI调用")
    print("-" * 30)
    
    if not ARK_API_AVAILABLE:
        print("⚠️  Ark API不可用，跳过实际API测试")
        return
    
    try:
        start_time = time.time()
        prompt = "请简单回答：你好"
        
        print(f"发送请求: {prompt}")
        completion = ai_service._call_ai_api(prompt)
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"✓ 响应时间: {response_time:.2f}秒")
        print(f"✓ 响应内容: {completion.choices[0].message.content[:100]}...")
        
    except Exception as e:
        print(f"✗ API调用失败: {e}")
        
        # 详细错误信息
        import traceback
        print("\n详细错误信息:")
        traceback.print_exc()

def test_bazi_enhancement():
    """测试八字增强分析"""
    print("\n测试八字增强分析")
    print("-" * 30)
    
    try:
        # 模拟八字数据
        bazi_data = {
            'year': '甲子',
            'month': '丙寅', 
            'day': '戊辰',
            'hour': '庚申'
        }
        
        birth_info = {
            'birth_time': '1984年2月15日10时',
            'gender': '男',
            'birth_place': '北京'
        }
        
        basic_analysis = "五行缺火，土旺金弱。性格偏内向，适合稳定工作。"
        
        start_time = time.time()
        result = ai_service.enhance_bazi_analysis(bazi_data, basic_analysis, birth_info)
        end_time = time.time()
        
        print(f"✓ 八字分析完成，耗时: {end_time - start_time:.2f}秒")
        print(f"✓ 分析结果长度: {len(result)}字符")
        print(f"✓ 结果预览: {result[:200]}...")
        
    except Exception as e:
        print(f"✗ 八字分析失败: {e}")
        
        # 详细错误信息
        import traceback
        print("\n详细错误信息:")
        traceback.print_exc()

def test_daily_fortune_enhancement():
    """测试每日运势增强分析"""
    print("\n测试每日运势增强分析")
    print("-" * 30)
    
    try:
        from datetime import date
        
        basic_fortune = "今日运势平稳，适合处理日常事务。财运一般，感情和谐。"
        
        start_time = time.time()
        result = ai_service.enhance_daily_fortune(
            zodiac="龙",
            date="2024-01-15", 
            basic_fortune=basic_fortune,
            user_birth_date=date(1988, 3, 20)
        )
        end_time = time.time()
        
        print(f"✓ 运势分析完成，耗时: {end_time - start_time:.2f}秒")
        print(f"✓ 分析结果长度: {len(result)}字符")
        print(f"✓ 结果预览: {result[:200]}...")
        
    except Exception as e:
        print(f"✗ 运势分析失败: {e}")
        
        # 详细错误信息
        import traceback
        print("\n详细错误信息:")
        traceback.print_exc()

def test_network_connectivity():
    """测试网络连接"""
    print("\n测试网络连接")
    print("-" * 30)
    
    try:
        import requests
        
        # 测试基本网络连接
        response = requests.get("https://www.baidu.com", timeout=5)
        print(f"✓ 基本网络连接正常 (状态码: {response.status_code})")
        
        # 测试API端点连接（如果知道的话）
        # 这里可能需要添加实际的volcengine API端点测试
        
    except Exception as e:
        print(f"✗ 网络连接测试失败: {e}")

if __name__ == "__main__":
    print("FateMaster AI超时问题诊断")
    print("=" * 50)
    
    # 基本诊断
    test_ai_service_basic()
    
    # 网络连接测试
    test_network_connectivity()
    
    # AI调用测试
    test_simple_ai_call()
    
    # 功能模块测试
    test_bazi_enhancement()
    test_daily_fortune_enhancement()
    
    print("\n" + "=" * 50)
    print("诊断完成")
    print("=" * 50)
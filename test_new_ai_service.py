#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试新的AI服务配置
验证90秒超时和优化的chat函数集成效果
"""

import os
import sys
import django
from django.conf import settings
import time

# Django项目路径
PROJECT_ROOT = "/Users/Zhuanz/Documents/LX-Ai"
sys.path.insert(0, PROJECT_ROOT)
os.chdir(PROJECT_ROOT)

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fatemaster.settings')
django.setup()

# 导入测试模块
from core.ai_service import AIService

def test_ai_service():
    """测试AI服务各项功能"""
    print("=" * 60)
    print("测试新的AI服务配置")
    print("=" * 60)
    
    ai_service = AIService()
    
    # 测试八字分析
    print("\n1. 测试八字分析AI增强...")
    start_time = time.time()
    try:
        bazi_data = "甲子年 丙寅月 戊午日 庚申时"
        result = ai_service.get_bazi_analysis(bazi_data, "男", "财运")
        elapsed = time.time() - start_time
        print(f"✅ 八字分析成功 - 耗时: {elapsed:.2f}秒")
        print(f"   响应长度: {len(result)}字符")
        print(f"   前100字符: {result[:100]}...")
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ 八字分析失败 - 耗时: {elapsed:.2f}秒")
        print(f"   错误: {str(e)}")
    
    # 测试梅花易数
    print("\n2. 测试梅花易数AI增强...")
    start_time = time.time()
    try:
        result = ai_service.get_meihua_analysis("山地剥", "地山谦", 5, "测试问题")
        elapsed = time.time() - start_time
        print(f"✅ 梅花易数成功 - 耗时: {elapsed:.2f}秒")
        print(f"   响应长度: {len(result)}字符")
        print(f"   前100字符: {result[:100]}...")
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ 梅花易数失败 - 耗时: {elapsed:.2f}秒")
        print(f"   错误: {str(e)}")
    
    # 测试八字合婚
    print("\n3. 测试八字合婚AI增强...")
    start_time = time.time()
    try:
        male_data = "甲子年 丙寅月 戊午日 庚申时"
        female_data = "乙丑年 丁卯月 己未日 辛酉时"
        result = ai_service.get_marriage_analysis(male_data, female_data)
        elapsed = time.time() - start_time
        print(f"✅ 八字合婚成功 - 耗时: {elapsed:.2f}秒")
        print(f"   响应长度: {len(result)}字符")
        print(f"   前100字符: {result[:100]}...")
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ 八字合婚失败 - 耗时: {elapsed:.2f}秒")
        print(f"   错误: {str(e)}")
    
    # 测试每日运势
    print("\n4. 测试每日运势AI增强...")
    start_time = time.time()
    try:
        result = ai_service.get_daily_fortune("双鱼座", "2024-01-21")
        elapsed = time.time() - start_time
        print(f"✅ 每日运势成功 - 耗时: {elapsed:.2f}秒")
        print(f"   响应长度: {len(result)}字符")
        print(f"   前100字符: {result[:100]}...")
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ 每日运势失败 - 耗时: {elapsed:.2f}秒")
        print(f"   错误: {str(e)}")
    
    print("\n" + "=" * 60)
    print("AI服务测试完成")
    print("=" * 60)

if __name__ == "__main__":
    test_ai_service()

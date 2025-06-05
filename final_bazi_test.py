#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
八字分析按钮修复验证
"""

import os
import sys
import django

# 添加项目路径到Python路径
sys.path.append('/Users/Zhuanz/Documents/LX-Ai')

# 设置Django设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fatemaster.settings')

# 初始化Django
django.setup()

import json
import requests
from pprint import pprint

def test_bazi_api_directly():
    """直接测试八字API"""
    print("=" * 60)
    print("测试八字分析API")
    print("=" * 60)
    
    url = 'http://127.0.0.1:8000/divination/api/bazi/'
    
    # 注意：这里使用和前端完全一致的数据格式
    data = {
        'birth_time': '1990-01-01 子时',  # 使用与前端完全一致的格式
        'gender': 'male',
        'birth_place': '北京',
        'ai_mode': False
    }
    
    print(f"请求数据: {json.dumps(data, ensure_ascii=False)}")
    print(f"目标URL: {url}")
    
    try:
        response = requests.post(
            url,
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"成功: {result.get('success')}")
            
            if result.get('success'):
                print(f"八字结果: {result.get('bazi')}")
                print(f"分析长度: {len(result.get('analysis', ''))}")
                print(f"AI增强: {result.get('ai_enhanced')}")
            else:
                print(f"API错误: {result.get('error')}")
        else:
            print(f"HTTP错误: {response.status_code}")
            print(f"响应内容: {response.text[:200]}")
    except Exception as e:
        print(f"请求异常: {e}")

if __name__ == "__main__":
    test_bazi_api_directly()

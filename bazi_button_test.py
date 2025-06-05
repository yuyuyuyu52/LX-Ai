#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试八字按钮点击问题
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

from django.test import Client
import json

def test_bazi_button_api():
    """测试八字分析API调用"""
    print("=" * 60)
    print("测试八字分析API调用")
    print("=" * 60)
    
    client = Client()
    
    # 模拟前端发送的数据格式 - 完全按照前端JS中的数据格式
    test_data = {
        'birth_time': '1990-01-01 子时',  # 使用与前端完全一致的时间格式
        'gender': 'male',
        'birth_place': '北京',
        'ai_mode': False
    }
    
    print(f"发送数据: {json.dumps(test_data, ensure_ascii=False)}")
    print("目标URL: /divination/api/bazi/")
    
    try:
        response = client.post(
            '/divination/api/bazi/',
            data=json.dumps(test_data),
            content_type='application/json',
        )
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"成功: {result.get('success')}")
                
                if result.get('success'):
                    print("✓ API调用成功!")
                    print(f"八字结果: {result.get('bazi')}")
                    print(f"分析长度: {len(result.get('analysis', ''))}")
                    print(f"AI增强: {result.get('ai_enhanced')}")
                else:
                    print(f"✗ API报错: {result.get('error')}")
            except Exception as e:
                print(f"✗ 解析响应失败: {e}")
                print(f"原始响应: {response.content[:200]}...")
        else:
            print(f"✗ HTTP请求失败: {response.status_code}")
            print(f"响应内容: {response.content}")
        
    except Exception as e:
        print(f"✗ 请求异常: {e}")

if __name__ == "__main__":
    test_bazi_button_api()

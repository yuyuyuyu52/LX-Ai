#!/usr/bin/env python3
import os
import sys
import django

# 添加项目路径
sys.path.append('/Users/Zhuanz/Documents/LX-Ai')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fatemaster.settings')

# 初始化Django
django.setup()

from core.ai_service import ai_service

def test_ai_service():
    print("测试AI服务连接...")
    
    # 测试基本调用
    try:
        print("\n1. 测试基本AI调用...")
        test_prompt = "你好，请简单回复一下。"
        completion = ai_service._call_ai_api(test_prompt)
        result = completion.choices[0].message.content
        print(f"AI响应: {result[:100]}...")
        print("✅ 基本AI调用成功")
    except Exception as e:
        print(f"❌ 基本AI调用失败: {e}")
        return False
    
    # 测试八字分析增强
    try:
        print("\n2. 测试八字分析AI增强...")
        bazi_data = {
            'year': '甲子',
            'month': '乙丑', 
            'day': '丙寅',
            'hour': '丁卯'
        }
        basic_analysis = "这是一个基础的八字分析结果。"
        birth_info = {
            'birth_time': '1990-01-01 子时',
            'gender': 'male',
            'birth_place': '北京'
        }
        enhanced_result = ai_service.enhance_bazi_analysis(bazi_data, basic_analysis, birth_info)
        print(f"增强分析结果: {enhanced_result[:200]}...")
        print("✅ 八字分析AI增强成功")
    except Exception as e:
        print(f"❌ 八字分析AI增强失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_ai_service()
    if success:
        print("\n🎉 AI服务测试全部通过！")
    else:
        print("\n💥 AI服务测试失败！")

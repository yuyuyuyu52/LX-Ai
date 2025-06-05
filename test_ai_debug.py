#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试AI模式是否真正调用AI功能
观察控制台输出中的AI提示词调试信息
"""

import requests
import json
import time

def test_ai_mode_with_debug():
    """测试AI模式并观察提示词调试输出"""
    print("🔍 测试AI模式是否真正调用AI功能")
    print("="*60)
    
    # 测试数据
    test_data = {
        "birth_time": "1990-05-15 14:30",
        "gender": "男",
        "birth_place": "北京市",
        "ai_mode": True  # 启用AI模式
    }
    
    print(f"📋 测试数据:")
    print(f"   出生时间: {test_data['birth_time']}")
    print(f"   性别: {test_data['gender']}")
    print(f"   出生地: {test_data['birth_place']}")
    print(f"   AI模式: {test_data['ai_mode']}")
    print("-"*60)
    
    print("🚀 发送八字分析请求...")
    print("📺 请观察Django服务器控制台输出，应该会看到:")
    print("   🤖 AI模式激活 - 正在发送提示词给DeepSeek-R1")
    print("   📝 提示词内容（长度: XXX字符）")
    print("   ✅ AI调用成功! 响应长度: XXX字符")
    print("-"*60)
    
    start_time = time.time()
    
    try:
        response = requests.post(
            "http://127.0.0.1:8001/divination/api/bazi/",
            headers={
                "Content-Type": "application/json",
                "X-CSRFToken": "test"  # 简化的CSRF token
            },
            json=test_data,
            timeout=120  # 2分钟超时
        )
        
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                print(f"✅ 八字分析请求成功!")
                print(f"⏱️  总耗时: {elapsed_time:.2f}秒")
                print(f"🤖 AI增强模式: {result.get('ai_enhanced', False)}")
                
                analysis = result.get('analysis', '')
                print(f"📄 分析结果长度: {len(analysis)}字符")
                print(f"📋 分析内容预览:")
                print("-"*40)
                print(analysis[:300] + "..." if len(analysis) > 300 else analysis)
                print("-"*40)
                
                # 判断是否真正使用了AI
                if result.get('ai_enhanced') and len(analysis) > 1000:
                    print("🎉 AI模式正常工作!")
                    print("   - AI增强标记: ✅")
                    print("   - 内容详细程度: ✅")
                    print("   - 响应时间合理: ✅")
                elif result.get('ai_enhanced'):
                    print("⚠️  AI模式可能有问题:")
                    print("   - AI增强标记: ✅")
                    print("   - 内容详细程度: ❌ (内容过短)")
                else:
                    print("❌ AI模式未启用:")
                    print("   - AI增强标记: ❌")
                    print("   - 可能的原因: 权限不足或AI服务故障")
                    
            else:
                print(f"❌ 八字分析失败: {result.get('error')}")
                
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时 (120秒)")
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {str(e)}")
    except Exception as e:
        print(f"❌ 未知错误: {str(e)}")
    
    print("="*60)
    print("🔍 调试说明:")
    print("1. 如果看到AI提示词输出 → AI模式正常调用")
    print("2. 如果只有基础分析 → AI模式未启用或权限不足")
    print("3. 如果没有任何特殊输出 → 需要检查AI服务配置")

if __name__ == "__main__":
    test_ai_mode_with_debug()

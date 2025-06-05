#!/usr/bin/env python3
"""
测试八字分析API响应的脚本
"""
import requests
import time
import json

def test_bazi_api():
    """测试八字分析API"""
    url = "http://127.0.0.1:8001/divination/api/bazi/"
    
    # 测试数据
    test_data = {
        "name": "测试用户",
        "birth_time": "1990-05-15T10:30:00",
        "birth_place": "北京",
        "ai_mode": True
    }
    
    headers = {
        'Content-Type': 'application/json',
    }
    
    print("🔍 开始测试八字分析API...")
    print(f"📡 请求URL: {url}")
    print(f"📤 请求数据: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
    print("-" * 50)
    
    start_time = time.time()
    
    try:
        # 设置60秒超时
        response = requests.post(url, json=test_data, headers=headers, timeout=60)
        end_time = time.time()
        
        response_time = end_time - start_time
        print(f"⏱️  响应时间: {response_time:.2f} 秒")
        print(f"📊 HTTP状态码: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ API响应成功!")
                print(f"🎯 返回数据结构:")
                
                if 'success' in data:
                    print(f"   - success: {data['success']}")
                if 'ai_enhanced' in data:
                    print(f"   - ai_enhanced: {data['ai_enhanced']}")
                if 'analysis' in data:
                    analysis_preview = data['analysis'][:100] + "..." if len(data['analysis']) > 100 else data['analysis']
                    print(f"   - analysis: {analysis_preview}")
                if 'detail_info' in data:
                    print(f"   - detail_info: {list(data['detail_info'].keys()) if isinstance(data['detail_info'], dict) else 'available'}")
                
                # 检查是否是AI超时的降级响应
                if data.get('ai_enhanced') == False and 'AI分析暂时不可用' in data.get('analysis', ''):
                    print("⚠️  检测到AI超时降级响应")
                else:
                    print("🎉 正常AI增强响应")
                    
            except json.JSONDecodeError:
                print("❌ 响应不是有效的JSON格式")
                print(f"响应内容: {response.text[:200]}...")
        else:
            print("❌ API请求失败")
            print(f"错误信息: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ 请求超时 (60秒)")
    except requests.exceptions.ConnectionError:
        print("🔌 连接错误 - 请确保Django服务器在运行")
    except Exception as e:
        print(f"❌ 请求出现异常: {str(e)}")
    
    print("-" * 50)

def test_bazi_marriage_api():
    """测试八字合婚API"""
    url = "http://127.0.0.1:8001/divination/api/bazi-marriage/"
    
    # 测试数据
    test_data = {
        "male_info": {
            "name": "张三",
            "birth_time": "1990-05-15T10:30:00",
            "birth_place": "北京"
        },
        "female_info": {
            "name": "李四",
            "birth_time": "1992-08-20T14:15:00",
            "birth_place": "上海"
        },
        "ai_mode": True
    }
    
    headers = {
        'Content-Type': 'application/json',
    }
    
    print("💕 开始测试八字合婚API...")
    print(f"📡 请求URL: {url}")
    print(f"📤 请求数据: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
    print("-" * 50)
    
    start_time = time.time()
    
    try:
        response = requests.post(url, json=test_data, headers=headers, timeout=60)
        end_time = time.time()
        
        response_time = end_time - start_time
        print(f"⏱️  响应时间: {response_time:.2f} 秒")
        print(f"📊 HTTP状态码: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ API响应成功!")
                print(f"🎯 返回数据结构:")
                
                if 'success' in data:
                    print(f"   - success: {data['success']}")
                if 'compatibility_score' in data:
                    print(f"   - compatibility_score: {data['compatibility_score']}")
                if 'ai_enhanced' in data:
                    print(f"   - ai_enhanced: {data['ai_enhanced']}")
                    
            except json.JSONDecodeError:
                print("❌ 响应不是有效的JSON格式")
                print(f"响应内容: {response.text[:200]}...")
        else:
            print("❌ API请求失败")
            print(f"错误信息: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ 请求超时 (60秒)")
    except Exception as e:
        print(f"❌ 请求出现异常: {str(e)}")
    
    print("-" * 50)

if __name__ == "__main__":
    print("🧪 FateMaster API 测试工具")
    print("=" * 50)
    
    # 测试八字分析API
    test_bazi_api()
    print("\n")
    
    # 测试八字合婚API  
    test_bazi_marriage_api()
    
    print("\n✨ 测试完成!")

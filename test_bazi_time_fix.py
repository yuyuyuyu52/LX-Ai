#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试八字时间格式修复
验证中文时辰解析是否正常工作
"""

import requests
import json
import sys

def test_bazi_time_parsing():
    """测试八字时间解析功能"""
    
    print("=== 测试八字分析时间格式修复 ===\n")
    
    # 测试数据 - 使用中文时辰格式
    test_cases = [
        {
            "name": "子时测试",
            "data": {
                "birth_time": "1995-06-15 子时",
                "gender": "男",
                "birth_place": "北京市"
            }
        },
        {
            "name": "午时测试", 
            "data": {
                "birth_time": "1990-03-20 午时",
                "gender": "女",
                "birth_place": "上海市"
            }
        },
        {
            "name": "申时测试",
            "data": {
                "birth_time": "1988-12-08 申时", 
                "gender": "男",
                "birth_place": "广州市"
            }
        }
    ]
    
    api_url = "http://localhost:8001/divination/api/bazi/"
    
    success_count = 0
    total_count = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"测试 {i}/{total_count}: {test_case['name']}")
        print(f"测试数据: {test_case['data']}")
        
        try:
            # 发送POST请求
            response = requests.post(
                api_url,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(test_case['data']),
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('success'):
                    print("✅ 测试成功!")
                    print(f"   八字: {result.get('bazi', {})}")
                    print(f"   生肖: {result.get('detail_info', {}).get('shengxiao', '未知')}")
                    print(f"   格局: {result.get('detail_info', {}).get('geju', '未知')}")
                    success_count += 1
                else:
                    print(f"❌ API返回错误: {result.get('error', '未知错误')}")
                    
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                print(f"   响应内容: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求异常: {str(e)}")
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析错误: {str(e)}")
        except Exception as e:
            print(f"❌ 未知错误: {str(e)}")
            
        print("-" * 50)
    
    print(f"\n=== 测试结果汇总 ===")
    print(f"总测试数: {total_count}")
    print(f"成功数: {success_count}")
    print(f"失败数: {total_count - success_count}")
    print(f"成功率: {success_count/total_count*100:.1f}%")
    
    if success_count == total_count:
        print("🎉 所有测试都通过了！时间格式修复成功！")
        return True
    else:
        print("⚠️  存在测试失败，需要进一步检查")
        return False

def test_marriage_time_parsing():
    """测试八字合婚时间解析功能"""
    
    print("\n=== 测试八字合婚时间格式修复 ===\n")
    
    test_data = {
        "male_info": {
            "name": "张三",
            "birth_time": "1992-08-15 辰时",
            "birth_place": "北京市"
        },
        "female_info": {
            "name": "李四", 
            "birth_time": "1994-02-20 亥时",
            "birth_place": "上海市"
        }
    }
    
    api_url = "http://localhost:8001/divination/api/bazi_marriage/"
    
    print("测试合婚数据:")
    print(f"男方: {test_data['male_info']}")
    print(f"女方: {test_data['female_info']}")
    
    try:
        response = requests.post(
            api_url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(test_data),
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                print("✅ 合婚测试成功!")
                print(f"   匹配度: {result.get('compatibility_score', 0)}分")
                print(f"   男方生肖: {result.get('detail_info', {}).get('male_shengxiao', '未知')}")
                print(f"   女方生肖: {result.get('detail_info', {}).get('female_shengxiao', '未知')}")
                return True
            else:
                print(f"❌ 合婚API返回错误: {result.get('error', '未知错误')}")
                return False
        else:
            print(f"❌ 合婚HTTP错误: {response.status_code}")
            print(f"   响应内容: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 合婚测试异常: {str(e)}")
        return False

if __name__ == "__main__":
    print("开始测试八字时间格式修复...")
    
    # 检查服务器是否可用
    try:
        response = requests.get("http://localhost:8001/", timeout=5)
        print("✅ 服务器连接正常\n")
    except:
        print("❌ 无法连接到服务器，请确保Django服务运行在 localhost:8001")
        sys.exit(1)
    
    # 执行测试
    bazi_success = test_bazi_time_parsing()
    marriage_success = test_marriage_time_parsing()
    
    print(f"\n{'='*60}")
    if bazi_success and marriage_success:
        print("🎉 全部测试通过！八字时间格式修复完成！")
        print("现在可以正常使用中文时辰进行八字分析了。")
    else:
        print("⚠️  测试未完全通过，需要进一步调试")

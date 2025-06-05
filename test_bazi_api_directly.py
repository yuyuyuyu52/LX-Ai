import os
import sys
import django
import time
import requests
import json

# 添加项目路径到Python路径
sys.path.append('/Users/Zhuanz/Documents/LX-Ai')

# 设置Django设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fatemaster.settings')

# 初始化Django
django.setup()

# 测试直接发送请求到API
def test_direct_api_call():
    print("=" * 60)
    print("直接调用八字API测试")
    print("=" * 60)
    
    url = "http://127.0.0.1:8000/divination/api/bazi/"
    
    payload = {
        'birth_time': '1990-01-01 子时',
        'gender': 'male',
        'birth_place': '北京',
        'ai_mode': False
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    print(f"发送数据: {json.dumps(payload, ensure_ascii=False)}")
    print(f"目标URL: {url}")
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"状态码: {response.status_code}")
        print(f"响应时间: {response.elapsed.total_seconds()} 秒")
        
        if response.status_code == 200:
            data = response.json()
            print(f"成功状态: {data.get('success')}")
            
            if data.get('success'):
                print("✓ API调用成功！")
                print(f"返回的八字: {data.get('bazi')}")
                print(f"分析长度: {len(data.get('analysis', ''))}")
                print(f"AI增强: {data.get('ai_enhanced')}")
            else:
                print(f"✗ API错误: {data.get('error')}")
        else:
            print(f"✗ HTTP错误: {response.status_code}")
            print(f"响应内容: {response.text[:200]}...")
    
    except Exception as e:
        print(f"✗ 请求异常: {e}")

def test_with_different_parameters():
    print("\n" + "=" * 60)
    print("使用不同参数进行测试")
    print("=" * 60)
    
    url = "http://127.0.0.1:8000/divination/api/bazi/"
    test_cases = [
        {
            "name": "标准参数",
            "payload": {
                'birth_time': '1990-01-01 子时',
                'gender': 'male',
                'birth_place': '北京',
                'ai_mode': False
            }
        },
        {
            "name": "ISO格式时间",
            "payload": {
                'birth_time': '1990-01-01T00:00:00',
                'gender': 'male',
                'birth_place': '北京',
                'ai_mode': False
            }
        },
        {
            "name": "只有日期",
            "payload": {
                'birth_time': '1990-01-01',
                'gender': 'male',
                'birth_place': '北京',
                'ai_mode': False
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n测试: {test_case['name']}")
        payload = test_case['payload']
        
        try:
            response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✓ 成功: {data.get('bazi')}")
                else:
                    print(f"✗ 失败: {data.get('error')}")
            else:
                print(f"✗ HTTP错误: {response.status_code}")
        
        except Exception as e:
            print(f"✗ 异常: {e}")

def test_debug_headers():
    """测试添加调试头部以检查CSRF和其他头部问题"""
    print("\n" + "=" * 60)
    print("使用调试头部进行测试")
    print("=" * 60)
    
    url = "http://127.0.0.1:8000/divination/api/bazi/"
    payload = {
        'birth_time': '1990-01-01 子时',
        'gender': 'male',
        'birth_place': '北京',
        'ai_mode': False
    }
    
    headers = {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',  # 模拟AJAX请求
        'X-Debug': 'true',  # 自定义调试头部
        'User-Agent': 'BaziButtonTest/1.0'  # 自定义用户代理
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✓ 成功: {data.get('bazi')}")
            else:
                print(f"✗ 失败: {data.get('error')}")
        else:
            print(f"✗ HTTP错误: {response.status_code}")
            print(f"响应内容: {response.text[:200]}...")
    
    except Exception as e:
        print(f"✗ 异常: {e}")

if __name__ == "__main__":
    print("八字按钮API直接调用测试")
    print("=" * 60)
    print("确保Django开发服务器正在运行")
    
    # 等待Django服务器启动
    print("等待5秒确保服务器已启动...")
    time.sleep(5)
    
    # 执行测试
    test_direct_api_call()
    test_with_different_parameters()
    test_debug_headers()
    
    print("\n所有测试完成！")

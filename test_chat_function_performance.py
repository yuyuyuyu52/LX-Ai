#!/usr/bin/env python3
"""
测试chat函数在四个占卜功能中的性能
"""

import time
import sys
import os
from datetime import datetime

# 添加项目路径
sys.path.append('/Users/Zhuanz/Documents/LX-Ai')

# 导入您的chat函数
from deepseekr1 import chat

def test_bazi_analysis():
    """测试八字分析"""
    print("🔮 测试八字分析AI响应时间")
    
    prompt = """
请根据以下八字信息进行详细分析：

【基本信息】
出生时间：1990年5月15日 14:30
性别：男
八字：庚午 辛巳 丙戌 乙未
日主：丙（火）
生肖：马

【五行统计】
金：2个  木：1个  水：0个  火：3个  土：2个

请提供详细的性格分析、运势预测和人生建议。
"""
    
    start_time = time.time()
    try:
        response = chat(role="user", content=prompt)
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"   ✅ 响应成功")
        print(f"   ⏱️ 响应时间: {duration:.2f}秒")
        print(f"   📝 响应长度: {len(response)}字符")
        print(f"   📄 响应预览: {response[:100]}...")
        
        return duration, len(response), True
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"   ❌ 响应失败: {e}")
        print(f"   ⏱️ 耗时: {duration:.2f}秒")
        return duration, 0, False

def test_tarot_reading():
    """测试塔罗占卜"""
    print("\n🃏 测试塔罗占卜AI响应时间")
    
    prompt = """
请根据以下塔罗牌阵进行详细解读：

【三张牌阵 - 爱情运势】
过去：恋人牌（正位）
现在：星星牌（正位）  
未来：太阳牌（正位）

【问题】
我想了解自己最近的感情运势，有什么需要注意的地方吗？

请提供详细的牌意解读和感情建议。
"""
    
    start_time = time.time()
    try:
        response = chat(role="user", content=prompt)
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"   ✅ 响应成功")
        print(f"   ⏱️ 响应时间: {duration:.2f}秒")
        print(f"   📝 响应长度: {len(response)}字符")
        print(f"   📄 响应预览: {response[:100]}...")
        
        return duration, len(response), True
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"   ❌ 响应失败: {e}")
        print(f"   ⏱️ 耗时: {duration:.2f}秒")
        return duration, 0, False

def test_meihua_yishu():
    """测试梅花易数"""
    print("\n🌸 测试梅花易数AI响应时间")
    
    prompt = """
请根据以下梅花易数卦象进行详细分析：

【起卦信息】
时间：2025年6月5日 15:30
地点：北京
问题：工作发展前景如何？

【卦象】
主卦：山火贲（☶☲）
变卦：山雷颐（☶☳）
动爻：六三爻

【分析要求】
1. 卦象基本含义
2. 动爻解析
3. 工作运势分析
4. 具体建议

请提供专业的易学分析。
"""
    
    start_time = time.time()
    try:
        response = chat(role="user", content=prompt)
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"   ✅ 响应成功")
        print(f"   ⏱️ 响应时间: {duration:.2f}秒")
        print(f"   📝 响应长度: {len(response)}字符")
        print(f"   📄 响应预览: {response[:100]}...")
        
        return duration, len(response), True
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"   ❌ 响应失败: {e}")
        print(f"   ⏱️ 耗时: {duration:.2f}秒")
        return duration, 0, False

def test_daily_fortune():
    """测试每日运势"""
    print("\n🌟 测试每日运势AI响应时间")
    
    prompt = """
请为以下用户提供今日运势分析：

【用户信息】
生肖：马
星座：金牛座
出生年份：1990年
性别：男

【今日信息】
日期：2025年6月5日
星期：星期四
农历：五月初十

【运势要求】
1. 整体运势
2. 爱情运势
3. 事业运势
4. 财运分析
5. 健康提醒
6. 幸运数字和颜色

请提供详细的今日运势指导。
"""
    
    start_time = time.time()
    try:
        response = chat(role="user", content=prompt)
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"   ✅ 响应成功")
        print(f"   ⏱️ 响应时间: {duration:.2f}秒")
        print(f"   📝 响应长度: {len(response)}字符")
        print(f"   📄 响应预览: {response[:100]}...")
        
        return duration, len(response), True
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        print(f"   ❌ 响应失败: {e}")
        print(f"   ⏱️ 耗时: {duration:.2f}秒")
        return duration, 0, False

def main():
    """主测试函数"""
    print("=" * 60)
    print("🚀 DeepSeek-R1 Chat函数性能测试")
    print("=" * 60)
    print(f"📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🤖 模型: deepseek-r1-250120")
    print(f"⚙️ 当前超时配置: 25秒")
    print()
    
    # 存储测试结果
    results = []
    
    # 测试四个功能
    tests = [
        ("八字分析", test_bazi_analysis),
        ("塔罗占卜", test_tarot_reading),
        ("梅花易数", test_meihua_yishu),
        ("每日运势", test_daily_fortune)
    ]
    
    for test_name, test_func in tests:
        try:
            duration, response_length, success = test_func()
            results.append({
                'name': test_name,
                'duration': duration,
                'length': response_length,
                'success': success
            })
        except Exception as e:
            print(f"   💥 测试 {test_name} 时发生异常: {e}")
            results.append({
                'name': test_name,
                'duration': 0,
                'length': 0,
                'success': False
            })
        
        # 每次测试后等待1秒
        time.sleep(1)
    
    # 统计结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    total_duration = 0
    success_count = 0
    total_length = 0
    
    for result in results:
        name = result['name']
        duration = result['duration']
        length = result['length']
        success = result['success']
        
        status = "✅ 成功" if success else "❌ 失败"
        timeout_status = "⚠️ 超时" if duration > 25 else "✅ 正常"
        
        print(f"{name:8} | {status:8} | {duration:6.2f}秒 | {timeout_status:8} | {length:5d}字符")
        
        if success:
            total_duration += duration
            success_count += 1
            total_length += length
    
    print("-" * 60)
    print(f"成功率: {success_count}/{len(tests)} ({success_count/len(tests)*100:.1f}%)")
    
    if success_count > 0:
        print(f"平均响应时间: {total_duration/success_count:.2f}秒")
        print(f"平均响应长度: {total_length/success_count:.0f}字符")
        print(f"总耗时: {total_duration:.2f}秒")
    
    # 超时分析
    timeout_count = sum(1 for r in results if r['duration'] > 25 and r['success'])
    if timeout_count > 0:
        print(f"\n⚠️ 超时问题:")
        print(f"   - {timeout_count}个功能响应时间超过25秒")
        print(f"   - 建议将AI_TIMEOUT调整为35-40秒")
    else:
        print(f"\n✅ 响应时间良好:")
        print(f"   - 所有功能均在25秒内响应")
        print(f"   - 当前超时配置合适")
    
    # 性能建议
    print(f"\n💡 性能优化建议:")
    if total_duration / len(tests) > 20:
        print(f"   - 平均响应时间较长，考虑优化prompt长度")
        print(f"   - 可以分批处理复杂分析")
    else:
        print(f"   - 响应速度良好，可以继续当前配置")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ 测试被用户中断")
    except Exception as e:
        print(f"\n💥 测试过程中出现异常: {e}")
        import traceback
        traceback.print_exc()

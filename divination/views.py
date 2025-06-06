from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
import json
import random
import logging
from datetime import datetime, date
from .models import BaziElement
from core.models import DivinationRecord, UserProfile, DailyFortune
from core.bazi_calculator import bazi_calculator
from core.fortune_calculator import meihua_calculator, fortune_calculator
from core.ai_service import ai_service
from core.decorators import check_usage_limit, membership_info
from lunar_python import Lunar

logger = logging.getLogger(__name__)


def parse_chinese_time(time_str):
    """
    解析中文时间格式 "YYYY-MM-DD 时辰名称" 为 datetime 对象
    
    Args:
        time_str: 时间字符串，格式如 "2024-01-01 子时"
    
    Returns:
        datetime: 解析后的datetime对象
    """
    # 中文时辰到小时的映射
    time_mapping = {
        '子时': 0,   # 23:00-01:00, 取0点
        '丑时': 2,   # 01:00-03:00, 取2点  
        '寅时': 4,   # 03:00-05:00, 取4点
        '卯时': 6,   # 05:00-07:00, 取6点
        '辰时': 8,   # 07:00-09:00, 取8点
        '巳时': 10,  # 09:00-11:00, 取10点
        '午时': 12,  # 11:00-13:00, 取12点
        '未时': 14,  # 13:00-15:00, 取14点
        '申时': 16,  # 15:00-17:00, 取16点
        '酉时': 18,  # 17:00-19:00, 取18点
        '戌时': 20,  # 19:00-21:00, 取20点
        '亥时': 22,  # 21:00-23:00, 取22点
    }
    
    try:
        # 分割日期和时辰
        parts = time_str.strip().split(' ')
        if len(parts) != 2:
            raise ValueError("时间格式错误")
        
        date_part = parts[0]
        time_part = parts[1]
        
        # 解析日期部分
        year, month, day = date_part.split('-')
        year, month, day = int(year), int(month), int(day)
        
        # 获取对应的小时
        if time_part not in time_mapping:
            raise ValueError(f"未知的时辰: {time_part}")
        
        hour = time_mapping[time_part]
        
        # 创建datetime对象
        return datetime(year, month, day, hour, 0, 0)
        
    except Exception as e:
        raise ValueError(f"时间解析失败: {str(e)}")


def bazi_analysis(request):
    """八字分析页面"""
    return render(request, 'divination/bazi.html', {'page_title': '八字分析'})

def meihua_yishu(request):
    """梅花易数页面"""
    return render(request, 'divination/meihua_new.html', {'page_title': '梅花易数'})

def bazi_marriage(request):
    """八字合婚页面"""
    return render(request, 'divination/bazi_marriage.html', {'page_title': '八字合婚'})

def daily_fortune(request):
    """每日运势页面"""
    return render(request, 'divination/daily_fortune.html', {'page_title': '每日运势'})

@csrf_exempt
@check_usage_limit()
@membership_info
def bazi_api(request):
    """八字分析API - 支持普通模式和AI增强模式"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            birth_time = data.get('birth_time')
            gender = data.get('gender', '男')
            birth_place = data.get('birth_place', '')
            ai_mode = data.get('ai_mode', False)

            # 检查AI模式权限
            if ai_mode and request.user.is_authenticated:
                profile, _ = UserProfile.objects.get_or_create(user=request.user)
                if not profile.can_use_ai():
                    return JsonResponse({'success': False, 'error': 'AI增强分析仅限会员使用，请升级会员后再试。'})

            # 🔍 DEBUG: 添加AI模式调试输出
            print("=" * 60)
            print(f"🔍 AI模式调试信息:")
            print(f"   - ai_mode参数: {ai_mode}")
            print(f"   - 用户已认证: {request.user.is_authenticated}")
            if request.user.is_authenticated:
                profile, _ = UserProfile.objects.get_or_create(user=request.user)
                print(f"   - 用户名: {request.user.username}")
                print(f"   - VIP状态: {profile.is_vip}")
                print(f"   - 可使用AI: {profile.can_use_ai()}")
                print(f"   - AI使用次数: {profile.ai_usage_count}")
            else:
                print(f"   - 用户未登录")
            print("=" * 60)
            
            # 解析出生时间
            try:
                if isinstance(birth_time, str):
                    # 处理中文时辰格式 "YYYY-MM-DD 时辰名称"
                    if ' ' in birth_time and any(time in birth_time for time in ['子时', '丑时', '寅时', '卯时', '辰时', '巳时', '午时', '未时', '申时', '酉时', '戌时', '亥时']):
                        birth_dt = parse_chinese_time(birth_time)
                    else:
                        # 处理ISO格式时间
                        birth_dt = datetime.fromisoformat(birth_time.replace('Z', '+00:00'))
                else:
                    birth_dt = datetime.now()
            except ValueError as e:
                return JsonResponse({'success': False, 'error': f'出生时间格式错误: {str(e)}'})
            except Exception as e:
                return JsonResponse({'success': False, 'error': '出生时间格式错误'})

            # 八字计算
            bazi_result = bazi_calculator.calculate_bazi(birth_dt, gender)
            da_yun = bazi_result.get('da_yun', {})
            gender_display = '男' if gender in ['male', '男'] else '女'
            basic_analysis = f"""
【八字排盘】\n年柱：{bazi_result['bazi_string']['year']}    月柱：{bazi_result['bazi_string']['month']}    日柱：{bazi_result['bazi_string']['day']}    时柱：{bazi_result['bazi_string']['hour']}\n\n【基本信息】\n性别：{gender_display}\n生肖：{bazi_result['shengxiao']}\n大运起运时间：{da_yun.get('start_age', '-')}岁 {da_yun.get('start_date', '-')}\n"""

            # AI增强分析
            final_analysis = basic_analysis
            actual_ai_used = False  # 跟踪AI是否真正被使用
            if ai_mode and request.user.is_authenticated:
                print("🔍 准备调用AI增强分析...")
                try:
                    birth_info = {
                        'birth_time': birth_time,
                        'gender': gender,
                        'birth_place': birth_place
                    }
                    print(f"📋 AI分析参数: {birth_info}")
                    print("🤖 调用 ai_service.enhance_bazi_analysis...")
                    
                    ai_analysis = ai_service.enhance_bazi_analysis(
                        bazi_result['bazi_string'],
                        basic_analysis,
                        birth_info
                    )
                    
                    print(f"✅ AI分析完成，结果长度: {len(ai_analysis)}字符")
                    final_analysis = ai_analysis
                    actual_ai_used = True  # 标记AI已成功使用
                    profile.ai_usage_count += 1
                    profile.save()
                    print(f"📊 更新用户AI使用次数: {profile.ai_usage_count}")
                except Exception as e:
                    print(f"❌ AI增强分析失败: {str(e)}")
                    logger.warning(f"AI增强分析失败，使用基础分析: {str(e)}")
                    # AI失败时提供用户友好的提示，但仍返回基础分析
                    final_analysis = basic_analysis + f"\n\n[注：AI增强分析暂时不可用，已为您提供完整的基础分析]"
                    actual_ai_used = False  # 标记AI未成功使用
            else:
                if ai_mode:
                    print("⚠️  AI模式已启用但条件不满足:")
                    print(f"   - ai_mode: {ai_mode}")
                    print(f"   - 用户已认证: {request.user.is_authenticated}")
                    if not request.user.is_authenticated:
                        print("   - 建议：用户需要登录才能使用AI功能")
                else:
                    print("ℹ️  使用普通模式（未启用AI）")

            # 保存占卜记录
            if request.user.is_authenticated:
                DivinationRecord.objects.create(
                    user=request.user,
                    divination_type='bazi',
                    result=final_analysis,
                    ai_enhanced=actual_ai_used  # 使用实际的AI使用状态
                )
                from core.models import Notification
                Notification.objects.create(
                    user=request.user,
                    title='八字分析完成',
                    message=f'您的{"AI增强" if actual_ai_used else ""}八字分析报告已生成完成。',
                    notification_type='success'
                )

            return JsonResponse({
                'success': True,
                'bazi': bazi_result['bazi_string'],
                'analysis': final_analysis,
                'ai_enhanced': actual_ai_used,  # 使用实际的AI使用状态
                'detail_info': {
                    'shengxiao': bazi_result['shengxiao'],
                    'wuxing_count': bazi_result['wuxing_count'],
                    'geju': bazi_result['geju'],
                    'da_yun': da_yun  # 新增大运起运信息
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'分析过程中出现错误：{str(e)}'})
    return JsonResponse({'success': False, 'error': '请求方法错误'})

@csrf_exempt
@check_usage_limit()
@membership_info
def bazi_marriage_api(request):
    """八字合婚API - 支持普通模式和AI增强模式"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # 解析嵌套的数据结构
            male_info = data.get('male_info', {})
            female_info = data.get('female_info', {})
            
            male_birth_time = male_info.get('birth_time')
            female_birth_time = female_info.get('birth_time')
            male_name = male_info.get('name', '男方')
            female_name = female_info.get('name', '女方')
            ai_mode = data.get('ai_mode', False)

            # 检查AI模式权限
            if ai_mode and request.user.is_authenticated:
                profile, _ = UserProfile.objects.get_or_create(user=request.user)
                if not profile.can_use_ai():
                    return JsonResponse({'success': False, 'error': 'AI增强分析仅限会员使用，请升级会员后再试。'})

            # 🔍 DEBUG: 添加AI模式调试输出
            print("=" * 60)
            print(f"🔍 八字合婚AI模式调试信息:")
            print(f"   - ai_mode参数: {ai_mode}")
            print(f"   - 用户已认证: {request.user.is_authenticated}")
            if request.user.is_authenticated:
                profile, _ = UserProfile.objects.get_or_create(user=request.user)
                print(f"   - 用户名: {request.user.username}")
                print(f"   - VIP状态: {profile.is_vip}")
                print(f"   - 可使用AI: {profile.can_use_ai()}")
                print(f"   - AI使用次数: {profile.ai_usage_count}")
            else:
                print(f"   - 用户未登录")
            print("=" * 60)

            # 解析出生时间
            try:
                if isinstance(male_birth_time, str):
                    # 处理中文时辰格式 "YYYY-MM-DD 时辰名称"
                    if ' ' in male_birth_time and any(time in male_birth_time for time in ['子时', '丑时', '寅时', '卯时', '辰时', '巳时', '午时', '未时', '申时', '酉时', '戌时', '亥时']):
                        male_dt = parse_chinese_time(male_birth_time)
                    else:
                        # 处理ISO格式时间
                        male_dt = datetime.fromisoformat(male_birth_time.replace('Z', '+00:00'))
                else:
                    male_dt = datetime.now()
                    
                if isinstance(female_birth_time, str):
                    # 处理中文时辰格式 "YYYY-MM-DD 时辰名称"
                    if ' ' in female_birth_time and any(time in female_birth_time for time in ['子时', '丑时', '寅时', '卯时', '辰时', '巳时', '午时', '未时', '申时', '酉时', '戌时', '亥时']):
                        female_dt = parse_chinese_time(female_birth_time)
                    else:
                        # 处理ISO格式时间
                        female_dt = datetime.fromisoformat(female_birth_time.replace('Z', '+00:00'))
                else:
                    female_dt = datetime.now()
            except ValueError as e:
                return JsonResponse({'success': False, 'error': f'出生时间格式错误: {str(e)}'})
            except Exception as e:
                return JsonResponse({'success': False, 'error': '出生时间格式错误'})

            # 分别计算男女双方八字
            from core.bazi_calculator import BaziCalculator
            bazi_calculator = BaziCalculator()
            male_bazi_data = bazi_calculator.calculate_bazi(male_dt, '男')
            female_bazi_data = bazi_calculator.calculate_bazi(female_dt, '女')
            
            # 八字合婚计算
            marriage_result = bazi_calculator.calculate_marriage_compatibility(male_bazi_data, female_bazi_data)
            
            # 基础分析结果
            basic_analysis = f"""
【八字合婚分析报告】

【基本信息】
{male_name}：{male_bazi_data['bazi_string']['year']} {male_bazi_data['bazi_string']['month']} {male_bazi_data['bazi_string']['day']} {male_bazi_data['bazi_string']['hour']}
生肖：{male_bazi_data['shengxiao']}  日主：{male_bazi_data['ri_zhu']}

{female_name}：{female_bazi_data['bazi_string']['year']} {female_bazi_data['bazi_string']['month']} {female_bazi_data['bazi_string']['day']} {female_bazi_data['bazi_string']['hour']}
生肖：{female_bazi_data['shengxiao']}  日主：{female_bazi_data['ri_zhu']}

【匹配度评分】
综合匹配度：{marriage_result['total_score']}分 - {marriage_result['level']}
{marriage_result['description']}

【详细分析】
生肖配对：{marriage_result['details']['shengxiao_score']}分
五行互补：{marriage_result['details']['wuxing_score']}分
日柱匹配：{marriage_result['details']['rizhu_score']}分
格局配合：{marriage_result['details']['geju_score']}分

【合婚建议】
根据八字分析，你们的匹配度为{marriage_result['total_score']}分，属于{marriage_result['level']}婚配。
{marriage_result['description']}

【注意事项】
- 夫妻相处要互相理解包容
- 保持良好的沟通和信任
- 在重要决策上多商量讨论
- 彼此支持对方的事业发展

* 以上合婚分析基于传统命理学，仅供参考娱乐。
            """

            # AI增强分析
            final_analysis = basic_analysis
            actual_ai_used = False  # 跟踪AI是否真正被使用
            if ai_mode and request.user.is_authenticated:
                print("🔍 准备调用八字合婚AI增强分析...")
                try:
                    from core.ai_service import AIService
                    ai_service = AIService()
                    
                    male_info_for_ai = {
                        'name': male_name,
                        'bazi': f"{male_bazi_data['bazi_string']['year']} {male_bazi_data['bazi_string']['month']} {male_bazi_data['bazi_string']['day']} {male_bazi_data['bazi_string']['hour']}",
                        'birth_time': male_birth_time
                    }
                    
                    female_info_for_ai = {
                        'name': female_name,
                        'bazi': f"{female_bazi_data['bazi_string']['year']} {female_bazi_data['bazi_string']['month']} {female_bazi_data['bazi_string']['day']} {female_bazi_data['bazi_string']['hour']}",
                        'birth_time': female_birth_time
                    }
                    
                    print(f"📋 八字合婚AI分析参数: 男方={male_info_for_ai}, 女方={female_info_for_ai}")
                    print("🤖 调用 ai_service.enhance_marriage_analysis...")
                    
                    ai_analysis = ai_service.enhance_marriage_analysis(
                        basic_analysis,
                        male_info_for_ai,
                        female_info_for_ai
                    )
                    
                    print(f"✅ 八字合婚AI分析完成，结果长度: {len(ai_analysis)}字符")
                    final_analysis = ai_analysis
                    actual_ai_used = True  # 标记AI已成功使用
                    profile.ai_usage_count += 1
                    profile.save()
                    print(f"📊 更新用户AI使用次数: {profile.ai_usage_count}")
                except Exception as e:
                    print(f"❌ 八字合婚AI增强分析失败: {str(e)}")
                    final_analysis = basic_analysis + f"\n\n[注：AI增强分析暂时不可用，已为您提供完整的基础分析]"
                    actual_ai_used = False  # 标记AI未成功使用
            else:
                print("🔍 八字合婚未启用AI模式或用户未登录")

            # 保存占卜记录
            if request.user.is_authenticated:
                DivinationRecord.objects.create(
                    user=request.user,
                    divination_type='marriage',
                    result=final_analysis,
                    ai_enhanced=ai_mode
                )
                from core.models import Notification
                Notification.objects.create(
                    user=request.user,
                    title='八字合婚完成',
                    message=f'{male_name}与{female_name}的{"AI增强" if actual_ai_used else ""}八字合婚分析已完成。',
                    notification_type='success'
                )

            return JsonResponse({
                'success': True,
                'compatibility_score': marriage_result['total_score'],
                'analysis': final_analysis,
                'ai_enhanced': actual_ai_used,  # 使用实际的AI使用状态
                'detail_info': {
                    'male_shengxiao': marriage_result['male_shengxiao'],
                    'female_shengxiao': marriage_result['female_shengxiao'],
                    'zodiac_score': marriage_result['details']['shengxiao_score'],
                    'wuxing_score': marriage_result['details']['wuxing_score']
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'合婚分析过程中出现错误：{str(e)}'})
    return JsonResponse({'success': False, 'error': '请求方法错误'})

@csrf_exempt
@check_usage_limit()
@membership_info
def meihua_api(request):
    """梅花易数API"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question', '')
            number1 = int(data.get('number1', 1))
            number2 = int(data.get('number2', 1))
            ai_mode = data.get('ai_mode', False)
            
            if not question.strip():
                return JsonResponse({'success': False, 'error': '请输入问题'})
            
            # 检查AI模式权限
            if ai_mode:
                if not request.user.is_authenticated:
                    return JsonResponse({'success': False, 'error': 'AI模式需要登录'})
                
                user_profile = request.user.userprofile
                if not user_profile.can_use_ai():
                    return JsonResponse({'success': False, 'error': 'AI模式仅限会员使用'})
            
            # 使用梅花易数计算器
            from core.fortune_calculator import MeihuaCalculator
            calculator = MeihuaCalculator()
            result = calculator.calculate_meihua(question)
            
            # 生成基础分析
            def generate_basic_meihua_analysis(result_data):
                return f"""
【梅花易数分析】

【问题】{result_data['question']}

【卦象信息】
主卦：{result_data['zhu_gua']['name']}
  上卦：{result_data['zhu_gua']['upper']['name']}（{result_data['zhu_gua']['upper']['nature']}）
  下卦：{result_data['zhu_gua']['lower']['name']}（{result_data['zhu_gua']['lower']['nature']}）

变卦：{result_data['bian_gua']['name']}
  上卦：{result_data['bian_gua']['upper']['name']}（{result_data['bian_gua']['upper']['nature']}）
  下卦：{result_data['bian_gua']['lower']['name']}（{result_data['bian_gua']['lower']['nature']}）

动爻：第{result_data['dong_yao']}爻

【体用分析】
体卦：{result_data['ti_yong']['ti_gua']['name']}（{result_data['ti_yong']['ti_gua']['wuxing']}）
用卦：{result_data['ti_yong']['yong_gua']['name']}（{result_data['ti_yong']['yong_gua']['wuxing']}）
关系：{result_data['ti_yong']['analysis']}

【五行分析】
{result_data['wuxing']['analysis']}

【时间预测】
{result_data['time_prediction']}

* 以上分析基于梅花易数传统理论，仅供参考娱乐。
                """
            
            basic_analysis = generate_basic_meihua_analysis(result)
            
            # AI增强分析
            final_analysis = basic_analysis
            actual_ai_used = False  # 跟踪AI是否真正被使用
            
            if ai_mode and request.user.is_authenticated:
                # 🔍 DEBUG: 添加AI模式调试输出
                print("=" * 60)
                print(f"🔍 梅花易数AI模式调试信息:")
                print(f"   - ai_mode参数: {ai_mode}")
                print(f"   - 用户已认证: {request.user.is_authenticated}")
                if request.user.is_authenticated:
                    profile = request.user.userprofile
                    print(f"   - 用户名: {request.user.username}")
                    print(f"   - VIP状态: {profile.is_vip}")
                    print(f"   - 可使用AI: {profile.can_use_ai()}")
                    print(f"   - AI使用次数: {profile.ai_usage_count}")
                print("=" * 60)
                
                print("🔍 准备调用梅花易数AI增强分析...")
                try:
                    from core.ai_service import AIService
                    ai_service = AIService()
                    
                    print(f"📋 AI分析参数: 问题={question}, 主卦={result['zhu_gua']['name']}, 变卦={result['bian_gua']['name']}, 动爻={result['dong_yao']}")
                    print("🤖 调用 ai_service.enhance_meihua_analysis...")
                    
                    ai_analysis = ai_service.enhance_meihua_analysis(
                        question=question,
                        main_gua=result['zhu_gua'],
                        bian_gua=result['bian_gua'],
                        dong_yao=result['dong_yao'],
                        basic_analysis=basic_analysis
                    )
                    
                    print(f"✅ AI分析完成，结果长度: {len(ai_analysis)}字符")
                    final_analysis = ai_analysis
                    actual_ai_used = True  # 标记AI已成功使用
                    
                    # 更新用户AI使用次数
                    user_profile.ai_usage_count += 1
                    user_profile.save()
                    print(f"📊 更新用户AI使用次数: {user_profile.ai_usage_count}")
                    
                except Exception as e:
                    print(f"❌ AI增强分析失败: {str(e)}")
                    logger.warning(f"梅花易数AI增强分析失败，使用基础分析: {str(e)}")
                    # AI失败时提供用户友好的提示，但仍返回基础分析
                    final_analysis = basic_analysis + f"\n\n[注：AI增强分析暂时不可用，已为您提供完整的基础分析]"
                    actual_ai_used = False  # 标记AI未成功使用
            else:
                print("🔍 梅花易数未启用AI模式或用户未登录")
            
            # 保存占卜记录
            if request.user.is_authenticated:
                DivinationRecord.objects.create(
                    user=request.user,
                    divination_type='meihua',
                    question=question,
                    result=final_analysis,
                    ai_enhanced=actual_ai_used  # 使用实际的AI使用状态
                )
                
                # 创建通知
                from core.models import Notification
                Notification.objects.create(
                    user=request.user,
                    title='梅花易数完成',
                    message=f'您关于"{question[:20]}..."的{"AI增强" if actual_ai_used else ""}梅花易数占卜已完成。',
                    notification_type='success'
                )
            
            return JsonResponse({
                'success': True,
                'main_gua': result['zhu_gua'],
                'bian_gua': result['bian_gua'],
                'dong_yao': result['dong_yao'],
                'analysis': final_analysis,
                'ai_enhanced': actual_ai_used,  # 使用实际AI使用状态
                'detail_info': {
                    'main_gua_name': result['zhu_gua']['name'],
                    'bian_gua_name': result['bian_gua']['name'],
                    'time_info': result['time_prediction']
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'梅花易数分析过程中出现错误：{str(e)}'})
    return JsonResponse({'success': False, 'error': '请求方法错误'})

@csrf_exempt
@check_usage_limit()
@membership_info
def daily_fortune_api(request):
    """每日运势API"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            birth_date = data.get('birth_date')
            ai_mode = data.get('ai_mode', False)
            
            if not birth_date:
                return JsonResponse({'success': False, 'error': '请输入出生日期'})
            
            # 检查AI模式权限
            if ai_mode:
                if not request.user.is_authenticated:
                    return JsonResponse({'success': False, 'error': 'AI模式需要登录'})
                
                user_profile = request.user.userprofile
                if not user_profile.can_use_ai():
                    return JsonResponse({'success': False, 'error': 'AI模式仅限会员使用'})

            # 🔍 DEBUG: 添加AI模式调试输出
            print("=" * 60)
            print(f"🔍 每日运势AI模式调试信息:")
            print(f"   - ai_mode参数: {ai_mode}")
            print(f"   - 用户已认证: {request.user.is_authenticated}")
            if request.user.is_authenticated:
                profile, _ = UserProfile.objects.get_or_create(user=request.user)
                print(f"   - 用户名: {request.user.username}")
                print(f"   - VIP状态: {profile.is_vip}")
                print(f"   - 可使用AI: {profile.can_use_ai()}")
                print(f"   - AI使用次数: {profile.ai_usage_count}")
            else:
                print(f"   - 用户未登录")
            print("=" * 60)
            
            # 解析出生日期获取生肖
            from datetime import datetime
            
            try:
                birth_dt = datetime.strptime(birth_date, '%Y-%m-%d')
            except ValueError:
                return JsonResponse({'success': False, 'error': '出生日期格式错误'})
            
            # 计算生肖
            zodiac_list = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
            zodiac = zodiac_list[(birth_dt.year - 4) % 12]
            
            # 使用运势计算器
            from core.fortune_calculator import FortuneCalculator
            calculator = FortuneCalculator()
            result = calculator.calculate_daily_fortune(zodiac, user_birth_date=birth_dt.date())
            
            # AI增强分析
            final_analysis = result['description']
            actual_ai_used = False  # 跟踪AI是否真正被使用
            if ai_mode and request.user.is_authenticated:
                print("🔍 准备调用每日运势AI增强分析...")
                try:
                    from core.ai_service import AIService
                    ai_service = AIService()
                    
                    user_info = {
                        'shengxiao': zodiac,
                        'constellation': '',
                        'gender': '',
                        'birth_year': str(birth_dt.year)
                    }
                    
                    fortune_data = {
                        'date': str(result['date']),
                        'lunar_date': '',
                        'weekday': result['date'].strftime('%A')
                    }
                    
                    print(f"📋 每日运势AI分析参数: 用户信息={user_info}, 运势数据={fortune_data}")
                    print("🤖 调用 ai_service.enhance_daily_fortune...")
                    
                    ai_analysis = ai_service.enhance_daily_fortune(user_info, fortune_data)
                    
                    print(f"✅ 每日运势AI分析完成，结果长度: {len(ai_analysis)}字符")
                    final_analysis = ai_analysis
                    actual_ai_used = True  # 标记AI已成功使用
                    
                    # 更新用户AI使用次数
                    user_profile.ai_usage_count += 1
                    user_profile.save()
                    print(f"📊 更新用户AI使用次数: {user_profile.ai_usage_count}")
                except Exception as e:
                    print(f"❌ 每日运势AI增强分析失败: {str(e)}")
                    # AI服务失败时使用基础分析
                    final_analysis = result['description'] + f"\n\n[注：AI增强分析暂时不可用，已为您提供完整的基础分析]"
                    actual_ai_used = False  # 标记AI未成功使用
            else:
                print("🔍 每日运势未启用AI模式或用户未登录")
            
            # 保存占卜记录
            if request.user.is_authenticated:
                DivinationRecord.objects.create(
                    user=request.user,
                    divination_type='daily_fortune',
                    result=final_analysis,
                    ai_enhanced=ai_mode
                )
                
                # 创建通知
                from core.models import Notification
                Notification.objects.create(
                    user=request.user,
                    title='每日运势完成',
                    message=f'您的{"AI增强" if ai_mode else ""}每日运势分析已完成。',
                    notification_type='success'
                )
            
            # 保存或更新每日运势记录
            from core.models import DailyFortune
            today = datetime.now().date()
            
            fortune_record, created = DailyFortune.objects.get_or_create(
                date=today,
                zodiac=result['zodiac'],
                defaults={
                    'overall_fortune': result['overall_fortune'],
                    'love_fortune': result['love_fortune'],
                    'career_fortune': result['career_fortune'],
                    'wealth_fortune': result['wealth_fortune'],
                    'health_fortune': result['health_fortune'],
                    'lucky_color': result['lucky_color'],
                    'lucky_number': result['lucky_number'],
                    'description': final_analysis
                }
            )
            
            return JsonResponse({
                'success': True,
                'zodiac': result['zodiac'],
                'fortune_scores': {
                    'overall': result['overall_fortune'],
                    'love': result['love_fortune'],
                    'career': result['career_fortune'],
                    'wealth': result['wealth_fortune'],
                    'health': result['health_fortune']
                },
                'lucky_elements': {
                    'color': result['lucky_color'],
                    'number': result['lucky_number'],
                    'direction': '东方'  # 可以后续完善方位计算
                },
                'analysis': final_analysis,
                'ai_enhanced': ai_mode,
                'detail_info': {
                    'date': result['date'].strftime('%Y-%m-%d'),
                    'wuxing_analysis': '',
                    'advice': ''
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'运势分析过程中出现错误：{str(e)}'})
    return JsonResponse({'success': False, 'error': '请求方法错误'})

def _get_day_ganzhi(self, birth_time):
    lunar = Lunar.fromDate(birth_time)
    gan_zhi = lunar.getDayGanZhi()  # 例如 '丙午'
    return gan_zhi[0], gan_zhi[1]

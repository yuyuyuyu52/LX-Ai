from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
import json
import random
from datetime import datetime, date
from .models import TarotCard, IChingHexagram, BaziElement
from core.models import DivinationRecord, UserProfile, DailyFortune
from core.bazi_calculator import bazi_calculator
from core.fortune_calculator import meihua_calculator, fortune_calculator
from core.ai_service import ai_service
from core.decorators import check_usage_limit, membership_info

def bazi_analysis(request):
    """八字分析页面"""
    return render(request, 'divination/bazi.html', {'page_title': '八字分析'})

def meihua_yishu(request):
    """梅花易数页面"""
    return render(request, 'divination/meihua_new.html', {'page_title': '梅花易数'})

def tarot_reading(request):
    """塔罗占卜页面"""
    return render(request, 'divination/tarot.html', {'page_title': '塔罗占卜'})

def yijing_divination(request):
    """易经卜卦页面"""
    return render(request, 'divination/yijing_new.html', {'page_title': '易经卜卦'})

def bazi_marriage(request):
    """八字合婚页面"""
    return render(request, 'divination/bazi_marriage.html', {'page_title': '八字合婚'})

def daily_fortune(request):
    """每日运势页面"""
    return render(request, 'divination/daily_fortune.html', {'page_title': '每日运势'})

@csrf_exempt
@check_usage_limit
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

            # 解析出生时间
            try:
                if isinstance(birth_time, str):
                    birth_dt = datetime.fromisoformat(birth_time.replace('Z', '+00:00'))
                else:
                    birth_dt = datetime.now()
            except:
                return JsonResponse({'success': False, 'error': '出生时间格式错误'})

            # 八字计算
            bazi_result = bazi_calculator.calculate_bazi(birth_dt, gender)
            basic_analysis = f"""
【八字排盘】\n年柱：{bazi_result['bazi_string']['year']}    月柱：{bazi_result['bazi_string']['month']}    日柱：{bazi_result['bazi_string']['day']}    时柱：{bazi_result['bazi_string']['hour']}\n\n【基本信息】\n性别：{gender}\n生肖：{bazi_result['shengxiao']}\n日主：{bazi_result['ri_zhu']}（{bazi_calculator.WUXING_TIANGAN[bazi_result['ri_zhu']]}）\n格局：{bazi_result['geju']}\n\n【五行统计】\n金：{bazi_result['wuxing_count']['金']}个  木：{bazi_result['wuxing_count']['木']}个  水：{bazi_result['wuxing_count']['水']}个  火：{bazi_result['wuxing_count']['火']}个  土：{bazi_result['wuxing_count']['土']}个\n\n【十神分析】\n年干：{bazi_result['shishen'].get('year_gan', '未知')}\n月干：{bazi_result['shishen'].get('month_gan', '未知')}\n时干：{bazi_result['shishen'].get('hour_gan', '未知')}\n\n【性格特点】\n日主{bazi_result['ri_zhu']}，五行属{bazi_calculator.WUXING_TIANGAN[bazi_result['ri_zhu']]}，性格特征明显。\n\n【事业财运】\n根据五行配置，适合发展相关行业。\n\n【感情婚姻】\n感情运势与个人格局密切相关。\n\n【健康运势】\n需要注意五行平衡，保持身心健康。\n\n* 以上分析基于传统八字命理学，仅供参考娱乐。\n"""

            # AI增强分析
            final_analysis = basic_analysis
            if ai_mode and request.user.is_authenticated:
                try:
                    birth_info = {
                        'birth_time': birth_time,
                        'gender': gender,
                        'birth_place': birth_place
                    }
                    ai_analysis = ai_service.enhance_bazi_analysis(
                        bazi_result['bazi_string'],
                        basic_analysis,
                        birth_info
                    )
                    final_analysis = ai_analysis
                    profile.ai_usage_count += 1
                    profile.save()
                except Exception as e:
                    final_analysis = basic_analysis + f"\n\n[AI增强分析暂时不可用，已为您提供基础分析]"

            # 保存占卜记录
            if request.user.is_authenticated:
                DivinationRecord.objects.create(
                    user=request.user,
                    divination_type='bazi',
                    result=final_analysis,
                    ai_enhanced=ai_mode
                )
                from core.models import Notification
                Notification.objects.create(
                    user=request.user,
                    title='八字分析完成',
                    message=f'您的{"AI增强" if ai_mode else ""}八字分析报告已生成完成。',
                    notification_type='success'
                )

            return JsonResponse({
                'success': True,
                'bazi': bazi_result['bazi_string'],
                'analysis': final_analysis,
                'ai_enhanced': ai_mode,
                'detail_info': {
                    'shengxiao': bazi_result['shengxiao'],
                    'wuxing_count': bazi_result['wuxing_count'],
                    'geju': bazi_result['geju']
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'分析过程中出现错误：{str(e)}'})
    return JsonResponse({'success': False, 'error': '请求方法错误'})

@csrf_exempt
@check_usage_limit
@membership_info
def bazi_marriage_api(request):
    """八字合婚API - 支持普通模式和AI增强模式"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            male_birth_time = data.get('male_birth_time')
            female_birth_time = data.get('female_birth_time')
            male_name = data.get('male_name', '男方')
            female_name = data.get('female_name', '女方')
            ai_mode = data.get('ai_mode', False)

            # 检查AI模式权限
            if ai_mode and request.user.is_authenticated:
                profile, _ = UserProfile.objects.get_or_create(user=request.user)
                if not profile.can_use_ai():
                    return JsonResponse({'success': False, 'error': 'AI增强分析仅限会员使用，请升级会员后再试。'})

            # 解析出生时间
            try:
                if isinstance(male_birth_time, str):
                    male_dt = datetime.fromisoformat(male_birth_time.replace('Z', '+00:00'))
                else:
                    male_dt = datetime.now()
                    
                if isinstance(female_birth_time, str):
                    female_dt = datetime.fromisoformat(female_birth_time.replace('Z', '+00:00'))
                else:
                    female_dt = datetime.now()
            except:
                return JsonResponse({'success': False, 'error': '出生时间格式错误'})

            # 八字合婚计算
            marriage_result = bazi_calculator.calculate_marriage_compatibility(male_dt, female_dt)
            
            # 基础分析结果
            basic_analysis = f"""
【八字合婚分析报告】

【基本信息】
{male_name}：{marriage_result['male_info']['bazi_string']['year']} {marriage_result['male_info']['bazi_string']['month']} {marriage_result['male_info']['bazi_string']['day']} {marriage_result['male_info']['bazi_string']['hour']}
生肖：{marriage_result['male_info']['shengxiao']}  五行：{bazi_calculator.WUXING_TIANGAN[marriage_result['male_info']['ri_zhu']]}

{female_name}：{marriage_result['female_info']['bazi_string']['year']} {marriage_result['female_info']['bazi_string']['month']} {marriage_result['female_info']['bazi_string']['day']} {marriage_result['female_info']['bazi_string']['hour']}
生肖：{marriage_result['female_info']['shengxiao']}  五行：{bazi_calculator.WUXING_TIANGAN[marriage_result['female_info']['ri_zhu']]}

【匹配度评分】
综合匹配度：{marriage_result['compatibility_score']:.1f}分

【详细分析】
生肖配对：{marriage_result['zodiac_compatibility']['score']}分 - {marriage_result['zodiac_compatibility']['description']}
五行互补：{marriage_result['wuxing_compatibility']['score']}分 - {marriage_result['wuxing_compatibility']['description']}
性格匹配：{marriage_result['personality_match']['score']}分 - {marriage_result['personality_match']['description']}

【合婚建议】
{marriage_result['marriage_advice']}

【注意事项】
- 夫妻相处要互相理解包容
- 保持良好的沟通和信任
- 在重要决策上多商量讨论
- 彼此支持对方的事业发展

* 以上合婚分析基于传统命理学，仅供参考娱乐。
            """

            # AI增强分析
            final_analysis = basic_analysis
            if ai_mode and request.user.is_authenticated:
                try:
                    marriage_info = {
                        'male_birth_time': male_birth_time,
                        'female_birth_time': female_birth_time,
                        'male_name': male_name,
                        'female_name': female_name
                    }
                    ai_analysis = ai_service.enhance_marriage_analysis(
                        marriage_result,
                        basic_analysis,
                        marriage_info
                    )
                    final_analysis = ai_analysis
                    profile.ai_usage_count += 1
                    profile.save()
                except Exception as e:
                    final_analysis = basic_analysis + f"\n\n[AI增强分析暂时不可用，已为您提供基础分析]"

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
                    message=f'{male_name}与{female_name}的{"AI增强" if ai_mode else ""}八字合婚分析已完成。',
                    notification_type='success'
                )

            return JsonResponse({
                'success': True,
                'compatibility_score': marriage_result['compatibility_score'],
                'analysis': final_analysis,
                'ai_enhanced': ai_mode,
                'detail_info': {
                    'male_shengxiao': marriage_result['male_info']['shengxiao'],
                    'female_shengxiao': marriage_result['female_info']['shengxiao'],
                    'zodiac_score': marriage_result['zodiac_compatibility']['score'],
                    'wuxing_score': marriage_result['wuxing_compatibility']['score']
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'合婚分析过程中出现错误：{str(e)}'})
    return JsonResponse({'success': False, 'error': '请求方法错误'})

@csrf_exempt
@check_usage_limit
@membership_info
def tarot_api(request):
    """塔罗占卜API"""
    if request.method == 'POST':
        data = json.loads(request.body)
        question = data.get('question', '')
        
        # 随机选择3张塔罗牌
        tarot_cards = [
            {'name': '愚者', 'meaning': '新的开始，纯真，自发性'},
            {'name': '魔术师', 'meaning': '意志力，创造力，技能'},
            {'name': '女祭司', 'meaning': '直觉，神秘，内在智慧'},
            {'name': '皇后', 'meaning': '丰富，母性，自然'},
            {'name': '皇帝', 'meaning': '权威，秩序，控制'},
            {'name': '教皇', 'meaning': '传统，宗教，学习'},
            {'name': '恋人', 'meaning': '爱情，和谐，关系'},
            {'name': '战车', 'meaning': '胜利，控制，意志力'},
            {'name': '力量', 'meaning': '勇气，耐心，温柔'},
            {'name': '隐者', 'meaning': '内省，寻求，指导'},
        ]
        
        selected_cards = random.sample(tarot_cards, 3)
        
        interpretation = f"""
        针对您的问题："{question}"
        
        过去 - {selected_cards[0]['name']}：{selected_cards[0]['meaning']}
        现在 - {selected_cards[1]['name']}：{selected_cards[1]['meaning']}
        未来 - {selected_cards[2]['name']}：{selected_cards[2]['meaning']}
        
        综合解读：
        您的情况正在经历重要的转变期。过去的经历为您积累了宝贵的智慧，
        现在是时候运用这些智慧来面对当前的挑战。未来充满机遇，
        只要保持积极的心态和坚定的信念，您将会取得成功。
        """
          # 保存占卜记录
        if request.user.is_authenticated:
            DivinationRecord.objects.create(
                user=request.user,
                divination_type='tarot',
                question=question,
                result=interpretation
            )
            
            # 创建占卜完成通知
            from core.models import Notification
            Notification.objects.create(
                user=request.user,
                title='塔罗占卜完成',
                message=f'您关于"{question[:20]}..."的塔罗占卜已完成，快来查看结果吧！',
                notification_type='success'
            )
        
        return JsonResponse({
            'success': True,
            'cards': selected_cards,
            'interpretation': interpretation
        })
    
    return JsonResponse({'success': False, 'error': '请求方法错误'})

@csrf_exempt
@check_usage_limit
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
            result = calculator.calculate_hexagram(number1, number2, question)
            
            # AI增强分析
            if ai_mode:
                try:
                    from core.ai_service import AIService
                    ai_service = AIService()
                    ai_analysis = ai_service.enhance_meihua_analysis(
                        question=question,
                        main_gua=result['main_gua'],
                        bian_gua=result['bian_gua'],
                        dong_yao=result['dong_yao'],
                        basic_analysis=result['analysis']
                    )
                    
                    # 更新用户AI使用次数
                    user_profile.ai_usage_count += 1
                    user_profile.save()
                    
                    final_analysis = ai_analysis
                except Exception as e:
                    # AI服务失败时使用基础分析
                    final_analysis = result['analysis']
                    ai_mode = False
            else:
                final_analysis = result['analysis']
            
            # 保存占卜记录
            if request.user.is_authenticated:
                DivinationRecord.objects.create(
                    user=request.user,
                    divination_type='meihua',
                    question=question,
                    result=final_analysis,
                    ai_enhanced=ai_mode
                )
                
                # 创建通知
                from core.models import Notification
                Notification.objects.create(
                    user=request.user,
                    title='梅花易数完成',
                    message=f'您关于"{question[:20]}..."的{"AI增强" if ai_mode else ""}梅花易数占卜已完成。',
                    notification_type='success'
                )
            
            return JsonResponse({
                'success': True,
                'main_gua': result['main_gua'],
                'bian_gua': result['bian_gua'],
                'dong_yao': result['dong_yao'],
                'analysis': final_analysis,
                'ai_enhanced': ai_mode,
                'detail_info': {
                    'main_gua_name': result['main_gua']['name'],
                    'bian_gua_name': result['bian_gua']['name'],
                    'time_info': result['time_info']
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'梅花易数分析过程中出现错误：{str(e)}'})
    return JsonResponse({'success': False, 'error': '请求方法错误'})

@csrf_exempt
@check_usage_limit
@membership_info
def yijing_api(request):
    """易经卜卦API - 支持普通模式和AI增强模式"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question', '')
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
            
            # 64卦数据（简化版）
            hexagram_data = [
                {'name': '乾', 'number': 1, 'lines': [1,1,1,1,1,1], 'meaning': '刚健中正', 'judgment': '元亨利贞'},
                {'name': '坤', 'number': 2, 'lines': [0,0,0,0,0,0], 'meaning': '柔顺厚德', 'judgment': '利牝马之贞'},
                {'name': '屯', 'number': 3, 'lines': [1,0,0,0,1,0], 'meaning': '始生之难', 'judgment': '元亨利贞'},
                {'name': '蒙', 'number': 4, 'lines': [0,1,0,0,0,1], 'meaning': '启蒙教育', 'judgment': '亨'},
                {'name': '需', 'number': 5, 'lines': [1,1,1,0,1,0], 'meaning': '需要等待', 'judgment': '有孚，光亨'},
                {'name': '讼', 'number': 6, 'lines': [0,1,0,1,1,1], 'meaning': '争讼纠纷', 'judgment': '有孚，窒'},
                {'name': '师', 'number': 7, 'lines': [0,1,0,0,0,0], 'meaning': '军队出征', 'judgment': '贞，丈人吉'},
                {'name': '比', 'number': 8, 'lines': [0,0,0,0,1,0], 'meaning': '亲密团结', 'judgment': '吉'}
            ]
            
            # 随机选择一个卦象
            selected_hexagram = random.choice(hexagram_data)
            
            # 生成基础解读
            basic_interpretation = f"""
【卦象信息】
卦名：{selected_hexagram['name']}卦（第{selected_hexagram['number']}卦）
卦意：{selected_hexagram['meaning']}
卦辞：{selected_hexagram['judgment']}

【卦象分析】
针对您的问题"{question}"，得到{selected_hexagram['name']}卦。此卦象征着{selected_hexagram['meaning']}的状态。

【现状分析】
当前情况呈现出{selected_hexagram['name']}卦的特征，表明您正处在一个{selected_hexagram['meaning']}的阶段。这提示您需要以相应的态度和方式来应对当前的局面。

【发展趋势】
根据卦象显示，未来的发展方向总体是{'积极向上' if '亨' in selected_hexagram['judgment'] or '吉' in selected_hexagram['judgment'] else '需要谨慎应对'}的。

【行动建议】
建议您在处理相关事务时，要把握好分寸，顺应自然规律，以诚待人，以正行事。

【总结】
易经提醒我们，万事万物都在变化之中，把握变化的规律，顺应天道，是获得成功的关键。希望这次卜卦能为您提供有益的启示。

* 易经卜卦仅供参考娱乐，人生路上还需理性思考，积极行动。
            """
            
            # AI增强分析
            final_interpretation = basic_interpretation
            if ai_mode:
                try:
                    from core.ai_service import AIService
                    ai_service = AIService()
                    
                    # 构建卦象信息字符串用于AI分析
                    hexagram_info = {
                        'name': selected_hexagram['name'],
                        'number': selected_hexagram['number'],
                        'meaning': selected_hexagram['meaning'],
                        'judgment': selected_hexagram['judgment'],
                        'lines': selected_hexagram['lines']
                    }
                    
                    ai_interpretation = ai_service.enhance_yijing_analysis(
                        question=question,
                        hexagram_info=hexagram_info,
                        basic_analysis=basic_interpretation
                    )
                    
                    # 更新用户AI使用次数
                    if request.user.is_authenticated:
                        user_profile = request.user.userprofile
                        user_profile.ai_usage_count += 1
                        user_profile.save()
                    
                    final_interpretation = ai_interpretation
                except Exception as e:
                    # AI服务失败时使用基础分析
                    final_interpretation = basic_interpretation
                    ai_mode = False
            
            # 保存占卜记录
            if request.user.is_authenticated:
                DivinationRecord.objects.create(
                    user=request.user,
                    divination_type='yijing',
                    question=question,
                    result=final_interpretation,
                    ai_enhanced=ai_mode
                )
                
                # 创建占卜完成通知
                from core.models import Notification
                Notification.objects.create(
                    user=request.user,
                    title='易经卜卦完成',
                    message=f'您关于"{question[:20]}..."的{"AI增强" if ai_mode else ""}易经卜卦已完成，得到{selected_hexagram["name"]}卦！',
                    notification_type='success'
                )
            
            return JsonResponse({
                'success': True,
                'hexagram': selected_hexagram,
                'interpretation': final_interpretation,
                'ai_enhanced': ai_mode,
                'detail_info': {
                    'hexagram_name': selected_hexagram['name'],
                    'hexagram_number': selected_hexagram['number'],
                    'hexagram_meaning': selected_hexagram['meaning']
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'易经卜卦过程中出现错误：{str(e)}'})
    
    return JsonResponse({'success': False, 'error': '请求方法错误'})

@csrf_exempt
@check_usage_limit
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
            
            # 使用运势计算器
            from core.fortune_calculator import FortuneCalculator
            calculator = FortuneCalculator()
            result = calculator.calculate_daily_fortune(birth_date)
            
            # AI增强分析
            if ai_mode:
                try:
                    from core.ai_service import AIService
                    ai_service = AIService()
                    ai_analysis = ai_service.enhance_daily_fortune_analysis(
                        birth_date=birth_date,
                        zodiac=result['zodiac'],
                        fortune_scores=result['fortune_scores'],
                        basic_analysis=result['analysis']
                    )
                    
                    # 更新用户AI使用次数
                    user_profile.ai_usage_count += 1
                    user_profile.save()
                    
                    final_analysis = ai_analysis
                except Exception as e:
                    # AI服务失败时使用基础分析
                    final_analysis = result['analysis']
                    ai_mode = False
            else:
                final_analysis = result['analysis']
            
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
            from datetime import datetime
            today = datetime.now().date()
            
            fortune_record, created = DailyFortune.objects.get_or_create(
                date=today,
                zodiac=result['zodiac'],
                defaults={
                    'overall_score': result['fortune_scores']['overall'],
                    'love_score': result['fortune_scores']['love'],
                    'career_score': result['fortune_scores']['career'],
                    'wealth_score': result['fortune_scores']['wealth'],
                    'health_score': result['fortune_scores']['health'],
                    'lucky_color': result['lucky_elements']['color'],
                    'lucky_number': result['lucky_elements']['number'],
                    'lucky_direction': result['lucky_elements']['direction'],
                    'description': final_analysis
                }
            )
            
            return JsonResponse({
                'success': True,
                'zodiac': result['zodiac'],
                'fortune_scores': result['fortune_scores'],
                'lucky_elements': result['lucky_elements'],
                'analysis': final_analysis,
                'ai_enhanced': ai_mode,
                'detail_info': {
                    'date': today.strftime('%Y-%m-%d'),
                    'wuxing_analysis': result.get('wuxing_analysis', ''),
                    'advice': result.get('advice', '')
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'运势分析过程中出现错误：{str(e)}'})
    return JsonResponse({'success': False, 'error': '请求方法错误'})

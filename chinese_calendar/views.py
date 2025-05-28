from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, date, timedelta
import random
from .models import ChineseCalendarDay, SolarTerm

def calendar_view(request):
    """黄历页面"""
    today = date.today()
    
    # 获取本月的黄历信息
    month_start = today.replace(day=1)
    next_month = month_start.replace(month=month_start.month + 1) if month_start.month < 12 else month_start.replace(year=month_start.year + 1, month=1)
    month_end = next_month - timedelta(days=1)
    
    # 生成本月的日期信息
    month_days = []
    current_date = month_start
    while current_date <= month_end:
        day_info = get_day_info(current_date)
        month_days.append(day_info)
        current_date += timedelta(days=1)
    
    return render(request, 'chinese_calendar/calendar.html', {
        'page_title': '黄历查询',
        'today': today,
        'month_days': month_days,
        'current_month': today.strftime('%Y年%m月')
    })

def get_day_info(target_date):
    """获取指定日期的黄历信息"""
    # 天干地支
    tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 简化的天干地支计算
    days_since_base = (target_date - date(1900, 1, 1)).days
    tg_index = (days_since_base + 6) % 10  # 调整基准
    dz_index = (days_since_base + 8) % 12  # 调整基准
    
    # 农历月份和日期（简化模拟）
    lunar_months = ["正月", "二月", "三月", "四月", "五月", "六月", 
                   "七月", "八月", "九月", "十月", "十一月", "腊月"]
    lunar_days = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
                 "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
                 "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
    
    # 模拟农历日期
    lunar_month_idx = (target_date.month - 1) % 12
    lunar_day_idx = (target_date.day - 1) % 30
    
    # 宜忌活动
    suitable_list = [
        "祭祀", "祈福", "求嗣", "开光", "塑绘", "斋醮", "订盟", "纳采", "嫁娶", "动土",
        "修造", "安门", "安床", "移徙", "入宅", "安香", "开市", "立券", "纳财", "沐浴",
        "理发", "造船", "乘船", "牧养", "畋猎", "栽种", "破土", "安葬", "启钻", "修坟"
    ]
    
    avoid_list = [
        "嫁娶", "动土", "开市", "安葬", "行丧", "修坟", "破土", "安门", "理发", "冠笄",
        "伐木", "开柱眼", "穿井", "拆卸", "栽种", "治病", "作灶", "船只", "词讼"
    ]
    
    # 随机选择宜忌（实际应该根据具体算法）
    suitable = random.sample(suitable_list, random.randint(3, 6))
    avoid = random.sample(avoid_list, random.randint(2, 5))
    
    # 星座计算
    constellations = [
        ("摩羯座", (12, 22), (1, 19)),
        ("水瓶座", (1, 20), (2, 18)),
        ("双鱼座", (2, 19), (3, 20)),
        ("白羊座", (3, 21), (4, 19)),
        ("金牛座", (4, 20), (5, 20)),
        ("双子座", (5, 21), (6, 21)),
        ("巨蟹座", (6, 22), (7, 22)),
        ("狮子座", (7, 23), (8, 22)),
        ("处女座", (8, 23), (9, 22)),
        ("天秤座", (9, 23), (10, 23)),
        ("天蝎座", (10, 24), (11, 22)),
        ("射手座", (11, 23), (12, 21))
    ]
    
    constellation = "未知"
    for name, (start_month, start_day), (end_month, end_day) in constellations:
        if ((target_date.month == start_month and target_date.day >= start_day) or
            (target_date.month == end_month and target_date.day <= end_day)):
            constellation = name
            break
    
    return {
        'date': target_date,
        'lunar_year': f"甲辰年",  # 简化，实际需要计算
        'lunar_month': lunar_months[lunar_month_idx],
        'lunar_day': lunar_days[lunar_day_idx],
        'tiangan': tiangan[tg_index],
        'dizhi': dizhi[dz_index],
        'ganzhi': tiangan[tg_index] + dizhi[dz_index],
        'constellation': constellation,
        'suitable_activities': ", ".join(suitable),
        'avoid_activities': ", ".join(avoid),
        'is_today': target_date == date.today(),
        'weekday': target_date.strftime('%A'),
        'weekday_cn': ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][target_date.weekday()]
    }

def today_fortune(request):
    """今日运势"""
    today = date.today()
    try:
        calendar_day = ChineseCalendarDay.objects.get(date=today)
    except ChineseCalendarDay.DoesNotExist:
        # 如果没有数据，创建一个示例
        calendar_day = ChineseCalendarDay(
            date=today,
            lunar_year="甲辰年",
            lunar_month="四月",
            lunar_day="廿一",
            tiangan="甲",
            dizhi="子",
            constellation="双子座",
            suitable_activities="祭祀，祈福，订盟，纳采，裁衣，合帐，冠笄",
            avoid_activities="开市，安床，安葬，入殓"
        )
    
    return render(request, 'chinese_calendar/today.html', {
        'page_title': '今日运势',
        'calendar_day': calendar_day
    })

def date_info_api(request, date_str):
    """日期信息API"""
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # 模拟农历数据
        lunar_months = ["正月", "二月", "三月", "四月", "五月", "六月", 
                       "七月", "八月", "九月", "十月", "十一月", "十二月"]
        lunar_days = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
                     "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
                     "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
        
        calendar_info = {
            'date': date_str,
            'lunar_year': '甲辰年',
            'lunar_month': lunar_months[target_date.month - 1],
            'lunar_day': lunar_days[target_date.day - 1],
            'tiangan': '甲',
            'dizhi': '子',
            'suitable': ['祭祀', '祈福', '纳采', '嫁娶', '安床'],
            'avoid': ['开市', '动土', '破土', '安葬'],
            'constellation': '双子座'
        }
        
        return JsonResponse({
            'success': True,
            'data': calendar_info
        })
    except ValueError:
        return JsonResponse({
            'success': False,
            'error': '日期格式错误'
        })

def calendar_api(request, date_str):
    """黄历详细信息API"""
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # 模拟黄历数据
        data = {
            'date': date_str,
            'lunar_date': '甲辰年 庚申月 丁卯日',
            'ganzhi': '甲辰年 庚申月 丁卯日',
            'constellation': '天秤座',
            'solar_term': '寒露',
            'wuxing': '木',
            'prosperity': '旺',
            'lucky_number': '3, 8',
            'suitable': ['祈福', '订盟', '纳采', '裁衣', '合帐', '冠笄'],
            'avoid': ['安葬', '掘井', '伐木', '破土', '启钻', '安门']
        }
        
        return JsonResponse(data)
        
    except ValueError:
        return JsonResponse({'error': '日期格式错误'}, status=400)

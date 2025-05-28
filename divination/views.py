from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import random
from datetime import datetime
from .models import TarotCard, IChingHexagram, BaziElement
from core.models import DivinationRecord

def bazi_analysis(request):
    """八字分析页面"""
    return render(request, 'divination/bazi.html', {'page_title': '八字分析'})

def meihua_yishu(request):
    """梅花易数页面"""
    return render(request, 'divination/meihua.html', {'page_title': '梅花易数'})

def tarot_reading(request):
    """塔罗占卜页面"""
    return render(request, 'divination/tarot.html', {'page_title': '塔罗占卜'})

def yijing_divination(request):
    """易经卜卦页面"""
    return render(request, 'divination/yijing.html', {'page_title': '易经卜卦'})

@csrf_exempt
def bazi_api(request):
    """八字分析API"""
    if request.method == 'POST':
        data = json.loads(request.body)
        birth_time = data.get('birth_time')
        gender = data.get('gender', '男')
        
        # 解析出生时间
        try:
            birth_dt = datetime.fromisoformat(birth_time.replace('Z', '+00:00'))
        except:
            birth_dt = datetime.now()
        
        # 八字计算的简化版本
        tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        
        # 基于出生时间的简化计算
        year_tg = tiangan[(birth_dt.year - 4) % 10]
        year_dz = dizhi[(birth_dt.year - 4) % 12]
        month_tg = tiangan[(birth_dt.month - 1 + (birth_dt.year - 1900) * 12) % 10]
        month_dz = dizhi[(birth_dt.month - 1) % 12]
        day_tg = tiangan[(birth_dt.day - 1 + birth_dt.month * 30) % 10]
        day_dz = dizhi[(birth_dt.day - 1) % 12]
        hour_tg = tiangan[(birth_dt.hour // 2) % 10]
        hour_dz = dizhi[(birth_dt.hour // 2) % 12]
        
        bazi = {
            'year': year_tg + year_dz,
            'month': month_tg + month_dz,
            'day': day_tg + day_dz,
            'hour': hour_tg + hour_dz
        }
        
        # 五行分析
        wuxing_map = {
            '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
            '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'
        }
        
        day_master = day_tg  # 日主
        day_master_wuxing = wuxing_map[day_master]
        
        # 生成个性化分析
        personality_traits = {
            '木': ['仁慈善良', '积极向上', '有责任感', '创造力强'],
            '火': ['热情开朗', '积极主动', '善于表达', '有领导力'],
            '土': ['稳重踏实', '诚实可靠', '包容性强', '有耐心'],
            '金': ['果断刚毅', '组织能力强', '追求完美', '重视秩序'],
            '水': ['聪明智慧', '善于变通', '直觉敏锐', '富有想象力']
        }
        
        career_advice = {
            '木': ['教育培训', '医疗保健', '文化艺术', '环保绿化'],
            '火': ['销售市场', '传媒娱乐', '电子科技', '金融投资'],
            '土': ['建筑工程', '农业种植', '房地产', '行政管理'],
            '金': ['金融银行', '机械制造', '法律执法', '军事安全'],
            '水': ['交通运输', '水利工程', '信息技术', '贸易物流']
        }
        
        traits = personality_traits.get(day_master_wuxing, ['性格独特'])
        careers = career_advice.get(day_master_wuxing, ['发展前景广阔'])
        
        analysis = f"""
【八字排盘】
年柱：{bazi['year']}    月柱：{bazi['month']}    日柱：{bazi['day']}    时柱：{bazi['hour']}

【命理分析】
日主为{day_master}，五行属{day_master_wuxing}。

【性格特点】
- {traits[0]}，天生具有{day_master_wuxing}的特质
- {traits[1]}，在人际交往中表现突出
- {traits[2]}，做事有始有终
- {traits[3]}，具有独特的个人魅力

【事业运势】
- 适合从事{careers[0]}相关工作
- {careers[1]}领域有较好发展前景
- {careers[2]}方面能发挥所长
- 建议在{careers[3]}方向深入发展

【财运分析】
- 以{day_master_wuxing}为财源，宜稳健理财
- 避免冲动投资，适合长期投资计划
- 中年后财运逐步提升
- 注意理财规划，积少成多

【感情运势】
- 重视感情，对待爱情认真专一
- 适合与五行互补的对象结合
- 家庭观念重，是顾家的好伴侣
- 子女缘分深厚，家庭和睦

【健康提醒】
- 注意{day_master_wuxing}脏腑的保养
- 保持规律作息，适量运动
- 心情开朗有助身体健康
- 定期体检，预防胜于治疗

【开运建议】
- 多接触{day_master_wuxing}属性的事物
- 选择适合的颜色和方位
- 佩戴相应的开运饰品
- 保持积极乐观的心态
        """
          # 保存占卜记录
        if request.user.is_authenticated:
            DivinationRecord.objects.create(
                user=request.user,
                divination_type='bazi',
                result=analysis
            )
            
            # 创建占卜完成通知
            from core.models import Notification
            Notification.objects.create(
                user=request.user,
                title='八字分析完成',
                message='您的八字分析报告已生成，可在个人档案中查看详细结果。',
                notification_type='success'
            )
        
        return JsonResponse({
            'success': True,
            'bazi': bazi,
            'analysis': analysis
        })
    
    return JsonResponse({'success': False, 'error': '请求方法错误'})

@csrf_exempt
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

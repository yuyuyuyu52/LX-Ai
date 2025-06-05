# -*- coding: utf-8 -*-
"""
梅花易数和每日运势算法
"""

import random
from datetime import datetime, timedelta

class MeihuaCalculator:
    """梅花易数计算器"""
    
    # 八卦基本信息
    BAGUA = {
        0: {'name': '坤', 'symbol': '☷', 'nature': '地', 'attribute': '顺', 'wuxing': '土'},
        1: {'name': '艮', 'symbol': '☶', 'nature': '山', 'attribute': '止', 'wuxing': '土'},
        2: {'name': '坎', 'symbol': '☵', 'nature': '水', 'attribute': '陷', 'wuxing': '水'},
        3: {'name': '巽', 'symbol': '☴', 'nature': '风', 'attribute': '入', 'wuxing': '木'},
        4: {'name': '震', 'symbol': '☳', 'nature': '雷', 'attribute': '动', 'wuxing': '木'},
        5: {'name': '离', 'symbol': '☲', 'nature': '火', 'attribute': '丽', 'wuxing': '火'},
        6: {'name': '兑', 'symbol': '☱', 'nature': '泽', 'attribute': '悦', 'wuxing': '金'},
        7: {'name': '乾', 'symbol': '☰', 'nature': '天', 'attribute': '健', 'wuxing': '金'}
    }
    
    # 64卦名称
    HEXAGRAM_NAMES = [
        '坤为地', '山地剥', '水地比', '风地观', '雷地豫', '火地晋', '泽地萃', '天地否',
        '地山谦', '艮为山', '水山蹇', '风山渐', '雷山小过', '火山旅', '泽山咸', '天山遁',
        '地水师', '山水蒙', '坎为水', '风水涣', '雷水解', '火水未济', '泽水困', '天水讼',
        '地风升', '山风蛊', '水风井', '巽为风', '雷风恒', '火风鼎', '泽风大过', '天风姤',
        '地雷复', '山雷颐', '水雷屯', '风雷益', '震为雷', '火雷噬嗑', '泽雷随', '天雷无妄',
        '地火明夷', '山火贲', '水火既济', '风火家人', '雷火丰', '离为火', '泽火革', '天火同人',
        '地泽临', '山泽损', '水泽节', '风泽中孚', '雷泽归妹', '火泽睽', '兑为泽', '天泽履',
        '地天泰', '山天大畜', '水天需', '风天小畜', '雷天大壮', '火天大有', '泽天夬', '乾为天'
    ]
    
    def __init__(self):
        pass
    
    def calculate_meihua(self, question, timestamp=None):
        """
        梅花易数计算
        
        Args:
            question: 问题
            timestamp: 时间戳（可选）
        
        Returns:
            dict: 卦象分析结果
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        # 基于时间起卦
        year = timestamp.year
        month = timestamp.month
        day = timestamp.day
        hour = timestamp.hour
        minute = timestamp.minute
        
        # 计算上卦（年+月+日）
        upper_num = (year + month + day) % 8
        upper_gua = self.BAGUA[upper_num]
        
        # 计算下卦（年+月+日+时）
        lower_num = (year + month + day + hour) % 8
        lower_gua = self.BAGUA[lower_num]
        
        # 计算动爻（年+月+日+时+分）
        dong_yao = ((year + month + day + hour + minute) % 6) + 1
        
        # 计算主卦卦数
        zhu_gua_num = upper_num * 8 + lower_num
        zhu_gua_name = self.HEXAGRAM_NAMES[zhu_gua_num]
        
        # 计算变卦
        bian_upper = upper_num
        bian_lower = lower_num
        
        # 根据动爻位置调整变卦
        if dong_yao <= 3:  # 动爻在下卦
            bian_lower = (lower_num + 1) % 8
        else:  # 动爻在上卦
            bian_upper = (upper_num + 1) % 8
        
        bian_gua_num = bian_upper * 8 + bian_lower
        bian_gua_name = self.HEXAGRAM_NAMES[bian_gua_num]
        
        # 体用分析
        ti_yong_analysis = self._analyze_ti_yong(upper_gua, lower_gua, dong_yao)
        
        # 五行分析
        wuxing_analysis = self._analyze_wuxing(upper_gua, lower_gua)
        
        # 时间预测
        time_prediction = self._predict_time(ti_yong_analysis, wuxing_analysis)
        
        result = {
            'zhu_gua': {
                'name': zhu_gua_name,
                'number': zhu_gua_num,
                'upper': upper_gua,
                'lower': lower_gua
            },
            'bian_gua': {
                'name': bian_gua_name,
                'number': bian_gua_num,
                'upper': self.BAGUA[bian_upper],
                'lower': self.BAGUA[bian_lower]
            },
            'dong_yao': dong_yao,
            'ti_yong': ti_yong_analysis,
            'wuxing': wuxing_analysis,
            'time_prediction': time_prediction,
            'question': question,
            'timestamp': timestamp
        }
        
        return result
    
    def _analyze_ti_yong(self, upper_gua, lower_gua, dong_yao):
        """分析体用关系"""
        if dong_yao <= 3:
            # 动爻在下卦，下卦为用，上卦为体
            ti_gua = upper_gua
            yong_gua = lower_gua
        else:
            # 动爻在上卦，上卦为用，下卦为体
            ti_gua = lower_gua
            yong_gua = upper_gua
        
        # 分析体用生克关系
        ti_wuxing = ti_gua['wuxing']
        yong_wuxing = yong_gua['wuxing']
        
        relation = self._get_wuxing_relation(yong_wuxing, ti_wuxing)
        
        return {
            'ti_gua': ti_gua,
            'yong_gua': yong_gua,
            'relation': relation,
            'analysis': self._interpret_ti_yong_relation(relation)
        }
    
    def _analyze_wuxing(self, upper_gua, lower_gua):
        """五行分析"""
        upper_wuxing = upper_gua['wuxing']
        lower_wuxing = lower_gua['wuxing']
        
        # 分析上下卦五行关系
        relation = self._get_wuxing_relation(upper_wuxing, lower_wuxing)
        
        return {
            'upper_wuxing': upper_wuxing,
            'lower_wuxing': lower_wuxing,
            'relation': relation,
            'analysis': self._interpret_wuxing_relation(relation, upper_wuxing, lower_wuxing)
        }
    
    def _get_wuxing_relation(self, from_element, to_element):
        """获取五行关系"""
        # 五行相生：木生火，火生土，土生金，金生水，水生木
        sheng_relations = {
            ('木', '火'): '生', ('火', '土'): '生', ('土', '金'): '生',
            ('金', '水'): '生', ('水', '木'): '生'
        }
        
        # 五行相克：木克土，土克水，水克火，火克金，金克木
        ke_relations = {
            ('木', '土'): '克', ('土', '水'): '克', ('水', '火'): '克',
            ('火', '金'): '克', ('金', '木'): '克'
        }
        
        if from_element == to_element:
            return '同'
        elif (from_element, to_element) in sheng_relations:
            return '生'
        elif (from_element, to_element) in ke_relations:
            return '克'
        else:
            return '泄'  # 被生即为泄
    
    def _interpret_ti_yong_relation(self, relation):
        """解释体用关系"""
        interpretations = {
            '生': '用生体，大吉之象。表示事情发展顺利，有贵人相助，外部环境对自身有利。建议把握机会，积极进取，但也要注意不要过于依赖外部助力。',
            '克': '用克体，不利之象。表示事情阻碍较多，外部环境对自身不利。建议谨慎行事，避免正面冲突，可以采取迂回策略，等待时机。',
            '同': '体用同类，平稳之象。表示事情发展平缓，内外力量平衡。建议按部就班，循序渐进，保持稳定发展，不宜冒进。',
            '泄': '体生用，有耗损之象。表示付出较多，收获相对较少。建议量力而行，注意节约资源，避免过度消耗，可以适当调整策略。'
        }
        return interpretations.get(relation, '体用关系复杂，需要结合具体卦象和动爻位置综合分析。')
    
    def _interpret_wuxing_relation(self, relation, upper_element, lower_element):
        """解释五行关系"""
        interpretations = {
            '生': f'{upper_element}生{lower_element}，上下和谐，发展顺利。表示上层力量滋养下层，整体发展良好。建议顺势而为，把握机遇。',
            '克': f'{upper_element}克{lower_element}，上压下制，需要调和。表示上层力量压制下层，可能造成内部矛盾。建议寻找平衡点，化解冲突。',
            '同': f'上下同为{upper_element}，力量集中，但需防过犹不及。表示力量过于集中，可能造成失衡。建议适当分散，保持平衡。',
            '泄': f'{lower_element}泄{upper_element}，下耗上力，注意节制。表示下层消耗上层力量，需要控制。建议合理分配资源，避免过度消耗。'
        }
        return interpretations.get(relation, '五行关系复杂，需要结合具体卦象和动爻位置综合分析。')
    
    def _predict_time(self, ti_yong_analysis, wuxing_analysis):
        """预测时间"""
        relation = ti_yong_analysis['relation']
        wuxing_relation = wuxing_analysis['relation']
        
        # 基础时间预测
        base_predictions = {
            '生': '1-3个月内见效果，春夏季更佳。',
            '克': '3-6个月内需谨慎，秋冬季注意。',
            '同': '2-4个月内平稳发展。',
            '泄': '4-8个月内需要耐心等待。'
        }
        
        # 五行关系对时间的影响
        wuxing_time_effects = {
            '生': '时间可能提前，进展加快。',
            '克': '时间可能延长，进展受阻。',
            '同': '时间相对稳定，按预期发展。',
            '泄': '时间可能延长，需要更多耐心。'
        }
        
        base_time = base_predictions.get(relation, '时间难以确定，建议综合考虑。')
        wuxing_effect = wuxing_time_effects.get(wuxing_relation, '')
        
        # 结合体用关系和五行关系给出更详细的时间预测
        detailed_prediction = f"{base_time}\n{wuxing_effect}\n"
        
        # 根据五行属性给出具体建议
        upper_wuxing = wuxing_analysis['upper_wuxing']
        lower_wuxing = wuxing_analysis['lower_wuxing']
        
        wuxing_timing = {
            '木': '春季（2-4月）',
            '火': '夏季（5-7月）',
            '土': '长夏（7-9月）',
            '金': '秋季（8-10月）',
            '水': '冬季（11-1月）'
        }
        
        detailed_prediction += f"建议关注{wuxing_timing.get(upper_wuxing, '')}和{wuxing_timing.get(lower_wuxing, '')}的时间节点。"
        
        return detailed_prediction


class FortuneCalculator:
    """每日运势计算器"""
    
    # 生肖对应数字
    ZODIAC_MAP = {
        '鼠': 0, '牛': 1, '虎': 2, '兔': 3, '龙': 4, '蛇': 5,
        '马': 6, '羊': 7, '猴': 8, '鸡': 9, '狗': 10, '猪': 11
    }
    
    # 幸运颜色
    LUCKY_COLORS = ['红色', '蓝色', '绿色', '黄色', '紫色', '白色', '黑色', '粉色', '橙色', '金色']
    
    # 幸运数字
    LUCKY_NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    
    def __init__(self):
        pass
    
    def calculate_daily_fortune(self, zodiac, date=None, user_birth_date=None):
        """
        计算每日运势
        
        Args:
            zodiac: 生肖
            date: 日期（默认今天）
            user_birth_date: 用户出生日期（用于个性化）
        
        Returns:
            dict: 运势结果
        """
        if date is None:
            date = datetime.now().date()
        
        # 基于生肖和日期计算基础运势
        zodiac_num = self.ZODIAC_MAP.get(zodiac, 0)
        date_factor = date.day + date.month * 31 + date.year
        
        # 计算各项运势（1-5星）
        base_seed = zodiac_num * 1000 + date_factor
        
        overall = self._calculate_fortune_score(base_seed, 1)
        love = self._calculate_fortune_score(base_seed, 2)
        career = self._calculate_fortune_score(base_seed, 3)
        wealth = self._calculate_fortune_score(base_seed, 4)
        health = self._calculate_fortune_score(base_seed, 5)
        
        # 幸运元素
        lucky_color = self.LUCKY_COLORS[base_seed % len(self.LUCKY_COLORS)]
        lucky_number = self.LUCKY_NUMBERS[base_seed % len(self.LUCKY_NUMBERS)]
        
        # 生成运势描述
        description = self._generate_fortune_description(
            zodiac, overall, love, career, wealth, health
        )
        
        result = {
            'zodiac': zodiac,
            'date': date,
            'overall_fortune': overall,
            'love_fortune': love,
            'career_fortune': career,
            'wealth_fortune': wealth,
            'health_fortune': health,
            'lucky_color': lucky_color,
            'lucky_number': lucky_number,
            'description': description
        }
        
        return result
    
    def _calculate_fortune_score(self, base_seed, category):
        """计算运势评分（1-5星）"""
        # 使用简单的随机种子算法
        seed = (base_seed + category * 123) % 1000
        
        # 正态分布，让3星概率最高
        if seed < 100:
            return 1
        elif seed < 250:
            return 2
        elif seed < 650:
            return 3
        elif seed < 850:
            return 4
        else:
            return 5
    
    def _generate_fortune_description(self, zodiac, overall, love, career, wealth, health):
        """生成运势描述"""
        descriptions = {
            '鼠': {
                'good': '机智聪明的你今天状态不错，直觉敏锐，适合处理复杂事务。',
                'average': '今天需要多一些耐心，不要急于求成，稳扎稳打更有利。',
                'poor': '今天运势稍显低迷，建议低调行事，避免重大决策。'
            },
            '牛': {
                'good': '踏实稳重的你今天运势良好，坚持努力会有收获。',
                'average': '今天宜守不宜攻，保持现状，等待更好的时机。',
                'poor': '今天可能会遇到一些阻碍，但你的坚韧会帮助你度过难关。'
            },
            '虎': {
                'good': '勇敢果断的你今天充满活力，是展现领导力的好时机。',
                'average': '今天需要控制一下脾气，理性处理问题会更好。',
                'poor': '今天不宜冲动行事，多听取他人意见，谨慎决策。'
            },
            '兔': {
                'good': '温和善良的你今天人缘很好，适合处理人际关系。',
                'average': '今天保持平常心，不要对结果期望过高。',
                'poor': '今天可能会有些敏感，建议多与亲友交流，获得支持。'
            },
            '龙': {
                'good': '自信强势的你今天运势强劲，适合开展新的项目。',
                'average': '今天需要注意细节，不要因为自信而忽略小问题。',
                'poor': '今天不宜太过张扬，低调一些会更安全。'
            },
            '蛇': {
                'good': '智慧深沉的你今天洞察力强，适合分析和规划。',
                'average': '今天保持神秘感，不要过早暴露自己的想法。',
                'poor': '今天可能会有些多疑，建议相信直觉，但也要客观判断。'
            },
            '马': {
                'good': '热情奔放的你今天活力四射，适合户外活动和社交。',
                'average': '今天需要控制节奏，不要太急躁，稳步前进。',
                'poor': '今天可能会感到焦虑不安，建议多做运动释放压力。'
            },
            '羊': {
                'good': '温柔体贴的你今天和谐运强，适合团队合作。',
                'average': '今天不要太过依赖他人，要有自己的主见。',
                'poor': '今天可能会有些犹豫不决，建议相信自己的判断。'
            },
            '猴': {
                'good': '机灵活泼的你今天思维活跃，创意无限，适合创新工作。',
                'average': '今天要专心一致，不要三心二意，专注更重要。',
                'poor': '今天可能会有些浮躁，建议静下心来，仔细思考。'
            },
            '鸡': {
                'good': '勤奋认真的你今天效率很高，适合处理细致的工作。',
                'average': '今天不要过于追求完美，适度就好。',
                'poor': '今天可能会有些挑剔，建议多一些包容和理解。'
            },
            '狗': {
                'good': '忠诚可靠的你今天贵人运旺，会得到他人的帮助。',
                'average': '今天保持诚信，继续发挥你的优势。',
                'poor': '今天可能会有些担忧，但你的善良会为你带来好运。'
            },
            '猪': {
                'good': '善良真诚的你今天福气满满，适合享受生活。',
                'average': '今天保持乐观心态，简单生活就是幸福。',
                'poor': '今天不要太过懒散，适当的努力会改善运势。'
            }
        }
        
        # 根据综合运势选择描述类型
        if overall >= 4:
            base_desc = descriptions.get(zodiac, {}).get('good', '今天运势不错。')
        elif overall >= 3:
            base_desc = descriptions.get(zodiac, {}).get('average', '今天运势平稳。')
        else:
            base_desc = descriptions.get(zodiac, {}).get('poor', '今天需要小心。')
        
        # 添加具体建议
        suggestions = []
        
        if love >= 4:
            suggestions.append('爱情运旺盛，单身者有机会遇到心仪对象，有伴者感情甜蜜。')
        elif love <= 2:
            suggestions.append('感情运势一般，建议多一些耐心和理解。')
        
        if career >= 4:
            suggestions.append('事业运佳，工作效率高，适合推进重要项目。')
        elif career <= 2:
            suggestions.append('工作中可能遇到阻碍，建议谨慎处理，不宜冒进。')
        
        if wealth >= 4:
            suggestions.append('财运不错，有意外收入的可能，但仍需理性理财。')
        elif wealth <= 2:
            suggestions.append('财运一般，不宜进行高风险投资，宜守不宜攻。')
        
        if health >= 4:
            suggestions.append('身体状况良好，精力充沛，适合进行体育锻炼。')
        elif health <= 2:
            suggestions.append('注意身体健康，避免过度劳累，保证充足睡眠。')
        
        full_description = base_desc + '\n\n' + '\n'.join(suggestions)
        
        return full_description

# 全局实例
meihua_calculator = MeihuaCalculator()
fortune_calculator = FortuneCalculator()

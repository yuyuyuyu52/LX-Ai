# -*- coding: utf-8 -*-
"""
八字计算核心算法
提供准确的八字排盘、五行分析、格局判断等功能
"""

from datetime import datetime, timedelta
import math
from lunar_python import Lunar  # 引入农历转换库

class BaziCalculator:
    """八字计算器"""
    
    # 天干
    TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    
    # 地支
    DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 五行属性
    WUXING_TIANGAN = {
        '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
        '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'
    }
    
    WUXING_DIZHI = {
        '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土', '巳': '火',
        '午': '火', '未': '土', '申': '金', '酉': '金', '戌': '土', '亥': '水'
    }
    
    # 十神关系
    SHISHEN = {
        '比肩': 0, '劫财': 1, '食神': 2, '伤官': 3, '偏财': 4,
        '正财': 5, '七杀': 6, '正官': 7, '偏印': 8, '正印': 9
    }
    
    # 生肖对应
    SHENGXIAO = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
    
    # 五行生克关系
    WUXING_SHENG = {
        '木': '火', '火': '土', '土': '金', '金': '水', '水': '木'
    }
    
    WUXING_KE = {
        '木': '土', '土': '水', '水': '火', '火': '金', '金': '木'
    }
    
    # 五行相生相克解释
    WUXING_RELATIONS = {
        '木生火': '木生火，表示生机勃勃，充满活力',
        '火生土': '火生土，表示温暖滋养，孕育万物',
        '土生金': '土生金，表示厚德载物，孕育财富',
        '金生水': '金生水，表示刚柔并济，智慧通达',
        '水生木': '水生木，表示滋养生长，生机无限',
        '木克土': '木克土，表示破土而出，突破束缚',
        '土克水': '土克水，表示固守本分，稳重踏实',
        '水克火': '水克火，表示冷静克制，理性思考',
        '火克金': '火克金，表示热情奔放，勇于创新',
        '金克木': '金克木，表示刚毅果断，雷厉风行'
    }
    
    # 十神解释
    SHISHEN_INTERPRETATIONS = {
        '比肩': '表示同辈、朋友、竞争对手，性格独立自主',
        '劫财': '表示争夺、竞争、压力，性格好胜要强',
        '食神': '表示才华、智慧、创造力，性格聪明伶俐',
        '伤官': '表示叛逆、创新、突破，性格特立独行',
        '偏财': '表示意外之财、投机、冒险，性格灵活多变',
        '正财': '表示稳定收入、理财、储蓄，性格踏实稳重',
        '七杀': '表示压力、挑战、竞争，性格坚强果断',
        '正官': '表示权威、地位、责任，性格正直严谨',
        '偏印': '表示学习、思考、研究，性格好学上进',
        '正印': '表示贵人、帮助、支持，性格温和善良'
    }
    
    # 格局解释
    GEJU_INTERPRETATIONS = {
        '身旺格': '日主力量强，性格坚强，有领导才能，但需注意控制脾气',
        '身弱格': '日主力量弱，性格温和，善于合作，但需注意增强自信',
        '中和格': '日主力量适中，性格平和，处事圆融，但需注意把握分寸'
    }
    
    def __init__(self):
        pass
    
    def calculate_bazi(self, birth_time, gender='男'):
        """
        计算八字
        
        Args:
            birth_time: 出生时间（datetime对象）
            gender: 性别
        
        Returns:
            dict: 包含完整八字信息的字典
        """
        # 转换为农历时间
        lunar = Lunar.fromDate(birth_time)
        
        # 获取年柱
        year_gan, year_zhi = self._get_year_ganzhi(lunar.getYear())
        
        # 获取月柱
        month_gan, month_zhi = self._get_month_ganzhi(lunar.getYear(), lunar.getMonth())
        
        # 获取日柱
        day_gan, day_zhi = self._get_day_ganzhi(birth_time)
        
        # 获取时柱
        hour_gan, hour_zhi = self._get_hour_ganzhi(birth_time.hour, day_gan)
        
        bazi = {
            'year': {'gan': year_gan, 'zhi': year_zhi},
            'month': {'gan': month_gan, 'zhi': month_zhi},
            'day': {'gan': day_gan, 'zhi': day_zhi},
            'hour': {'gan': hour_gan, 'zhi': hour_zhi}
        }
        
        # 计算日主和格局
        ri_zhu = day_gan  # 日主
        
        # 五行统计
        wuxing_count = self._count_wuxing(bazi)
        
        # 十神分析
        shishen_analysis = self._analyze_shishen(bazi, ri_zhu)
        
        # 格局判断
        geju = self._determine_geju(bazi, ri_zhu, wuxing_count)
        
        # 生肖
        shengxiao = self.SHENGXIAO[(lunar.getYear() - 4) % 12]
        
        # 五行关系分析
        wuxing_relations = self._analyze_wuxing_relations(bazi)
        
        # 十神详细分析
        shishen_details = self._analyze_shishen_details(shishen_analysis)
        
        # 格局详细分析
        geju_details = self._analyze_geju_details(geju, wuxing_count)
        
        result = {
            'bazi': bazi,
            'bazi_string': {
                'year': year_gan + year_zhi,
                'month': month_gan + month_zhi,
                'day': day_gan + day_zhi,
                'hour': hour_gan + hour_zhi
            },
            'ri_zhu': ri_zhu,
            'wuxing_count': wuxing_count,
            'shishen': shishen_analysis,
            'geju': geju,
            'shengxiao': shengxiao,
            'gender': gender,
            'wuxing_relations': wuxing_relations,
            'shishen_details': shishen_details,
            'geju_details': geju_details
        }
        
        return result
    
    def _get_year_ganzhi(self, year):
        """计算年柱干支"""
        # 以1864年甲子年为基准
        base_year = 1864
        offset = (year - base_year) % 60
        gan_index = offset % 10
        zhi_index = offset % 12
        return self.TIANGAN[gan_index], self.DIZHI[zhi_index]
    
    def _get_month_ganzhi(self, year, month):
        """计算月柱干支"""
        # 月柱地支固定：正月寅，二月卯...
        month_zhi_map = {
            1: '寅', 2: '卯', 3: '辰', 4: '巳', 5: '午', 6: '未',
            7: '申', 8: '酉', 9: '戌', 10: '亥', 11: '子', 12: '丑'
        }
        
        zhi = month_zhi_map[month]
        
        # 月干计算：甲己之年丙作首
        year_gan_index = (year - 4) % 10
        month_gan_starts = [2, 4, 6, 8, 0, 2, 4, 6, 8, 0]  # 对应甲乙丙丁戊己庚辛壬癸年的正月天干
        
        gan_index = (month_gan_starts[year_gan_index] + month - 1) % 10
        gan = self.TIANGAN[gan_index]
        
        return gan, zhi
    
    def _get_day_ganzhi(self, birth_time):
        """计算日柱干支"""
        # 以1900年1月31日庚辰日为基准
        base_date = datetime(1900, 1, 31)
        days_diff = (birth_time.date() - base_date.date()).days
        
        # 1900年1月31日是庚辰日，庚=6，辰=4
        gan_index = (6 + days_diff) % 10
        zhi_index = (4 + days_diff) % 12
        
        return self.TIANGAN[gan_index], self.DIZHI[zhi_index]
    
    def _get_hour_ganzhi(self, hour, day_gan):
        """计算时柱干支"""
        # 时辰地支
        hour_zhi_map = {
            (23, 0): '子',  # 23:00-01:00
            (1, 2): '丑',   # 01:00-03:00
            (3, 4): '寅',   # 03:00-05:00
            (5, 6): '卯',   # 05:00-07:00
            (7, 8): '辰',   # 07:00-09:00
            (9, 10): '巳',  # 09:00-11:00
            (11, 12): '午', # 11:00-13:00
            (13, 14): '未', # 13:00-15:00
            (15, 16): '申', # 15:00-17:00
            (17, 18): '酉', # 17:00-19:00
            (19, 20): '戌', # 19:00-21:00
            (21, 22): '亥'  # 21:00-23:00
        }
        
        zhi = None
        for (start, end), zhi_name in hour_zhi_map.items():
            if start <= hour <= end:
                zhi = zhi_name
                break
        
        if not zhi:
            if hour >= 23 or hour < 1:
                zhi = '子'
            elif hour < 3:
                zhi = '丑'
            elif hour < 5:
                zhi = '寅'
            elif hour < 7:
                zhi = '卯'
            elif hour < 9:
                zhi = '辰'
            elif hour < 11:
                zhi = '巳'
            elif hour < 13:
                zhi = '午'
            elif hour < 15:
                zhi = '未'
            elif hour < 17:
                zhi = '申'
            elif hour < 19:
                zhi = '酉'
            elif hour < 21:
                zhi = '戌'
            else:
                zhi = '亥'
        
        # 时干计算：甲己还加甲
        day_gan_index = self.TIANGAN.index(day_gan)
        hour_zhi_index = self.DIZHI.index(zhi)
        
        hour_gan_starts = [0, 2, 4, 6, 8, 0, 2, 4, 6, 8]  # 甲乙丙丁戊己庚辛壬癸日的子时天干
        gan_index = (hour_gan_starts[day_gan_index] + hour_zhi_index) % 10
        gan = self.TIANGAN[gan_index]
        
        return gan, zhi
    
    def _count_wuxing(self, bazi):
        """统计五行数量"""
        count = {'金': 0, '木': 0, '水': 0, '火': 0, '土': 0}
        
        for pillar in ['year', 'month', 'day', 'hour']:
            gan = bazi[pillar]['gan']
            zhi = bazi[pillar]['zhi']
            
            count[self.WUXING_TIANGAN[gan]] += 1
            count[self.WUXING_DIZHI[zhi]] += 1
        
        return count
    
    def _analyze_shishen(self, bazi, ri_zhu):
        """分析十神"""
        ri_zhu_wuxing = self.WUXING_TIANGAN[ri_zhu]
        shishen_result = {}
        
        # 五行生克关系
        wuxing_order = ['木', '火', '土', '金', '水']
        ri_index = wuxing_order.index(ri_zhu_wuxing)
        
        for pillar in ['year', 'month', 'hour']:  # 不包括日柱
            gan = bazi[pillar]['gan']
            gan_wuxing = self.WUXING_TIANGAN[gan]
            gan_index = wuxing_order.index(gan_wuxing)
            
            # 计算十神关系
            relation = (gan_index - ri_index) % 5
            
            if gan_wuxing == ri_zhu_wuxing:
                shishen_result[pillar + '_gan'] = '比肩'
            elif relation == 1:
                shishen_result[pillar + '_gan'] = '食神'
            elif relation == 2:
                shishen_result[pillar + '_gan'] = '偏财'
            elif relation == 3:
                shishen_result[pillar + '_gan'] = '七杀'
            elif relation == 4:
                shishen_result[pillar + '_gan'] = '偏印'
        
        return shishen_result
    
    def _determine_geju(self, bazi, ri_zhu, wuxing_count):
        """判断格局"""
        ri_zhu_wuxing = self.WUXING_TIANGAN[ri_zhu]
        
        # 计算日主五行力量
        ri_zhu_strength = wuxing_count[ri_zhu_wuxing]
        
        # 计算生助日主的五行力量
        sheng_ri_zhu = wuxing_count.get(self.WUXING_SHENG.get(ri_zhu_wuxing), 0)
        
        # 计算克制日主的五行力量
        ke_ri_zhu = wuxing_count.get(self.WUXING_KE.get(ri_zhu_wuxing), 0)
        
        # 计算总力量
        total_strength = ri_zhu_strength + sheng_ri_zhu - ke_ri_zhu
        
        # 判断格局
        if total_strength >= 4:
            return '身旺格'
        elif total_strength <= 1:
            return '身弱格'
        else:
            return '中和格'
    
    def calculate_marriage_compatibility(self, male_bazi_data, female_bazi_data):
        """
        计算八字合婚
        
        Args:
            male_bazi_data: 男方八字数据
            female_bazi_data: 女方八字数据
        
        Returns:
            dict: 合婚分析结果
        """
        # 生肖配对
        male_shengxiao = male_bazi_data['shengxiao']
        female_shengxiao = female_bazi_data['shengxiao']
        shengxiao_score = self._calculate_shengxiao_compatibility(male_shengxiao, female_shengxiao)
        
        # 五行互补
        male_wuxing = male_bazi_data['wuxing_count']
        female_wuxing = female_bazi_data['wuxing_count']
        wuxing_score = self._calculate_wuxing_compatibility(male_wuxing, female_wuxing)
        
        # 日柱匹配
        male_ri_zhu = male_bazi_data['ri_zhu']
        female_ri_zhu = female_bazi_data['ri_zhu']
        rizhu_score = self._calculate_rizhu_compatibility(male_ri_zhu, female_ri_zhu)
        
        # 格局配合
        male_geju = male_bazi_data['geju']
        female_geju = female_bazi_data['geju']
        geju_score = self._calculate_geju_compatibility(male_geju, female_geju)
        
        # 综合评分
        total_score = (shengxiao_score * 0.3 + wuxing_score * 0.3 + 
                      rizhu_score * 0.25 + geju_score * 0.15)
        
        # 等级判断
        if total_score >= 85:
            level = '上上等'
            description = '天作之合，非常相配'
        elif total_score >= 75:
            level = '上等'
            description = '相配度很高，婚姻幸福'
        elif total_score >= 65:
            level = '中上等'
            description = '比较相配，需要磨合'
        elif total_score >= 55:
            level = '中等'
            description = '一般相配，需要努力经营'
        elif total_score >= 45:
            level = '中下等'
            description = '相配度较低，需要谨慎'
        else:
            level = '下等'
            description = '不太相配，建议慎重考虑'
        
        return {
            'total_score': round(total_score, 1),
            'level': level,
            'description': description,
            'details': {
                'shengxiao_score': shengxiao_score,
                'wuxing_score': wuxing_score,
                'rizhu_score': rizhu_score,
                'geju_score': geju_score
            },
            'male_shengxiao': male_shengxiao,
            'female_shengxiao': female_shengxiao
        }
    
    def _calculate_shengxiao_compatibility(self, male_zodiac, female_zodiac):
        """计算生肖配对得分"""
        # 生肖配对表（简化版）
        compatibility_map = {
            ('鼠', '龙'): 95, ('鼠', '猴'): 90, ('鼠', '牛'): 80,
            ('牛', '蛇'): 95, ('牛', '鸡'): 90, ('牛', '鼠'): 80,
            ('虎', '马'): 95, ('虎', '狗'): 90, ('虎', '猪'): 80,
            ('兔', '羊'): 95, ('兔', '猪'): 90, ('兔', '狗'): 80,
            ('龙', '鸡'): 95, ('龙', '鼠'): 95, ('龙', '猴'): 85,
            ('蛇', '牛'): 95, ('蛇', '鸡'): 90, ('蛇', '猴'): 80,
            ('马', '虎'): 95, ('马', '狗'): 90, ('马', '羊'): 85,
            ('羊', '兔'): 95, ('羊', '猪'): 90, ('羊', '马'): 85,
            ('猴', '鼠'): 90, ('猴', '龙'): 85, ('猴', '蛇'): 80,
            ('鸡', '蛇'): 90, ('鸡', '牛'): 90, ('鸡', '龙'): 95,
            ('狗', '虎'): 90, ('狗', '马'): 90, ('狗', '兔'): 80,
            ('猪', '兔'): 90, ('猪', '羊'): 90, ('猪', '虎'): 80
        }
        
        # 查找配对得分
        score = compatibility_map.get((male_zodiac, female_zodiac), 
                                     compatibility_map.get((female_zodiac, male_zodiac), 60))
        
        return score
    
    def _calculate_wuxing_compatibility(self, male_wuxing, female_wuxing):
        """计算五行互补得分"""
        # 简化的五行互补计算
        total_male = sum(male_wuxing.values())
        total_female = sum(female_wuxing.values())
        
        compatibility_score = 0
        for element in ['金', '木', '水', '火', '土']:
            male_ratio = male_wuxing[element] / total_male
            female_ratio = female_wuxing[element] / total_female
            
            # 互补性评分（一强一弱更好）
            if abs(male_ratio - female_ratio) > 0.3:
                compatibility_score += 20
            elif abs(male_ratio - female_ratio) > 0.2:
                compatibility_score += 15
            else:
                compatibility_score += 10
        
        return min(compatibility_score, 100)
    
    def _calculate_rizhu_compatibility(self, male_rizhu, female_rizhu):
        """计算日柱匹配得分"""
        male_wuxing = self.WUXING_TIANGAN[male_rizhu]
        female_wuxing = self.WUXING_TIANGAN[female_rizhu]
        
        # 五行生克关系评分
        wuxing_order = ['木', '火', '土', '金', '水']
        male_index = wuxing_order.index(male_wuxing)
        female_index = wuxing_order.index(female_wuxing)
        
        relation = (female_index - male_index) % 5
        
        if relation == 0:  # 同类
            return 75
        elif relation == 1:  # 女生男
            return 85
        elif relation == 2:  # 女克男
            return 65
        elif relation == 3:  # 男克女
            return 70
        else:  # 男生女
            return 80
    
    def _calculate_geju_compatibility(self, male_geju, female_geju):
        """计算格局配合得分"""
        geju_scores = {
            ('身旺格', '身弱格'): 85,
            ('身弱格', '身旺格'): 85,
            ('中和格', '中和格'): 80,
            ('身旺格', '身旺格'): 70,
            ('身弱格', '身弱格'): 70,
            ('中和格', '身旺格'): 75,
            ('中和格', '身弱格'): 75,
            ('身旺格', '中和格'): 75,
            ('身弱格', '中和格'): 75
        }
        
        return geju_scores.get((male_geju, female_geju), 70)
    
    def _analyze_wuxing_relations(self, bazi):
        """分析五行关系"""
        relations = []
        
        # 分析天干五行关系
        for pillar in ['year', 'month', 'day', 'hour']:
            gan = bazi[pillar]['gan']
            gan_wuxing = self.WUXING_TIANGAN[gan]
            
            for other_pillar in ['year', 'month', 'day', 'hour']:
                if pillar != other_pillar:
                    other_gan = bazi[other_pillar]['gan']
                    other_wuxing = self.WUXING_TIANGAN[other_gan]
                    
                    # 分析生克关系
                    if self.WUXING_SHENG[gan_wuxing] == other_wuxing:
                        relations.append({
                            'type': '生',
                            'from': f'{pillar}干{gan}',
                            'to': f'{other_pillar}干{other_gan}',
                            'interpretation': self.WUXING_RELATIONS[f'{gan_wuxing}生{other_wuxing}']
                        })
                    elif self.WUXING_KE[gan_wuxing] == other_wuxing:
                        relations.append({
                            'type': '克',
                            'from': f'{pillar}干{gan}',
                            'to': f'{other_pillar}干{other_gan}',
                            'interpretation': self.WUXING_RELATIONS[f'{gan_wuxing}克{other_wuxing}']
                        })
        
        # 分析地支五行关系
        for pillar in ['year', 'month', 'day', 'hour']:
            zhi = bazi[pillar]['zhi']
            zhi_wuxing = self.WUXING_DIZHI[zhi]
            
            for other_pillar in ['year', 'month', 'day', 'hour']:
                if pillar != other_pillar:
                    other_zhi = bazi[other_pillar]['zhi']
                    other_wuxing = self.WUXING_DIZHI[other_zhi]
                    
                    # 分析生克关系
                    if self.WUXING_SHENG[zhi_wuxing] == other_wuxing:
                        relations.append({
                            'type': '生',
                            'from': f'{pillar}支{zhi}',
                            'to': f'{other_pillar}支{other_zhi}',
                            'interpretation': self.WUXING_RELATIONS[f'{zhi_wuxing}生{other_wuxing}']
                        })
                    elif self.WUXING_KE[zhi_wuxing] == other_wuxing:
                        relations.append({
                            'type': '克',
                            'from': f'{pillar}支{zhi}',
                            'to': f'{other_pillar}支{other_zhi}',
                            'interpretation': self.WUXING_RELATIONS[f'{zhi_wuxing}克{other_wuxing}']
                        })
        
        return relations
    
    def _analyze_shishen_details(self, shishen_analysis):
        """分析十神详细含义"""
        details = {}
        
        for pillar, shishen in shishen_analysis.items():
            details[pillar] = {
                'name': shishen,
                'interpretation': self.SHISHEN_INTERPRETATIONS[shishen]
            }
        
        return details
    
    def _analyze_geju_details(self, geju, wuxing_count):
        """分析格局详细含义"""
        return {
            'name': geju,
            'interpretation': self.GEJU_INTERPRETATIONS[geju],
            'wuxing_analysis': self._analyze_geju_wuxing(geju, wuxing_count)
        }
    
    def _analyze_geju_wuxing(self, geju, wuxing_count):
        """分析格局的五行特征"""
        total = sum(wuxing_count.values())
        wuxing_ratios = {k: v/total for k, v in wuxing_count.items()}
        
        if geju == '身旺格':
            return {
                'strength': '强',
                'characteristics': '五行力量集中，气势强盛',
                'suggestions': '宜发挥优势，但需注意控制'
            }
        elif geju == '身弱格':
            return {
                'strength': '弱',
                'characteristics': '五行力量分散，气势较弱',
                'suggestions': '宜寻求帮助，增强实力'
            }
        else:  # 中和格
            return {
                'strength': '中',
                'characteristics': '五行力量均衡，气势平和',
                'suggestions': '宜顺势而为，保持平衡'
            }

# 全局八字计算器实例
bazi_calculator = BaziCalculator()

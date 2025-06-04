# -*- coding: utf-8 -*-
"""
AI增强分析服务
使用DeepSeek API提供AI增强的占卜分析
"""

import os
import logging

logger = logging.getLogger(__name__)

# 尝试导入Ark API，如果不可用则创建一个模拟类
try:
    from volcenginesdkarkruntime import Ark
    ARK_API_AVAILABLE = True
except ImportError:
    logger.warning("volcenginesdkarkruntime 模块不可用，AI增强功能将受限")
    ARK_API_AVAILABLE = False
    
    # 创建模拟响应类
    class MockMessage:
        """模拟消息类"""
        def __init__(self, content):
            self.content = content
    
    class MockChoice:
        """模拟选择类"""
        def __init__(self, content):
            self.message = MockMessage(content)
    
    class MockResponse:
        """模拟API响应类"""
        def __init__(self, content):
            self.choices = [MockChoice(content)]
    
    # 创建模拟的Ark API类
    class MockArk:
        """模拟Ark API类，在无法导入真实API时使用"""
        def __init__(self, api_key=None):
            self.api_key = api_key
            self.chat = MockChat()
    
    class MockChat:
        """模拟Chat API类"""
        def __init__(self):
            self.completions = MockCompletions()
    
    class MockCompletions:
        """模拟Completions API类"""
        def create(self, model=None, messages=None):
            # 返回一个模拟的响应
            return MockResponse("AI增强功能暂时不可用，请检查系统配置或稍后再试。")

class AIService:
    """AI增强分析服务类"""
    
    def __init__(self):
        # 从环境变量或设置中读取API Key
        self.api_key = "5234644f-dd06-47c9-9389-636c4cbd691b"
        if ARK_API_AVAILABLE:
            self.client = Ark(api_key=self.api_key)
        else:
            self.client = MockArk(api_key=self.api_key)
        self.model = "deepseek-r1-250120"
    
    def enhance_bazi_analysis(self, bazi_data, basic_analysis, birth_info):
        """
        AI增强八字分析
        
        Args:
            bazi_data: 八字数据
            basic_analysis: 基础分析结果
            birth_info: 出生信息
        
        Returns:
            str: AI增强的分析结果
        """
        # 如果Ark API不可用，直接返回基础分析
        if not ARK_API_AVAILABLE:
            logger.warning("无法使用AI增强功能：volcenginesdkarkruntime模块未安装")
            return f"AI增强功能暂时不可用（缺少必要依赖）。\n\n{basic_analysis}"
            
        try:
            prompt = f"""
请作为一名专业的八字命理大师，对以下八字进行深度分析：

【基本信息】
出生时间：{birth_info.get('birth_time', '')}
性别：{birth_info.get('gender', '')}
出生地：{birth_info.get('birth_place', '')}

【八字排盘】
年柱：{bazi_data.get('year', '')}
月柱：{bazi_data.get('month', '')}
日柱：{bazi_data.get('day', '')}
时柱：{bazi_data.get('hour', '')}

【基础分析】
{basic_analysis}

请从以下角度进行AI增强分析：
1. 五行生克制化的深度解析
2. 十神关系与格局分析
3. 大运流年的运势走向
4. 性格特质的细致刻画
5. 事业发展的具体建议
6. 感情婚姻的详细分析
7. 财运状况的专业判断
8. 健康方面的贴心提醒
9. 开运方法的实用指导

请用专业而通俗易懂的语言，为用户提供准确、详细、实用的命理分析。
"""
            
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            logger.error(f"AI增强八字分析失败: {str(e)}")
            return f"AI分析暂时不可用，请稍后再试。\n\n{basic_analysis}"
    
    def enhance_marriage_analysis(self, male_bazi, female_bazi, basic_analysis):
        """
        AI增强八字合婚分析
        
        Args:
            male_bazi: 男方八字
            female_bazi: 女方八字
            basic_analysis: 基础合婚分析
        
        Returns:
            str: AI增强的合婚分析
        """
        # 如果Ark API不可用，直接返回基础分析
        if not ARK_API_AVAILABLE:
            logger.warning("无法使用AI增强功能：volcenginesdkarkruntime模块未安装")
            return f"AI增强功能暂时不可用（缺少必要依赖）。\n\n{basic_analysis}"
            
        try:
            prompt = f"""
请作为专业的八字合婚大师，分析以下两人的八字合婚情况：

【男方八字】
年柱：{male_bazi.get('year', '')}
月柱：{male_bazi.get('month', '')}
日柱：{male_bazi.get('day', '')}
时柱：{male_bazi.get('hour', '')}

【女方八字】
年柱：{female_bazi.get('year', '')}
月柱：{female_bazi.get('month', '')}
日柱：{female_bazi.get('day', '')}
时柱：{female_bazi.get('hour', '')}

【基础分析】
{basic_analysis}

请从以下维度进行深度合婚分析：
1. 五行互补情况分析
2. 十神配合的和谐度
3. 生肖配对的吉凶判断
4. 性格匹配度评估
5. 事业发展的互助情况
6. 财运方面的协调性
7. 健康运势的相互影响
8. 子女运势的分析
9. 婚姻稳定性预测
10. 具体的婚配建议

请给出专业、客观、实用的合婚建议，帮助这对情侣更好地了解彼此的契合度。
"""
            
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            logger.error(f"AI增强合婚分析失败: {str(e)}")
            return f"AI分析暂时不可用，请稍后再试。\n\n{basic_analysis}"
    
    def enhance_meihua_analysis(self, question, main_gua, bian_gua, dong_yao, basic_analysis):
        """
        AI增强梅花易数分析
        
        Args:
            question: 用户问题
            main_gua: 主卦信息
            bian_gua: 变卦信息
            dong_yao: 动爻信息
            basic_analysis: 基础分析
        
        Returns:
            str: AI增强的梅花易数分析
        """
        # 如果Ark API不可用，直接返回基础分析
        if not ARK_API_AVAILABLE:
            logger.warning("无法使用AI增强功能：volcenginesdkarkruntime模块未安装")
            return f"AI增强功能暂时不可用（缺少必要依赖）。\n\n{basic_analysis}"
            
        try:
            # 构建卦象信息
            hexagram_info = f"""
本卦：{main_gua['name']}（{main_gua.get('description', '')}）
变卦：{bian_gua['name']}（{bian_gua.get('description', '')}）
动爻：第{dong_yao}爻
"""
            
            prompt = f"""
请作为梅花易数大师，深度分析以下卦象：

【咨询问题】
{question}

【卦象信息】
{hexagram_info}

【基础分析】
{basic_analysis}

请从梅花易数的角度进行AI增强分析：
1. 体用关系的深度解析
2. 五行生克的具体影响
3. 卦象变化的时间预测
4. 事态发展的详细过程
5. 有利因素与不利因素
6. 最佳行动时机的把握
7. 趋吉避凶的具体方法
8. 决策建议的实用指导

请结合传统梅花易数理论，为用户提供准确、实用的决策建议。
"""
            
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            logger.error(f"AI增强梅花易数分析失败: {str(e)}")
            return f"AI分析暂时不可用，请稍后再试。\n\n{basic_analysis}"
    
    def enhance_daily_fortune(self, zodiac, date, basic_fortune, user_birth_date=None, additional_info=None):
        """
        AI增强每日运势分析
        
        Args:
            zodiac: 生肖
            date: 日期
            basic_fortune: 基础运势
            user_birth_date: 用户出生日期（可选，用于个性化分析）
            additional_info: 额外信息（可选）
        
        Returns:
            str: AI增强的运势分析
        """
        try:
            # 构建个性化信息
            personal_info = ""
            if user_birth_date:
                from datetime import datetime, date as date_type
                if isinstance(user_birth_date, str):
                    birth_dt = datetime.strptime(user_birth_date, '%Y-%m-%d').date()
                elif isinstance(user_birth_date, date_type):
                    birth_dt = user_birth_date
                else:
                    birth_dt = user_birth_date
                
                # 计算年龄和人生阶段
                today = datetime.now().date()
                age = today.year - birth_dt.year - ((today.month, today.day) < (birth_dt.month, birth_dt.day))
                
                if age < 25:
                    life_stage = "青春成长期"
                elif age < 35:
                    life_stage = "事业起步期"
                elif age < 45:
                    life_stage = "事业发展期"
                elif age < 55:
                    life_stage = "成熟稳定期"
                else:
                    life_stage = "智慧沉淀期"
                
                personal_info = f"\n【个人特征】\n生肖：{zodiac}\n年龄阶段：{life_stage}（{age}岁）"
            
            # 添加时间节点特殊分析
            time_context = self._get_time_context(date)
            
            prompt = f"""
请作为专业的运势分析师和人生导师，为{zodiac}生肖的人分析{date}的详细运势。

【基础运势】
{basic_fortune}
{personal_info}

【时间背景】
{time_context}

请从以下角度进行深度AI增强分析：

1. **综合运势解读**：结合生肖特性和时间因素，分析今日整体运势走向

2. **情感关系指导**：
   - 单身者的桃花运分析和遇缘建议
   - 有伴者的感情维护和增进技巧
   - 家庭关系的和谐相处之道

3. **事业发展策略**：
   - 工作中的机遇识别和把握
   - 职场人际关系的处理技巧
   - 适合今日推进的重要事项

4. **财富管理建议**：
   - 收入机会和投资方向分析
   - 消费理财的明智选择
   - 避免财务风险的注意事项

5. **健康养生指导**：
   - 身体健康的关注重点
   - 适合的运动和养生方式
   - 情绪管理和压力释放方法

6. **人际交往智慧**：
   - 社交场合的应对技巧
   - 贵人相助的机会把握
   - 化解人际矛盾的方法

7. **学习成长建议**：
   - 技能提升的最佳方向
   - 知识积累的有效途径
   - 自我完善的实践方法

8. **开运转运方法**：
   - 具体的开运行动建议
   - 能量提升的实用技巧
   - 改善运势的生活习惯

9. **风险规避提醒**：
   - 需要特别注意的事项
   - 可能的挑战和应对策略
   - 避免不利影响的预防措施

10. **每日行动指南**：
    - 今日最佳行动时间
    - 推荐的重要决策方向
    - 简单易行的幸运提升法

请用温暖、智慧、实用的语言，结合现代生活实际，为用户提供有价值的人生指导和实用建议。分析要具体深入，避免泛泛而谈，让用户能够真正受益并付诸行动。
"""
            
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            logger.error(f"AI增强运势分析失败: {str(e)}")
            return f"AI分析暂时不可用，请稍后再试。\n\n{basic_fortune}"
    
    def _get_time_context(self, date):
        """获取时间背景信息"""
        try:
            from datetime import datetime
            if isinstance(date, str):
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            else:
                date_obj = date
            
            # 获取月份和季节信息
            month = date_obj.month
            day = date_obj.day
            
            season_map = {
                (12, 1, 2): "冬季",
                (3, 4, 5): "春季", 
                (6, 7, 8): "夏季",
                (9, 10, 11): "秋季"
            }
            
            season = "春季"  # 默认值
            for months, season_name in season_map.items():
                if month in months:
                    season = season_name
                    break
            
            # 特殊日期分析
            special_dates = {
                (1, 1): "新年伊始，万象更新",
                (2, 14): "情人节，爱意浓浓",
                (3, 8): "妇女节，关爱女性",
                (5, 1): "劳动节，勤劳致富",
                (6, 1): "儿童节，童心未泯",
                (9, 10): "教师节，尊师重道",
                (10, 1): "国庆节，举国欢庆",
                (12, 25): "圣诞节，温馨祥和"
            }
            
            special_note = special_dates.get((month, day), "")
            
            # 月初、月中、月末的不同能量
            if day <= 10:
                month_phase = "月初新气象，适合新的开始"
            elif day <= 20:
                month_phase = "月中稳定期，适合稳步推进"
            else:
                month_phase = "月末收尾期，适合总结反思"
            
            context = f"当前时节：{season}，{month_phase}"
            if special_note:
                context += f"，{special_note}"
            
            return context
            
        except Exception as e:
            return "时间背景：普通日子，保持平常心"
    
    def enhance_yijing_analysis(self, question, hexagram_info, basic_analysis):
        """
        AI增强易经卜卦分析
        
        Args:
            question: 用户问题
            hexagram_info: 卦象信息
            basic_analysis: 基础分析
        
        Returns:
            str: AI增强的易经卜卦分析
        """
        try:
            # 构建卦象信息描述
            hexagram_desc = f"{hexagram_info['name']}卦（第{hexagram_info['number']}卦）- {hexagram_info['meaning']}"
            
            prompt = f"""
请作为易经卜卦大师，深入分析以下卦象：

【咨询问题】
{question}

【卦象信息】
卦名：{hexagram_desc}
卦辞：{hexagram_info['judgment']}

【基础分析】
{basic_analysis}

请从以下维度进行AI增强分析：
1. 卦象的深层含义解析
2. 六爻变化的详细解读
3. 事态发展的可能走向
4. 人际关系的影响分析
5. 时间节点的关键提示
6. 内在心理的启发与思考
7. 外在环境的应对策略
8. 趋吉避凶的具体建议
9. 变通之道与智慧启示

请结合传统易经哲学与现代生活实际，为用户提供深刻、实用的指导。
"""
            
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            logger.error(f"AI增强易经分析失败: {str(e)}")
            return f"AI分析暂时不可用，请稍后再试。\n\n{basic_analysis}"

# 全局AI服务实例
ai_service = AIService()

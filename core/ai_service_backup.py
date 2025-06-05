# -*- coding: utf-8 -*-
"""
AI增强分析服务
使用优化的DeepSeek-R1 chat函数提供AI增强的占卜分析
"""

import os
import logging
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError

logger = logging.getLogger(__name__)

# 配置参数
AI_TIMEOUT = 90  # AI请求超时时间（秒）- 根据您的chat函数测试结果调整为90秒
MAX_RETRIES = 1  # 减少重试次数提高响应速度

# 使用优化的chat函数
def chat(role: str = "user", content: str = "你好"):
    """优化的chat函数，直接调用DeepSeek-R1"""
    from volcenginesdkarkruntime import Ark
    client = Ark(api_key="5234644f-dd06-47c9-9389-636c4cbd691b")
    
    completion = client.chat.completions.create(
        model="deepseek-r1-250120",
        messages=[
            {"role": role, "content": content}
        ]
    )
    return completion.choices[0].message.content

class AIService:
    """AI增强分析服务类"""
    
    def __init__(self):
        # 直接使用chat函数，无需初始化客户端
        pass
    
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
作为八字命理师，分析八字：{bazi_data.get('year', '')} {bazi_data.get('month', '')} {bazi_data.get('day', '')} {bazi_data.get('hour', '')}

出生：{birth_info.get('birth_time', '')} {birth_info.get('gender', '')}

基础分析：{basic_analysis}

请简要分析：
1. 性格特质
2. 事业财运
3. 感情婚姻
4. 健康注意
5. 开运建议

要求：简洁明了，300字内。
"""
            
            completion = self._call_ai_api(prompt)
            
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
八字合婚分析：

男方：{male_bazi.get('year', '')} {male_bazi.get('month', '')} {male_bazi.get('day', '')} {male_bazi.get('hour', '')}
女方：{female_bazi.get('year', '')} {female_bazi.get('month', '')} {female_bazi.get('day', '')} {female_bazi.get('hour', '')}

基础分析：{basic_analysis}

请分析：
1. 五行互补与性格匹配
2. 生肖配对与事业协助
3. 婚姻稳定性与财运
4. 健康子女运
5. 婚配建议

要求：简洁明了，300字内。
"""
            
            completion = self._call_ai_api(prompt)
            
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
            prompt = f"""
梅花易数分析：

问题：{question}
本卦：{main_gua['name']} → 变卦：{bian_gua['name']}
动爻：第{dong_yao}爻

基础分析：{basic_analysis}

请分析：
1. 体用关系与五行生克
2. 卦象变化的时间预测
3. 有利与不利因素
4. 最佳行动时机
5. 趋吉避凶方法

要求：简洁明了，300字内。
"""
            
            completion = self._call_ai_api(prompt)
            
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
            # 简化个性化信息
            personal_info = f"生肖：{zodiac}"
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
                
                if age < 30:
                    life_stage = "青年期"
                elif age < 50:
                    life_stage = "中年期"
                else:
                    life_stage = "成熟期"
                
                personal_info += f"，{life_stage}"
            
            prompt = f"""
{zodiac}生肖{date}运势分析：

基础运势：{basic_fortune}
个人特征：{personal_info}

请分析：
1. 综合运势
2. 事业财运
3. 感情人际
4. 健康注意
5. 开运建议

要求：实用具体，400字内。
"""
            
            completion = self._call_ai_api(prompt)
            
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
易经卜卦分析：

问题：{question}
卦象：{hexagram_desc}
卦辞：{hexagram_info['judgment']}

基础分析：{basic_analysis}

请分析：
1. 卦象深层含义
2. 事态发展走向
3. 人际关系影响
4. 应对策略建议
5. 趋吉避凶智慧

要求：简洁明了，300字内。
"""
            
            completion = self._call_ai_api(prompt)
            
            return completion.choices[0].message.content
            
        except Exception as e:
            logger.error(f"AI增强易经分析失败: {str(e)}")
            return f"AI分析暂时不可用，请稍后再试。\n\n{basic_analysis}"
    
    def _call_ai_api(self, prompt):
        """调用AI API，带超时和重试机制"""
        if not ARK_API_AVAILABLE:
            raise RuntimeError("ARK API不可用")
        
        for attempt in range(MAX_RETRIES + 1):
            try:
                with ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        self.client.chat.completions.create,
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    completion = future.result(timeout=AI_TIMEOUT)
                    return completion
            
            except FutureTimeoutError:
                logger.warning(f"AI请求超时，正在重试...（尝试次数：{attempt + 1}）")
            except Exception as e:
                logger.error(f"调用AI API失败: {str(e)}")
                raise RuntimeError(f"调用AI API失败: {str(e)}") from e
            
        raise RuntimeError("调用AI API超时，请稍后再试")

# 全局AI服务实例
ai_service = AIService()

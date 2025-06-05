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
    
    def _call_ai_with_timeout(self, prompt, timeout_seconds=AI_TIMEOUT):
        """
        使用超时控制调用AI
        
        Args:
            prompt: 提示词
            timeout_seconds: 超时时间（秒）
        
        Returns:
            str: AI响应结果
        """
        # 🔍 DEBUG: 打印实际发送给AI的提示词
        print("=" * 80)
        print("🤖 AI模式激活 - 正在发送提示词给DeepSeek-R1")
        print("=" * 80)
        print(f"📝 提示词内容（长度: {len(prompt)}字符）:")
        print("-" * 40)
        print(prompt)
        print("-" * 40)
        print("⏰ 开始AI调用...")
        
        def ai_call():
            return chat(role="user", content=prompt)
        
        retry_count = 0
        while retry_count <= MAX_RETRIES:
            try:
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(ai_call)
                    
                    try:
                        result = future.result(timeout=timeout_seconds)
                        
                        # 🔍 DEBUG: 打印AI响应结果
                        print(f"✅ AI调用成功! 响应长度: {len(result)}字符")
                        print(f"📄 AI响应内容预览:")
                        print("-" * 40)
                        print(result[:200] + "..." if len(result) > 200 else result)
                        print("=" * 80)
                        
                        return result
                    except FutureTimeoutError:
                        retry_count += 1
                        if retry_count <= MAX_RETRIES:
                            logger.warning(f"AI请求超时，正在重试...（尝试次数：{retry_count}）")
                            time.sleep(2)
                        else:
                            return "AI增强八字分析失败: 调用AI API超时，请稍后再试"
                        
            except Exception as e:
                retry_count += 1
                if retry_count <= MAX_RETRIES:
                    logger.warning(f"AI请求失败，正在重试...（尝试次数：{retry_count}）：{str(e)}")
                    time.sleep(2)
                else:
                    logger.error(f"AI增强分析失败: {str(e)}")
                    return f"AI增强分析失败: {str(e)}"
        
        return "AI增强分析失败: 达到最大重试次数"
    
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
        try:
            # 优化后的提示词 - 保持详细但更结构化
            prompt = f"""请作为专业八字命理师，深度分析以下八字信息：

【基本信息】
八字：{bazi_data.get('year', '')} {bazi_data.get('month', '')} {bazi_data.get('day', '')} {bazi_data.get('hour', '')}
出生时间：{birth_info.get('birth_time', '')}
性别：{birth_info.get('gender', '')}
出生地：{birth_info.get('birth_place', '')}

【基础分析】
{basic_analysis}

请提供专业详细的八字分析，包含以下方面：

1. **命格特质**：详细解析日主强弱、格局类型、用神忌神
2. **性格分析**：深入分析性格特点、天赋才能、行为模式
3. **事业运势**：分析适合的职业方向、事业发展阶段、成功因素
4. **财运分析**：财富获得方式、理财能力、投资建议
5. **感情婚姻**：感情模式、婚姻状况、配偶特征、感情运势
6. **健康状况**：体质特点、易患疾病、养生建议
7. **人生建议**：根据八字特点给出人生规划和发展建议

要求：分析要专业详细，语言通俗易懂，具有实用指导价值。请以Markdown格式返回，不要使用```markdown```包裹内容。"""

            return self._call_ai_with_timeout(prompt)
            
        except Exception as e:
            logger.error(f"AI增强八字分析失败: {str(e)}")
            return f"AI增强分析失败，使用基础分析结果。\n\n{basic_analysis}"
    
    def enhance_marriage_analysis(self, basic_analysis, male_info, female_info):
        """
        AI增强八字合婚分析
        
        Args:
            basic_analysis: 基础分析结果
            male_info: 男方信息
            female_info: 女方信息
        
        Returns:
            str: AI增强的合婚分析结果
        """
        try:
            prompt = f"""请作为专业命理师，深度分析以下八字合婚信息：

【男方信息】
姓名：{male_info.get('name', '')}
八字：{male_info.get('bazi', '')}
出生时间：{male_info.get('birth_time', '')}

【女方信息】
姓名：{female_info.get('name', '')}
八字：{female_info.get('bazi', '')}
出生时间：{female_info.get('birth_time', '')}

【基础合婚分析】
{basic_analysis}

请提供专业详细的八字合婚分析，包含：

1. **五行互补分析**：两人五行配置的互补性和影响
2. **生肖配对解析**：生肖关系对感情的影响
3. **性格匹配度**：双方性格的契合度和磨合建议
4. **事业财运配合**：事业发展的相互影响和支持
5. **子女运势**：子女缘分和教育建议
6. **婚姻运势预测**：不同阶段的婚姻状况预测
7. **化解建议**：针对不利因素的化解方法
8. **婚姻经营建议**：如何维护和谐美满的婚姻

要求：分析专业全面，建议实用可行，语言温和正面。请以Markdown格式返回，不要使用```markdown```包裹内容。"""

            return self._call_ai_with_timeout(prompt)
            
        except Exception as e:
            logger.error(f"AI增强合婚分析失败: {str(e)}")
            return f"AI增强分析失败，使用基础分析结果。\n\n{basic_analysis}"
    
    def enhance_meihua_analysis(self, question, main_gua, bian_gua, dong_yao, basic_analysis):
        """
        AI增强梅花易数分析
        
        Args:
            question: 用户提出的问题
            main_gua: 主卦信息
            bian_gua: 变卦信息
            dong_yao: 动爻位置
            basic_analysis: 基础分析结果
        
        Returns:
            str: AI增强的梅花易数分析结果
        """
        try:
            # 构建卦象信息字符串
            gua_info = f"""问题：{question}
            
主卦：{main_gua['name']} 
  上卦：{main_gua['upper']['name']}（{main_gua['upper']['nature']}）
  下卦：{main_gua['lower']['name']}（{main_gua['lower']['nature']}）

变卦：{bian_gua['name']}
  上卦：{bian_gua['upper']['name']}（{bian_gua['upper']['nature']}）
  下卦：{bian_gua['lower']['name']}（{bian_gua['lower']['nature']}）

动爻：第{dong_yao}爻"""

            prompt = f"""请作为专业易学大师，深度解析以下梅花易数卦象：

【卦象信息】
{gua_info}

【基础分析】
{basic_analysis}

请提供专业详细的梅花易数分析，包含：

1. **卦象解读**：主卦、变卦的深层含义和象征
2. **动爻分析**：变爻对整体卦象的影响和指示
3. **时空分析**：起卦时间地点对预测的影响
4. **五行生克**：卦中五行关系的作用和变化
5. **应期判断**：事情发生的时间节点预测
6. **吉凶分析**：整体运势的吉凶倾向
7. **具体建议**：根据卦象给出的行动指导
8. **趋吉避凶**：如何利用卦象信息趋利避害

要求：解析深入透彻，预测准确明确，建议实用有效。请以Markdown格式返回，不要使用```markdown```包裹内容。"""

            return self._call_ai_with_timeout(prompt)
            
        except Exception as e:
            logger.error(f"AI增强梅花易数分析失败: {str(e)}")
            return f"AI增强分析失败，使用基础分析结果。\n\n{basic_analysis}"
    
    def enhance_daily_fortune(self, user_info, fortune_data):
        """
        AI增强每日运势分析
        
        Args:
            user_info: 用户信息
            fortune_data: 运势数据
        
        Returns:
            str: AI增强的每日运势分析
        """
        try:
            prompt = f"""请作为专业运势分析师，为用户提供详细的今日运势指导：

【用户信息】
生肖：{user_info.get('shengxiao', '')}
星座：{user_info.get('constellation', '')}
性别：{user_info.get('gender', '')}
出生年份：{user_info.get('birth_year', '')}

【日期信息】
公历：{fortune_data.get('date', '')}
农历：{fortune_data.get('lunar_date', '')}
星期：{fortune_data.get('weekday', '')}

请提供专业详细的今日运势分析，包含：

1. **整体运势**：今日总体运气指数和主要趋势
2. **爱情运势**：感情发展、桃花运、情侣关系建议
3. **事业运势**：工作表现、人际关系、决策建议
4. **财运分析**：收入机会、投资理财、消费建议
5. **健康运势**：身体状况、养生重点、注意事项
6. **幸运指数**：幸运数字、幸运颜色、幸运方位
7. **注意事项**：今日需要特别注意的方面
8. **开运建议**：提升运势的具体方法

要求：分析准确实用，建议具体可行，语言亲切温暖。请以Markdown格式返回，不要使用```markdown```包裹内容。"""

            return self._call_ai_with_timeout(prompt)
            
        except Exception as e:
            logger.error(f"AI增强每日运势分析失败: {str(e)}")
            return f"AI增强分析失败: {str(e)}"
    
    # 兼容的方法名，用于测试和外部调用
    def get_bazi_analysis(self, bazi_data, gender, focus="综合"):
        """
        获取八字分析（兼容方法）
        
        Args:
            bazi_data: 八字数据字符串
            gender: 性别
            focus: 关注重点
        
        Returns:
            str: AI分析结果
        """
        # 构建模拟的数据结构
        if isinstance(bazi_data, str):
            parts = bazi_data.split()
            bazi_dict = {
                'year': parts[0] if len(parts) > 0 else '',
                'month': parts[1] if len(parts) > 1 else '',
                'day': parts[2] if len(parts) > 2 else '',
                'hour': parts[3] if len(parts) > 3 else ''
            }
        else:
            bazi_dict = bazi_data
        
        birth_info = {
            'gender': gender,
            'birth_time': bazi_data,
            'birth_place': '未指定'
        }
        
        return self.enhance_bazi_analysis(bazi_dict, f"基础分析：关注{focus}", birth_info)
    
    def get_meihua_analysis(self, shang_gua, xia_gua, dong_yao, question=""):
        """
        获取梅花易数分析（兼容方法）
        
        Args:
            shang_gua: 上卦
            xia_gua: 下卦
            dong_yao: 动爻
            question: 问题
        
        Returns:
            str: AI分析结果
        """
        # 创建模拟的卦象数据结构
        main_gua = {
            'name': f"{shang_gua}{xia_gua}卦",
            'upper': {'name': shang_gua, 'nature': ''},
            'lower': {'name': xia_gua, 'nature': ''}
        }
        
        bian_gua = {
            'name': f"{shang_gua}{xia_gua}变卦",
            'upper': {'name': shang_gua, 'nature': ''},
            'lower': {'name': xia_gua, 'nature': ''}
        }
        
        basic_analysis = f"基础分析：{shang_gua}变{xia_gua}，动爻在第{dong_yao}爻"
        
        return self.enhance_meihua_analysis(question, main_gua, bian_gua, dong_yao, basic_analysis)
    
    def get_marriage_analysis(self, male_bazi, female_bazi):
        """
        获取八字合婚分析（兼容方法）
        
        Args:
            male_bazi: 男方八字
            female_bazi: 女方八字
        
        Returns:
            str: AI分析结果
        """
        if isinstance(male_bazi, str):
            male_parts = male_bazi.split()
            male_dict = {
                'year': male_parts[0] if len(male_parts) > 0 else '',
                'month': male_parts[1] if len(male_parts) > 1 else '',
                'day': male_parts[2] if len(male_parts) > 2 else '',
                'hour': male_parts[3] if len(male_parts) > 3 else ''
            }
        else:
            male_dict = male_bazi
            
        if isinstance(female_bazi, str):
            female_parts = female_bazi.split()
            female_dict = {
                'year': female_parts[0] if len(female_parts) > 0 else '',
                'month': female_parts[1] if len(female_parts) > 1 else '',
                'day': female_parts[2] if len(female_parts) > 2 else '',
                'hour': female_parts[3] if len(female_parts) > 3 else ''
            }
        else:
            female_dict = female_bazi
        
        male_info = {
            'name': '男方',
            'bazi': male_bazi,
            'gender': '男'
        }
        
        female_info = {
            'name': '女方', 
            'bazi': female_bazi,
            'gender': '女'
        }
        
        basic_analysis = f"基础合婚分析：男方{male_bazi}，女方{female_bazi}"
        
        return self.enhance_marriage_analysis(basic_analysis, male_info, female_info)
    
    def get_daily_fortune(self, constellation, date):
        """
        获取每日运势分析（兼容方法）
        
        Args:
            constellation: 星座
            date: 日期
        
        Returns:
            str: AI分析结果
        """
        user_info = {
            'constellation': constellation,
            'shengxiao': '',
            'gender': '',
            'birth_year': ''
        }
        
        fortune_data = {
            'date': date,
            'lunar_date': '',
            'weekday': ''
        }
        
        return self.enhance_daily_fortune(user_info, fortune_data)

# 全局AI服务实例
ai_service = AIService()

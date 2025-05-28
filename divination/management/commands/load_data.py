from django.core.management.base import BaseCommand
from divination.models import TarotCard, IChingHexagram, BaziElement

class Command(BaseCommand):
    help = '初始化占卜数据库'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化占卜数据...')
        
        # 首先检查是否有用户
        from django.contrib.auth.models import User
        from core.models import DivinationRecord
        
        # 创建示例用户（如果不存在）
        sample_users = ['命理爱好者', '小张', '王女士', '李先生', '神秘客']
        created_users = []
        
        for username in sample_users:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'password': 'pbkdf2_sha256$600000$dummy$dummy'}
            )
            if created:
                created_users.append(user)
                self.stdout.write(f'创建示例用户: {username}')
        
        # 创建基本的塔罗牌数据
        tarot_cards = [
            ('愚者', 'The Fool', 0, 'major', '新开始,冒险,纯真', '鲁莽,不成熟,缺乏经验'),
            ('魔术师', 'The Magician', 1, 'major', '创造力,意志力,技能', '欺骗,缺乏技能,缺乏意志力'),
            ('女祭司', 'The High Priestess', 2, 'major', '直觉,神秘,内在智慧', '缺乏直觉,秘密被揭露,内在混乱'),
            ('皇后', 'The Empress', 3, 'major', '丰收,母性,创造', '依赖,空虚,缺乏成长'),
            ('皇帝', 'The Emperor', 4, 'major', '权威,稳定,控制', '专制,缺乏纪律,灵活性不足'),
        ]
        
        for name, name_en, card_number, suit, upright, reversed in tarot_cards:
            card, created = TarotCard.objects.get_or_create(
                name=name,
                defaults={
                    'name_en': name_en,
                    'card_number': card_number,
                    'suit': suit,
                    'upright_meaning': upright,
                    'reversed_meaning': reversed
                }
            )
            if created:
                self.stdout.write(f'创建塔罗牌: {name}')
        
        # 创建基本的易经卦象
        hexagrams = [
            (1, '乾', '乾为天', '111111', '刚健中正，自强不息', '天行健，君子以自强不息'),
            (2, '坤', '坤为地', '000000', '厚德载物，包容万象', '地势坤，君子以厚德载物'),
            (3, '屯', '水雷屯', '010001', '初始艰难，坚持必成', '云雷屯，君子以经纶'),
            (4, '蒙', '山水蒙', '100010', '启蒙教育，循序渐进', '山下出泉，蒙'),
        ]
        
        for number, name, chinese_name, binary, meaning, judgment in hexagrams:
            hexagram, created = IChingHexagram.objects.get_or_create(
                number=number,
                defaults={
                    'name': name,
                    'chinese_name': chinese_name,
                    'binary': binary,
                    'meaning': meaning,
                    'judgment': judgment,
                    'image': f'《象》曰：{judgment}'
                }
            )
            if created:
                self.stdout.write(f'创建卦象: {chinese_name}')
        
        # 创建基本的八字元素
        elements = [
            ('甲', 'tiangan', 'mu'),
            ('乙', 'tiangan', 'mu'),
            ('丙', 'tiangan', 'huo'),
            ('丁', 'tiangan', 'huo'),
            ('子', 'dizhi', 'shui'),
            ('丑', 'dizhi', 'tu'),
            ('寅', 'dizhi', 'mu'),
            ('卯', 'dizhi', 'mu'),
        ]
        
        for name, element_type, wuxing in elements:
            element, created = BaziElement.objects.get_or_create(
                name=name,
                defaults={
                    'element_type': element_type,
                    'wuxing': wuxing
                }
            )
            if created:
                self.stdout.write(f'创建八字元素: {name}')
        
        # 创建示例占卜记录
        sample_records = [
            ('bazi', '小张', '今年事业运如何？', '根据您的八字分析，今年事业运势较好，适合主动出击，把握机会。建议在秋季有重要决策。'),
            ('tarot', '王女士', '感情方面的困惑', '塔罗牌显示您目前的感情状况需要更多的沟通和理解。星币三逆位提醒您要更加珍惜当前的关系。'),
            ('meihua', '李先生', '投资理财建议', '梅花易数显示，近期财运平稳，不宜冒险投资，建议以稳健理财为主。'),
            ('yijing', '神秘客', '人生方向指导', '《易经》泽天夬卦，表示您正处于突破期，需要果断决策，但要注意方式方法。'),
            ('bazi', '命理爱好者', '性格分析', '您的八字显示性格稳重，具有很强的责任心，适合从事管理或教育相关工作。'),
        ]
        
        for div_type, username, question, result in sample_records:
            try:
                user = User.objects.get(username=username)
                record, created = DivinationRecord.objects.get_or_create(
                    user=user,
                    divination_type=div_type,
                    question=question,
                    defaults={'result': result}
                )
                if created:
                    self.stdout.write(f'创建占卜记录: {username} - {div_type}')
            except User.DoesNotExist:
                continue
        
        self.stdout.write(self.style.SUCCESS('占卜数据初始化完成！'))

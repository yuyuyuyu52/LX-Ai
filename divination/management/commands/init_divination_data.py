from django.core.management.base import BaseCommand
from divination.models import TarotCard, IChingHexagram, BaziElement

class Command(BaseCommand):
    help = '初始化占卜数据库'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化占卜数据...')
        
        # 创建塔罗牌数据
        self.create_tarot_cards()
        
        # 创建易经卦象数据
        self.create_iching_hexagrams()
        
        # 创建八字五行数据
        self.create_bazi_elements()
        
        self.stdout.write(self.style.SUCCESS('占卜数据初始化完成！'))    
    def create_tarot_cards(self):
        """创建塔罗牌数据"""
        tarot_cards = [
            # 大阿卡那牌
            ('愚者', 'The Fool', 0, 'major', '新开始,冒险,纯真', '开始新的旅程,保持初心'),
            ('魔术师', 'The Magician', 1, 'major', '创造力,意志力,技能', '运用智慧和技能实现目标'),
            ('女祭司', 'The High Priestess', 2, 'major', '直觉,神秘,内在智慧', '倾听内心的声音和直觉'),
            ('皇后', 'The Empress', 3, 'major', '丰收,母性,创造', '充满爱与创造力的时期'),
            ('皇帝', 'The Emperor', 4, 'major', '权威,稳定,控制', '建立秩序与稳定的基础'),
            ('教皇', 'The Hierophant', 5, 'major', '传统,指导,信仰', '寻求精神指导和传统智慧'),
            ('恋人', 'The Lovers', 6, 'major', '爱情,选择,结合', '重要的感情选择和决定'),
            ('战车', 'The Chariot', 7, 'major', '胜利,意志,前进', '克服困难取得胜利'),
            ('力量', 'Strength', 8, 'major', '勇气,坚持,内在力量', '用智慧和耐心解决问题'),
            ('隐者', 'The Hermit', 9, 'major', '寻找,内省,指导', '寻求内在智慧和指导'),
            ('命运之轮', 'Wheel of Fortune', 10, 'major', '变化,命运,循环', '生命的转折点和变化'),
            ('正义', 'Justice', 11, 'major', '平衡,公正,决定', '做出公正和平衡的决定'),
            ('倒吊人', 'The Hanged Man', 12, 'major', '牺牲,等待,新视角', '以新的角度看待问题'),
            ('死神', 'Death', 13, 'major', '转变,结束,重生', '一个阶段的结束和新的开始'),
            ('节制', 'Temperance', 14, 'major', '平衡,调和,耐心', '在各方面寻求平衡'),
            ('恶魔', 'The Devil', 15, 'major', '诱惑,束缚,物质', '摆脱束缚和负面影响'),
            ('塔', 'The Tower', 16, 'major', '突变,破坏,启示', '突然的变化带来新的认识'),
            ('星星', 'The Star', 17, 'major', '希望,灵感,治愈', '重新找到希望和方向'),
            ('月亮', 'The Moon', 18, 'major', '幻象,直觉,潜意识', '注意潜意识的信号'),
            ('太阳', 'The Sun', 19, 'major', '成功,喜悦,活力', '充满阳光和正能量的时期'),
            ('审判', 'Judgement', 20, 'major', '觉醒,重生,召唤', '精神的觉醒和重新开始'),
            ('世界', 'The World', 21, 'major', '完成,成就,圆满', '达成目标和圆满成功'),
            
            # 小阿卡那牌示例（权杖花色）
            ('权杖王牌', 'Ace of Wands', 1, 'wands', '创造力,灵感,新开始', '创意项目的开始'),
            ('权杖二', 'Two of Wands', 2, 'wands', '计划,选择,个人力量', '制定长远计划'),
            ('权杖三', 'Three of Wands', 3, 'wands', '扩展,远见,领导力', '扩大视野和影响力'),
            ('权杖四', 'Four of Wands', 4, 'wands', '庆祝,和谐,里程碑', '庆祝取得的成就'),
            ('权杖五', 'Five of Wands', 5, 'wands', '竞争,冲突,挑战', '面对竞争和挑战'),
        ]
        
        for name, name_en, card_number, suit, upright, reversed in tarot_cards:
            TarotCard.objects.get_or_create(
                name=name,
                defaults={
                    'name_en': name_en,
                    'card_number': card_number,
                    'suit': suit,
                    'upright_meaning': upright,
                    'reversed_meaning': reversed
                }
            )
        
        self.stdout.write('塔罗牌数据创建完成')    
    def create_iching_hexagrams(self):
        """创建易经卦象数据"""
        hexagrams = [
            (1, '乾', '乾为天', '111111', '刚健中正，自强不息', '天行健，君子以自强不息'),
            (2, '坤', '坤为地', '000000', '厚德载物，包容万象', '地势坤，君子以厚德载物'),
            (3, '屯', '水雷屯', '010001', '初始艰难，坚持必成', '云雷屯，君子以经纶'),
            (4, '蒙', '山水蒙', '100010', '启蒙教育，循序渐进', '山下出泉，蒙'),
            (5, '需', '水天需', '010111', '等待时机，耐心坚持', '云上于天，需'),
            (6, '讼', '天水讼', '111010', '争讼不休，和解为上', '天与水违行，讼'),
            (7, '师', '地水师', '000010', '用兵如神，师出有名', '地中有水，师'),
            (8, '比', '水地比', '010000', '亲密团结，和睦相处', '水在地上，比'),
        ]
        
        for number, name, chinese_name, binary, meaning, judgment in hexagrams:
            IChingHexagram.objects.get_or_create(
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
        
        self.stdout.write('易经卦象数据创建完成')    
    def create_bazi_elements(self):
        """创建八字五行数据"""
        elements = [
            # 天干
            ('甲', 'tiangan', 'mu'),
            ('乙', 'tiangan', 'mu'),
            ('丙', 'tiangan', 'huo'),
            ('丁', 'tiangan', 'huo'),
            ('戊', 'tiangan', 'tu'),
            ('己', 'tiangan', 'tu'),
            ('庚', 'tiangan', 'jin'),
            ('辛', 'tiangan', 'jin'),
            ('壬', 'tiangan', 'shui'),
            ('癸', 'tiangan', 'shui'),
            
            # 地支
            ('子', 'dizhi', 'shui'),
            ('丑', 'dizhi', 'tu'),
            ('寅', 'dizhi', 'mu'),
            ('卯', 'dizhi', 'mu'),
            ('辰', 'dizhi', 'tu'),
            ('巳', 'dizhi', 'huo'),
            ('午', 'dizhi', 'huo'),
            ('未', 'dizhi', 'tu'),
            ('申', 'dizhi', 'jin'),
            ('酉', 'dizhi', 'jin'),
            ('戌', 'dizhi', 'tu'),
            ('亥', 'dizhi', 'shui'),
        ]
        
        for name, element_type, wuxing in elements:
            BaziElement.objects.get_or_create(
                name=name,
                defaults={
                    'element_type': element_type,
                    'wuxing': wuxing
                }
            )
        
        self.stdout.write('八字五行数据创建完成')

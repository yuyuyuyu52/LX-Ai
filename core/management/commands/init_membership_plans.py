"""
创建初始会员套餐数据
"""
from django.core.management.base import BaseCommand
from core.models import MembershipPlan

class Command(BaseCommand):
    help = '创建初始会员套餐数据'
    
    def handle(self, *args, **options):
        # 创建单日会员套餐
        daily_plan, created = MembershipPlan.objects.get_or_create(
            plan_type='daily',
            defaults={
                'name': '单日会员',
                'price': 80.00,
                'duration_days': 1,
                'description': '体验一天的完整会员服务，享受AI增强功能',
                'features': [
                    'AI增强八字分析',
                    '精准塔罗占卜',
                    '专业梅花易数',
                    '24小时无限次使用',
                    '专属客服支持'
                ],
                'sort_order': 1
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'成功创建单日会员套餐: {daily_plan.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'单日会员套餐已存在: {daily_plan.name}'))
        
        # 创建年度会员套餐
        annual_plan, created = MembershipPlan.objects.get_or_create(
            plan_type='annual',
            defaults={
                'name': '年度会员',
                'price': 365.00,
                'duration_days': 365,
                'description': '全年无忧的会员服务，享受所有高级功能',
                'features': [
                    '全年无限使用',
                    'AI深度分析',
                    '独家运势报告',
                    '优先客服响应',
                    '专属会员标识',
                    '历史记录永久保存'
                ],
                'sort_order': 2
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'成功创建年度会员套餐: {annual_plan.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'年度会员套餐已存在: {annual_plan.name}'))
        
        self.stdout.write(self.style.SUCCESS('会员套餐初始化完成！'))

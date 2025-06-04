"""
会员系统测试文件
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from .models import UserProfile, MembershipPlan, MembershipOrder, PaymentRecord
from .email_service import EmailService


class MembershipModelTests(TestCase):
    """会员模型测试"""
    
    def setUp(self):
        """测试数据准备"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            phone='13888888888'
        )
        
        # 创建会员套餐
        self.daily_plan = MembershipPlan.objects.create(
            name='每日会员',
            plan_type='daily',
            price=Decimal('80.00'),
            duration_days=1,
            features=['无限制占卜', '专属客服'],
            is_active=True
        )
        
        self.annual_plan = MembershipPlan.objects.create(
            name='年度会员',
            plan_type='annual',
            price=Decimal('365.00'),
            duration_days=365,
            features=['无限制占卜', '专属客服', '专属报告'],
            is_active=True
        )
    
    def test_membership_plan_creation(self):
        """测试会员套餐创建"""
        self.assertEqual(self.daily_plan.name, '每日会员')
        self.assertEqual(self.daily_plan.price, Decimal('80.00'))
        self.assertEqual(self.daily_plan.duration_days, 1)
        self.assertTrue(self.daily_plan.is_active)
    
    def test_membership_order_creation(self):
        """测试会员订单创建"""
        order = MembershipOrder.objects.create(
            user=self.user,
            plan=self.daily_plan,
            total_amount=self.daily_plan.price
        )
        
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.plan, self.daily_plan)
        self.assertEqual(order.total_amount, Decimal('80.00'))
        self.assertEqual(order.status, 'pending')
        self.assertIsNotNone(order.order_number)
    
    def test_membership_activation(self):
        """测试会员激活"""
        order = MembershipOrder.objects.create(
            user=self.user,
            plan=self.daily_plan,
            total_amount=self.daily_plan.price,
            status='paid'
        )
        
        # 激活会员
        order.activate_membership()
        
        # 检查订单状态
        order.refresh_from_db()
        self.assertEqual(order.status, 'completed')
        self.assertIsNotNone(order.activated_at)
        
        # 检查用户档案
        self.profile.refresh_from_db()
        self.assertTrue(self.profile.is_vip)
        self.assertIsNotNone(self.profile.vip_expires_at)
    
    def test_membership_extension(self):
        """测试会员续期"""
        # 先激活一个会员
        order1 = MembershipOrder.objects.create(
            user=self.user,
            plan=self.daily_plan,
            total_amount=self.daily_plan.price,
            status='paid'
        )
        order1.activate_membership()
        
        # 获取第一次的到期时间
        self.profile.refresh_from_db()
        first_expiry = self.profile.vip_expires_at
        
        # 再次购买会员
        order2 = MembershipOrder.objects.create(
            user=self.user,
            plan=self.daily_plan,
            total_amount=self.daily_plan.price,
            status='paid'
        )
        order2.activate_membership()
        
        # 检查到期时间是否延长
        self.profile.refresh_from_db()
        self.assertGreater(self.profile.vip_expires_at, first_expiry)
    
    def test_order_expiration(self):
        """测试订单过期"""
        order = MembershipOrder.objects.create(
            user=self.user,
            plan=self.daily_plan,
            total_amount=self.daily_plan.price
        )
        
        # 模拟订单过期
        order.created_at = timezone.now() - timedelta(hours=25)
        order.save()
        
        self.assertTrue(order.is_expired())
    
    def test_payment_record_creation(self):
        """测试支付记录创建"""
        order = MembershipOrder.objects.create(
            user=self.user,
            plan=self.daily_plan,
            total_amount=self.daily_plan.price
        )
        
        payment = PaymentRecord.objects.create(
            order=order,
            payment_method='alipay',
            amount=order.total_amount,
            trade_no='test_transaction_123'
        )
        
        self.assertEqual(payment.order, order)
        self.assertEqual(payment.payment_method, 'alipay')
        self.assertEqual(payment.amount, Decimal('80.00'))
        self.assertEqual(payment.trade_no, 'test_transaction_123')


class MembershipViewTests(TestCase):
    """会员视图测试"""
    
    def setUp(self):
        """测试数据准备"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            phone='13888888888'
        )
        
        self.daily_plan = MembershipPlan.objects.create(
            name='每日会员',
            plan_type='daily',
            price=Decimal('80.00'),
            duration_days=1,
            is_active=True
        )
    
    def test_membership_plans_view(self):
        """测试会员套餐页面"""
        response = self.client.get(reverse('core:membership_plans'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '每日会员')
        self.assertContains(response, '80.00')
    
    def test_purchase_membership_view_authenticated(self):
        """测试已登录用户购买会员"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(reverse('core:purchase_membership'), {
            'plan': self.daily_plan.id,
            'payment_method': 'alipay'
        })
        
        # 应该重定向到支付页面
        self.assertEqual(response.status_code, 302)
        
        # 检查订单是否创建
        order = MembershipOrder.objects.filter(user=self.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.plan, self.daily_plan)
    
    def test_purchase_membership_view_anonymous(self):
        """测试匿名用户购买会员"""
        response = self.client.post(reverse('core:purchase_membership'), {
            'plan': self.daily_plan.id,
            'payment_method': 'alipay'
        })
        
        # 应该重定向到登录页面
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))
    
    def test_membership_orders_view(self):
        """测试会员订单页面"""
        self.client.login(username='testuser', password='testpass123')
        
        # 创建测试订单
        order = MembershipOrder.objects.create(
            user=self.user,
            plan=self.daily_plan,
            total_amount=self.daily_plan.price
        )
        
        response = self.client.get(reverse('core:membership_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, order.order_number)
    
    def test_membership_status_api(self):
        """测试会员状态API"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse('core:check_membership_status'))
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertFalse(data['is_vip'])
        self.assertIsNone(data['expires_at'])


class MembershipMiddlewareTests(TestCase):
    """会员中间件测试"""
    
    def setUp(self):
        """测试数据准备"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            phone='13888888888',
            is_vip=True,
            vip_expires_at=timezone.now() - timedelta(days=1)  # 已过期
        )
    
    def test_expired_membership_cleanup(self):
        """测试过期会员清理"""
        self.client.login(username='testuser', password='testpass123')
        
        # 访问任意页面触发中间件
        response = self.client.get('/')
        
        # 检查会员状态是否被清理
        self.profile.refresh_from_db()
        self.assertFalse(self.profile.is_vip)
        self.assertIsNone(self.profile.vip_expires_at)


class EmailServiceTests(TestCase):
    """邮件服务测试"""
    
    def setUp(self):
        """测试数据准备"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.daily_plan = MembershipPlan.objects.create(
            name='每日会员',
            plan_type='daily',
            price=Decimal('80.00'),
            duration_days=1,
            is_active=True
        )
        
        self.order = MembershipOrder.objects.create(
            user=self.user,
            plan=self.daily_plan,
            total_amount=self.daily_plan.price,
            status='paid'
        )
        
        self.email_service = EmailService()
    
    def test_send_purchase_confirmation(self):
        """测试发送购买确认邮件"""
        result = self.email_service.send_purchase_confirmation(self.order)
        self.assertTrue(result)
    
    def test_send_membership_activated(self):
        """测试发送会员激活邮件"""
        result = self.email_service.send_membership_activated(self.order)
        self.assertTrue(result)
    
    def test_send_expiry_warning(self):
        """测试发送到期提醒邮件"""
        result = self.email_service.send_expiry_warning(self.user, days_left=3)
        self.assertTrue(result)
    
    def test_send_membership_expired(self):
        """测试发送会员过期邮件"""
        result = self.email_service.send_membership_expired(self.user)
        self.assertTrue(result)


class MembershipIntegrationTests(TestCase):
    """会员系统集成测试"""
    
    def setUp(self):
        """测试数据准备"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            phone='13888888888'
        )
        
        self.daily_plan = MembershipPlan.objects.create(
            name='每日会员',
            plan_type='daily',
            price=Decimal('80.00'),
            duration_days=1,
            is_active=True
        )
    
    def test_complete_membership_flow(self):
        """测试完整的会员购买流程"""
        # 1. 登录
        self.client.login(username='testuser', password='testpass123')
        
        # 2. 查看会员套餐
        response = self.client.get(reverse('core:membership_plans'))
        self.assertEqual(response.status_code, 200)
        
        # 3. 购买会员
        response = self.client.post(reverse('core:purchase_membership'), {
            'plan': self.daily_plan.id,
            'payment_method': 'alipay'
        })
        self.assertEqual(response.status_code, 302)
        
        # 4. 获取创建的订单
        order = MembershipOrder.objects.filter(user=self.user).first()
        self.assertIsNotNone(order)
        
        # 5. 模拟支付成功
        response = self.client.post(
            reverse('core:process_payment', args=[order.order_number]),
            {'action': 'confirm_payment'}
        )
        self.assertEqual(response.status_code, 302)
        
        # 6. 检查会员状态
        self.profile.refresh_from_db()
        self.assertTrue(self.profile.is_vip)
        self.assertIsNotNone(self.profile.vip_expires_at)
        
        # 7. 检查订单状态
        order.refresh_from_db()
        self.assertEqual(order.status, 'completed')
        
        # 8. 查看订单历史
        response = self.client.get(reverse('core:membership_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, order.order_number)

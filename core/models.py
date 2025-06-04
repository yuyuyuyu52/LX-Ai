from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class SMSVerification(models.Model):
    """短信验证码模型"""
    phone_number = models.CharField(max_length=11, verbose_name='手机号码', db_index=True)
    code = models.CharField(max_length=6, verbose_name='验证码')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    expire_at = models.DateTimeField(verbose_name='过期时间')
    is_used = models.BooleanField(default=False, verbose_name='是否已使用')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='请求IP地址')
    attempt_count = models.IntegerField(default=0, verbose_name='验证尝试次数')
    
    def __str__(self):
        return f"{self.phone_number} - {self.code} ({'已使用' if self.is_used else '未使用'})"
    
    def save(self, *args, **kwargs):
        # 设置默认过期时间为10分钟后
        if not self.expire_at:
            self.expire_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)
    
    def is_valid(self):
        """检查验证码是否有效"""
        return not self.is_used and timezone.now() < self.expire_at and self.attempt_count < 5
    
    def increment_attempt(self):
        """增加验证尝试次数"""
        self.attempt_count += 1
        self.save(update_fields=['attempt_count'])
    
    @classmethod
    def cleanup_expired(cls):
        """清理过期的验证码记录"""
        expired_count = cls.objects.filter(expire_at__lt=timezone.now()).delete()[0]
        return expired_count
    
    class Meta:
        verbose_name = '短信验证码'
        verbose_name_plural = '短信验证码'
        ordering = ['-created_at']

class UserProfile(models.Model):
    """用户档案模型"""
    MEMBERSHIP_CHOICES = [
        ('free', '普通用户'),
        ('vip', '会员用户'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号码')
    phone_verified = models.BooleanField(default=False, verbose_name='手机已验证')
    birth_date = models.DateTimeField(null=True, blank=True, verbose_name='出生时间')
    birth_place = models.CharField(max_length=100, null=True, blank=True, verbose_name='出生地点')
    gender = models.CharField(max_length=10, choices=[('male', '男'), ('female', '女')], null=True, blank=True, verbose_name='性别')
    membership = models.CharField(max_length=10, choices=MEMBERSHIP_CHOICES, default='free', verbose_name='会员类型')
    membership_expire_date = models.DateTimeField(null=True, blank=True, verbose_name='会员到期时间')
    ai_usage_count = models.IntegerField(default=0, verbose_name='AI使用次数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    def is_vip(self):
        """检查是否为会员"""
        if self.membership == 'vip':
            if self.membership_expire_date:
                from django.utils import timezone
                return timezone.now() < self.membership_expire_date
            return True
        return False
    
    def can_use_ai(self):
        """检查是否可以使用AI功能"""
        return self.is_vip()
    
    class Meta:
        verbose_name = '用户档案'
        verbose_name_plural = '用户档案'
    
    def __str__(self):
        return f"{self.user.username}的档案"

class DivinationRecord(models.Model):
    """占卜记录模型"""
    DIVINATION_TYPES = [
        ('bazi', '八字分析'),
        ('bazi_marriage', '八字合婚'),
        ('meihua', '梅花易数'),
        ('daily_fortune', '每日运势'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    divination_type = models.CharField(max_length=50, choices=DIVINATION_TYPES, verbose_name='占卜类型')
    question = models.TextField(blank=True, verbose_name='问题')
    result = models.TextField(verbose_name='结果')
    ai_enhanced = models.BooleanField(default=False, verbose_name='AI增强分析')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '占卜记录'
        verbose_name_plural = '占卜记录'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_divination_type_display()} - {self.created_at.strftime('%Y-%m-%d')}"

class Notification(models.Model):
    """用户通知模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='标题')
    message = models.TextField(verbose_name='消息内容')
    notification_type = models.CharField(max_length=20, choices=[
        ('info', '信息'),
        ('success', '成功'),
        ('warning', '警告'),
        ('error', '错误')
    ], default='info', verbose_name='通知类型')
    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '用户通知'
        verbose_name_plural = '用户通知'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class DailyFortune(models.Model):
    """每日运势模型"""
    ZODIAC_CHOICES = [
        ('rat', '鼠'), ('ox', '牛'), ('tiger', '虎'), ('rabbit', '兔'),
        ('dragon', '龙'), ('snake', '蛇'), ('horse', '马'), ('goat', '羊'),
        ('monkey', '猴'), ('rooster', '鸡'), ('dog', '狗'), ('pig', '猪')
    ]
    
    date = models.DateField(verbose_name='日期')
    zodiac = models.CharField(max_length=10, choices=ZODIAC_CHOICES, verbose_name='生肖')
    overall_fortune = models.IntegerField(default=3, verbose_name='综合运势（1-5星）')
    love_fortune = models.IntegerField(default=3, verbose_name='爱情运势（1-5星）')
    career_fortune = models.IntegerField(default=3, verbose_name='事业运势（1-5星）')
    wealth_fortune = models.IntegerField(default=3, verbose_name='财运（1-5星）')
    health_fortune = models.IntegerField(default=3, verbose_name='健康运势（1-5星）')
    lucky_color = models.CharField(max_length=20, default='红色', verbose_name='幸运颜色')
    lucky_number = models.CharField(max_length=10, default='8', verbose_name='幸运数字')
    description = models.TextField(verbose_name='运势描述')
    ai_enhanced = models.BooleanField(default=False, verbose_name='AI增强分析')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '每日运势'
        verbose_name_plural = '每日运势'
        unique_together = ['date', 'zodiac']
        ordering = ['-date', 'zodiac']
    
    def __str__(self):
        return f"{self.date} - {self.get_zodiac_display()}运势"

class MembershipPlan(models.Model):
    """会员套餐模型"""
    PLAN_TYPES = [
        ('daily', '单日会员'),
        ('annual', '年度会员'),
    ]
    
    name = models.CharField(max_length=50, verbose_name='套餐名称')
    plan_type = models.CharField(max_length=10, choices=PLAN_TYPES, verbose_name='套餐类型')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    duration_days = models.IntegerField(verbose_name='有效天数')
    description = models.TextField(blank=True, verbose_name='套餐描述')
    features = models.JSONField(default=list, verbose_name='套餐特权')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '会员套餐'
        verbose_name_plural = '会员套餐'
        ordering = ['sort_order', 'price']
    
    def __str__(self):
        return f"{self.name} - ¥{self.price}"

class MembershipOrder(models.Model):
    """会员订单模型"""
    ORDER_STATUS_CHOICES = [
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('expired', '已过期'),
        ('cancelled', '已取消'),
        ('refunded', '已退款'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('wechat', '微信支付'),
        ('alipay', '支付宝'),
        ('mock', '模拟支付'),  # 开发测试用
    ]
    
    order_id = models.CharField(max_length=32, unique=True, verbose_name='订单号')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE, verbose_name='会员套餐')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单金额')
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending', verbose_name='订单状态')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True, verbose_name='支付方式')
    payment_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    expire_time = models.DateTimeField(verbose_name='订单过期时间')
    trade_no = models.CharField(max_length=100, null=True, blank=True, verbose_name='第三方交易号')
    remark = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            import uuid
            self.order_id = uuid.uuid4().hex
        if not self.expire_time:
            self.expire_time = timezone.now() + timedelta(hours=24)  # 24小时内支付
        super().save(*args, **kwargs)
    
    def is_expired(self):
        """检查订单是否过期"""
        return timezone.now() > self.expire_time and self.status == 'pending'
    
    def activate_membership(self):
        """激活会员"""
        if self.status == 'paid':
            profile = self.user.userprofile
            profile.membership = 'vip'
            
            # 计算会员到期时间
            current_time = timezone.now()
            if profile.membership_expire_date and profile.membership_expire_date > current_time:
                # 如果当前还是会员，在现有基础上延期
                expire_date = profile.membership_expire_date + timedelta(days=self.plan.duration_days)
            else:
                # 新开通会员或已过期，从当前时间开始计算
                expire_date = current_time + timedelta(days=self.plan.duration_days)
            
            profile.membership_expire_date = expire_date
            profile.save()
            
            # 创建通知
            Notification.objects.create(
                user=self.user,
                title='会员开通成功',
                message=f'恭喜您成功开通{self.plan.name}，有效期至{expire_date.strftime("%Y年%m月%d日")}',
                notification_type='success'
            )
            
            return True
        return False
    
    class Meta:
        verbose_name = '会员订单'
        verbose_name_plural = '会员订单'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.order_id} - {self.user.username} - {self.plan.name}"

class PaymentRecord(models.Model):
    """支付记录模型"""
    order = models.ForeignKey(MembershipOrder, on_delete=models.CASCADE, verbose_name='关联订单')
    payment_method = models.CharField(max_length=20, verbose_name='支付方式')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='支付金额')
    trade_no = models.CharField(max_length=100, verbose_name='第三方交易号')
    payment_data = models.JSONField(default=dict, verbose_name='支付回调数据')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '支付记录'
        verbose_name_plural = '支付记录'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.order.order_id} - ¥{self.amount}"

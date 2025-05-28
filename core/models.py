from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateTimeField(null=True, blank=True)
    birth_place = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', '男'), ('female', '女')], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}的档案"

class DivinationRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    divination_type = models.CharField(max_length=50, choices=[
        ('bazi', '八字分析'),
        ('meihua', '梅花易数'),
        ('tarot', '塔罗占卜'),
        ('yijing', '易经卜卦')
    ])
    question = models.TextField(blank=True)
    result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
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

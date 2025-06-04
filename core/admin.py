from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from django.utils import timezone
from .models import UserProfile, DivinationRecord, Notification, SMSVerification, MembershipPlan, MembershipOrder, PaymentRecord

@admin.register(SMSVerification)
class SMSVerificationAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created_at', 'expire_at', 'is_used')
    list_filter = ('is_used', 'created_at')
    search_fields = ('phone_number',)
    readonly_fields = ('created_at', 'expire_at')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'membership_status', 'membership_expire_date', 'birth_date', 'birth_place', 'gender', 'divination_count', 'created_at')
    list_filter = ('membership', 'gender', 'phone_verified', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone_number', 'birth_place')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'ai_usage_count')
    
    fieldsets = (
        ('用户基本信息', {
            'fields': ('user', 'phone_number', 'phone_verified', 'created_at')
        }),
        ('个人信息', {
            'fields': ('birth_date', 'birth_place', 'gender'),
            'classes': ('wide',)
        }),
        ('会员信息', {
            'fields': ('membership', 'membership_expire_date'),
            'classes': ('wide',)
        }),
        ('使用统计', {
            'fields': ('ai_usage_count',),
        }),
    )
    
    def membership_status(self, obj):
        if obj.is_vip():
            days_left = (obj.membership_expire_date - timezone.now()).days if obj.membership_expire_date else 0
            color = 'green' if days_left > 7 else 'orange' if days_left > 0 else 'red'
            return format_html(
                '<span style="color: {}; font-weight: bold;">VIP会员 ({}天)</span>',
                color,
                days_left if days_left > 0 else '已过期'
            )
        return format_html('<span style="color: gray;">普通用户</span>')
    membership_status.short_description = '会员状态'
    
    def divination_count(self, obj):
        count = DivinationRecord.objects.filter(user=obj.user).count()
        if count > 0:
            return format_html('<span style="color: green; font-weight: bold;">{}</span>', count)
        return count
    divination_count.short_description = '占卜次数'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(DivinationRecord)
class DivinationRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'divination_type', 'question_preview', 'result_preview', 'created_at')
    list_filter = ('divination_type', 'created_at', 'user__userprofile__gender')
    search_fields = ('user__username', 'question', 'result')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    list_per_page = 20
    
    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'divination_type', 'created_at')
        }),
        ('占卜内容', {
            'fields': ('question', 'result'),
            'classes': ('wide',)
        }),
    )
    
    def question_preview(self, obj):
        if obj.question:
            return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
        return '-'
    question_preview.short_description = '问题预览'
    
    def result_preview(self, obj):
        return obj.result[:100] + '...' if len(obj.result) > 100 else obj.result
    result_preview.short_description = '结果预览'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'user__userprofile')
    
    actions = ['export_records']
    
    def export_records(self, request, queryset):
        # 简单的导出功能
        from django.http import HttpResponse
        import csv
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="divination_records.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['用户', '占卜类型', '问题', '结果', '时间'])
        
        for record in queryset:
            writer.writerow([
                record.user.username if record.user else '匿名',
                record.get_divination_type_display(),
                record.question or '',
                record.result[:200],  # 限制长度
                record.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        return response
    export_records.short_description = '导出选中记录为CSV'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'title', 'message')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'notification_type', 'is_read', 'created_at')
        }),
        ('通知内容', {
            'fields': ('title', 'message'),
            'classes': ('wide',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f'已将 {queryset.count()} 条通知标记为已读。')
    mark_as_read.short_description = '标记为已读'
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, f'已将 {queryset.count()} 条通知标记为未读。')
    mark_as_unread.short_description = '标记为未读'


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan_type', 'price', 'duration_days', 'is_active', 'sort_order', 'created_at')
    list_filter = ('plan_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    list_editable = ('is_active', 'sort_order')
    ordering = ('sort_order', 'price')
    
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'plan_type', 'price', 'duration_days', 'sort_order')
        }),
        ('套餐详情', {
            'fields': ('description', 'features'),
            'classes': ('wide',)
        }),
        ('状态信息', {
            'fields': ('is_active', 'created_at'),
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # 为features字段添加帮助文本
        if 'features' in form.base_fields:
            form.base_fields['features'].help_text = '以JSON列表格式输入特权，例如：["AI增强分析", "无限次使用", "专属客服"]'
        return form


@admin.register(MembershipOrder)
class MembershipOrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'plan', 'amount', 'status', 'payment_method', 'created_at', 'payment_time')
    list_filter = ('status', 'payment_method', 'created_at', 'plan__plan_type')
    search_fields = ('order_id', 'user__username', 'trade_no')
    date_hierarchy = 'created_at'
    readonly_fields = ('order_id', 'created_at', 'updated_at', 'expire_time')
    list_per_page = 25
    ordering = ('-created_at',)
    
    fieldsets = (
        ('订单信息', {
            'fields': ('order_id', 'user', 'plan', 'amount', 'created_at', 'updated_at')
        }),
        ('支付信息', {
            'fields': ('status', 'payment_method', 'payment_time', 'expire_time', 'trade_no'),
            'classes': ('wide',)
        }),
        ('备注信息', {
            'fields': ('remark',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_membership', 'cancel_orders']
    
    def activate_membership(self, request, queryset):
        """手动激活会员"""
        activated_count = 0
        for order in queryset.filter(status='paid'):
            if order.activate_membership():
                activated_count += 1
        
        if activated_count > 0:
            self.message_user(request, f'成功激活 {activated_count} 个会员订单。')
        else:
            self.message_user(request, '没有可激活的订单。', level='warning')
    activate_membership.short_description = '激活会员'
    
    def cancel_orders(self, request, queryset):
        """取消订单"""
        cancelled_count = queryset.filter(status='pending').update(status='cancelled')
        if cancelled_count > 0:
            self.message_user(request, f'成功取消 {cancelled_count} 个待支付订单。')
        else:
            self.message_user(request, '没有可取消的订单。', level='warning')
    cancel_orders.short_description = '取消待支付订单'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'plan')


@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = ('trade_no', 'order', 'amount', 'payment_method', 'created_at')
    list_filter = ('payment_method', 'created_at')
    search_fields = ('trade_no', 'order__order_id')
    date_hierarchy = 'created_at'
    readonly_fields = ('trade_no', 'created_at')
    list_per_page = 25
    ordering = ('-created_at',)
    
    fieldsets = (
        ('支付记录', {
            'fields': ('trade_no', 'order', 'amount', 'payment_method', 'created_at')
        }),
        ('支付数据', {
            'fields': ('payment_data',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order', 'order__user')

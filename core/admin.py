from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import UserProfile, DivinationRecord, Notification

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'birth_place', 'gender', 'divination_count', 'created_at')
    list_filter = ('gender', 'created_at')
    search_fields = ('user__username', 'user__email', 'birth_place')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    
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

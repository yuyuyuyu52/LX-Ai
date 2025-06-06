# Generated by Django 5.2.1 on 2025-05-28 17:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('message', models.TextField(verbose_name='消息内容')),
                ('notification_type', models.CharField(choices=[('info', '信息'), ('success', '成功'), ('warning', '警告'), ('error', '错误')], default='info', max_length=20, verbose_name='通知类型')),
                ('is_read', models.BooleanField(default=False, verbose_name='是否已读')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '用户通知',
                'verbose_name_plural': '用户通知',
                'ordering': ['-created_at'],
            },
        ),
    ]

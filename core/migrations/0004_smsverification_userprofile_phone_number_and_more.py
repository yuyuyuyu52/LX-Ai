# Generated by Django 5.2 on 2025-06-03 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_divinationrecord_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SMSVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(db_index=True, max_length=11, verbose_name='手机号码')),
                ('code', models.CharField(max_length=6, verbose_name='验证码')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('expire_at', models.DateTimeField(verbose_name='过期时间')),
                ('is_used', models.BooleanField(default=False, verbose_name='是否已使用')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='请求IP地址')),
                ('attempt_count', models.IntegerField(default=0, verbose_name='验证尝试次数')),
            ],
            options={
                'verbose_name': '短信验证码',
                'verbose_name_plural': '短信验证码',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='手机号码'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone_verified',
            field=models.BooleanField(default=False, verbose_name='手机已验证'),
        ),
    ]

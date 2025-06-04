from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = '更新数据库模型结构'

    def handle(self, *args, **options):
        # 检查UserProfile表是否有phone_number字段
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA table_info(core_userprofile);")
            columns = [col[1] for col in cursor.fetchall()]
            
            # 如果没有phone_number字段，则添加
            if 'phone_number' not in columns:
                self.stdout.write(self.style.WARNING('正在添加phone_number字段...'))
                cursor.execute("ALTER TABLE core_userprofile ADD COLUMN phone_number VARCHAR(11) NULL;")
                self.stdout.write(self.style.SUCCESS('成功添加phone_number字段'))
            
            # 如果没有phone_verified字段，则添加
            if 'phone_verified' not in columns:
                self.stdout.write(self.style.WARNING('正在添加phone_verified字段...'))
                cursor.execute("ALTER TABLE core_userprofile ADD COLUMN phone_verified BOOL NOT NULL DEFAULT 0;")
                self.stdout.write(self.style.SUCCESS('成功添加phone_verified字段'))
        
        # 创建短信验证码表
        with connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS core_smsverification (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number VARCHAR(11) NOT NULL,
                code VARCHAR(6) NOT NULL,
                created_at DATETIME NOT NULL,
                expire_at DATETIME NOT NULL,
                is_used BOOL NOT NULL DEFAULT 0
            );
            """)
            self.stdout.write(self.style.SUCCESS('成功创建/更新SMS验证码表'))
        
        self.stdout.write(self.style.SUCCESS('数据库更新完成！'))

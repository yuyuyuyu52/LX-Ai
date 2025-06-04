#!/bin/bash
# FateMaster 会员系统快速启动脚本

echo "=== FateMaster 会员系统启动 ==="
echo

# 检查是否在正确的目录
if [ ! -f "manage.py" ]; then
    echo "错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 1. 数据库迁移
echo "1. 执行数据库迁移..."
python3 manage.py migrate

# 2. 初始化会员套餐
echo "2. 初始化会员套餐..."
python3 manage.py init_membership_plans

# 3. 创建超级用户 (如果不存在)
echo "3. 检查超级用户..."
python3 manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(is_superuser=True).exists():
    print('需要创建超级用户，请按提示输入信息:')
    exit(1)
else:
    print('超级用户已存在')
"

if [ $? -eq 1 ]; then
    echo "创建超级用户:"
    python3 manage.py createsuperuser
fi

# 4. 运行系统检查
echo "4. 系统检查..."
python3 manage.py check

# 5. 启动开发服务器
echo "5. 启动开发服务器..."
echo
echo "🚀 服务器启动成功！"
echo "📱 访问地址:"
echo "   主页: http://localhost:8000/"
echo "   会员套餐: http://localhost:8000/membership/"
echo "   管理后台: http://localhost:8000/admin/"
echo "   会员状态API: http://localhost:8000/api/membership/status/"
echo
echo "🛑 按 Ctrl+C 停止服务器"
echo

python3 manage.py runserver 8000

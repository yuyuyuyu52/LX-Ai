# FateMaster 会员系统部署指南

## 系统概述

FateMaster 会员系统是一个完整的Django应用程序，提供两种会员套餐：
- **每日会员**: ¥80，有效期1天
- **年度会员**: ¥365，有效期365天

## 功能特性

### 核心功能
- ✅ 会员套餐管理
- ✅ 订单处理和支付流程
- ✅ 会员状态自动管理
- ✅ 使用次数限制（非VIP用户每日10次）
- ✅ 自动到期清理和通知
- ✅ 完整的管理后台

### 用户功能
- ✅ 会员套餐选择和购买
- ✅ 支付方式选择（支付宝/微信支付）
- ✅ 订单状态跟踪
- ✅ 会员历史记录查看
- ✅ 实时会员状态显示

### 管理功能
- ✅ Django Admin 完整集成
- ✅ 订单管理和状态控制
- ✅ 支付记录追踪
- ✅ 会员数据统计
- ✅ 自动化邮件通知

## 部署步骤

### 1. 环境准备

确保已安装 Python 3.8+ 和相关依赖：

```bash
pip install django==5.2.1
pip install mysqlclient  # 如果使用MySQL
```

### 2. 数据库迁移

运行数据库迁移以创建会员系统相关表：

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. 初始化会员套餐

运行管理命令创建初始会员套餐：

```bash
python manage.py init_membership_plans
```

### 4. 配置设置

#### Django 设置配置 (settings.py)

```python
# 中间件配置（已配置）
MIDDLEWARE = [
    # ... 其他中间件
    'core.middleware.MembershipMiddleware',  # 会员中间件
]

# 邮件配置（开发环境）
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# 生产环境邮件配置
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.163.com'
# EMAIL_PORT = 25
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your_email@163.com'
# EMAIL_HOST_PASSWORD = 'your_password'
# DEFAULT_FROM_EMAIL = 'FateMaster <your_email@163.com>'

# 会员系统配置
MEMBERSHIP_CONFIG = {
    'ORDER_EXPIRE_HOURS': 24,  # 订单过期时间（小时）
    'EXPIRY_WARNING_DAYS': 3,   # 到期提醒天数
    'MAX_DAILY_USAGE': 10,      # 非VIP用户每日使用限制
    'CLEANUP_DAYS': 30,         # 过期订单清理天数
}
```

### 5. URL 配置

确保在主 `urls.py` 中包含了会员系统的URL：

```python
# fatemaster/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    # ... 其他应用的URL
]
```

### 6. 创建超级用户

```bash
python manage.py createsuperuser
```

### 7. 收集静态文件（生产环境）

```bash
python manage.py collectstatic
```

## 生产环境配置

### 1. 数据库配置

**MySQL 配置**：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fatemaster_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

### 2. 支付集成

**替换模拟支付**：

当前系统使用模拟支付进行开发测试。生产环境需要集成真实支付：

```python
# core/membership_views.py - process_payment 函数
# 替换以下代码块：

# 模拟支付处理（开发环境）
# payment_success = True  # 模拟支付成功

# 真实支付集成（生产环境）
if payment_method == 'alipay':
    payment_success = process_alipay_payment(order)
elif payment_method == 'wechat':
    payment_success = process_wechat_payment(order)
```

### 3. 邮件服务配置

**配置SMTP邮件服务**：

```python
# 使用163邮箱示例
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@163.com'
EMAIL_HOST_PASSWORD = 'your_app_password'  # 邮箱授权码
DEFAULT_FROM_EMAIL = 'FateMaster <your_email@163.com>'
```

### 4. 定时任务配置

**设置定时清理任务**：

使用 crontab 设置自动执行过期会员清理：

```bash
# 编辑 crontab
crontab -e

# 添加以下任务（每天凌晨2点执行）
0 2 * * * /path/to/your/venv/bin/python /path/to/your/project/manage.py clean_expired_memberships
```

### 5. 安全配置

**生产环境安全设置**：

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# CSRF 和安全配置
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

## 测试指南

### 运行测试

```bash
# 运行会员系统测试
python manage.py test core.test_membership

# 运行所有测试
python manage.py test
```

### 测试覆盖的功能

- ✅ 会员套餐创建和管理
- ✅ 订单生成和处理
- ✅ 支付流程模拟
- ✅ 会员激活和续期
- ✅ 过期处理和清理
- ✅ 邮件通知服务
- ✅ 中间件功能
- ✅ 完整购买流程

## 管理指南

### Django Admin 管理

访问 `/admin/` 使用超级用户账号登录，可以管理：

1. **会员套餐管理** (`MembershipPlan`)
   - 创建/编辑套餐
   - 设置价格和功能
   - 启用/禁用套餐

2. **订单管理** (`MembershipOrder`)
   - 查看所有订单
   - 手动激活会员
   - 取消订单
   - 订单状态筛选

3. **支付记录** (`PaymentRecord`)
   - 查看支付详情
   - 交易记录追踪
   - 支付状态管理

### 常用管理命令

```bash
# 初始化会员套餐
python manage.py init_membership_plans

# 清理过期会员
python manage.py clean_expired_memberships

# 检查会员系统状态
python manage.py shell
>>> from core.models import MembershipPlan, MembershipOrder
>>> MembershipPlan.objects.all()
>>> MembershipOrder.objects.filter(status='completed').count()
```

## 监控和维护

### 1. 日志监控

建议设置日志记录以监控：
- 支付异常
- 邮件发送失败
- 系统错误

### 2. 数据备份

定期备份数据库，特别是：
- 用户数据
- 订单记录
- 支付记录

### 3. 性能监控

监控关键指标：
- 订单转化率
- 支付成功率
- 用户活跃度
- 系统响应时间

## 常见问题

### Q: 支付后会员没有激活？
A: 检查 `process_payment` 视图中的支付处理逻辑，确保支付成功后调用了 `order.activate_membership()`。

### Q: 邮件通知没有发送？
A: 检查邮件配置是否正确，开发环境使用控制台输出，生产环境需要配置SMTP。

### Q: 用户使用次数限制不生效？
A: 确保在占卜API中正确使用了 `@check_usage_limit` 装饰器。

### Q: 会员到期后状态没有更新？
A: 检查 `MembershipMiddleware` 是否已添加到 `MIDDLEWARE` 设置中。

## 技术支持

如需技术支持或发现问题，请检查：
1. Django 日志输出
2. 数据库连接状态
3. 邮件服务配置
4. 支付接口状态

---

**部署完成后，访问 `/membership/plans/` 查看会员套餐页面，开始使用会员系统！**

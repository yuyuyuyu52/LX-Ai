# FateMaster - 命理大师

一个基于Django+MySQL的专业命理分析网站，提供八字分析、梅花易数、塔罗占卜和黄历查询等功能。

## 功能特色

### 🔮 命理分析
- **八字分析**: 根据出生时间分析性格特征、运势走向
- **梅花易数**: 古老的占卜智慧，预测事物发展趋势
- **塔罗占卜**: 神秘的塔罗牌阵，指引人生方向
- **易经卜卦**: 传统易经智慧，解答人生疑惑

### 📅 黄历查询
- **今日运势**: 查看当日宜忌事项
- **农历信息**: 完整的农历日期信息
- **节气查询**: 二十四节气详细信息

### 👤 用户系统
- **个人档案**: 保存用户出生信息
- **历史记录**: 查看占卜历史记录
- **结果保存**: 重要占卜结果永久保存

## 技术架构

### 后端技术
- **Django 5.2.1**: Python Web框架
- **MySQL**: 关系型数据库
- **mysqlclient**: MySQL数据库连接器

### 前端技术
- **Bootstrap 5**: 响应式UI框架
- **Font Awesome**: 图标库
- **原生JavaScript**: 交互逻辑

### 项目结构
```
fatemaster/
├── manage.py                 # Django管理脚本
├── fatemaster/              # 项目配置目录
│   ├── settings.py          # 项目设置
│   ├── urls.py              # 主URL配置
│   └── wsgi.py              # WSGI配置
├── core/                    # 核心应用
│   ├── models.py            # 用户档案、占卜记录模型
│   ├── views.py             # 核心视图函数
│   └── urls.py              # 核心应用URL配置
├── divination/              # 占卜应用
│   ├── models.py            # 占卜相关模型
│   ├── views.py             # 占卜算法和API
│   └── urls.py              # 占卜应用URL配置
├── chinese_calendar/        # 黄历应用
│   ├── models.py            # 日历数据模型
│   ├── views.py             # 日历查询视图
│   └── urls.py              # 日历应用URL配置
├── templates/               # 模板文件
│   ├── base.html            # 基础模板
│   ├── core/                # 核心应用模板
│   ├── divination/          # 占卜应用模板
│   └── chinese_calendar/    # 日历应用模板
└── static/                  # 静态文件
    ├── css/                 # 样式文件
    ├── js/                  # JavaScript文件
    └── images/              # 图片资源
```

## 安装指南

### 环境要求
- Python 3.8+
- MySQL 5.7+
- pip包管理器

### 安装步骤

1. **安装Python依赖**
```bash
pip install django mysqlclient pillow requests beautifulsoup4
```

2. **配置数据库**
```sql
CREATE DATABASE fatemaster_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'fatemaster'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON fatemaster_db.* TO 'fatemaster'@'localhost';
FLUSH PRIVILEGES;
```

3. **更新数据库配置**
编辑 `fatemaster/settings.py`，更新数据库连接信息：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fatemaster_db',
        'USER': 'fatemaster',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

4. **数据库迁移**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **创建超级用户**
```bash
python manage.py createsuperuser
```

6. **运行开发服务器**
```bash
python manage.py runserver
```

## 使用说明

### 访问网站
打开浏览器访问 `http://localhost:8000`

### 主要功能使用

#### 八字分析
1. 点击导航栏"命理分析" → "八字分析"
2. 输入出生日期、时辰、性别等信息
3. 点击"开始八字分析"获取详细分析结果

#### 塔罗占卜
1. 进入塔罗占卜页面
2. 输入您想咨询的问题
3. 选择合适的牌阵类型
4. 获取塔罗牌指引和解读

#### 黄历查询
1. 访问黄历查询页面
2. 查看今日运势和宜忌
3. 选择特定日期查询农历信息

### 管理后台
访问 `http://localhost:8000/admin` 进入Django管理后台，可以管理用户、占卜记录等数据。

## 开发说明

### 扩展功能
- 添加更多占卜算法
- 集成第三方支付系统
- 增加社交分享功能
- 开发移动应用

### API接口
项目提供RESTful API接口：
- `/divination/api/bazi/` - 八字分析API
- `/divination/api/tarot/` - 塔罗占卜API
- `/calendar/api/date/<date>/` - 日期信息API

### 自定义配置
可以通过修改 `settings.py` 来自定义：
- 数据库配置
- 静态文件路径
- 时区设置
- 调试模式

## 部署建议

### 生产环境配置
1. 设置 `DEBUG = False`
2. 配置 `ALLOWED_HOSTS`
3. 使用HTTPS
4. 配置静态文件服务器
5. 使用专业数据库服务

### 性能优化
- 启用数据库连接池
- 配置Redis缓存
- 使用CDN加速静态资源
- 启用Gzip压缩

## 许可证
此项目仅供学习和研究使用。

## 联系方式
如有问题或建议，请通过以下方式联系：
- 邮箱: info@fatemaster.com
- 电话: 400-123-4567

---

*注意：本项目中的占卜算法为简化版本，仅供娱乐参考，不构成专业建议。*

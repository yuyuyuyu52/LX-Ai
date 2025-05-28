# 灵汐命理平台 - 使用指南

## 🌙 欢迎来到灵汐命理平台

**静心观命，感悟人生智慧**

---

## 🚀 快速开始

### 启动开发服务器
```bash
cd LX-Ai
python manage.py runserver
```
然后访问 `http://127.0.0.1:8000`

### 访问管理后台
```bash
python manage.py createsuperuser  # 首次需要创建管理员账户
```
访问 `http://127.0.0.1:8000/admin`

## 🎨 设计系统使用

### CSS类名规范

#### 按钮组件
```html
<!-- 主要按钮 -->
<button class="zen-btn zen-btn-primary">确认</button>

<!-- 次要按钮 -->
<button class="zen-btn zen-btn-secondary">取消</button>

<!-- 轮廓按钮 -->
<button class="zen-btn zen-btn-outline">了解更多</button>
```

#### 卡片组件
```html
<!-- 基础卡片 -->
<div class="zen-card">
    <div class="zen-card-header">
        <h5 class="zen-subtitle">标题</h5>
    </div>
    <div class="zen-card-body">
        内容区域
    </div>
</div>
```

#### 表单组件
```html
<!-- 表单控件 -->
<label class="zen-form-label">标签</label>
<input class="zen-form-control" type="text" placeholder="请输入...">
<select class="zen-form-control">
    <option>选项1</option>
</select>
```

### 颜色系统

#### CSS变量
```css
var(--zen-bg)          /* 背景色 #FDF9F3 */
var(--zen-primary)     /* 主文字色 #3E2C1D */
var(--zen-secondary)   /* 次文字色 #A89E92 */
var(--zen-accent)      /* 强调色 #C8B89E */
var(--zen-decoration)  /* 装饰色 #E7DAC6 */
```

#### 文字颜色类
```html
<span class="zen-text-primary">主要文字</span>
<span class="zen-text-secondary">次要文字</span>
<span class="zen-text-accent">强调文字</span>
<span class="zen-text-decoration">装饰文字</span>
```

## 📱 页面功能说明

### 首页 (`/`)
- Hero区域展示品牌核心理念
- 统计数据展示平台活跃度
- 功能特色介绍各项服务
- 最新占卜记录展示
- 今日运势快速入口

### 占卜功能
- **八字分析** (`/divination/bazi/`)：生辰八字详细分析
- **塔罗占卜** (`/divination/tarot/`)：多种牌阵占卜
- **梅花易数** (`/divination/meihua/`)：传统易学占卜
- **易经卜卦** (`/divination/yijing/`)：六十四卦占卜

### 黄历功能
- **日历查询** (`/calendar/`)：查看特定日期黄历
- **今日运势** (`/calendar/today/`)：当日详细运势分析

### 用户功能
- **用户注册** (`/register/`)：新用户注册
- **用户登录** (`/login/`)：用户身份验证
- **个人档案** (`/profile/`)：查看和管理个人信息
- **搜索记录** (`/search/`)：搜索历史占卜记录

## 🎯 设计原则

### 1. 极简主义
- 避免不必要的装饰元素
- 保持界面清洁简洁
- 突出核心功能和内容

### 2. 东方美学
- 使用传统中式配色
- 融入禅意文化元素
- 体现含蓄内敛的美感

### 3. 用户体验
- 确保操作流程顺畅
- 提供清晰的视觉反馈
- 保持一致的交互模式

### 4. 情感设计
- 营造温暖亲切的氛围
- 注重文案的情感表达
- 创造治愈系的视觉体验

## 🔧 开发注意事项

### 添加新页面
1. 继承 `base.html` 模板
2. 使用 `zen-` 前缀的CSS类
3. 遵循既定的设计规范
4. 保持品牌一致性

### 样式开发
1. 新样式添加到 `zen-style.css`
2. 使用CSS变量定义的颜色
3. 遵循命名规范
4. 确保响应式设计

### 文案撰写
1. 体现禅意文化内涵
2. 使用温和友善的语调
3. 避免过于商业化的表达
4. 突出情感关怀

## 📊 性能优化

### 图片优化
- 使用合适的图片格式
- 压缩图片文件大小
- 实现懒加载机制

### CSS优化
- 避免重复样式定义
- 使用CSS变量提高维护性
- 合理组织样式结构

### JavaScript优化
- 最小化DOM操作
- 使用事件委托
- 避免内存泄漏

## 🌟 特色功能

### 1. 通知系统
```javascript
// 显示成功通知
const notification = document.createElement('div');
notification.className = 'zen-notification';
notification.innerHTML = '<i class="fas fa-check-circle me-2"></i>操作成功';
document.body.appendChild(notification);
```

### 2. 时辰运势卡片
```html
<div class="zen-time-fortune-card zen-fortune-good">
    <div class="fw-bold zen-text-primary">子时</div>
    <div class="small zen-text-secondary">23:00-01:00</div>
    <div class="zen-badge zen-badge-accent mt-1">吉</div>
</div>
```

### 3. 进度条组件
```html
<div class="zen-progress">
    <div class="zen-progress-bar zen-progress-primary" style="width: 75%"></div>
</div>
```

## 🎨 自定义主题

### 修改配色方案
在 `zen-style.css` 文件的 `:root` 选择器中修改CSS变量：

```css
:root {
    --zen-bg: #你的背景色;
    --zen-primary: #你的主色调;
    --zen-secondary: #你的次要色;
    --zen-accent: #你的强调色;
    --zen-decoration: #你的装饰色;
}
```

### 添加新组件
1. 在CSS文件中定义样式
2. 遵循 `.zen-` 命名规范
3. 确保与现有设计协调
4. 提供使用示例

## 📞 支持与反馈

如果在使用过程中遇到问题或有改进建议，请：

1. 检查控制台错误信息
2. 确认CSS和JavaScript文件正确加载
3. 验证模板语法正确性
4. 查看Django开发服务器日志

---

*愿每一位使用者都能在灵汐命理平台找到内心的宁静与智慧。*

**文档版本**：v1.0  
**最后更新**：2025年5月29日

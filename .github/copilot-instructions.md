<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# FateMaster 项目 - Copilot 指令

这是一个基于Django和MySQL的命理分析网站项目，提供八字分析、塔罗占卜、梅花易数和黄历查询等功能。

## 项目架构
- **后端**: Django 5.2.1 + MySQL
- **前端**: Bootstrap 5 + 原生JavaScript
- **语言**: Python 3.8+, HTML5, CSS3, JavaScript

## 代码规范

### Python/Django
- 遵循PEP 8代码规范
- 使用Django最佳实践
- 模型命名使用CamelCase
- 视图函数使用snake_case
- 优先使用类视图处理复杂逻辑
- 所有字符串使用中文注释

### 前端
- 使用Bootstrap 5组件系统
- JavaScript使用ES6+语法
- CSS使用BEM命名规范
- 响应式设计优先
- 优化用户体验和交互

### 数据库
- 使用MySQL数据库
- 模型字段使用中文verbose_name
- 建立适当的外键关系
- 添加数据库索引优化查询

## 功能模块

### core应用 - 核心功能
- 用户档案管理
- 占卜记录存储
- 首页和基础页面

### divination应用 - 占卜功能
- 八字分析算法
- 塔罗牌占卜
- 梅花易数
- 易经卜卦
- API接口提供

### chinese_calendar应用 - 黄历功能
- 农历日期转换
- 黄历宜忌查询
- 节气信息

## 开发要求

1. **安全性**: 使用Django内置的安全特性，防止CSRF、XSS等攻击
2. **性能**: 优化数据库查询，使用缓存
3. **用户体验**: 提供友好的错误提示和加载状态
4. **国际化**: 支持中文本地化
5. **测试**: 为关键功能编写单元测试

## 占卜算法说明

- 八字分析基于传统命理学原理
- 塔罗占卜提供多种牌阵选择
- 所有占卜结果仅供娱乐参考
- 实现时注重用户体验和界面美观

## 特别注意

- 所有用户输入需要验证和清理
- 占卜结果需要格式化展示
- 支持游客使用和注册用户
- 提供占卜历史记录功能
- 确保移动端兼容性

/**
 * Markdown 格式化工具
 * 使用marked.js库将Markdown文本转换为HTML格式显示
 */

// 配置marked选项
marked.setOptions({
    breaks: true,  // 支持GitHub风格的换行
    gfm: true,     // 启用GitHub风格的Markdown
    headerIds: false, // 禁用标题ID生成
    mangle: false,  // 禁用标题ID混淆
    sanitize: false, // 允许HTML标签
    smartLists: true, // 使用更智能的列表行为
    smartypants: true, // 使用更智能的标点符号
    xhtml: false   // 不使用xhtml
});

// 基础Markdown格式化函数
function formatMarkdown(text) {
    if (!text) return '';
    return marked.parse(text);
}

// 进阶AI格式化函数，处理更复杂的结构
function formatAIMarkdown(text) {
    if (!text) return '';
    return marked.parse(text);
}

// 简单版本，主要处理换行和强调
function formatSimpleMarkdown(text) {
    if (!text) return '';
    return marked.parse(text);
}

/**
 * Markdown 格式化工具
 * 用于将Markdown文本转换为HTML格式显示
 */

// 基础Markdown格式化函数
function formatMarkdown(text) {
    if (!text) return '';
    
    return text
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/#{3}\s+(.*?)(\n|$)/g, '<h3>$1</h3>')
        .replace(/#{2}\s+(.*?)(\n|$)/g, '<h2>$1</h2>')
        .replace(/#{1}\s+(.*?)(\n|$)/g, '<h1>$1</h1>')
        .replace(/`{3}([\s\S]*?)`{3}/g, '<pre><code>$1</code></pre>')
        .replace(/`(.*?)`/g, '<code>$1</code>')
        .replace(/!\[(.*?)\]\((.*?)\)/g, '<img alt="$1" src="$2">')
        .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>')
        .replace(/(\n|^)(\d+\.\s+)(.*?)(\n|$)/g, '$1<ol><li>$3</li></ol>$4')
        .replace(/(\n|^)(\-\s+)(.*?)(\n|$)/g, '$1<ul><li>$3</li></ul>$4')
        .replace(/>>\s+(.*?)(\n|$)/g, '<blockquote>$1</blockquote>')
        .replace(/【(.*?)】/g, '<span class="badge bg-light text-dark me-2">$1</span>');
}

// 进阶AI格式化函数，处理更复杂的结构
function formatAIMarkdown(text) {
    if (!text) return '';
    
    // 处理AI分析的特殊格式
    return text
        .replace(/(\d+\.\s*\*\*.*?\*\*)/g, '<h6 class="text-primary mt-4 mb-2">$1</h6>')
        .replace(/\*\*(.*?)\*\*/g, '<strong class="text-dark">$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/【(.*?)】/g, '<span class="badge bg-light text-dark me-2">$1</span>')
        .replace(/\n/g, '<br>')
        .replace(/(\- .*?)(<br>|$)/g, '<li class="mb-1">$1</li>')
        .replace(/(<li.*?<\/li>)/g, '<ul class="list-unstyled ms-3">$1</ul>');
}

// 简单版本，主要处理换行和强调
function formatSimpleMarkdown(text) {
    if (!text) return '';
    
    return text
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/【(.*?)】/g, '<span class="badge bg-light text-dark me-2">$1</span>');
}

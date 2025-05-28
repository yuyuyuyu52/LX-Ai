// 全局JavaScript功能

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化工具提示
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // 初始化弹出框
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // 添加页面加载动画
    addPageAnimations();
    
    // 初始化导航栏滚动效果
    initNavbarScrollEffect();
    
    // 初始化通知系统
    initNotificationSystem();
});

// 通知系统
function initNotificationSystem() {
    const notificationDropdown = document.getElementById('notificationDropdown');
    const notificationCount = document.querySelector('.notification-count');
    const notificationList = document.getElementById('notificationList');
    const markAllReadBtn = document.getElementById('markAllRead');
    
    if (!notificationDropdown) return;
    
    // 加载通知
    loadNotifications();
    
    // 定期检查新通知
    setInterval(loadNotifications, 30000); // 每30秒检查一次
    
    // 标记所有已读
    if (markAllReadBtn) {
        markAllReadBtn.addEventListener('click', function() {
            markAllNotificationsRead();
        });
    }
}

function loadNotifications() {
    fetch('/api/notifications/')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateNotificationUI(data.notifications, data.unread_count);
            }
        })
        .catch(error => {
            console.error('加载通知失败:', error);
        });
}

function updateNotificationUI(notifications, unreadCount) {
    const notificationCount = document.querySelector('.notification-count');
    const notificationList = document.getElementById('notificationList');
    
    // 更新通知数量
    if (notificationCount) {
        if (unreadCount > 0) {
            notificationCount.textContent = unreadCount;
            notificationCount.style.display = 'inline-block';
        } else {
            notificationCount.style.display = 'none';
        }
    }
    
    // 更新通知列表
    if (notificationList) {
        if (notifications.length === 0) {
            notificationList.innerHTML = '<div class="text-center p-3 text-muted">暂无通知</div>';
        } else {
            let notificationHTML = '';
            notifications.forEach(notification => {
                const typeIcon = getNotificationIcon(notification.type);
                const readClass = notification.is_read ? 'opacity-75' : '';
                
                notificationHTML += `
                    <div class="dropdown-item notification-item ${readClass}" data-notification-id="${notification.id}">
                        <div class="d-flex">
                            <div class="flex-shrink-0 me-2">
                                <i class="${typeIcon} text-${notification.type}"></i>
                            </div>
                            <div class="flex-grow-1">
                                <h6 class="mb-1 fs-6">${notification.title}</h6>
                                <p class="mb-1 small text-muted">${notification.message}</p>
                                <small class="text-muted">${notification.created_at}</small>
                            </div>
                            ${!notification.is_read ? '<div class="flex-shrink-0"><span class="badge bg-primary rounded-pill">新</span></div>' : ''}
                        </div>
                    </div>
                `;
            });
            notificationList.innerHTML = notificationHTML;
            
            // 添加点击事件
            document.querySelectorAll('.notification-item').forEach(item => {
                item.addEventListener('click', function() {
                    const notificationId = this.dataset.notificationId;
                    markNotificationRead(notificationId);
                });
            });
        }
    }
}

function getNotificationIcon(type) {
    const icons = {
        'info': 'fas fa-info-circle',
        'success': 'fas fa-check-circle',
        'warning': 'fas fa-exclamation-triangle',
        'error': 'fas fa-times-circle'
    };
    return icons[type] || 'fas fa-bell';
}

function markNotificationRead(notificationId) {
    fetch('/api/notifications/mark-read/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            notification_id: notificationId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadNotifications(); // 重新加载通知列表
        }
    })
    .catch(error => {
        console.error('标记通知已读失败:', error);
    });
}

function markAllNotificationsRead() {
    fetch('/api/notifications/mark-all-read/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadNotifications(); // 重新加载通知列表
        }
    })
    .catch(error => {
        console.error('标记所有通知已读失败:', error);
    });
}

function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
}

// 页面动画
function addPageAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);

    // 观察所有卡片元素
    document.querySelectorAll('.card, .feature-card').forEach(card => {
        observer.observe(card);
    });
}

// 导航栏滚动效果
function initNavbarScrollEffect() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(102, 126, 234, 0.95)';
            navbar.style.backdropFilter = 'blur(10px)';
        } else {
            navbar.style.background = '';
            navbar.style.backdropFilter = '';
        }
    });
}

// 用户登录功能
function handleLogin() {
    const form = document.getElementById('loginForm');
    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        if (!username || !password) {
            showAlert('请填写用户名和密码', 'warning');
            return;
        }
        
        // 这里应该发送登录请求到服务器
        // 暂时模拟登录成功
        showAlert('登录成功！', 'success');
        setTimeout(() => {
            location.reload();
        }, 1000);
    });
}

// 用户注销
function logout() {
    if (confirm('确定要退出登录吗？')) {
        // 发送注销请求
        fetch('/auth/logout/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfToken()
            }
        })
        .then(() => {
            location.reload();
        })
        .catch(error => {
            console.error('Logout error:', error);
            showAlert('退出失败，请重试', 'danger');
        });
    }
}

// 获取CSRF Token
function getCsrfToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfToken ? csrfToken.value : '';
}

// 显示提示信息
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 80px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // 自动移除提示
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// 加载动画控制
function showLoading(element, text = '加载中...') {
    if (!element) return;
    
    element.disabled = true;
    element.dataset.originalText = element.innerHTML;
    element.innerHTML = `<i class="fas fa-spinner fa-spin me-2"></i>${text}`;
}

function hideLoading(element) {
    if (!element) return;
    
    element.disabled = false;
    if (element.dataset.originalText) {
        element.innerHTML = element.dataset.originalText;
    }
}

// 时间格式化
function formatDate(date) {
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(date).toLocaleDateString('zh-CN', options);
}

// 节流函数
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// 防抖函数
function debounce(func, delay) {
    let timeoutId;
    return function() {
        const context = this;
        const args = arguments;
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(context, args), delay);
    };
}

// 平滑滚动到元素
function scrollToElement(element, offset = 0) {
    if (typeof element === 'string') {
        element = document.querySelector(element);
    }
    
    if (element) {
        const elementPosition = element.offsetTop - offset;
        window.scrollTo({
            top: elementPosition,
            behavior: 'smooth'
        });
    }
}

// 复制文本到剪贴板
function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(() => {
            showAlert('已复制到剪贴板', 'success');
        }).catch(err => {
            console.error('复制失败:', err);
            showAlert('复制失败', 'danger');
        });
    } else {
        // 降级方案
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            document.execCommand('copy');
            showAlert('已复制到剪贴板', 'success');
        } catch (err) {
            showAlert('复制失败', 'danger');
        }
        document.body.removeChild(textArea);
    }
}

// 本地存储辅助函数
const Storage = {
    set: function(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.error('存储失败:', e);
        }
    },
    
    get: function(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (e) {
            console.error('读取存储失败:', e);
            return defaultValue;
        }
    },
    
    remove: function(key) {
        try {
            localStorage.removeItem(key);
        } catch (e) {
            console.error('删除存储失败:', e);
        }
    }
};

// API请求辅助函数
const API = {
    get: function(url) {
        return fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            }
        }).then(response => response.json());
    },
    
    post: function(url, data) {
        return fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify(data)
        }).then(response => response.json());
    }
};

// 初始化登录表单
handleLogin();

// 狗蛋导航系统后台管理脚本
const API_BASE_URL = 'http://82.156.52.192:5000/api';

// 全局状态
let currentTab = 'users';
let currentEditingSite = null;
let currentSessionToken = null;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 在DOM加载完成后才读取localStorage
    currentSessionToken = localStorage.getItem('admin_session_token');
    console.log('DOM加载完成，读取令牌:', currentSessionToken);
    checkLoginStatus();
});

// 检查登录状态
async function checkLoginStatus() {
    console.log('检查登录状态，当前令牌:', currentSessionToken);
    
    // 如果会话令牌不存在，直接显示登录页面
    if (!currentSessionToken) {
        console.log('令牌不存在，显示登录页面');
        showLoginModal();
        return;
    }

    // 会话令牌存在，验证其有效性
    try {
        console.log('开始验证会话令牌');
        const response = await fetch(`${API_BASE_URL}/auth/verify`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_token: currentSessionToken })
        });

        console.log('验证响应状态:', response.status);
        const result = await response.json();
        console.log('验证结果:', result);
        
        if (result.valid) {
            // 会话有效，初始化后台管理界面
            console.log('会话有效，初始化管理界面');
            initializeAdmin();
            document.getElementById('current-user').textContent = result.username;
        } else {
            // 会话无效，清除令牌并显示登录页面
            console.log('会话无效，清除令牌');
            localStorage.removeItem('admin_session_token');
            currentSessionToken = null;
            showLoginModal();
        }
    } catch (error) {
        console.error('验证会话失败:', error);
        // 验证失败，清除令牌并显示登录页面
        localStorage.removeItem('admin_session_token');
        currentSessionToken = null;
        showLoginModal();
    }
}

// 显示登录模态框
function showLoginModal() {
    // 隐藏主界面
    document.getElementById('admin-container').style.display = 'none';
    
    // 显示登录界面
    document.getElementById('login-container').style.display = 'flex';
    
    // 设置登录表单提交事件
    document.getElementById('login-form').addEventListener('submit', handleLogin);
}

// 处理登录
async function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            throw new Error('登录失败');
        }

        const result = await response.json();
        
        // 保存会话令牌
        localStorage.setItem('admin_session_token', result.session_token);
        currentSessionToken = result.session_token;
        
        // 隐藏登录界面，显示主界面
        document.getElementById('login-container').style.display = 'none';
        document.getElementById('admin-container').style.display = 'block';
        
        document.getElementById('current-user').textContent = result.username;
        initializeAdmin();
        
    } catch (error) {
        console.error('登录失败:', error);
        showMessage('用户名或密码错误', 'error');
    }
}

// 初始化后台管理
function initializeAdmin() {
    // 显示管理界面，隐藏登录界面
    document.getElementById('admin-container').style.display = 'block';
    document.getElementById('login-container').style.display = 'none';
    
    // 设置标签页切换事件
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            if (this.dataset.tab === 'logout') {
                logout();
                return;
            }
            switchTab(this.dataset.tab);
        });
    });

    // 设置表单提交事件
    document.getElementById('site-form').addEventListener('submit', handleSiteFormSubmit);

    // 加载默认标签页数据
    switchTab('users');
}

// 切换标签页
function switchTab(tabName) {
    // 移除所有标签页的active类
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // 激活当前标签页
    document.getElementById(`${tabName}-tab`).classList.add('active');
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

    currentTab = tabName;

    // 加载对应标签页的数据
    switch(tabName) {
        case 'users':
            loadUsersData();
            break;
        case 'sites':
            loadSitesData();
            break;
        case 'stats':
            loadStatsData();
            break;
    }
}

// 加载用户数据
async function loadUsersData() {
    try {
        showLoading('users-table-body');
        
        // 获取用户列表
        const usersResponse = await fetch(`${API_BASE_URL}/auth/users`, {
            headers: {
                'X-Session-Token': currentSessionToken
            }
        });
        if (!usersResponse.ok) {
            if (usersResponse.status === 401) {
                handleUnauthorized();
                return;
            }
            throw new Error('获取用户数据失败');
        }
        const usersData = await usersResponse.json();

        // 获取用户收藏统计
        const favoritesResponse = await fetch(`${API_BASE_URL}/favorites/stats`, {
            headers: {
                'X-Session-Token': currentSessionToken
            }
        });
        const favoritesData = await favoritesResponse.ok ? await favoritesResponse.json() : { users: {} };

        // 更新统计卡片
        updateUserStats(usersData.users || []);

        // 更新用户表格
        updateUsersTable(usersData.users || [], favoritesData.users || {});

    } catch (error) {
        console.error('加载用户数据失败:', error);
        showMessage('加载用户数据失败', 'error');
    }
}

// 更新用户统计信息
function updateUserStats(users) {
    const today = new Date().toISOString().split('T')[0];
    const todayUsers = users.filter(user => 
        user.created_at && user.created_at.startsWith(today)
    ).length;

    document.getElementById('total-users').textContent = users.length;
    document.getElementById('today-users').textContent = todayUsers;
    document.getElementById('active-users').textContent = users.length; // 简化处理
}

// 更新用户表格
function updateUsersTable(users, favoritesStats) {
    const tbody = document.getElementById('users-table-body');
    tbody.innerHTML = '';

    if (users.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center;">暂无用户数据</td></tr>';
        return;
    }

    users.forEach(user => {
        const row = document.createElement('tr');
        const favoritesCount = favoritesStats[user.id] || 0;
        
        row.innerHTML = `
            <td>${user.id}</td>
            <td>${user.username}</td>
            <td>${user.email || '-'}</td>
            <td>${formatDate(user.created_at)}</td>
            <td>${favoritesCount}</td>
            <td>
                <button class="action-btn delete-btn" onclick="deleteUser(${user.id})">删除</button>
            </td>
        `;
        
        tbody.appendChild(row);
    });
}

// 加载网站数据
async function loadSitesData() {
    try {
        showLoading('sites-table-body');
        
        // 获取网站列表
        const sitesResponse = await fetch(`${API_BASE_URL}/sites?category=all`, {
            headers: {
                'X-Session-Token': currentSessionToken
            }
        });
        if (!sitesResponse.ok) {
            if (sitesResponse.status === 401) {
                handleUnauthorized();
                return;
            }
            throw new Error('获取网站数据失败');
        }
        const sitesData = await sitesResponse.json();

        // 获取网站收藏统计
        const favoritesResponse = await fetch(`${API_BASE_URL}/favorites/site-stats`, {
            headers: {
                'X-Session-Token': currentSessionToken
            }
        });
        const favoritesData = await favoritesResponse.ok ? await favoritesResponse.json() : { sites: {} };

        // 更新统计卡片
        updateSiteStats(sitesData.sites || []);

        // 更新网站表格
        updateSitesTable(sitesData.sites || [], favoritesData.sites || {});

    } catch (error) {
        console.error('加载网站数据失败:', error);
        showMessage('加载网站数据失败', 'error');
    }
}

// 更新网站统计信息
function updateSiteStats(sites) {
    const categoryCounts = {
        'ai': 0,
        'work': 0,
        'study': 0,
        'entertainment': 0,
        'tools': 0
    };

    sites.forEach(site => {
        if (categoryCounts.hasOwnProperty(site.category)) {
            categoryCounts[site.category]++;
        }
    });

    document.getElementById('total-sites').textContent = sites.length;
    document.getElementById('ai-sites').textContent = categoryCounts.ai;
    document.getElementById('work-sites').textContent = categoryCounts.work;
    document.getElementById('study-sites').textContent = categoryCounts.study;
    document.getElementById('entertainment-sites').textContent = categoryCounts.entertainment;
    document.getElementById('tools-sites').textContent = categoryCounts.tools;
}

// 更新网站表格
function updateSitesTable(sites, favoritesStats) {
    const tbody = document.getElementById('sites-table-body');
    const categoryFilter = document.getElementById('category-filter').value;
    
    tbody.innerHTML = '';

    // 过滤网站
    const filteredSites = sites.filter(site => 
        categoryFilter === 'all' || site.category === categoryFilter
    );

    if (filteredSites.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align: center;">暂无网站数据</td></tr>';
        return;
    }

    filteredSites.forEach(site => {
        const row = document.createElement('tr');
        const favoritesCount = favoritesStats[site.id] || 0;
        
        row.innerHTML = `
            <td>${site.id}</td>
            <td>${site.name}</td>
            <td><a href="${site.url}" target="_blank">${site.url}</a></td>
            <td>${getCategoryDisplayName(site.category)}</td>
            <td>${site.icon || '-'}</td>
            <td>${site.description || '-'}</td>
            <td>${favoritesCount}</td>
            <td>
                <button class="action-btn edit-btn" onclick="editSite(${site.id})">编辑</button>
                <button class="action-btn delete-btn" onclick="deleteSite(${site.id})">删除</button>
            </td>
        `;
        
        tbody.appendChild(row);
    });
}

// 加载统计信息
async function loadStatsData() {
    try {
        // 获取网站统计
        const sitesResponse = await fetch(`${API_BASE_URL}/stats`, {
            headers: {
                'X-Session-Token': currentSessionToken
            }
        });
        if (!sitesResponse.ok) {
            if (sitesResponse.status === 401) {
                handleUnauthorized();
                return;
            }
            throw new Error('获取统计信息失败');
        }
        const sitesStats = await sitesResponse.json();

        // 获取用户统计
        const usersResponse = await fetch(`${API_BASE_URL}/auth/stats`, {
            headers: {
                'X-Session-Token': currentSessionToken
            }
        });
        const usersStats = await usersResponse.ok ? await usersResponse.json() : { total: 0, today: 0 };

        // 获取收藏统计
        const favoritesResponse = await fetch(`${API_BASE_URL}/favorites/stats`, {
            headers: {
                'X-Session-Token': currentSessionToken
            }
        });
        const favoritesStats = await favoritesResponse.ok ? await favoritesResponse.json() : { total: 0, today: 0 };

        // 更新统计信息
        updateStatsOverview(sitesStats, usersStats, favoritesStats);
        updateCategoryChart(sitesStats.stats || {});
        updateActivityStats(usersStats, favoritesStats);

    } catch (error) {
        console.error('加载统计信息失败:', error);
        showMessage('加载统计信息失败', 'error');
    }
}

// 更新统计概览
function updateStatsOverview(sitesStats, usersStats, favoritesStats) {
    document.getElementById('overview-total-sites').textContent = 
        Object.values(sitesStats.stats || {}).reduce((sum, count) => sum + count, 0);
    document.getElementById('overview-total-users').textContent = usersStats.total || 0;
    document.getElementById('overview-total-favorites').textContent = favoritesStats.total || 0;
}

// 更新分类图表
function updateCategoryChart(categoryStats) {
    const chartContainer = document.getElementById('category-chart');
    chartContainer.innerHTML = '';

    if (Object.keys(categoryStats).length === 0) {
        chartContainer.innerHTML = '<p>暂无分类数据</p>';
        return;
    }

    const total = Object.values(categoryStats).reduce((sum, count) => sum + count, 0);
    
    Object.entries(categoryStats).forEach(([category, count]) => {
        const percentage = ((count / total) * 100).toFixed(1);
        const categoryName = getCategoryDisplayName(category);
        
        const chartItem = document.createElement('div');
        chartItem.style.marginBottom = '10px';
        chartItem.innerHTML = `
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>${categoryName}</span>
                <span>${count} (${percentage}%)</span>
            </div>
            <div style="background: #ecf0f1; height: 8px; border-radius: 4px;">
                <div style="background: #3498db; height: 100%; width: ${percentage}%; border-radius: 4px;"></div>
            </div>
        `;
        
        chartContainer.appendChild(chartItem);
    });
}

// 更新活跃度统计
function updateActivityStats(usersStats, favoritesStats) {
    document.getElementById('today-new-users').textContent = usersStats.today || 0;
    document.getElementById('today-new-favorites').textContent = favoritesStats.today || 0;
    document.getElementById('recent-active-users').textContent = usersStats.total || 0; // 简化处理
}

// 显示添加网站表单
function showAddSiteForm() {
    currentEditingSite = null;
    document.getElementById('site-modal-title').textContent = '添加网站';
    document.getElementById('site-form').reset();
    document.getElementById('site-modal').style.display = 'flex';
}

// 编辑网站
async function editSite(siteId) {
    try {
        const response = await fetch(`${API_BASE_URL}/sites/${siteId}`, {
            headers: {
                'X-Session-Token': currentSessionToken
            }
        });
        if (!response.ok) {
            if (response.status === 401) {
                handleUnauthorized();
                return;
            }
            throw new Error('获取网站信息失败');
        }
        const siteData = await response.json();

        currentEditingSite = siteId;
        document.getElementById('site-modal-title').textContent = '编辑网站';
        document.getElementById('site-name').value = siteData.name;
        document.getElementById('site-url').value = siteData.url;
        document.getElementById('site-category').value = siteData.category;
        document.getElementById('site-icon').value = siteData.icon || '';
        document.getElementById('site-description').value = siteData.description || '';
        document.getElementById('site-modal').style.display = 'flex';

    } catch (error) {
        console.error('获取网站信息失败:', error);
        showMessage('获取网站信息失败', 'error');
    }
}

// 处理网站表单提交
async function handleSiteFormSubmit(event) {
    event.preventDefault();

    const formData = {
        name: document.getElementById('site-name').value,
        url: document.getElementById('site-url').value,
        category: document.getElementById('site-category').value,
        icon: document.getElementById('site-icon').value,
        description: document.getElementById('site-description').value
    };

    try {
        let response;
        
        if (currentEditingSite) {
            // 编辑现有网站
            response = await fetch(`${API_BASE_URL}/sites/${currentEditingSite}`, {
                method: 'PUT',
                headers: { 
                    'Content-Type': 'application/json',
                    'X-Session-Token': currentSessionToken
                },
                body: JSON.stringify(formData)
            });
        } else {
            // 添加新网站
            response = await fetch(`${API_BASE_URL}/sites`, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'X-Session-Token': currentSessionToken
                },
                body: JSON.stringify(formData)
            });
        }

        if (!response.ok) {
            if (response.status === 401) {
                handleUnauthorized();
                return;
            }
            throw new Error('保存网站失败');
        }

        closeSiteModal();
        showMessage('网站保存成功', 'success');
        loadSitesData(); // 重新加载数据

    } catch (error) {
        console.error('保存网站失败:', error);
        showMessage('保存网站失败', 'error');
    }
}

// 删除网站
async function deleteSite(siteId) {
    if (!confirm('确定要删除这个网站吗？此操作不可撤销。')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/sites/${siteId}`, {
            method: 'DELETE',
            headers: {
                'X-Session-Token': currentSessionToken
            }
        });

        if (!response.ok) {
            if (response.status === 401) {
                handleUnauthorized();
                return;
            }
            throw new Error('删除网站失败');
        }

        showMessage('网站删除成功', 'success');
        loadSitesData(); // 重新加载数据

    } catch (error) {
        console.error('删除网站失败:', error);
        showMessage('删除网站失败', 'error');
    }
}

// 删除用户
async function deleteUser(userId) {
    if (!confirm('确定要删除这个用户吗？此操作不可撤销。')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/auth/users/${userId}`, {
            method: 'DELETE',
            headers: {
                'X-Session-Token': currentSessionToken
            }
        });

        if (!response.ok) {
            if (response.status === 401) {
                handleUnauthorized();
                return;
            }
            throw new Error('删除用户失败');
        }

        showMessage('用户删除成功', 'success');
        loadUsersData(); // 重新加载数据

    } catch (error) {
        console.error('删除用户失败:', error);
        showMessage('删除用户失败', 'error');
    }
}

// 关闭网站模态框
function closeSiteModal() {
    document.getElementById('site-modal').style.display = 'none';
    currentEditingSite = null;
}

// 过滤网站
function filterSites() {
    loadSitesData();
}

// 刷新用户数据
function refreshUsers() {
    loadUsersData();
}

// 刷新网站数据
function refreshSites() {
    loadSitesData();
}

// 刷新统计信息
function refreshStats() {
    loadStatsData();
}

// 退出管理
async function logout() {
    if (confirm('确定要退出后台管理吗？')) {
        try {
            // 通知后端注销会话
            await fetch(`${API_BASE_URL}/auth/logout`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_token: currentSessionToken })
            });
        } catch (error) {
            console.error('注销会话失败:', error);
        }
        
        // 清除本地存储
        localStorage.removeItem('admin_session_token');
        currentSessionToken = null;
        
        // 显示登录界面
        document.getElementById('admin-container').style.display = 'none';
        document.getElementById('login-container').style.display = 'flex';
        
        // 清空登录表单
        document.getElementById('login-form').reset();
        showMessage('已成功退出', 'success');
    }
}

// 工具函数
function getCategoryDisplayName(category) {
    const categoryMap = {
        'ai': 'AI',
        'work': '工作',
        'study': '学习',
        'entertainment': '娱乐',
        'tools': '工具'
    };
    return categoryMap[category] || category;
}

function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN');
}

function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<tr><td colspan="8" style="text-align: center;"><div class="loading"></div> 加载中...</td></tr>';
    }
}

function showMessage(message, type = 'info') {
    const toast = document.getElementById('message-toast');
    const toastMessage = document.getElementById('toast-message');
    
    toastMessage.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// 处理未授权访问
function handleUnauthorized() {
    localStorage.removeItem('admin_session_token');
    currentSessionToken = null;
    showMessage('会话已过期，请重新登录', 'error');
    setTimeout(() => {
        document.getElementById('admin-container').style.display = 'none';
        document.getElementById('login-container').style.display = 'flex';
        document.getElementById('login-form').reset();
    }, 2000);
}

// 为后端API添加缺失的路由
async function initializeAdminAPI() {
    // 这些路由需要在后端app.py中添加
    console.log('后台管理API初始化完成');
}

// 初始化API
initializeAdminAPI();
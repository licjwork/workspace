let currentCategory = 'all';
let searchKeyword = '';
let sitesData = [];
let currentUser = null;

// 初始化页面
document.addEventListener('DOMContentLoaded', function() {
    loadSites();
    loadNews();
    setupEventListeners();
    checkLoginStatus();
});

async function setupEventListeners() {
    // 分类点击事件
    document.querySelectorAll('.category').forEach(category => {
        category.addEventListener('click', function() {
            document.querySelectorAll('.category').forEach(cat => cat.classList.remove('active'));
            this.classList.add('active');
            currentCategory = this.dataset.category;
            loadSites();
        });
    });

    // 搜索框回车事件
    document.getElementById('searchInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchSites();
        }
    });
}

function searchSites() {
    searchKeyword = document.getElementById('searchInput').value.toLowerCase();
    loadSites();
}

async function loadSites() {
    try {
        // 构建查询参数
        const params = new URLSearchParams();
        if (currentCategory !== 'all') {
            params.append('category', currentCategory);
        }
        if (searchKeyword) {
            params.append('search', searchKeyword);
        }
        
        // 添加用户认证信息
        if (currentUser) {
            params.append('session_token', currentUser.session_token);
        }
        
        const response = await fetch(`http://82.156.52.192:5000/api/sites?${params}`);
        
        if (response.ok) {
            const data = await response.json();
            sitesData = data.sites;
            displaySites(sitesData);
        } else {
            throw new Error('后端服务响应错误');
        }
    } catch (error) {
        console.log('后端服务连接失败，使用前端默认数据');
        // 使用前端默认数据作为后备
        const defaultSites = [
            {
                name: "百度",
                url: "https://www.baidu.com",
                category: "tools",
                icon: "🔍",
                description: "中文搜索引擎"
            },
            {
                name: "GitHub",
                url: "https://github.com",
                category: "work",
                icon: "💻",
                description: "代码托管平台"
            },
            {
                name: "知乎",
                url: "https://www.zhihu.com",
                category: "study",
                icon: "📚",
                description: "知识分享社区"
            },
            {
                name: "哔哩哔哩",
                url: "https://www.bilibili.com",
                category: "entertainment",
                icon: "🎮",
                description: "视频分享平台"
            },
            {
                name: "Google",
                url: "https://www.google.com",
                category: "tools",
                icon: "🌐",
                description: "全球搜索引擎"
            },
            {
                name: "Stack Overflow",
                url: "https://stackoverflow.com",
                category: "work",
                icon: "❓",
                description: "编程问答社区"
            },
            {
                name: "OpenAI",
                url: "https://openai.com",
                category: "ai",
                icon: "🤖",
                description: "人工智能研究"
            }
        ];
        
        let filteredSites = defaultSites.filter(site => {
            const matchesCategory = currentCategory === 'all' || site.category === currentCategory;
            const matchesSearch = searchKeyword === '' || 
                site.name.toLowerCase().includes(searchKeyword) ||
                site.description.toLowerCase().includes(searchKeyword);
            return matchesCategory && matchesSearch;
        });
        
        displaySites(filteredSites);
    }
}

function displaySites(sites) {
    const container = document.getElementById('sitesContainer');
    
    if (sites.length === 0) {
        container.innerHTML = '<div class="no-results">没有找到匹配的网站</div>';
        return;
    }

    container.innerHTML = sites.map(site => {
        // 根据健康状态显示不同的图标
        let healthIcon = '🟡'; // 默认未知状态
        let healthTooltip = '状态未知';
        
        if (site.health_status === 'healthy') {
            healthIcon = '🟢';
            healthTooltip = '网站正常';
        } else if (site.health_status === 'slow') {
            healthIcon = '🟡';
            healthTooltip = '网站较慢';
        } else if (site.health_status === 'very_slow') {
            healthIcon = '🟠';
            healthTooltip = '网站很慢';
        } else if (site.health_status === 'unhealthy') {
            healthIcon = '🔴';
            healthTooltip = '网站异常';
        } else if (site.health_status === 'unreachable') {
            healthIcon = '⚫';
            healthTooltip = '无法访问';
        }
        
        // 如果有响应时间，添加到提示中
        if (site.response_time) {
            healthTooltip += ` (${site.response_time}ms)`;
        }
        
        return `
        <div class="site-card">
            <div class="site-content" onclick="openSite('${site.url}')">
                <div class="site-icon">${site.icon}</div>
                <h3>${site.name}</h3>
                <p>${site.description}</p>
                <div class="health-status" title="${healthTooltip}">${healthIcon}</div>
            </div>
            <div class="favorite-btn ${site.is_favorite ? 'favorited' : ''}" onclick="handleFavoriteClick(${site.id})">
                ${site.is_favorite ? '❤️' : '🤍'}
            </div>
        </div>
        `;
    }).join('');
}

function openSite(url) {
    window.open(url, '_blank');
}

function handleFavoriteClick(siteId) {
    if (!currentUser) {
        // 未登录，跳转到登录页面
        showLoginForm();
        return;
    }
    
    // 已登录，执行收藏/取消收藏操作
    toggleFavorite(siteId);
}

async function toggleFavorite(siteId) {
    const site = sitesData.find(s => s.id === siteId);
    if (!site) return;
    
    const params = new URLSearchParams();
    params.append('site_id', siteId);
    
    if (currentUser) {
        params.append('session_token', currentUser.session_token);
    } else {
        params.append('user_id', 'default');
    }
    
    try {
        if (site.is_favorite) {
            // 取消收藏
            const response = await fetch(`http://82.156.52.192:5000/api/favorites/${siteId}?${params}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                site.is_favorite = false;
                updateSiteCard(siteId);
            } else {
                alert('取消收藏失败，请重试');
            }
        } else {
            // 添加收藏
            const response = await fetch('http://82.156.52.192:5000/api/favorites', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    site_id: siteId,
                    session_token: currentUser ? currentUser.session_token : null,
                    user_id: currentUser ? null : 'default'
                })
            });
            
            const data = await response.json();
            if (!data.error) {
                site.is_favorite = true;
                updateSiteCard(siteId);
            } else {
                alert('收藏失败，请重试');
            }
        }
    } catch (error) {
        console.error('收藏操作失败:', error);
        alert('网络错误，请重试');
    }
}

// 添加新网站
async function addSite(siteData) {
    try {
        const response = await fetch('http://82.156.52.192:5000/api/sites', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(siteData)
        });
        
        if (response.ok) {
            loadSites(); // 重新加载数据
            return true;
        }
    } catch (error) {
        console.error('添加网站失败:', error);
    }
    return false;
}

// 删除网站
async function deleteSite(siteId) {
    try {
        const response = await fetch(`/api/sites/${siteId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadSites(); // 重新加载数据
            return true;
        }
    } catch (error) {
        console.error('删除网站失败:', error);
    }
    return false;
}

let currentSlide = 0;
let newsSlides = [];

// 加载最新资讯
async function loadNews() {
    try {
        const response = await fetch('http://82.156.52.192:5000/api/news');
        
        if (response.ok) {
            const newsData = await response.json();
            
            const newsSlidesContainer = document.getElementById('newsSlides');
            const newsUpdateTime = document.getElementById('newsUpdateTime');
            
            // 清空现有内容
            newsSlidesContainer.innerHTML = '';
            
            // 添加主要新闻摘要
            if (newsData.content && newsData.content !== '暂无资讯') {
                const mainSlide = document.createElement('div');
                mainSlide.className = 'news-slide';
                mainSlide.innerHTML = `
                    <h4>📰 今日要闻</h4>
                    <p>${newsData.content}</p>
                `;
                newsSlidesContainer.appendChild(mainSlide);
                newsSlides.push(mainSlide);
            }
            
            // 添加详细新闻列表
            if (newsData.news_list && newsData.news_list.length > 0) {
                newsData.news_list.forEach(news => {
                    const slide = document.createElement('div');
                    slide.className = 'news-slide';
                    slide.innerHTML = `
                        <h4>${news.title || '新闻标题'}</h4>
                        <p>${news.summary || '新闻摘要'}</p>
                    `;
                    newsSlidesContainer.appendChild(slide);
                    newsSlides.push(slide);
                });
            }
            
            // 如果没有新闻，显示等待信息
            if (newsSlides.length === 0) {
                const waitSlide = document.createElement('div');
                waitSlide.className = 'news-slide';
                waitSlide.innerHTML = `
                    <h4>📰 等待新闻更新</h4>
                    <p>每日08:00自动推送最新资讯</p>
                `;
                newsSlidesContainer.appendChild(waitSlide);
                newsSlides.push(waitSlide);
            }
            
            // 更新时间和指示器
            if (newsData.last_update) {
                newsUpdateTime.textContent = `最后更新: ${newsData.last_update}`;
            }
            
            // 创建指示器
            createIndicators();
            
            // 显示第一张幻灯片
            showSlide(0);
        }
    } catch (error) {
        console.log('资讯加载失败，使用默认信息');
        const newsSlidesContainer = document.getElementById('newsSlides');
        newsSlidesContainer.innerHTML = `
            <div class="news-slide">
                <h4>📰 资讯服务暂时不可用</h4>
                <p>请稍后再试</p>
            </div>
        `;
    }
}

// 创建指示器
function createIndicators() {
    const indicatorsContainer = document.getElementById('newsIndicators');
    indicatorsContainer.innerHTML = '';
    
    for (let i = 0; i < newsSlides.length; i++) {
        const indicator = document.createElement('div');
        indicator.className = `news-indicator ${i === 0 ? 'active' : ''}`;
        indicator.onclick = () => showSlide(i);
        indicatorsContainer.appendChild(indicator);
    }
}

// 显示指定幻灯片
function showSlide(index) {
    if (index < 0) index = newsSlides.length - 1;
    if (index >= newsSlides.length) index = 0;
    
    currentSlide = index;
    const slidesContainer = document.getElementById('newsSlides');
    slidesContainer.style.transform = `translateX(-${index * 100}%)`;
    
    // 更新指示器
    const indicators = document.querySelectorAll('.news-indicator');
    indicators.forEach((indicator, i) => {
        indicator.classList.toggle('active', i === index);
    });
}

// 上一页
function prevSlide() {
    showSlide(currentSlide - 1);
}

// 下一页
function nextSlide() {
    showSlide(currentSlide + 1);
}

// 用户认证相关函数
function checkLoginStatus() {
    const sessionToken = localStorage.getItem('session_token');
    if (sessionToken) {
        // 验证会话
        fetch('http://82.156.52.192:5000/api/auth/verify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ session_token: sessionToken })
        })
        .then(response => response.json())
        .then(data => {
            if (data.valid) {
                currentUser = {
                    id: data.user_id,
                    username: data.username,
                    session_token: sessionToken
                };
                updateUserPanel();
            } else {
                localStorage.removeItem('session_token');
                localStorage.removeItem('user_info');
            }
        })
        .catch(error => {
            console.error('验证会话失败:', error);
        });
    }
}

function showLoginForm() {
    document.getElementById('authModal').style.display = 'flex';
    // 默认显示登录标签页
    showTab('login');
}

function closeAuthModal() {
    document.getElementById('authModal').style.display = 'none';
    clearAuthMessage();
}

function showTab(tabName) {
    // 隐藏所有标签页
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.style.display = 'none';
    });
    
    // 移除所有活动状态
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // 显示选中的标签页
    document.getElementById(tabName + 'Tab').style.display = 'block';
    
    // 找到对应的按钮并激活
    document.querySelectorAll('.tab-btn').forEach(btn => {
        if (btn.textContent.includes(tabName === 'login' ? '登录' : '注册')) {
            btn.classList.add('active');
        }
    });
}

function login() {
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    
    if (!username || !password) {
        showAuthMessage('请输入用户名和密码', 'error');
        return;
    }
    
    fetch('http://82.156.52.192:5000/api/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => {
        console.log('登录响应状态:', response.status);
        console.log('登录响应头:', response.headers);
        return response.json();
    })
    .then(data => {
        console.log('登录响应数据:', data);
        if (data.error) {
            showAuthMessage(data.error, 'error');
        } else {
            currentUser = data;
            localStorage.setItem('session_token', data.session_token);
            localStorage.setItem('user_info', JSON.stringify(data));
            updateUserPanel();
            closeAuthModal();
            showAuthMessage('登录成功！', 'success');
            loadSites(); // 重新加载网站以更新收藏状态
            
            // 更新木鱼组件状态
            if (window.woodenFish && typeof window.woodenFish.updateUI === 'function') {
                window.woodenFish.updateUI();
            }
        }
    })
    .catch(error => {
        console.error('登录请求失败:', error);
        showAuthMessage('登录失败，请检查网络连接', 'error');
    });
}

function register() {
    const username = document.getElementById('registerUsername').value;
    const password = document.getElementById('registerPassword').value;
    const email = document.getElementById('registerEmail').value;
    
    if (!username || !password) {
        showAuthMessage('请输入用户名和密码', 'error');
        return;
    }
    
    if (username.length < 3) {
        showAuthMessage('用户名至少需要3个字符', 'error');
        return;
    }
    
    if (password.length < 6) {
        showAuthMessage('密码至少需要6个字符', 'error');
        return;
    }
    
    fetch('http://82.156.52.192:5000/api/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password, email })
    })
    .then(response => {
        console.log('注册响应状态:', response.status);
        console.log('注册响应头:', response.headers);
        return response.json();
    })
    .then(data => {
        console.log('注册响应数据:', data);
        if (data.error) {
            showAuthMessage(data.error, 'error');
        } else {
            showAuthMessage('注册成功！请登录', 'success');
            setTimeout(() => {
                showTab('login');
                document.getElementById('loginUsername').value = username;
            }, 1000);
        }
    })
    .catch(error => {
        console.error('注册请求失败:', error);
        showAuthMessage('注册失败，请检查网络连接', 'error');
    });
}

function logout() {
    const sessionToken = localStorage.getItem('session_token');
    
    if (sessionToken) {
        fetch('http://82.156.52.192:5000/api/auth/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ session_token: sessionToken })
        })
        .catch(error => console.error('注销失败:', error));
    }
    
    localStorage.removeItem('session_token');
    localStorage.removeItem('user_info');
    currentUser = null;
    updateUserPanel();
    loadSites(); // 重新加载网站以更新收藏状态
    
    // 更新木鱼组件状态
    if (window.woodenFish && typeof window.woodenFish.updateUI === 'function') {
        window.woodenFish.updateUI();
    }
}

function updateUserPanel() {
    const loginBtn = document.getElementById('loginBtn');
    const userInfo = document.getElementById('userInfo');
    const usernameSpan = document.getElementById('username');
    
    if (currentUser) {
        loginBtn.style.display = 'none';
        userInfo.style.display = 'flex';
        usernameSpan.textContent = currentUser.username;
    } else {
        loginBtn.style.display = 'block';
        userInfo.style.display = 'none';
    }
}

function updateSiteCard(siteId) {
    const site = sitesData.find(s => s.id === siteId);
    if (!site) return;
    
    const siteCard = document.querySelector(`.site-card[onclick*="${siteId}"]`) || 
                     document.querySelector(`.site-card:has(.favorite-btn[onclick*="${siteId}"])`);
    
    if (siteCard) {
        const favoriteBtn = siteCard.querySelector('.favorite-btn');
        if (favoriteBtn) {
            favoriteBtn.innerHTML = site.is_favorite ? '❤️' : '🤍';
            favoriteBtn.classList.toggle('favorited', site.is_favorite);
        }
    }
}

function showAuthMessage(message, type) {
    const messageDiv = document.getElementById('authMessage');
    messageDiv.textContent = message;
    messageDiv.className = 'auth-message ' + type;
    messageDiv.style.display = 'block';
}

function clearAuthMessage() {
    const messageDiv = document.getElementById('authMessage');
    messageDiv.style.display = 'none';
    messageDiv.textContent = '';
}

// 修改收藏功能以支持用户认证
function toggleFavorite(siteId) {
    const site = sitesData.find(s => s.id === siteId);
    if (!site) return;
    
    const params = new URLSearchParams();
    params.append('site_id', siteId);
    
    if (currentUser) {
        params.append('session_token', currentUser.session_token);
    } else {
        params.append('user_id', 'default');
    }
    
    if (site.is_favorite) {
        // 取消收藏
        fetch(`http://82.156.52.192:5000/api/favorites/${siteId}?${params}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                site.is_favorite = false;
                updateSiteCard(siteId);
            }
        })
        .catch(error => console.error('取消收藏失败:', error));
    } else {
        // 添加收藏
        fetch('http://82.156.52.192:5000/api/favorites', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                site_id: siteId,
                session_token: currentUser ? currentUser.session_token : null,
                user_id: currentUser ? null : 'default'
            })
        })
        .then(response => response.json())
        .then(data => {
            if (!data.error) {
                site.is_favorite = true;
                updateSiteCard(siteId);
            }
        })
        .catch(error => console.error('添加收藏失败:', error));
    }
}
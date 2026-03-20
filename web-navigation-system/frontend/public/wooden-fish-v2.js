// 敲木鱼小组件 v2.0 - 支持数据库存储和排行榜
class WoodenFishV2 {
    constructor() {
        this.count = 0;
        this.userId = null;
        this.isLoggedIn = false;
        this.isPlaying = false;
        this.soundPlayer = new KnockSound();
        this.init();
    }

    init() {
        this.createWoodenFishElement();
        this.checkLoginStatus();
        this.bindEvents();
    }

    async checkLoginStatus() {
        try {
            // 检查localStorage中的session_token（与收藏功能保持一致）
            const sessionToken = localStorage.getItem('session_token');
            if (sessionToken) {
                // 从localStorage获取用户信息
                const userInfo = localStorage.getItem('user_info');
                if (userInfo) {
                    const userData = JSON.parse(userInfo);
                    this.userId = userData.user_id || userData.id || 'unknown_user';
                    this.isLoggedIn = true;
                } else {
                    // 如果没有用户信息，验证会话获取用户ID
                    const response = await fetch('/nav/api/auth/verify', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ session_token: sessionToken })
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        if (data.valid && data.user_id) {
                            this.userId = data.user_id;
                            this.isLoggedIn = true;
                            // 保存用户信息到localStorage
                            localStorage.setItem('user_info', JSON.stringify({
                                user_id: data.user_id,
                                username: data.username
                            }));
                        } else {
                            this.userId = null;
                            this.isLoggedIn = false;
                            this.count = 0;
                        }
                    } else {
                        this.userId = null;
                        this.isLoggedIn = false;
                        this.count = 0;
                    }
                }
                
                if (this.isLoggedIn) {
                    await this.loadUserData();
                    this.updateUI();
                }
            } else {
                // 未登录状态
                this.userId = null;
                this.isLoggedIn = false;
                this.count = 0;
                this.updateUI();
            }
        } catch (error) {
            console.warn('检查登录状态失败:', error);
            this.userId = null;
            this.isLoggedIn = false;
            this.count = 0;
            this.updateUI();
        }
    }

    showLoginPrompt() {
        this.fishElement.style.opacity = '0.5';
        this.fishElement.style.cursor = 'not-allowed';
        this.fishTooltip.textContent = '请先登录';
        this.counterElement.textContent = '0';
        this.count = 0;
    }

    updateUI() {
        // 根据登录状态更新UI
        if (this.isLoggedIn) {
            this.fishElement.style.opacity = '1';
            this.fishElement.style.cursor = 'pointer';
            this.fishTooltip.textContent = '敲木鱼';
        } else {
            this.fishElement.style.opacity = '0.5';
            this.fishElement.style.cursor = 'not-allowed';
            this.fishTooltip.textContent = '请先登录';
        }
        this.counterElement.textContent = this.count;
    }

    createWoodenFishElement() {
        const fishHtml = `
            <div id="wooden-fish-container" class="wooden-fish-container">
                <div class="wooden-fish" id="wooden-fish">
                    <div class="fish-icon">🐟</div>
                    <div class="fish-counter" id="fish-counter">0</div>
                    <div class="achievement-badge" id="achievement-badge" style="display: none;"></div>
                </div>
                <div class="fish-tooltip">敲木鱼</div>
                <div class="leaderboard-btn" id="leaderboard-btn">🏆</div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', fishHtml);
        
        // 初始化木鱼DOM元素引用
        this.initDOMReferences();
    }

    initDOMReferences() {
        // 初始化DOM元素引用
        this.fishElement = document.getElementById('wooden-fish');
        this.counterElement = document.getElementById('fish-counter');
        this.fishTooltip = document.querySelector('.fish-tooltip');
        this.achievementBadge = document.getElementById('achievement-badge');
        this.leaderboardBtn = document.getElementById('leaderboard-btn');
        
        // 检查DOM元素是否成功获取
        if (!this.fishElement) {
            console.warn('木鱼元素未找到');
        }
    }

    createDOM() {
        // 创建木鱼容器
        const container = document.createElement('div');
        container.id = 'wooden-fish-container';
        container.className = 'wooden-fish-container';
        
        // 创建木鱼元素
        const fishElement = document.createElement('div');
        fishElement.id = 'wooden-fish';
        fishElement.className = 'wooden-fish';
        fishElement.innerHTML = '🐟';
        
        // 创建计数器
        const counterElement = document.createElement('div');
        counterElement.id = 'fish-counter';
        counterElement.className = 'fish-counter';
        counterElement.textContent = '0';
        
        // 创建工具提示
        const tooltipElement = document.createElement('div');
        tooltipElement.id = 'fish-tooltip';
        tooltipElement.className = 'fish-tooltip';
        tooltipElement.textContent = '敲木鱼';
        
        // 组装DOM结构
        container.appendChild(fishElement);
        container.appendChild(counterElement);
        container.appendChild(tooltipElement);
        
        // 添加到页面
        document.body.appendChild(container);
        
        // 保存引用
        this.fishElement = fishElement;
        this.counterElement = counterElement;
        this.fishTooltip = tooltipElement;
    }

    async syncToDatabase() {
        try {
            if (!this.isLoggedIn || !this.userId) {
                console.warn('用户未登录，无法同步到数据库');
                return;
            }
            
            // 确保userId是数字类型
            const userId = parseInt(this.userId);
            if (isNaN(userId)) {
                console.warn('用户ID格式错误，无法同步到数据库');
                return;
            }
            
            console.log(`同步用户 ${userId} 的木鱼计数 ${this.count} 到数据库`);
            
            const response = await fetch(`/nav/api/wooden-fish/user/${userId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    count: this.count
                })
            });
            
            if (!response.ok) {
                throw new Error('同步失败');
            }
            
            console.log(`用户 ${userId} 的木鱼计数同步成功`);
        } catch (error) {
            console.warn('数据库同步失败:', error);
        }
    }

    async loadUserData() {
        try {
            if (!this.isLoggedIn || !this.userId) {
                this.count = 0;
                this.updateUI();
                return;
            }
            
            console.log(`加载用户 ${this.userId} 的木鱼数据`);
            
            // 从localStorage加载本地计数（优先使用本地数据）
            const storedCount = localStorage.getItem(`woodenFishCount_${this.userId}`);
            if (storedCount) {
                this.count = parseInt(storedCount);
                console.log(`从localStorage加载用户 ${this.userId} 的计数: ${this.count}`);
            } else {
                // 如果没有本地数据，再从数据库加载
                try {
                    const response = await fetch(`/nav/api/wooden-fish/user/${this.userId}`);
                    if (response.ok) {
                        const userData = await response.json();
                        this.count = userData.count || 0;
                        console.log(`从数据库加载用户 ${this.userId} 的计数: ${this.count}`);
                        // 保存到localStorage
                        localStorage.setItem(`woodenFishCount_${this.userId}`, this.count.toString());
                    } else {
                        this.count = 0;
                        console.log(`数据库无用户 ${this.userId} 的数据，初始化为0`);
                    }
                } catch (dbError) {
                    console.warn('数据库加载失败，使用默认值:', dbError);
                    this.count = 0;
                }
            }
            
            if (this.counterElement) {
                this.counterElement.textContent = this.count;
            }
            
            // 检查成就
            this.checkAchievements();
            this.updateUI();
        } catch (error) {
            console.warn('加载用户数据失败:', error);
            this.count = 0;
            this.updateUI();
        }
    }

    async knock() {
        if (this.isPlaying) return;
        
        // 立即检查登录状态（确保与主脚本同步）
        await this.checkLoginStatus();
        
        // 检查登录状态
        if (!this.isLoggedIn) {
            this.triggerLogin();
            return;
        }
        
        this.isPlaying = true;
        
        // 本地累加计数
        this.count++;
        
        // 保存到localStorage
        localStorage.setItem(`woodenFishCount_${this.userId}`, this.count.toString());
        console.log(`用户 ${this.userId} 的木鱼计数已保存到localStorage: ${this.count}`);
        
        // 播放音效
        this.soundPlayer.playRealKnock();
        
        // 更新UI
        this.counterElement.textContent = this.count;
        
        // 动画效果
        this.fishElement.classList.add('knocking');
        setTimeout(() => {
            this.fishElement.classList.remove('knocking');
            this.isPlaying = false;
        }, 300);
        
        // 异步保存数据到数据库（不影响本地计数）
        this.syncToDatabase().catch(error => {
            console.warn('数据库同步失败，但本地计数已保存:', error);
        });
        
        // 检查成就
        this.checkAchievements();
        
        console.log(`🐟 用户 ${this.userId} 敲木鱼 ${this.count} 次`);
    }

    triggerLogin() {
        // 直接调用现有的登录弹窗
        if (typeof showLoginForm === 'function') {
            showLoginForm();
        } else {
            // 备用方案：显示简单提示
            alert('请先登录才能敲木鱼');
        }
    }

    checkAchievements() {
        const achievements = [
            { count: 10, title: "新手敲击者", emoji: "🎯" },
            { count: 50, title: "木鱼爱好者", emoji: "🥉" },
            { count: 100, title: "敲击大师", emoji: "🥈" },
            { count: 500, title: "木鱼达人", emoji: "🥇" },
            { count: 1000, title: "木鱼之神", emoji: "👑" }
        ];
        
        const achievement = achievements.find(a => this.count === a.count);
        if (achievement) {
            this.showAchievement(achievement);
        }
    }

    showAchievement(achievement) {
        this.achievementBadge.textContent = achievement.emoji;
        this.achievementBadge.style.display = 'block';
        this.achievementBadge.setAttribute('title', achievement.title);
        
        // 显示成就通知
        this.showNotification(`成就解锁: ${achievement.title} ${achievement.emoji}`);
        
        // 3秒后隐藏徽章
        setTimeout(() => {
            this.achievementBadge.style.display = 'none';
        }, 3000);
    }

    showNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'achievement-notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #4CAF50;
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            z-index: 1001;
            animation: slideIn 0.5s ease-out;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.5s ease-in';
            setTimeout(() => notification.remove(), 500);
        }, 3000);
    }

    async showLeaderboard() {
        // 检查登录状态
        if (!this.isLoggedIn) {
            this.showNotification('请先登录查看排行榜');
            return;
        }
        
        try {
            const response = await fetch('/nav/api/wooden-fish/leaderboard');
            if (response.ok) {
                const data = await response.json();
                this.displayLeaderboard(data);
            } else {
                this.showNotification('获取排行榜失败');
            }
        } catch (error) {
            console.warn('获取排行榜失败:', error);
            this.showNotification('获取排行榜失败');
        }
    }

    displayLeaderboard(leaderboard) {
        const modal = document.createElement('div');
        modal.className = 'leaderboard-modal';
        modal.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            z-index: 1002;
            min-width: 300px;
        `;
        
        // 获取当前用户的用户名
        const userInfo = localStorage.getItem('user_info');
        const currentUsername = userInfo ? JSON.parse(userInfo).username : null;
        
        let content = '<h3>🏆 木鱼排行榜</h3><ul>';
        leaderboard.forEach((item, index) => {
            const isCurrentUser = item.username === currentUsername;
            const displayName = this.maskUsername(item.username);
            const rank = index + 1;
            const style = isCurrentUser ? 'style="color: #4CAF50; font-weight: bold;"' : '';
            content += `<li ${style}>${rank}. ${displayName}: ${item.count}次</li>`;
        });
        content += '</ul><button onclick="this.parentElement.remove()">关闭</button>';
        
        modal.innerHTML = content;
        document.body.appendChild(modal);
    }
    
    maskUsername(username) {
        if (!username) {
            return '匿名用户';
        }
        
        // 用户名长度至少为4才进行脱敏处理
        // 这样"abcd"会显示为"a**d"，而"abc"会直接显示"abc"
        if (username.length >= 4) {
            const firstChar = username.charAt(0);
            const lastChar = username.charAt(username.length - 1);
            return `${firstChar}**${lastChar}`;
        }
        
        // 长度小于4的用户名直接显示
        return username;
    }

    bindEvents() {
        // 重新获取DOM元素引用（确保DOM已创建）
        this.fishElement = document.getElementById('wooden-fish');
        this.leaderboardBtn = document.getElementById('leaderboard-btn');
        
        if (this.fishElement) {
            this.fishElement.addEventListener('click', () => this.knock());
            this.fishElement.addEventListener('touchstart', (e) => {
                e.preventDefault();
                this.knock();
            });
        }
        
        if (this.leaderboardBtn) {
            this.leaderboardBtn.addEventListener('click', () => this.showLeaderboard());
        }
        
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && !e.target.matches('input, textarea')) {
                e.preventDefault();
                this.knock();
            }
        });

        // 监听登录状态变化（监听页面上的登录状态变化）
        // 由于现有的登录系统会更新页面状态，我们可以通过检查用户面板来监听状态变化
        
        // 定期检查登录状态（每5秒检查一次）
        setInterval(() => {
            this.checkLoginStatus();
        }, 5000);
    }
}

// 初始化
window.WoodenFishV2 = WoodenFishV2;
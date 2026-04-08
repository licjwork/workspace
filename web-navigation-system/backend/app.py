from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
import json
import time
import hashlib
from functools import wraps

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# 会话验证装饰器
def require_admin_session(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 从请求头获取会话令牌
        session_token = request.headers.get('X-Session-Token')
        
        if not session_token:
            return jsonify({'error': '需要登录'}), 401
        
        # 验证会话
        conn = sqlite3.connect('database/navigation.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT u.id, u.username, s.expires_at 
            FROM user_sessions s 
            JOIN users u ON s.user_id = u.id 
            WHERE s.session_token = ? AND s.expires_at > ?
        ''', (session_token, time.time()))
        
        session = cursor.fetchone()
        conn.close()
        
        if not session:
            return jsonify({'error': '会话无效或已过期'}), 401
        
        # 将会话信息添加到请求上下文中
        request.admin_user_id = session[0]
        request.admin_username = session[1]
        
        return f(*args, **kwargs)
    return decorated_function

# 数据库初始化
def init_db():
    db_path = 'database/navigation.db'
    os.makedirs('/home/ubuntu/.openclaw/workspace/web-navigation-system/database', exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建网站表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            category TEXT NOT NULL,
            icon TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建收藏表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site_id INTEGER NOT NULL,
            user_id TEXT DEFAULT 'default',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (site_id) REFERENCES sites(id),
            UNIQUE(site_id, user_id)
        )
    ''')
    
    # 创建用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建用户会话表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_token TEXT UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # 创建木鱼表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wooden_fish (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            count INTEGER DEFAULT 0,
            last_knock_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # 创建木鱼表索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_wooden_fish_user_id ON wooden_fish(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_wooden_fish_count ON wooden_fish(count DESC)')
    
    # 插入默认数据
    default_sites = [
        ('百度', 'https://www.baidu.com', 'tools', '🔍', '中文搜索引擎'),
        ('GitHub', 'https://github.com', 'work', '💻', '代码托管平台'),
        ('知乎', 'https://www.zhihu.com', 'study', '📚', '知识分享社区'),
        ('哔哩哔哩', 'https://www.bilibili.com', 'entertainment', '🎮', '视频分享平台'),
        ('Google', 'https://www.google.com', 'tools', '🌐', '全球搜索引擎'),
        ('Stack Overflow', 'https://stackoverflow.com', 'work', '❓', '编程问答社区'),
        ('OpenAI', 'https://openai.com', 'ai', '🤖', '人工智能研究'),
        ('YouTube', 'https://www.youtube.com', 'entertainment', '🎥', '视频分享平台'),
        ('淘宝', 'https://www.taobao.com', 'tools', '🛒', '电商平台'),
        ('微博', 'https://weibo.com', 'entertainment', '💬', '社交媒体')
    ]
    
    cursor.execute('SELECT COUNT(*) FROM sites')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT INTO sites (name, url, category, icon, description)
            VALUES (?, ?, ?, ?, ?)
        ''', default_sites)
    
    conn.commit()
    conn.close()

# 获取所有网站
@app.route('/api/sites', methods=['GET'])
def get_sites():
    category = request.args.get('category', 'all')
    search = request.args.get('search', '')
    session_token = request.args.get('session_token')
    
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    # 获取用户ID（如果已登录）
    user_id = 'default'
    if session_token:
        cursor.execute('''
            SELECT u.id FROM user_sessions s 
            JOIN users u ON s.user_id = u.id 
            WHERE s.session_token = ? AND s.expires_at > ?
        ''', (session_token, time.time()))
        session = cursor.fetchone()
        if session:
            user_id = str(session[0])
    
    # 处理"我的收藏"分类
    if category == 'favorites':
        # 获取用户收藏的网站
        query = '''
            SELECT s.* FROM sites s 
            JOIN favorites f ON s.id = f.site_id 
            WHERE f.user_id = ?
        '''
        params = [user_id]
        
        if search:
            query += ' AND (s.name LIKE ? OR s.description LIKE ?)'
            params.extend([f'%{search}%', f'%{search}%'])
        
        query += ' ORDER BY s.name'
    else:
        query = 'SELECT * FROM sites WHERE 1=1'
        params = []
        
        if category != 'all':
            query += ' AND category = ?'
            params.append(category)
        
        if search:
            query += ' AND (name LIKE ? OR description LIKE ?)'
            params.extend([f'%{search}%', f'%{search}%'])
        
        query += ' ORDER BY name'
    
    cursor.execute(query, params)
    sites = cursor.fetchall()
    
    result = []
    for site in sites:
        # 检查用户是否收藏了该网站
        cursor.execute('SELECT id FROM favorites WHERE site_id = ? AND user_id = ?', 
                       (site[0], user_id))
        is_favorited = cursor.fetchone() is not None
        
        result.append({
            'id': site[0],
            'name': site[1],
            'url': site[2],
            'category': site[3],
            'icon': site[4],
            'description': site[5],
            'is_favorite': is_favorited
        })
    
    conn.close()
    
    return jsonify({'sites': result})

# 添加新网站
@app.route('/api/sites', methods=['POST'])
@require_admin_session
def add_site():
    data = request.json
    
    required_fields = ['name', 'url', 'category']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
    
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO sites (name, url, category, icon, description)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['name'], data['url'], data['category'], 
          data.get('icon', ''), data.get('description', '')))
    
    conn.commit()
    site_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'id': site_id, 'message': '网站添加成功'})

# 获取单个网站信息
@app.route('/api/sites/<int:site_id>', methods=['GET'])
@require_admin_session
def get_site(site_id):
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM sites WHERE id = ?', (site_id,))
    site = cursor.fetchone()
    
    if not site:
        conn.close()
        return jsonify({'error': '网站不存在'}), 404
    
    site_info = {
        'id': site[0],
        'name': site[1],
        'url': site[2],
        'category': site[3],
        'icon': site[4],
        'description': site[5]
    }
    
    conn.close()
    return jsonify(site_info)

# 更新网站
@app.route('/api/sites/<int:site_id>', methods=['PUT'])
@require_admin_session
def update_site(site_id):
    data = request.json
    
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM sites WHERE id = ?', (site_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': '网站不存在'}), 404
    
    update_fields = []
    params = []
    
    if 'name' in data:
        update_fields.append('name = ?')
        params.append(data['name'])
    if 'url' in data:
        update_fields.append('url = ?')
        params.append(data['url'])
    if 'category' in data:
        update_fields.append('category = ?')
        params.append(data['category'])
    if 'icon' in data:
        update_fields.append('icon = ?')
        params.append(data['icon'])
    if 'description' in data:
        update_fields.append('description = ?')
        params.append(data['description'])
    
    if update_fields:
        params.append(site_id)
        cursor.execute(f'''
            UPDATE sites SET {', '.join(update_fields)} WHERE id = ?
        ''', params)
        conn.commit()
    
    conn.close()
    return jsonify({'message': '网站更新成功'})

# 删除网站
@app.route('/api/sites/<int:site_id>', methods=['DELETE'])
@require_admin_session
def delete_site(site_id):
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM sites WHERE id = ?', (site_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': '网站删除成功'})

# 获取分类统计
@app.route('/api/stats', methods=['GET'])
@require_admin_session
def get_stats():
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT category, COUNT(*) as count 
        FROM sites 
        GROUP BY category
    ''')
    stats = cursor.fetchall()
    
    conn.close()
    
    result = {}
    for category, count in stats:
        result[category] = count
    
    return jsonify({'stats': result})

# 网站健康检测
@app.route('/api/sites/<int:site_id>/health', methods=['GET'])
def check_site_health(site_id):
    """检查单个网站的健康状态"""
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    # 获取网站信息
    cursor.execute('SELECT * FROM sites WHERE id = ?', (site_id,))
    site = cursor.fetchone()
    
    if not site:
        conn.close()
        return jsonify({'error': '网站不存在'}), 404
    
    # 检查网站可用性（带重试机制）
    import requests
    import time
    
    url = site[2]  # url字段
    max_retries = 2
    
    for attempt in range(max_retries + 1):
        start_time = time.time()
        
        try:
            response = requests.get(url, timeout=10)
            response_time = int((time.time() - start_time) * 1000)  # 毫秒
            
            if response.status_code == 200:
                if response_time < 1000:
                    health_status = 'healthy'
                elif response_time < 3000:
                    health_status = 'slow'
                else:
                    health_status = 'very_slow'
                break  # 成功，退出重试循环
            else:
                health_status = 'unhealthy'
                response_time = None
                if attempt < max_retries:
                    time.sleep(1)  # 等待1秒后重试
                    continue
                break
                
        except requests.exceptions.RequestException:
            health_status = 'unreachable'
            response_time = None
            if attempt < max_retries:
                time.sleep(1)  # 等待1秒后重试
                continue
            break
    
    # 更新网站状态
    cursor.execute('''
        UPDATE sites 
        SET health_status = ?, last_checked = CURRENT_TIMESTAMP, response_time = ?
        WHERE id = ?
    ''', (health_status, response_time, site_id))
    
    # 记录历史
    cursor.execute('''
        INSERT INTO site_health_history (site_id, health_status, response_time)
        VALUES (?, ?, ?)
    ''', (site_id, health_status, response_time))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'site_id': site_id,
        'health_status': health_status,
        'response_time': response_time,
        'status_code': response.status_code if health_status != 'unreachable' else None
    })

# 批量检测所有网站健康状态
@app.route('/api/sites/health/check-all', methods=['POST'])
@require_admin_session
def check_all_sites_health():
    """批量检测所有网站的健康状态"""
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, url, name FROM sites')
    sites = cursor.fetchall()
    
    results = []
    unhealthy_sites = []
    
    for site_id, url, name in sites:
        # 这里可以调用check_site_health的逻辑，但为了避免循环导入，我们复制代码
        import requests
        import time
        
        max_retries = 2
        
        for attempt in range(max_retries + 1):
            start_time = time.time()
            
            try:
                response = requests.get(url, timeout=10)
                response_time = int((time.time() - start_time) * 1000)
                
                if response.status_code == 200:
                    if response_time < 1000:
                        health_status = 'healthy'
                    elif response_time < 3000:
                        health_status = 'slow'
                    else:
                        health_status = 'very_slow'
                    break  # 成功，退出重试循环
                else:
                    health_status = 'unhealthy'
                    response_time = None
                    if attempt < max_retries:
                        time.sleep(1)  # 等待1秒后重试
                        continue
                    break
                    
            except requests.exceptions.RequestException:
                health_status = 'unreachable'
                response_time = None
                if attempt < max_retries:
                    time.sleep(1)  # 等待1秒后重试
                    continue
                break
        
        # 更新网站状态
        cursor.execute('''
            UPDATE sites 
            SET health_status = ?, last_checked = CURRENT_TIMESTAMP, response_time = ?
            WHERE id = ?
        ''', (health_status, response_time, site_id))
        
        # 记录历史
        cursor.execute('''
            INSERT INTO site_health_history (site_id, health_status, response_time)
            VALUES (?, ?, ?)
        ''', (site_id, health_status, response_time))
        
        # 记录异常网站用于告警
        if health_status in ['unhealthy', 'unreachable']:
            unhealthy_sites.append({
                'id': site_id,
                'name': name,
                'url': url,
                'status': health_status
            })
        
        results.append({
            'site_id': site_id,
            'health_status': health_status,
            'response_time': response_time
        })
    
    conn.commit()
    conn.close()
    
    # 如果有异常网站，发送飞书通知
    if unhealthy_sites and len(unhealthy_sites) > 0:
        send_health_alert(unhealthy_sites)
    
    return jsonify({'results': results, 'unhealthy_count': len(unhealthy_sites)})

def send_health_alert(unhealthy_sites):
    """发送网站健康告警到飞书"""
    import requests
    
    # 构建告警消息
    message = "🚨 网站健康检测告警\n\n"
    message += f"检测到 {len(unhealthy_sites)} 个网站异常：\n"
    
    for site in unhealthy_sites:
        status_text = "无法访问" if site['status'] == 'unreachable' else "网站异常"
        message += f"• {site['name']} ({site['url']}) - {status_text}\n"
    
    message += "\n请及时检查相关网站。"
    
    try:
        # 发送飞书消息
        # 这里需要配置飞书webhook，暂时先打印日志
        print(f"网站健康告警: {message}")
        
        # TODO: 配置飞书webhook后启用
        # response = requests.post(
        #     '飞书webhook地址',
        #     json={
        #         "msg_type": "text",
        #         "content": {"text": message}
        #     }
        # )
        
    except Exception as e:
        print(f"发送告警失败: {e}")

# 获取网站健康状态
@app.route('/api/sites/<int:site_id>/health', methods=['GET'])
def get_site_health(site_id):
    """获取网站的健康状态信息"""
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT s.name, s.url, s.health_status, s.last_checked, s.response_time,
               COUNT(shh.id) as history_count
        FROM sites s
        LEFT JOIN site_health_history shh ON s.id = shh.site_id
        WHERE s.id = ?
        GROUP BY s.id
    ''', (site_id,))
    
    site = cursor.fetchone()
    
    if not site:
        conn.close()
        return jsonify({'error': '网站不存在'}), 404
    
    # 获取最近7天的健康历史
    cursor.execute('''
        SELECT health_status, response_time, checked_at
        FROM site_health_history
        WHERE site_id = ?
        ORDER BY checked_at DESC
        LIMIT 7
    ''', (site_id,))
    
    history = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        'site_id': site_id,
        'name': site[0],
        'url': site[1],
        'health_status': site[2],
        'last_checked': site[3],
        'response_time': site[4],
        'history_count': site[5],
        'recent_history': [
            {
                'health_status': h[0],
                'response_time': h[1],
                'checked_at': h[2]
            }
            for h in history
        ]
    })

# 获取最新资讯
@app.route('/api/news', methods=['GET'])
def get_news():
    news_file = '/home/ubuntu/.openclaw/workspace/web-navigation-system/backend/news.json'
    
    # 如果news.json文件存在，读取它
    if os.path.exists(news_file):
        with open(news_file, 'r') as f:
            news_data = json.load(f)
            # 确保news_list存在
            if 'news_list' not in news_data:
                news_data['news_list'] = []
    else:
        # 如果文件不存在，尝试从Tavily获取最新国际新闻
        try:
            import subprocess
            result = subprocess.run([
                'python3', '/home/ubuntu/.openclaw/workspace/skills/tavily/scripts/tavily_search.py',
                'latest international news world news breaking news',
                '--api-key', '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',
                '--topic', 'news',
                '--max-results', '5'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # 提取AI回答部分
                lines = result.stdout.split('\n')
                ai_answer = ""
                in_ai_section = False
                
                for line in lines:
                    if '=== AI ANSWER ===' in line:
                        in_ai_section = True
                        continue
                    elif '=== RESULTS ===' in line:
                        break
                    elif in_ai_section:
                        ai_answer += line.strip() + " "
                
                ai_answer = ai_answer.strip()
                
                # 简单翻译成中文
                if ai_answer:
                    chinese_content = ai_answer
                    # 翻译关键词
                    translations = {
                        'world news': '世界新闻',
                        'international': '国际',
                        'Italy': '意大利',
                        'France': '法国',
                        'Japan': '日本',
                        'U.S.': '美国',
                        'Iran': '伊朗',
                        'China': '中国',
                        'Germany': '德国',
                        'Russia': '俄罗斯',
                        'Britain': '英国',
                        'Canada': '加拿大',
                        'Australia': '澳大利亚',
                        'India': '印度',
                        'Brazil': '巴西',
                        'South Korea': '韩国',
                        'President': '总统',
                        'Prime Minister': '总理',
                        'government': '政府',
                        'election': '选举',
                        'crisis': '危机',
                        'talks': '会谈',
                        'minister': '部长',
                        'spending': '花费',
                        'resigning': '辞职',
                        'winning': '赢得',
                        'concerns': '担忧',
                        'reports': '报道',
                        'arrest': '逮捕'
                    }
                    
                    for eng, chn in translations.items():
                        chinese_content = chinese_content.replace(eng, chn)
                    
                    news_data = {
                        'last_update': time.strftime('%Y-%m-%d %H:%M:%S'),
                        'content': chinese_content,
                        'news_list': [
                            {'index': 1, 'summary': '国际新闻摘要', 'title': '最新国际动态'}
                        ]
                    }
                else:
                    news_data = {
                        'last_update': '',
                        'content': '暂无资讯',
                        'news_list': []
                    }
            else:
                raise Exception(f"Tavily搜索失败: {result.stderr}")
        except Exception as e:
            print(f"获取新闻失败: {e}")
            news_data = {
                'last_update': '',
                'content': '暂无资讯',
                'news_list': []
            }
    
    return jsonify(news_data)

# 获取微博热搜
@app.route('/api/weibo/hot', methods=['GET'])
def get_weibo_hot():
    # 模拟微博热搜数据
    hot_data = {
        "last_update": "2026-03-15 04:47:00",
        "hot_list": [
            {
                "rank": 1,
                "title": "#油价突破100美元#",
                "heat": "3.2亿",
                "tag": "新"
            },
            {
                "rank": 2,
                "title": "#德黑兰爆炸事件#",
                "heat": "2.8亿",
                "tag": "热"
            },
            {
                "rank": 3,
                "title": "#波士顿冰河救援#",
                "heat": "1.5亿",
                "tag": "沸"
            },
            {
                "rank": 4,
                "title": "#伊朗战争最新动态#",
                "heat": "1.2亿",
                "tag": "热"
            },
            {
                "rank": 5,
                "title": "#全球能源危机#",
                "heat": "9800万",
                "tag": "新"
            },
            {
                "rank": 6,
                "title": "#中东局势分析#",
                "heat": "7500万",
                "tag": "热"
            },
            {
                "rank": 7,
                "title": "#国际油价波动#",
                "heat": "6200万",
                "tag": "新"
            },
            {
                "rank": 8,
                "title": "#美国军事行动#",
                "heat": "5500万",
                "tag": "热"
            },
            {
                "rank": 9,
                "title": "#全球市场影响#",
                "heat": "4800万",
                "tag": "新"
            },
            {
                "rank": 10,
                "title": "#地区冲突升级#",
                "heat": "4200万",
                "tag": "热"
            }
        ]
    }
    
    return jsonify(hot_data)

# 添加收藏
@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    data = request.json
    
    if 'site_id' not in data:
        return jsonify({'error': '缺少site_id参数'}), 400
    
    # 获取用户ID，优先使用session_token验证的真实用户ID
    user_id = 'default'
    if 'session_token' in data:
        # 验证会话
        conn = sqlite3.connect('database/navigation.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.id FROM user_sessions s 
            JOIN users u ON s.user_id = u.id 
            WHERE s.session_token = ? AND s.expires_at > ?
        ''', (data['session_token'], time.time()))
        session = cursor.fetchone()
        conn.close()
        
        if session:
            user_id = str(session[0])
    elif 'user_id' in data:
        user_id = data['user_id']
    
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    # 检查网站是否存在
    cursor.execute('SELECT id FROM sites WHERE id = ?', (data['site_id'],))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': '网站不存在'}), 404
    
    # 检查是否已收藏
    cursor.execute('SELECT id FROM favorites WHERE site_id = ? AND user_id = ?', 
                   (data['site_id'], user_id))
    if cursor.fetchone():
        conn.close()
        return jsonify({'error': '已收藏该网站'}), 400
    
    # 添加收藏
    cursor.execute('''
        INSERT INTO favorites (site_id, user_id)
        VALUES (?, ?)
    ''', (data['site_id'], user_id))
    
    conn.commit()
    favorite_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'id': favorite_id, 'message': '收藏成功'})

# 用户注册
@app.route('/api/auth/register', methods=['POST'])
def register_user():
    data = request.json
    
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': '用户名和密码不能为空'}), 400
    
    username = data['username'].strip()
    password = data['password']
    email = data.get('email', '').strip()
    
    if len(username) < 4:
        return jsonify({'error': '用户名至少4个字符'}), 400
    
    if len(password) < 6:
        return jsonify({'error': '密码至少6个字符'}), 400
    
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    # 检查用户名是否已存在
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    if cursor.fetchone():
        conn.close()
        return jsonify({'error': '用户名已存在'}), 400
    
    # 插入新用户（简单密码存储，实际项目中应该加密）
    cursor.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                   (username, password, email))
    
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'id': user_id, 'message': '注册成功'})

# 用户登录
@app.route('/api/auth/login', methods=['POST'])
def login_user():
    data = request.json
    
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': '用户名和密码不能为空'}), 400
    
    username = data['username']
    password = data['password']
    
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    # 验证用户凭据
    cursor.execute('SELECT id, username FROM users WHERE username = ? AND password = ?',
                   (username, password))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return jsonify({'error': '用户名或密码错误'}), 401
    
    # 生成简单的会话令牌
    import hashlib
    import time
    token_data = f"{user[0]}{username}{time.time()}"
    session_token = hashlib.md5(token_data.encode()).hexdigest()
    
    # 设置过期时间（24小时）
    expires_at = time.time() + 24 * 60 * 60
    
    # 存储会话
    cursor.execute('INSERT INTO user_sessions (user_id, session_token, expires_at) VALUES (?, ?, ?)',
                   (user[0], session_token, expires_at))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'user_id': user[0],
        'username': user[1],
        'session_token': session_token,
        'expires_at': expires_at
    })

# 用户注销
@app.route('/api/auth/logout', methods=['POST'])
def logout_user():
    data = request.json
    
    if 'session_token' not in data:
        return jsonify({'error': '缺少会话令牌'}), 400
    
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM user_sessions WHERE session_token = ?', (data['session_token'],))
    conn.commit()
    conn.close()
    
    return jsonify({'message': '注销成功'})

# 验证会话
@app.route('/api/auth/verify', methods=['POST'])
def verify_session():
    data = request.json
    
    if 'session_token' not in data:
        return jsonify({'error': '缺少会话令牌'}), 400
    
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT u.id, u.username, s.expires_at 
        FROM user_sessions s 
        JOIN users u ON s.user_id = u.id 
        WHERE s.session_token = ? AND s.expires_at > ?
    ''', (data['session_token'], time.time()))
    
    session = cursor.fetchone()
    conn.close()
    
    if not session:
        return jsonify({'valid': False, 'error': '会话无效或已过期'})
    
    return jsonify({
        'valid': True,
        'user_id': session[0],
        'username': session[1],
        'expires_at': session[2]
    })

# 取消收藏
@app.route('/api/favorites/<int:site_id>', methods=['DELETE'])
def remove_favorite(site_id):
    # 获取用户ID，优先使用session_token验证的真实用户ID
    user_id = request.args.get('user_id', 'default')
    session_token = request.args.get('session_token')
    
    if session_token:
        # 验证会话
        conn = sqlite3.connect('database/navigation.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.id FROM user_sessions s 
            JOIN users u ON s.user_id = u.id 
            WHERE s.session_token = ? AND s.expires_at > ?
        ''', (session_token, time.time()))
        session = cursor.fetchone()
        conn.close()
        
        if session:
            user_id = str(session[0])
    
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM favorites WHERE site_id = ? AND user_id = ?', 
                   (site_id, user_id))
    conn.commit()
    
    deleted_count = cursor.rowcount
    conn.close()
    
    if deleted_count == 0:
        return jsonify({'error': '未收藏该网站'}), 404
    
    return jsonify({'message': '取消收藏成功', 'deleted_count': deleted_count})

# 获取收藏列表
@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    # 获取用户ID，优先使用session_token验证的真实用户ID
    user_id = request.args.get('user_id', 'default')
    session_token = request.args.get('session_token')
    
    if session_token:
        # 验证会话
        conn = sqlite3.connect('database/navigation.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.id FROM user_sessions s 
            JOIN users u ON s.user_id = u.id 
            WHERE s.session_token = ? AND s.expires_at > ?
        ''', (session_token, time.time()))
        session = cursor.fetchone()
        conn.close()
        
        if session:
            user_id = str(session[0])
    
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT s.*, f.created_at as favorited_at
        FROM sites s
        INNER JOIN favorites f ON s.id = f.site_id
        WHERE f.user_id = ?
        ORDER BY f.created_at DESC
    ''', (user_id,))
    
    favorites = cursor.fetchall()
    conn.close()
    
    result = []
    for site in favorites:
        result.append({
            'id': site[0],
            'name': site[1],
            'url': site[2],
            'category': site[3],
            'icon': site[4],
            'description': site[5],
            'favorited_at': site[7]
        })
    
    return jsonify({'favorites': result})

# 检查是否收藏
@app.route('/api/favorites/<int:site_id>', methods=['GET'])
def check_favorite(site_id):
    user_id = request.args.get('user_id', 'default')
    
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM favorites WHERE site_id = ? AND user_id = ?', 
                   (site_id, user_id))
    
    is_favorited = cursor.fetchone() is not None
    conn.close()
    
    return jsonify({'is_favorited': is_favorited})

# ====================
# 后台管理API
# ====================

# 获取所有用户列表
@app.route('/api/auth/users', methods=['GET'])
@require_admin_session
def get_all_users():
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, username, email, created_at FROM users ORDER BY created_at DESC')
    users = cursor.fetchall()
    conn.close()
    
    result = []
    for user in users:
        result.append({
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'created_at': user[3]
        })
    
    return jsonify({'users': result})

# 获取用户统计信息
@app.route('/api/auth/stats', methods=['GET'])
@require_admin_session
def get_user_stats():
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    # 总用户数
    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]
    
    # 今日新增用户
    today = time.strftime('%Y-%m-%d')
    cursor.execute('SELECT COUNT(*) FROM users WHERE DATE(created_at) = ?', (today,))
    today_users = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'total': total_users,
        'today': today_users
    })

# 删除用户
@app.route('/api/auth/users/<int:user_id>', methods=['DELETE'])
@require_admin_session
def delete_user(user_id):
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    # 先删除用户的收藏记录
    cursor.execute('DELETE FROM favorites WHERE user_id = ?', (user_id,))
    # 删除用户的会话记录
    cursor.execute('DELETE FROM user_sessions WHERE user_id = ?', (user_id,))
    # 删除用户的木鱼数据
    cursor.execute('DELETE FROM wooden_fish WHERE user_id = ?', (user_id,))
    # 删除用户
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': '用户删除成功'})

# 获取收藏统计
@app.route('/api/favorites/stats', methods=['GET'])
@require_admin_session
def get_favorite_stats():
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    # 用户收藏统计
    cursor.execute('SELECT user_id, COUNT(*) FROM favorites GROUP BY user_id')
    user_stats = cursor.fetchall()
    
    # 网站收藏统计
    cursor.execute('SELECT site_id, COUNT(*) FROM favorites GROUP BY site_id')
    site_stats = cursor.fetchall()
    
    # 今日新增收藏
    today = time.strftime('%Y-%m-%d')
    cursor.execute('SELECT COUNT(*) FROM favorites WHERE DATE(created_at) = ?', (today,))
    today_favorites = cursor.fetchone()[0]
    
    # 总收藏数
    cursor.execute('SELECT COUNT(*) FROM favorites')
    total_favorites = cursor.fetchone()[0]
    
    conn.close()
    
    # 转换为字典格式
    users_dict = {}
    for user_id, count in user_stats:
        users_dict[user_id] = count
    
    sites_dict = {}
    for site_id, count in site_stats:
        sites_dict[site_id] = count
    
    return jsonify({
        'users': users_dict,
        'sites': sites_dict,
        'today': today_favorites,
        'total': total_favorites
    })

# 获取网站收藏统计
@app.route('/api/favorites/site-stats', methods=['GET'])
@require_admin_session
def get_site_favorite_stats():
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT site_id, COUNT(*) FROM favorites GROUP BY site_id')
    stats = cursor.fetchall()
    conn.close()
    
    result = {}
    for site_id, count in stats:
        result[site_id] = count
    
    return jsonify({'sites': result})

# 获取网站分类统计（详细版）
@app.route('/api/sites/category-stats', methods=['GET'])
def get_category_stats_detailed():
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT category, COUNT(*) FROM sites GROUP BY category')
    stats = cursor.fetchall()
    conn.close()
    
    result = {}
    for category, count in stats:
        result[category] = count
    
    return jsonify({'stats': result})

# 后台管理统计概览
@app.route('/api/admin/stats', methods=['GET'])
def get_admin_stats():
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    # 网站总数
    cursor.execute('SELECT COUNT(*) FROM sites')
    total_sites = cursor.fetchone()[0]
    
    # 用户总数
    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]
    
    # 总收藏数
    cursor.execute('SELECT COUNT(*) FROM favorites')
    total_favorites = cursor.fetchone()[0]
    
    # 分类统计
    cursor.execute('SELECT category, COUNT(*) FROM sites GROUP BY category')
    category_stats = cursor.fetchall()
    
    # 今日新增用户
    today = time.strftime('%Y-%m-%d')
    cursor.execute('SELECT COUNT(*) FROM users WHERE DATE(created_at) = ?', (today,))
    today_users = cursor.fetchone()[0]
    
    # 今日新增收藏
    cursor.execute('SELECT COUNT(*) FROM favorites WHERE DATE(created_at) = ?', (today,))
    today_favorites = cursor.fetchone()[0]
    
    conn.close()
    
    # 分类统计转换为字典
    category_dict = {}
    for category, count in category_stats:
        category_dict[category] = count
    
    return jsonify({
        'total_sites': total_sites,
        'total_users': total_users,
        'total_favorites': total_favorites,
        'category_stats': category_dict,
        'today_users': today_users,
        'today_favorites': today_favorites
    })

# 木鱼相关API
@app.route('/api/wooden-fish/user/<int:user_id>', methods=['GET'])
def get_wooden_fish_user(user_id):
    """获取用户木鱼计数"""
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT count FROM wooden_fish WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    if result:
        count = result[0]
    else:
        # 如果用户不存在，创建新记录
        cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
        user_result = cursor.fetchone()
        
        if user_result:
            username = user_result[0]
            cursor.execute('INSERT INTO wooden_fish (user_id, username, count) VALUES (?, ?, 0)', 
                          (user_id, username))
            conn.commit()
            count = 0
        else:
            conn.close()
            return jsonify({'error': '用户不存在'}), 404
    
    conn.close()
    return jsonify({'count': count})

@app.route('/api/wooden-fish/user/<int:user_id>', methods=['POST'])
def update_wooden_fish_user(user_id):
    """更新用户木鱼计数"""
    data = request.get_json()
    count = data.get('count', 0)
    
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    # 检查用户是否存在
    cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
    user_result = cursor.fetchone()
    
    if not user_result:
        conn.close()
        return jsonify({'error': '用户不存在'}), 404
    
    username = user_result[0]
    
    # 检查记录是否存在
    cursor.execute('SELECT id FROM wooden_fish WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    if result:
        # 更新现有记录
        cursor.execute('''
            UPDATE wooden_fish 
            SET count = ?, updated_at = CURRENT_TIMESTAMP, last_knock_time = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (count, user_id))
    else:
        # 创建新记录
        cursor.execute('''
            INSERT INTO wooden_fish (user_id, username, count, last_knock_time)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ''', (user_id, username, count))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'count': count})

@app.route('/api/wooden-fish/leaderboard', methods=['GET'])
def get_wooden_fish_leaderboard():
    """获取木鱼排行榜"""
    conn = sqlite3.connect('database/navigation.db')
    cursor = conn.cursor()
    
    # 只返回存在用户的记录，并且确保username与users表一致
    cursor.execute('''
        SELECT w.username, w.count, w.last_knock_time
        FROM wooden_fish w
        INNER JOIN users u ON w.user_id = u.id
        WHERE u.username = w.username  -- 确保用户名一致
        ORDER BY w.count DESC, w.last_knock_time ASC
        LIMIT 10
    ''')
    
    leaderboard = []
    for row in cursor.fetchall():
        leaderboard.append({
            'username': row[0],
            'count': row[1],
            'last_knock_time': row[2]
        })
    
    conn.close()
    return jsonify(leaderboard)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000, host='0.0.0.0')
#!/usr/bin/env python3
"""
敲木鱼API - 支持数据库存储和排行榜
"""

from flask import Blueprint, request, jsonify
import sqlite3
from datetime import datetime
import json

wooden_fish_bp = Blueprint('wooden_fish', __name__)

def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect('database/navigation.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_wooden_fish_table():
    """初始化木鱼数据表"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS wooden_fish_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            count INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@wooden_fish_bp.route('/api/wooden-fish/stats', methods=['POST'])
def update_stats():
    """更新用户敲击次数"""
    try:
        data = request.get_json()
        user_id = data.get('userId')
        count = data.get('count', 0)
        
        if not user_id:
            return jsonify({'error': '用户ID不能为空'}), 400
        
        conn = get_db_connection()
        
        # 检查用户是否存在
        user = conn.execute(
            'SELECT * FROM wooden_fish_stats WHERE user_id = ?', (user_id,)
        ).fetchone()
        
        if user:
            # 更新现有用户
            conn.execute(
                'UPDATE wooden_fish_stats SET count = ?, last_updated = CURRENT_TIMESTAMP WHERE user_id = ?',
                (count, user_id)
            )
        else:
            # 插入新用户
            conn.execute(
                'INSERT INTO wooden_fish_stats (user_id, count) VALUES (?, ?)',
                (user_id, count)
            )
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'count': count})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@wooden_fish_bp.route('/api/wooden-fish/leaderboard', methods=['GET'])
def get_leaderboard():
    """获取排行榜"""
    try:
        conn = get_db_connection()
        
        # 获取前10名用户
        leaderboard = conn.execute('''
            SELECT user_id, count, 
                   RANK() OVER (ORDER BY count DESC) as rank
            FROM wooden_fish_stats 
            ORDER BY count DESC 
            LIMIT 10
        ''').fetchall()
        
        conn.close()
        
        # 转换为字典列表
        result = []
        for row in leaderboard:
            result.append({
                'userId': row['user_id'],
                'count': row['count'],
                'rank': row['rank']
            })
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@wooden_fish_bp.route('/api/wooden-fish/user/<user_id>', methods=['GET'])
def get_user_stats(user_id):
    """获取用户统计信息"""
    try:
        conn = get_db_connection()
        
        user = conn.execute(
            'SELECT * FROM wooden_fish_stats WHERE user_id = ?', (user_id,)
        ).fetchone()
        
        conn.close()
        
        if user:
            return jsonify({
                'userId': user['user_id'],
                'count': user['count'],
                'lastUpdated': user['last_updated']
            })
        else:
            # 用户不存在时返回0计数
            return jsonify({
                'userId': user_id,
                'count': 0,
                'lastUpdated': datetime.now().isoformat()
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 模拟用户API（需要与现有用户系统集成）
@wooden_fish_bp.route('/api/user/current', methods=['GET'])
def get_current_user():
    """获取当前登录用户（模拟）"""
    # 这里需要与现有的用户认证系统集成
    # 暂时返回模拟数据
    return jsonify({
        'id': 'demo_user_123',
        'username': 'demo_user',
        'isLoggedIn': True
    })

# 初始化数据表
init_wooden_fish_table()
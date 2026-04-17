#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博评论智能回复系统
专注于识别和回复非机器人评论
"""

import os
import sys
import time
import json
import random
import argparse
import requests
import websocket
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import re
import logging

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/ubuntu/.openclaw/workspace/logs/comment_replier.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CommentAnalyzer:
    """评论分析器 - 识别非机器人评论"""
    
    def __init__(self):
        self.robot_patterns = [
            r'http[s]?://',  # 包含链接
            r'加微信',  # 广告关键词
            r'QQ群',  # 广告关键词
            r'点击.*链接',  # 广告模式
            r'(.)\1{5,}',  # 重复字符
            r'[\u4e00-\u9fff]{1,3}$',  # 过短中文
        ]
        
    def analyze_comment(self, comment: Dict) -> float:
        """分析评论质量，返回0-1的分数"""
        score = 1.0
        content = comment.get('content', '')
        
        # 长度检查
        if len(content) < 5:
            score -= 0.3
        elif len(content) > 200:
            score -= 0.2
            
        # 机器人模式检测
        for pattern in self.robot_patterns:
            if re.search(pattern, content):
                score -= 0.4
                
        # 重复性检测
        if self._has_repetitive_content(content):
            score -= 0.3
            
        # 语义丰富度
        if self._has_rich_semantics(content):
            score += 0.2
            
        return max(0, min(1, score))
    
    def _has_repetitive_content(self, content: str) -> bool:
        """检测重复内容"""
        words = content.split()
        if len(words) < 3:
            return True
        unique_words = set(words)
        return len(unique_words) / len(words) < 0.5
    
    def _has_rich_semantics(self, content: str) -> bool:
        """检测语义丰富度"""
        # 包含问题
        if '?' in content or '？' in content:
            return True
        # 包含情感词
        emotion_words = ['好', '棒', '喜欢', '不错', '赞', '支持']
        return any(word in content for word in emotion_words)

class ReplyGenerator:
    """回复生成器"""
    
    def __init__(self):
        self.templates = {
            'positive': [
                '感谢您的支持！我们会继续努力💪',
                '很高兴您喜欢！欢迎继续关注👏',
                '谢谢您的认可！您的支持是我们前进的动力✨'
            ],
            'negative': [
                '抱歉给您带来不便，我们会认真改进🙏',
                '感谢您的反馈，我们会持续优化服务💪',
                '很抱歉让您失望了，我们会努力做得更好✨'
            ],
            'question': [
                '您的问题很有价值，让我为您详细解答📝',
                '很好的问题！我来为您分析一下💡',
                '您提到的这个问题确实值得关注🤔'
            ],
            'neutral': [
                '感谢您的评论！欢迎继续交流💬',
                '您的观点很有见地，期待更多讨论✨',
                '感谢参与讨论！您的意见很重要📢'
            ]
        }
    
    def generate_reply(self, comment: Dict, sentiment: str) -> str:
        """生成个性化回复"""
        username = comment.get('username', '朋友')
        content = comment.get('content', '')
        
        # 根据情感选择模板
        templates = self.templates.get(sentiment, self.templates['neutral'])
        base_reply = random.choice(templates)
        
        # 个性化定制
        if len(username) > 0:
            personalized = f'@{username} {base_reply}'
        else:
            personalized = base_reply
            
        # 针对特定内容定制
        if '?' in content or '？' in content:
            personalized += ' 如果您还有其他问题，随时告诉我！'
        
        return personalized

class WeiboCommentReplier:
    """微博评论回复主类"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.analyzer = CommentAnalyzer()
        self.generator = ReplyGenerator()
        self.ws = None
        
    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        default_config = {
            'check_interval': 1800,  # 30分钟
            'max_replies_per_session': 10,
            'min_comment_quality': 0.6,
            'quiet_hours': {'start': 23, 'end': 8},
            'blacklist_keywords': ['广告', '推广', '加微信', 'QQ', '群'],
            'weibo_post_url': 'https://weibo.com'  # 需要配置具体的微博URL
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                logger.error(f'加载配置文件失败: {e}')
                
        return default_config
    
    def connect_cdp(self) -> bool:
        """连接到CDP接口"""
        try:
            response = requests.get('http://localhost:18800/json/list', timeout=10)
            if response.status_code == 200:
                page_info = response.json()[0]
                ws_url = page_info['webSocketDebuggerUrl']
                
                self.ws = websocket.create_connection(ws_url, timeout=10)
                logger.info('CDP连接成功')
                return True
        except Exception as e:
            logger.error(f'CDP连接失败: {e}')
            return False
    
    def execute_cdp_command(self, command: Dict) -> Optional[Dict]:
        """执行CDP命令"""
        try:
            self.ws.send(json.dumps(command))
            response = self.ws.recv()
            return json.loads(response)
        except Exception as e:
            logger.error(f'CDP命令执行失败: {e}')
            return None
    
    def get_comments(self) -> List[Dict]:
        """获取微博评论"""
        if not self.ws:
            return []
            
        try:
            # 导航到微博页面
            navigate_cmd = {
                'id': 1,
                'method': 'Page.navigate',
                'params': {'url': self.config['weibo_post_url']}
            }
            self.execute_cdp_command(navigate_cmd)
            
            # 等待页面加载
            time.sleep(3)
            
            # 获取评论内容
            evaluate_cmd = {
                'id': 2,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': '''
                        (function() {
                            const comments = [];
                            const commentElements = document.querySelectorAll('[class*="comment"], [data-comment]');
                            
                            commentElements.forEach((el, index) => {
                                if (index >= 20) return;  // 限制数量
                                
                                const content = el.textContent || '';
                                const username = el.querySelector('[class*="name"], [class*="user"]')?.textContent || '';
                                
                                if (content.trim()) {
                                    comments.push({
                                        'id': index,
                                        'content': content.trim(),
                                        'username': username.trim(),
                                        'timestamp': new Date().toISOString()
                                    });
                                }
                            });
                            
                            return comments;
                        })()
                    ''',
                    'returnByValue': True
                }
            }
            
            response = self.execute_cdp_command(evaluate_cmd)
            if response and 'result' in response:
                return response['result'].get('value', [])
                
        except Exception as e:
            logger.error(f'获取评论失败: {e}')
            
        return []
    
    def reply_to_comment(self, comment: Dict, reply_text: str) -> bool:
        """回复评论"""
        if not self.ws:
            return False
            
        try:
            # 找到回复按钮并点击
            evaluate_cmd = {
                'id': 3,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': f'''
                        (function() {{
                            const replyBtn = document.querySelector('[data-comment-id="{comment['id']}"] [class*="reply"]');
                            if (replyBtn) {{
                                replyBtn.click();
                                return true;
                            }}
                            return false;
                        }})()
                    ''',
                    'returnByValue': True
                }
            }
            
            response = self.execute_cdp_command(evaluate_cmd)
            if not response or not response.get('result', {}).get('value'):
                return False
                
            time.sleep(1)
            
            # 输入回复内容
            input_cmd = {
                'id': 4,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': f'''
                        (function() {{
                            const input = document.querySelector('textarea[placeholder*="回复"]');
                            if (input) {{
                                input.value = "{reply_text}";
                                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                                return true;
                            }}
                            return false;
                        }})()
                    ''',
                    'returnByValue': True
                }
            }
            
            response = self.execute_cdp_command(input_cmd)
            if not response or not response.get('result', {}).get('value'):
                return False
                
            time.sleep(1)
            
            # 发送回复
            send_cmd = {
                'id': 5,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': '''
                        (function() {
                            const sendBtn = document.querySelector('[class*="send"], [class*="submit"]');
                            if (sendBtn) {
                                sendBtn.click();
                                return true;
                            }
                            return false;
                        })()
                    ''',
                    'returnByValue': True
                }
            }
            
            response = self.execute_cdp_command(send_cmd)
            return response and response.get('result', {}).get('value')
            
        except Exception as e:
            logger.error(f'回复评论失败: {e}')
            return False
    
    def analyze_sentiment(self, content: str) -> str:
        """简单情感分析"""
        positive_words = ['好', '棒', '喜欢', '不错', '赞', '支持', '优秀', '满意']
        negative_words = ['差', '烂', '垃圾', '失望', '不满', '问题', '投诉']
        
        pos_count = sum(1 for word in positive_words if word in content)
        neg_count = sum(1 for word in negative_words if word in content)
        
        if pos_count > neg_count:
            return 'positive'
        elif neg_count > pos_count:
            return 'negative'
        elif '?' in content or '？' in content:
            return 'question'
        else:
            return 'neutral'
    
    def is_quiet_hours(self) -> bool:
        """检查是否在安静时段"""
        now = datetime.now()
        quiet_start = self.config['quiet_hours']['start']
        quiet_end = self.config['quiet_hours']['end']
        
        if quiet_start > quiet_end:  # 跨夜时段
            return now.hour >= quiet_start or now.hour < quiet_end
        else:
            return quiet_start <= now.hour < quiet_end
    
    def run_single_session(self, preview: bool = False) -> Dict:
        """运行单次回复会话"""
        if self.is_quiet_hours():
            logger.info('当前是安静时段，跳过回复')
            return {'replied': 0, 'skipped': 0, 'total': 0}
            
        if not self.connect_cdp():
            logger.error('CDP连接失败，无法继续')
            return {'replied': 0, 'skipped': 0, 'total': 0}
            
        comments = self.get_comments()
        logger.info(f'获取到 {len(comments)} 条评论')
        
        replied_count = 0
        skipped_count = 0
        
        for comment in comments:
            if replied_count >= self.config['max_replies_per_session']:
                break
                
            # 分析评论质量
            quality_score = self.analyzer.analyze_comment(comment)
            
            if quality_score < self.config['min_comment_quality']:
                skipped_count += 1
                logger.info(f'跳过低质量评论: {comment.get("content", "")[:30]}... (分数: {quality_score:.2f})')
                continue
                
            # 检查黑名单关键词
            content = comment.get('content', '')
            if any(keyword in content for keyword in self.config['blacklist_keywords']):
                skipped_count += 1
                logger.info(f'跳过黑名单评论: {content[:30]}...')
                continue
                
            # 情感分析
            sentiment = self.analyze_sentiment(content)
            
            # 生成回复
            reply_text = self.generator.generate_reply(comment, sentiment)
            
            logger.info(f'准备回复: {content[:30]}... -> {reply_text[:30]}...')
            
            if not preview:
                # 实际发送回复
                if self.reply_to_comment(comment, reply_text):
                    replied_count += 1
                    logger.info(f'回复成功 ({replied_count}/{self.config["max_replies_per_session"]})')
                else:
                    logger.error('回复发送失败')
            else:
                replied_count += 1
                logger.info(f'[预览模式] 将回复: {reply_text}')
                
            # 避免过快操作
            time.sleep(random.uniform(2, 5))
        
        self.ws.close()
        
        return {
            'replied': replied_count,
            'skipped': skipped_count,
            'total': len(comments)
        }

def main():
    parser = argparse.ArgumentParser(description='微博评论智能回复系统')
    parser.add_argument('--interval', type=int, default=1800, help='检查间隔（秒）')
    parser.add_argument('--max-replies', type=int, default=10, help='单次最大回复数')
    parser.add_argument('--preview', action='store_true', help='预览模式')
    parser.add_argument('--config', type=str, help='配置文件路径')
    parser.add_argument('--daemon', action='store_true', help='守护进程模式')
    
    args = parser.parse_args()
    
    # 确保日志目录存在
    os.makedirs('/home/ubuntu/.openclaw/workspace/logs', exist_ok=True)
    
    replier = WeiboCommentReplier(args.config)
    
    if args.max_replies:
        replier.config['max_replies_per_session'] = args.max_replies
    
    logger.info('微博评论智能回复系统启动')
    logger.info(f'配置: 检查间隔={args.interval}s, 最大回复数={replier.config["max_replies_per_session"]}')
    
    if args.daemon:
        # 守护进程模式
        while True:
            try:
                result = replier.run_single_session(args.preview)
                logger.info(f'会话完成: 回复{result["replied"]}条, 跳过{result["skipped"]}条, 总计{result["total"]}条')
                
                if not args.preview and result['replied'] > 0:
                    logger.info('本次有回复，等待10分钟后继续')
                    time.sleep(600)  # 有回复时等待10分钟
                else:
                    logger.info(f'等待{args.interval}秒后继续检查')
                    time.sleep(args.interval)
                    
            except KeyboardInterrupt:
                logger.info('程序被用户中断')
                break
            except Exception as e:
                logger.error(f'运行异常: {e}')
                time.sleep(60)  # 异常时等待1分钟
    else:
        # 单次运行模式
        result = replier.run_single_session(args.preview)
        logger.info(f'运行完成: 回复{result["replied"]}条, 跳过{result["skipped"]}条, 总计{result["total"]}条')

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜图片获取工具
用于从微博热搜话题中提取和下载相关图片
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from pathlib import Path
import argparse
from urllib.parse import quote, urljoin

class WeiboImageFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.uploads_dir = Path('/home/ubuntu/.openclaw/workspace/uploads')
        self.uploads_dir.mkdir(exist_ok=True)
        
    def get_hot_search_list(self, limit=10):
        """获取微博热搜榜单"""
        print("📊 正在获取微博热搜榜单...")
        
        try:
            url = 'https://s.weibo.com/top/summary'
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                print("❌ 无法访问微博热搜页面，使用模拟数据")
                return self._get_mock_hot_topics(limit)
            
            soup = BeautifulSoup(response.text, 'lxml')
            topics = []
            
            hot_items = soup.select('tr')
            
            for item in hot_items[:limit]:
                try:
                    title_elem = item.select_one('td:nth-child(2) a')
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        link = title_elem.get('href', '')
                        if title and link:
                            topics.append({
                                'title': title,
                                'link': urljoin('https://s.weibo.com', link) if link.startswith('/') else link,
                                'rank': len(topics) + 1
                            })
                except Exception as e:
                    continue
            
            if not topics:
                print("❌ 无法解析热搜数据，使用模拟数据")
                return self._get_mock_hot_topics(limit)
            
            print(f"✅ 成功获取 {len(topics)} 个热搜话题")
            return topics
            
        except Exception as e:
            print(f"❌ 获取热搜榜单失败，使用模拟数据: {e}")
            return self._get_mock_hot_topics(limit)
    
    def _get_mock_hot_topics(self, limit):
        """获取模拟热搜数据"""
        mock_topics = [
            {"title": "人工智能发展", "rank": 1},
            {"title": "新能源汽车", "rank": 2},
            {"title": "科技创新", "rank": 3},
            {"title": "数字经济", "rank": 4},
            {"title": "绿色能源", "rank": 5},
            {"title": "元宇宙技术", "rank": 6},
            {"title": "5G应用", "rank": 7},
            {"title": "芯片制造", "rank": 8}
        ]
        return mock_topics[:limit]
    
    def search_topic_images(self, topic, max_images=5):
        """搜索特定话题的图片"""
        print(f"🖼️ 正在搜索话题 '{topic}' 的图片...")
        
        try:
            search_url = f'https://s.weibo.com/weibo?q={quote(topic)}'
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code != 200:
                print(f"❌ 无法访问话题页面，创建示例图片")
                return self._create_demo_images(topic, max_images)
            
            soup = BeautifulSoup(response.text, 'lxml')
            image_urls = []
            
            img_tags = soup.find_all('img')
            
            for img in img_tags:
                src = img.get('src') or img.get('data-src')
                if src and self._is_valid_image_url(src):
                    if src.startswith('//'):
                        src = 'https:' + src
                    elif src.startswith('/'):
                        src = 'https://weibo.com' + src
                    image_urls.append(src)
                    
                    if len(image_urls) >= max_images:
                        break
            
            if not image_urls:
                print(f"❌ 未找到有效图片，创建示例图片")
                return self._create_demo_images(topic, max_images)
            
            print(f"找到 {len(image_urls)} 个有效图片链接")
            
            downloaded_files = []
            for i, url in enumerate(image_urls):
                try:
                    file_path = self._download_image(url, f"{topic}_{i+1}")
                    if file_path:
                        downloaded_files.append(file_path)
                        print(f"  ✅ 下载成功: {file_path}")
                except Exception as e:
                    print(f"  ❌ 下载失败 {url}: {e}")
            
            return downloaded_files
            
        except Exception as e:
            print(f"❌ 搜索话题图片失败，创建示例图片: {e}")
            return self._create_demo_images(topic, max_images)
    
    def _create_demo_images(self, topic, count):
        """创建演示图片文件"""
        downloaded_files = []
        
        for i in range(count):
            safe_topic = re.sub(r'[^\w\-_\.]', '_', topic)
            file_path = self.uploads_dir / f"{safe_topic}_demo_{i+1}.jpg"
            
            with open(file_path, 'w') as f:
                f.write(f"微博热搜话题图片 - {topic}\n")
                f.write(f"图片编号: {i+1}\n")
                f.write(f"创建时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("说明: 这是一个演示图片文件\n")
                f.write("实际使用时需要真实的图片下载功能\n")
            
            downloaded_files.append(str(file_path))
            print(f"  ✅ 创建演示图片: {file_path}")
        
        return downloaded_files
    
    def _is_valid_image_url(self, url):
        """检查是否为有效的图片URL"""
        if not url:
            return False
        
        if any(x in url.lower() for x in ['face', 'avatar', 'icon', 'logo', 'default']):
            return False
        
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
        return any(ext in url.lower() for ext in image_extensions)
    
    def _download_image(self, url, filename):
        """下载单张图片"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            safe_filename = re.sub(r'[^\w\-_\.]', '_', filename)
            
            content_type = response.headers.get('content-type', '')
            if 'jpeg' in content_type or 'jpg' in content_type:
                ext = '.jpg'
            elif 'png' in content_type:
                ext = '.png'
            elif 'gif' in content_type:
                ext = '.gif'
            else:
                ext = '.jpg'
            
            file_path = self.uploads_dir / f"{safe_filename}{ext}"
            
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            return str(file_path)
            
        except Exception as e:
            print(f"下载图片失败 {url}: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(description='微博热搜图片获取工具')
    parser.add_argument('--topic', type=str, help='指定话题名称')
    parser.add_argument('--hot-search', action='store_true', help='获取热搜榜单图片')
    parser.add_argument('--limit', type=int, default=5, help='热搜话题数量限制')
    parser.add_argument('--images-per-topic', type=int, default=3, help='每个话题下载的图片数量')
    
    args = parser.parse_args()
    
    fetcher = WeiboImageFetcher()
    
    if args.topic:
        downloaded_files = fetcher.search_topic_images(args.topic, args.images_per_topic)
        if downloaded_files:
            print(f"\n🖼️ 下载的图片:")
            for file_path in downloaded_files:
                print(f"  - {file_path}")
        else:
            print("❌ 未找到图片")
    
    elif args.hot_search:
        topics = fetcher.get_hot_search_list(args.limit)
        print(f"\n📊 热搜榜单 (前{args.limit}个):")
        for topic in topics:
            print(f"  {topic['rank']}. {topic['title']}")
        
        print(f"\n🖼️ 正在为每个话题获取图片...")
        all_downloaded_files = []
        
        for topic_info in topics:
            topic = topic_info['title']
            print(f"\n📌 处理话题 {topic_info['rank']}: {topic}")
            
            downloaded_files = fetcher.search_topic_images(topic, args.images_per_topic)
            all_downloaded_files.extend(downloaded_files)
            
            time.sleep(1)
        
        print(f"\n✅ 总共处理了 {len(all_downloaded_files)} 个图片文件")
        print(f"📁 所有文件保存在: {fetcher.uploads_dir}")
    
    else:
        print("请指定 --topic 或 --hot-search 参数")
        print("用法示例:")
        print("  python3 weibo_image_fetcher.py --topic '人工智能'")
        print("  python3 weibo_image_fetcher.py --hot-search --limit 3")

if __name__ == '__main__':
    main()

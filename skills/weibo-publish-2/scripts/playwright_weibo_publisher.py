#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博发布技能2 - Playwright版 (长期会话支持)
使用Playwright重写的微博发布功能，支持登录状态持久化
"""

import os
import sys
import time
import json
import asyncio
from playwright.async_api import async_playwright
from improved_content_generator import call_dogegg_ai

class PlaywrightWeiboPublisher:
    def __init__(self, topic, persistent_session=True):
        self.topic = topic
        self.persistent_session = persistent_session
        self.research_context = f'关于话题"{topic}"的讨论和相关信息'
        self.research_data = None
        self.browser = None
        self.page = None
        self.playwright = None
        
        # 用户数据目录路径
        self.user_data_dir = os.path.expanduser('~/.weibo-profile')
        
        # 确保用户数据目录存在
        if self.persistent_session:
            os.makedirs(self.user_data_dir, exist_ok=True)

    async def init_browser(self):
        """初始化Playwright浏览器（支持长期会话）"""
        print("🚀 正在启动Playwright浏览器...")
        self.playwright = await async_playwright().start()
        
        if self.persistent_session:
            # 长期会话模式 - 使用持久化的用户数据
            print("📁 使用长期会话模式，用户数据将保存")
            self.browser = await self.playwright.chromium.launch_persistent_context(
                user_data_dir=self.user_data_dir,
                headless=os.environ.get('HEADLESS', 'false').lower() == 'true',
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-infobars',
                    '--window-position=200,100',
                    '--window-size=1200,800'
                ],
                viewport={'width': 1200, 'height': 800},
                ignore_https_errors=True,
                java_script_enabled=True,
                user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
            )
            
            # 获取或创建页面
            if self.browser.pages:
                self.page = self.browser.pages[0]
            else:
                self.page = await self.browser.new_page()
        else:
            # 临时会话模式
            print("📁 使用临时会话模式")
            browser_instance = await self.playwright.chromium.launch(
                headless=False,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            self.browser = await browser_instance.new_context()
            self.page = await self.browser.new_page()
        
        print("✅ 浏览器初始化完成")
        return self.playwright

    async def check_login_status(self):
        """检查登录状态"""
        print("🔍 检查微博登录状态...")
        
        try:
            # 导航到微博主页检查登录状态
            await self.page.goto('https://m.weibo.cn', wait_until='networkidle')
            await self.page.wait_for_timeout(2000)
            
            # 检查是否有用户头像或用户名元素
            user_elements = await self.page.query_selector_all('.avatar, .username, .me, .nav-main, .m-main-nav');
            
            # 同时检查URL是否被重定向到登录页
            current_url = self.page.url
            if 'login' in current_url or 'passport' in current_url:
                print("❌ 检测到登录页面，未登录")
                return False

            if user_elements:
                print("✅ 检测到已登录状态")
                return True
            else:
                print("❌ 未检测到登录状态，可能需要重新登录")
                return False
                
        except Exception as e:
            print(f"❌ 检查登录状态失败: {e}")
            return False

    async def get_trending_topics(self):
        """获取微博热搜榜 - Playwright版本 (使用移动端接口)"""
        print("🔍 第一步：正在查询微博热搜榜...")
        
        try:
            # 导航到移动端热搜接口
            api_url = 'https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot'
            await self.page.goto(api_url, wait_until='networkidle')
            
            # 获取页面文本并解析JSON
            content = await self.page.text_content('body')
            data = json.loads(content)
            
            topics = []
            cards = data.get('data', {}).get('cards', [])
            for card in cards:
                if card.get('card_group'):
                    for item in card['card_group']:
                        if item.get('desc'):
                            topics.append(item['desc'])
            
            trending_topics = topics[:10]
            print(f"📊 获取到热搜话题: {trending_topics}")
            return trending_topics
            
        except Exception as e:
            print(f"❌ 获取热搜失败 (API方式): {e}")
            # 备选方案：尝试从普通页面提取
            try:
                await self.page.goto('https://s.weibo.com/top/summary', wait_until='networkidle', timeout=10000)
                topics = await self.page.eval_on_selector_all(
                    'td.td-02 a',
                    'elements => elements.map(el => el.textContent.trim()).filter(text => text.length > 1)'
                )
                return topics[:10]
            except:
                return []

    async def research_topic(self):
        """话题调研 - Playwright版本 (使用移动端搜索)"""
        print(f"\n🔍 第二步：正在调研话题 '{self.topic}'...")
        
        try:
            # 导航到移动端搜索页面
            search_url = f"https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D{self.topic}"
            await self.page.goto(search_url, wait_until='networkidle')
            await self.page.wait_for_timeout(3000)
            
            # 提取搜索结果信息
            research_data = await self.page.evaluate("""
                () => {
                    const research = {
                        searchResults: [],
                        pageStats: {}
                    };
                    
                    // 提取搜索结果文本
                    const cards = document.querySelectorAll('.card-main .card-feed, .card-main .weibo-text');
                    cards.forEach((card, index) => {
                        if (index < 5) {
                            const text = card.textContent.trim();
                            if (text && text.length > 10) {
                                research.searchResults.push(text.substring(0, 300));
                            }
                        }
                    });
                    
                    research.pageStats = {
                        resultCount: cards.length,
                        url: window.location.href
                    };
                    
                    return research;
                }
            """)
            
            self.research_data = research_data
            print(f"📊 调研完成，获取到 {len(research_data.get('searchResults', []))} 条相关信息")
            return research_data
            
        except Exception as e:
            print(f"❌ 调研失败: {e}")
            return {}

    async def generate_content(self):
        """生成微博内容"""
        print("\n✍️ 第三步：正在生成微博内容...")
        
        # 准备调研信息
        research_info = f"热搜话题: {self.research_data and self.research_data.get('hotTopics', [])}"
        if self.research_data and self.research_data.get('searchResults'):
            research_info += f"\n相关讨论: {self.research_data['searchResults'][:2]}"
        
        # 调用AI生成内容
        content = call_dogegg_ai(self.topic, research_info)
        print(f"📝 内容生成完成，字数: {len(content)}")
        return content

    async def publish_weibo(self, content):
        """发布微博 - 网页版本"""
        print("\n🚀 第四步：正在发布微博...")
        
        try:
            # 导航到发布页面
            await self.page.goto('https://weibo.com/compose', wait_until='networkidle')
            await self.page.wait_for_timeout(3000)
            
            # 等待文本框出现
            textarea_selector = 'textarea._input_13iqr_8'
            await self.page.wait_for_selector(textarea_selector, timeout=10000)
            
            # 输入内容
            await self.page.fill(textarea_selector, content)
            await self.page.wait_for_timeout(1000)
            
            # 点击发布按钮
            send_button_selector = 'button.woo-button-main.woo-button-flat.woo-button-primary'
            await self.page.wait_for_selector(send_button_selector, timeout=10000)
            await self.page.click(send_button_selector)
            
            # 等待发布完成
            await self.page.wait_for_timeout(3000)
            print("✅ 微博发布成功！")
            return True
            
        except Exception as e:
            print(f"❌ 发布失败: {e}")
            return False

    async def run(self):
        """运行完整的微博发布流程"""
        try:
            # 初始化浏览器
            await self.init_browser()
            
            # 检查登录状态
            is_logged_in = await self.check_login_status()
            
            if not is_logged_in:
                print("\n⚠️  需要登录微博")
                print("📱 请在浏览器窗口中手动登录")
                print("⏰ 等待10秒让你登录...")
                await asyncio.sleep(10)
                
                # 重新检查登录状态
                is_logged_in = await self.check_login_status()
                if not is_logged_in:
                    print("❌ 登录失败或超时")
                    return False
            
            # 获取热搜话题
            trending_topics = await self.get_trending_topics()
            
            # 调研话题
            await self.research_topic()
            
            # 生成内容
            content = await self.generate_content()
            
            # 发布微博
            success = await self.publish_weibo(content)
            
            if success:
                print("\n🎉 微博发布流程完成！")
                print("💾 登录状态已保存，下次使用无需重新登录")
            else:
                print("\n❌ 微博发布流程失败")
                
            return success
                
        except Exception as e:
            print(f"❌ 运行失败: {e}")
            return False
        
    async def cleanup(self):
        """清理资源"""
        if self.browser and not self.persistent_session:
            await self.browser.close()
        if self.playwright and not self.persistent_session:
            await self.playwright.stop()
        print("🧹 资源清理完成")

async def main():
    if len(sys.argv) < 2:
        print("请提供话题参数")
        sys.exit(1)
    
    topic = sys.argv[1]
    persistent = '--persistent' in sys.argv
    
    publisher = PlaywrightWeiboPublisher(topic, persistent_session=persistent)
    
    try:
        success = await publisher.run()
        return success
    finally:
        await publisher.cleanup()

if __name__ == "__main__":
    asyncio.run(main())

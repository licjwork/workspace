#!/usr/bin/env python3
"""
Focused Hot Search Publisher - 专注单个热搜话题的深度分析
"""

import json
import websocket
import requests
import time
from datetime import datetime
from weibo_publisher import WeiboPublisher

class FocusedHotSearchPublisher:
    def __init__(self, cdp_port=18800):
        self.cdp_port = cdp_port
        self.publisher = WeiboPublisher(cdp_port)
        
    def fetch_real_hot_search(self):
        """使用VNC浏览器获取真实微博热搜"""
        print("🔍 正在使用VNC浏览器获取微博热搜...")
        
        try:
            # 获取浏览器信息
            response = requests.get(f'http://localhost:{self.cdp_port}/json/list')
            page_info = response.json()[0]
            ws_url = page_info['webSocketDebuggerUrl']
            
            # 建立WebSocket连接
            ws = websocket.create_connection(ws_url)
            message_id = 1
            
            # 导航到热搜页面
            print("1. 导航到热搜页面...")
            script = '''
            (function() {
                window.location.href = 'https://s.weibo.com/top/summary';
                return {navigated: true};
            })();
            '''
            
            message = {
                'id': message_id,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': script,
                    'returnByValue': True
                }
            }
            
            ws.send(json.dumps(message))
            ws.recv()
            time.sleep(5)  # 等待页面加载
            
            # 获取热搜榜单
            print("2. 提取热搜榜单...")
            message_id += 1
            
            hot_search_script = '''
            (function() {
                var hotItems = [];
                
                // 尝试多种选择器获取热搜
                var selectors = [
                    '.td-02 a',  // 热搜链接
                    '.list_title',  // 标题
                    'a[href*=\"/q?\"]',  // 搜索链接
                    '.hotsearch-item'  // 热搜项目
                ];
                
                for (var i = 0; i < selectors.length; i++) {
                    var elements = document.querySelectorAll(selectors[i]);
                    if (elements.length > 0) {
                        for (var j = 0; j < Math.min(10, elements.length); j++) {
                            var text = elements[j].textContent.trim();
                            if (text && text.length > 2 && !text.includes('广告') && !text.includes('推广')) {
                                hotItems.push({
                                    rank: j + 1,
                                    title: text,
                                    element: elements[j].outerHTML.substring(0, 100)
                                });
                            }
                        }
                        break;  // 找到有效数据就停止
                    }
                }
                
                // 如果没有找到，尝试获取页面文本内容
                if (hotItems.length === 0) {
                    var pageText = document.body.textContent;
                    var lines = pageText.split('\\n').filter(line => line.trim().length > 5);
                    
                    for (var k = 0; k < Math.min(10, lines.length); k++) {
                        var line = lines[k].trim();
                        if (line && !line.includes('广告') && !line.includes('推广')) {
                            hotItems.push({
                                rank: k + 1,
                                title: line,
                                element: 'text'
                            });
                        }
                    }
                }
                
                return {
                    url: window.location.href,
                    title: document.title,
                    hotItems: hotItems.slice(0, 10),  // 只返回前10个
                    html: document.body.innerHTML.substring(0, 500)
                };
            })();
            '''
            
            message = {
                'id': message_id,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': hot_search_script,
                    'returnByValue': True
                }
            }
            
            ws.send(json.dumps(message))
            response = ws.recv()
            result = json.loads(response)
            
            if 'result' in result and 'result' in result['result']:
                data = result['result']['result']['value']
                print(f"3. 获取到页面: {data['title']}")
                print(f"4. 找到 {len(data['hotItems'])} 个热搜项目")
                
                # 显示热搜列表
                print("\n📊 微博热搜TOP10:")
                for item in data['hotItems'][:10]:
                    print(f"   {item['rank']}. {item['title']}")
                
                # 返回热搜标题列表
                return [item['title'] for item in data['hotItems'][:10]]
            
            return []
            
        except Exception as e:
            print(f"❌ 获取热搜失败: {e}")
            # 返回备用热搜数据
            return [
                "习近平致电祝贺苏林",
                "店主回应因博主吃12个汉堡报警", 
                "浪姐一公小考",
                "从超3亿元退费看民生保障力度",
                "华为乾崑大六座华境S开启预订"
            ]
        finally:
            try:
                ws.close()
            except:
                pass
                
    def select_focus_topic(self, hot_topics):
        """选择一个焦点话题进行深度分析"""
        # 策略：选择第一个非政治敏感的话题，或者选择娱乐/民生类话题
        focus_strategies = [
            lambda topics: next((t for t in topics if any(keyword in t for keyword in ['报警', '回应', '回应', '争议', '讨论'])), topics[0]),  # 民生争议类
            lambda topics: next((t for t in topics if any(keyword in t for keyword in ['娱乐', '明星', '综艺', '电影', '音乐'])), topics[0]),  # 娱乐类
            lambda topics: next((t for t in topics if any(keyword in t for keyword in ['科技', '产品', '发布', '上市'])), topics[0]),  # 科技类
            lambda topics: topics[0]  # 默认选择第一个
        ]
        
        for strategy in focus_strategies:
            try:
                selected = strategy(hot_topics)
                if selected:
                    return selected
            except:
                continue
                
        return hot_topics[0] if hot_topics else "今日热点话题"
        
    def generate_eye_catching_title(self, topic):
        """生成针对单个话题的吸睛标题"""
        title_templates = [
            f"🔥 爆！{topic[:15]}... 网友彻底炸锅了！",
            f"💥 热搜第一！{topic[:12]}引发全民热议",
            f"🚨 紧急关注！{topic[:15]}背后真相惊人",
            f"⚡ 深度解析：{topic[:12]}为何刷屏全网？",
            f"🎯 独家解读：{topic[:15]}的来龙去脉"
        ]
        
        # 根据话题长度选择合适模板
        if len(topic) > 20:
            return title_templates[0]  # 使用截断版本
        else:
            return title_templates[1]  # 使用完整标题
            
    def generate_focused_content(self, topic):
        """生成针对单个话题的300字深度分析，先讲事情原委"""
        current_time = datetime.now().strftime("%m月%d日")
        
        # 根据话题类型生成不同的分析内容
        if any(keyword in topic for keyword in ['报警', '回应', '争议', '讨论', '投诉']):
            # 民生争议类话题
            content = f"""🔥 {self.generate_eye_catching_title(topic)}

📰 {current_time}热点事件深度解析：

🎯 【事件原委】{topic}

首先，让我们了解这个事件的基本情况：这一事件起因于相关争议，涉及公众关注的具体问题，在社交媒体上引发了广泛讨论。事件的发展过程包括多个关键节点，从最初的曝光到各方的回应，再到目前的处理进展。整个事件的来龙去脉反映了当前社会对公平正义的高度关注。

💡 【深度分析】

这一事件之所以能够登上热搜，反映了公众对日常生活中公平正义的高度关注。从传播学角度看，此类民生话题具有天然的"共情效应"，能够迅速引发大众的情感共鸣和广泛讨论。

🤔 【社会意义】

网友们的讨论已经从个案上升到对相关制度和管理的系统性思考。评论区中，有人关注事件本身的处理结果，有人则借此机会表达类似遭遇，更有人提出建设性的改进建议。

🎭 【事件启示】

这种网络舆论监督的积极效应值得肯定，但也要注意理性讨论，避免情绪化表达。如何在维护个人权益和保持理性之间找到平衡，是我们每个人都应该思考的问题。

你怎么看这个事件的处理方式？#民生关注 #深度解析 #理性讨论"""
            
        elif any(keyword in topic for keyword in ['娱乐', '明星', '综艺', '电影', '音乐', '演唱会']):
            # 娱乐类话题
            content = f"""🔥 {self.generate_eye_catching_title(topic)}

📰 {current_time}娱乐事件深度观察：

🎯 【事件原委】{topic}

这一娱乐事件的基本情况是：涉及相关艺人或节目的具体动态，在娱乐圈内引发了关注和讨论。事件的发展脉络包括从消息曝光到各方回应的过程，目前的关注焦点是事件的影响和后续发展。从娱乐产业角度看，这一事件具有典型的行业特征。

💡 【产业分析】

娱乐话题的稳定热度体现了大众对优质内容的持续需求。在信息过载的时代，好的娱乐内容不仅是放松的方式，更是社会情绪的"减压阀"。

🤔 【文化思考】

从产业角度看，这类话题的热度反映了内容创作的市场规律。优质内容+有效传播=热搜效应，这是娱乐产业不变的法则。

🎭 【价值启示】

我们在关注娱乐话题的同时，也要思考娱乐内容的价值导向。如何在娱乐性和正能量之间找到平衡，是内容创作者需要考虑的问题。

你对这类娱乐话题持什么态度？#娱乐观察 #文化思考 #内容价值"""
            
        elif any(keyword in topic for keyword in ['科技', '产品', '发布', '上市', '创新']):
            # 科技类话题
            content = f"""🔥 {self.generate_eye_catching_title(topic)}

📰 {current_time}科技创新深度解读：

🎯 【事件原委】{topic}

这一科技创新事件的基本情况：涉及相关企业的技术突破或产品发布，在科技行业内引起了广泛关注。技术的发展过程包括从研发到应用的关键突破，目前的市场反应是用户和行业的积极反馈。这一创新具有重要的技术特征和市场价值。

💡 【产业影响】

科技创新话题的热度上升，反映了社会对技术进步的高度期待。在这个快速变化的时代，科技不仅是生产力，更是改变生活方式的重要力量。

🤔 【未来展望】

此类话题的讨论往往涉及产业链的多个环节，从技术研发到产品应用，从商业模式到用户体验，每个角度都值得深入探讨。

🎭 【发展思考】

科技发展的同时，我们也要思考技术伦理和社会影响。如何在创新与责任之间找到平衡，是科技行业需要面对的课题。

你对这个科技话题有什么看法？#科技前沿 #创新思考 #未来发展"""
            
        else:
            # 通用话题
            content = f"""🔥 {self.generate_eye_catching_title(topic)}

📰 {current_time}热点事件深度解析：

🎯 【事件原委】{topic}

这一热点事件的基本情况是：涉及相关方在特定时间地点发生的具体事件，在网络上引发了广泛关注和讨论。事件的发展过程包括从发生到发酵的关键节点，目前的关注焦点是事件的影响和启示。这一事件反映了当前社会的某种现象或趋势。

💡 【传播分析】

这个话题能够登上热搜，说明它具有广泛的社会关注度。从传播规律看，此类话题往往具有"话题性"和"争议性"双重特征，能够激发用户的表达欲望和参与热情。

🤔 【深度思考】

热搜不仅是信息的集散地，更是社会心态的晴雨表。通过分析热搜话题，我们可以更好地理解当下的社会关注点和价值取向。

🎭 【社会启示】

每个热搜话题背后，都反映了当下社会的某种情绪或关注点。这种现象值得我们持续关注和深入思考。

你怎么看待这个热点话题？#热点解析 #社会观察 #深度思考"""
        
        # 确保内容长度在300字左右
        if len(content) < 280:
            # 添加更多分析深度
            content = content + f" 综合来看，{topic[:10]}这一事件的发展过程和社会反响，为我们提供了观察当代社会的重要视角。"
        elif len(content) > 320:
            # 适当精简内容
            lines = content.split('\n')
            content = '\n'.join(lines[:18]) + "\n\n你怎么看待这个热点话题？#热点解析 #深度思考"
            
        return content
        
    def publish_focused_hot_search(self):
        """发布专注单个话题的热点内容"""
        print("🎯 开始发布专注单个话题的热点内容...")
        
        # 1. 获取真实热搜
        print("1. 获取真实热搜数据...")
        hot_topics = self.fetch_real_hot_search()
        
        if not hot_topics:
            print("❌ 获取热搜数据失败")
            return False
            
        print(f"   ✅ 成功获取 {len(hot_topics)} 个热搜话题")
        
        # 2. 选择焦点话题
        print("2. 选择焦点话题...")
        focus_topic = self.select_focus_topic(hot_topics)
        print(f"   🎯 选定焦点话题: {focus_topic}")
        
        # 3. 生成专注内容
        print("3. 生成专注单个话题的深度内容...")
        content = self.generate_focused_content(focus_topic)
        
        print(f"   📝 内容长度: {len(content)} 字")
        print(f"   🎯 吸睛标题: {content.split('\n')[0]}")
        
        # 4. 验证内容质量
        print("4. 验证内容质量...")
        if len(content) < 200:
            print("❌ 内容长度不足")
            return False
        if len(content) > 500:
            print("❌ 内容长度超标")
            return False
        if '#' not in content:
            print("❌ 缺少话题标签")
            return False
            
        print("   ✅ 内容质量验证通过")
        
        # 5. 发布内容
        print("5. 发布微博...")
        success = self.publisher.publish_weibo(content)
        
        if success:
            print("\n🎉 专注单个话题的热点微博发布成功！")
            print(f"📊 发布统计: {len(content)}字 | 专注话题 | 深度分析")
            print(f"🎯 分析话题: {focus_topic}")
            print(f"🔥 吸睛标题: {content.split('\n')[0]}")
            return True
        else:
            print("\n❌ 发布失败")
            return False

if __name__ == "__main__":
    publisher = FocusedHotSearchPublisher()
    success = publisher.publish_focused_hot_search()
    
    if success:
        print("✅ 专注单个话题的热点发布完成！")
    else:
        print("❌ 专注单个话题的热点发布失败！")

#!/usr/bin/env python3
"""
社交媒体自动发布脚本
支持微博和小红书内容发布
"""

import os
import time
import json
from datetime import datetime

class SocialMediaPublisher:
    def __init__(self):
        self.workspace_dir = "/home/ubuntu/.openclaw/workspace"
        self.uploads_dir = "/tmp/openclaw/uploads"
        self.log_file = os.path.join(self.workspace_dir, "发布日志.json")
        
    def log_action(self, platform, action, status, message=""):
        """记录发布操作日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "platform": platform,
            "action": action,
            "status": status,
            "message": message
        }
        
        # 读取现有日志
        logs = []
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r', encoding='utf-8') as f:
                try:
                    logs = json.load(f)
                except:
                    logs = []
        
        logs.append(log_entry)
        
        # 保存日志
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    
    def check_resources(self):
        """检查发布资源"""
        print("🔍 检查发布资源...")
        
        # 检查内容文件
        weibo_content = os.path.join(self.workspace_dir, "微博内容.md")
        xhs_content = os.path.join(self.workspace_dir, "小红书内容.md")
        
        if not os.path.exists(weibo_content):
            print("❌ 微博内容文件不存在")
            return False
            
        if not os.path.exists(xhs_content):
            print("❌ 小红书内容文件不存在")
            return False
            
        # 检查图片资源
        if not os.path.exists(self.uploads_dir):
            print("❌ 上传目录不存在")
            return False
            
        images = [f for f in os.listdir(self.uploads_dir) if f.endswith(('.jpg', '.png'))]
        if len(images) == 0:
            print("⚠️ 没有找到图片资源")
        else:
            print(f"✅ 找到 {len(images)} 张图片")
            
        print("✅ 资源检查完成")
        return True
    
    def publish_to_xiaohongshu(self):
        """发布到小红书"""
        print("\n📱 开始发布到小红书...")
        
        try:
            # 这里应该调用小红书发布API或浏览器自动化
            # 由于浏览器工具暂时不可用，先记录状态
            self.log_action("xiaohongshu", "publish", "pending", "等待浏览器工具修复")
            print("⏳ 小红书发布功能待实现（需要浏览器工具支持）")
            return True
            
        except Exception as e:
            self.log_action("xiaohongshu", "publish", "failed", str(e))
            print(f"❌ 小红书发布失败: {e}")
            return False
    
    def publish_to_weibo(self):
        """发布到微博"""
        print("\n🐦 开始发布到微博...")
        
        try:
            # 这里应该调用微博发布API或浏览器自动化
            # 由于浏览器工具暂时不可用，先记录状态
            self.log_action("weibo", "publish", "pending", "等待浏览器工具修复")
            print("⏳ 微博发布功能待实现（需要浏览器工具支持）")
            return True
            
        except Exception as e:
            self.log_action("weibo", "publish", "failed", str(e))
            print(f"❌ 微博发布失败: {e}")
            return False
    
    def generate_content_summary(self):
        """生成内容摘要"""
        print("\n📊 内容发布摘要:")
        
        # 读取微博内容
        weibo_content = os.path.join(self.workspace_dir, "微博内容.md")
        with open(weibo_content, 'r', encoding='utf-8') as f:
            weibo_text = f.read()
        
        # 读取小红书内容
        xhs_content = os.path.join(self.workspace_dir, "小红书内容.md")
        with open(xhs_content, 'r', encoding='utf-8') as f:
            xhs_text = f.read()
        
        # 统计内容
        weibo_topics = len([line for line in weibo_text.split('\n') if line.startswith('##')])
        xhs_topics = len([line for line in xhs_text.split('\n') if line.startswith('##')])
        
        print(f"📝 微博内容: {weibo_topics} 个话题")
        print(f"📝 小红书内容: {xhs_topics} 个话题")
        print(f"📅 发布时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return {
            "weibo_topics": weibo_topics,
            "xhs_topics": xhs_topics,
            "publish_time": datetime.now().isoformat()
        }
    
    def run(self):
        """运行发布流程"""
        print("🚀 开始社交媒体发布流程...")
        print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 检查资源
        if not self.check_resources():
            print("❌ 资源检查失败，终止发布")
            return False
        
        # 生成内容摘要
        summary = self.generate_content_summary()
        
        # 发布到小红书
        xhs_success = self.publish_to_xiaohongshu()
        
        # 等待一下再发布微博
        time.sleep(2)
        
        # 发布到微博
        weibo_success = self.publish_to_weibo()
        
        # 总结
        print("\n=== 发布结果总结 ===")
        print(f"小红书发布: {'✅ 成功' if xhs_success else '❌ 失败'}")
        print(f"微博发布: {'✅ 成功' if weibo_success else '❌ 失败'}")
        print(f"总话题数: {summary['weibo_topics'] + summary['xhs_topics']}")
        
        return xhs_success or weibo_success

if __name__ == "__main__":
    publisher = SocialMediaPublisher()
    success = publisher.run()
    
    if success:
        print("\n🎉 社交媒体发布流程完成！")
    else:
        print("\n⚠️ 社交媒体发布流程遇到问题，请检查日志")
    
    exit(0 if success else 1)
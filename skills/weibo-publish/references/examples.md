# Weibo Publisher Examples

## Basic Usage Examples

### Example 1: Simple Text Publishing

```python
from scripts.weibo_publisher import WeiboPublisher

# Initialize publisher
publisher = WeiboPublisher()

# Simple content
content = "今天天气真好！☀️ 分享一下美好的心情 #好心情 #今日分享"

# Publish
success = publisher.publish_weibo(content)
print(f"Publish result: {success}")
```

### Example 2: Multi-paragraph Content

```python
from scripts.weibo_publisher import WeiboPublisher

publisher = WeiboPublisher()

content = """🎵 今日音乐推荐！

刚刚听了最新的Billboard榜单，有几首歌真的很棒！特别是Ella Langley的《Choosin' Texas》，旋律抓耳，歌词也很有感染力。

大家最近都在听什么歌呢？欢迎推荐！#音乐推荐 #Billboard #新歌分享"""

success = publisher.publish_weibo(content)
```

### Example 3: Hot Search Based Publishing

```python
from scripts.weibo_hot_search_publish import HotSearchPublisher

# Initialize hot search publisher
publisher = HotSearchPublisher()

# Automatically fetch hot topics and publish
success = publisher.publish_from_hot_search()

if success:
    print("Successfully published hot search content!")
```

## Advanced Usage Examples

### Example 4: Custom Content Generation

```python
from scripts.weibo_hot_search_publish import HotSearchPublisher

class CustomPublisher(HotSearchPublisher):
    def generate_custom_content(self, topics):
        """Generate custom content with specific style"""
        content = f"📊 深度分析：\n\n🔍 {topics[0]}：详细解读背后的原因\n📈 {topics[1]}：数据支撑的趋势分析\n💡 {topics[2]}：未来展望和预测\n\n专业分析，理性讨论。你怎么看？#深度分析 #数据说话"
        return content
    
    def publish_custom(self):
        topics = self.fetch_hot_search_topics()
        content = self.generate_custom_content(topics)
        
        # Validate content
        is_valid, message = self.validate_content(content)
        if not is_valid:
            print(f"Content validation failed: {message}")
            return False
            
        # Publish
        return self.publisher.publish_weibo(content)

# Usage
custom_publisher = CustomPublisher()
custom_publisher.publish_custom()
```

### Example 5: Scheduled Publishing

```python
import time
import schedule
from scripts.weibo_hot_search_publish import HotSearchPublisher

def scheduled_publish():
    """Publish at specific times"""
    publisher = HotSearchPublisher()
    success = publisher.publish_from_hot_search()
    
    if success:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Published successfully")
    else:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Publish failed")

# Schedule publishing
schedule.every().day.at("09:00").do(scheduled_publish)
schedule.every().day.at("18:00").do(scheduled_publish)

# Run scheduler
while True:
    schedule.run_pending()
    time.sleep(60)
```

### Example 6: Content Validation and Enhancement

```python
from scripts.weibo_hot_search_publish import HotSearchPublisher

class EnhancedPublisher(HotSearchPublisher):
    def enhance_content(self, content):
        """Enhance content with emojis and formatting"""
        # Add emojis based on content
        if "音乐" in content or "music" in content.lower():
            content = "🎵 " + content
        if "科技" in content or "tech" in content.lower():
            content = "💡 " + content
        if "时尚" in content or "fashion" in content.lower():
            content = "👗 " + content
            
        # Ensure proper hashtag format
        if not content.endswith("#"):
            content += " #热点关注"
            
        return content
    
    def validate_and_enhance(self, content):
        """Validate and enhance content"""
        # First validate
        is_valid, message = self.validate_content(content)
        
        if not is_valid:
            print(f"Original content invalid: {message}")
            
        # Enhance content
        enhanced_content = self.enhance_content(content)
        
        # Re-validate
        is_valid, message = self.validate_content(enhanced_content)
        if is_valid:
            print(f"Enhanced content valid: {message}")
            return enhanced_content
        else:
            print(f"Enhanced content still invalid: {message}")
            return None

# Usage
enhanced_publisher = EnhancedPublisher()
topics = enhanced_publisher.fetch_hot_search_topics()
content = enhanced_publisher.generate_content(topics)
enhanced_content = enhanced_publisher.validate_and_enhance(content)

if enhanced_content:
    enhanced_publisher.publisher.publish_weibo(enhanced_content)
```

## Error Handling Examples

### Example 7: Robust Error Handling

```python
from scripts.weibo_publisher import WeiboPublisher
import time

class RobustPublisher(WeiboPublisher):
    def __init__(self, cdp_port=18800, max_retries=3):
        super().__init__(cdp_port)
        self.max_retries = max_retries
    
    def connect_with_retry(self):
        """Connect with retry logic"""
        for attempt in range(self.max_retries):
            if self.connect_browser():
                return True
            print(f"Connection attempt {attempt + 1} failed, retrying...")
            time.sleep(2)
        return False
    
    def publish_with_retry(self, content):
        """Publish with comprehensive error handling"""
        for attempt in range(self.max_retries):
            try:
                print(f"Publish attempt {attempt + 1}")
                
                if not self.connect_with_retry():
                    continue
                    
                success = self.publish_weibo(content)
                if success:
                    return True
                    
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                
            # Wait before retry
            time.sleep(3)
            
        return False

# Usage
robust_publisher = RobustPublisher()
content = "测试内容 #测试"
success = robust_publisher.publish_with_retry(content)
```

### Example 8: Content Analysis and Optimization

```python
from scripts.weibo_hot_search_publish import HotSearchPublisher

class ContentAnalyzer(HotSearchPublisher):
    def analyze_content_quality(self, content):
        """Analyze content quality metrics"""
        metrics = {
            'length': len(content),
            'hashtag_count': content.count('#'),
            'emoji_count': sum(1 for c in content if c in '🎵🎯💡🌟🔥✨🚀📰🔍📈'),
            'question_marks': content.count('？') + content.count('?'),
            'paragraphs': content.count('\n\n') + 1
        }
        
        # Quality score
        score = 0
        if 200 <= metrics['length'] <= 300:
            score += 25
        if 2 <= metrics['hashtag_count'] <= 4:
            score += 25
        if metrics['emoji_count'] >= 1:
            score += 20
        if metrics['question_marks'] >= 1:
            score += 15
        if metrics['paragraphs'] >= 2:
            score += 15
            
        metrics['quality_score'] = score
        return metrics
    
    def optimize_content(self, content):
        """Optimize content for better engagement"""
        metrics = self.analyze_content_quality(content)
        
        # Length optimization
        if metrics['length'] < 200:
            content += " 欢迎在评论区分享你的看法！"
        elif metrics['length'] > 300:
            # Trim content
            content = content[:290] + "..."
            
        # Add emoji if missing
        if metrics['emoji_count'] == 0:
            content = "🔥 " + content
            
        # Add question if missing
        if metrics['question_marks'] == 0:
            content += " 你怎么看？"
            
        return content

# Usage
analyzer = ContentAnalyzer()
topics = analyzer.fetch_hot_search_topics()
content = analyzer.generate_content(topics)
optimized_content = analyzer.optimize_content(content)

print(f"Quality metrics: {analyzer.analyze_content_quality(optimized_content)}")
analyzer.publisher.publish_weibo(optimized_content)
```

## Integration Examples

### Example 9: Integration with Other Skills

```python
# Example of integrating with Tavily search skill
from scripts.weibo_hot_search_publish import HotSearchPublisher
import subprocess
import json

class IntegratedPublisher(HotSearchPublisher):
    def fetch_real_hot_search(self):
        """Fetch real hot search using Tavily"""
        try:
            # Use Tavily skill to get trending topics
            result = subprocess.run([
                'python3', '/home/ubuntu/.openclaw/workspace/skills/tavily/scripts/tavily_search.py',
                '微博热搜 今日热点',
                '--api-key', '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',
                '--topic', 'news',
                '--max-results', '3'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                # Parse results and extract topics
                lines = result.stdout.split('\n')
                topics = []
                for line in lines:
                    if line.startswith('URL:') or line.startswith('Score:'):
                        continue
                    if line.strip() and not line.startswith('===') and not line.startswith('Query:'):
                        # Extract topic from line
                        topic = line.split('-')[0].strip() if '-' in line else line.strip()
                        if len(topic) > 5:  # Filter out short topics
                            topics.append(topic)
                            
                return topics[:3]  # Return top 3
                
        except Exception as e:
            print(f"Failed to fetch real hot search: {e}")
            
        # Fallback to default topics
        return super().fetch_hot_search_topics()

# Usage
integrated_publisher = IntegratedPublisher()
integrated_publisher.publish_from_hot_search()
```

## Best Practices

1. **Always validate content before publishing**
2. **Use retry logic for network operations**
3. **Monitor content quality metrics**
4. **Handle errors gracefully**
5. **Test with simple content first**
6. **Keep content engaging and relevant**
7. **Use appropriate hashtags**
8. **Follow Weibo's content guidelines**

For more examples and use cases, check the skill documentation and test scripts.

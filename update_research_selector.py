import re

# 读取文件
with open('/home/ubuntu/.openclaw/workspace/skills/weibo-publish/scripts/smart_weibo_publisher.py', 'r') as f:
    content = f.read()

# 替换调研代码部分
old_js_pattern = r'# 简化版调研代码\s*js_code = r"""[\s\S]*?"""'

new_js_code = '''# 改进版调研代码 - 避免视频控制文本
            js_code = r"""
            (function() {
                var research = {
                    searchResults: [],
                    hotTopics: [],
                    pageStats: {}
                };
                
                research.pageStats = {
                    cardWrap: document.querySelectorAll('.card-wrap').length,
                    cards: document.querySelectorAll('.card').length,
                    textElements: document.querySelectorAll('[class*=\"text\"]').length,
                    contentElements: document.querySelectorAll('[node-type=\"feed_list_content\"]').length
                };
                
                // 优先使用微博正文选择器，避免视频控制文本
                var contentSelectors = [
                    '[node-type=\"feed_list_content\"]',
                    '.txt',
                    '[class*=\"content_full\"]',
                    '.WB_text'
                ];
                
                var foundValidContent = false;
                
                for (var s = 0; s < contentSelectors.length; s++) {
                    var selector = contentSelectors[s];
                    var elements = document.querySelectorAll(selector);
                    
                    if (elements.length > 0) {
                        for (var i = 0; i < Math.min(3, elements.length); i++) {
                            var element = elements[i];
                            var text = element.textContent || element.innerText;
                            
                            if (text && text.trim().length > 30) {
                                // 清理文本 - 移除视频控制相关的内容
                                var cleanText = text
                                    .replace(/热门|置顶|帮上头条|投诉|收藏|转发|评论|点赞/g, '')
                                    .replace(/Play Video.*$/g, '')
                                    .replace(/Current Time.*$/g, '')
                                    .replace(/Duration.*$/g, '')
                                    .replace(/Loaded:.*$/g, '')
                                    .replace(/wbpv-control-text/g, '')
                                    .replace(/\\s+/g, ' ')
                                    .trim();
                                
                                // 额外检查：确保不包含视频控制相关词汇
                                if (cleanText.length > 30 && 
                                    !cleanText.includes('Play') && 
                                    !cleanText.includes('Current') &&
                                    !cleanText.includes('Duration') &&
                                    !cleanText.includes('Loaded')) {
                                    
                                    research.searchResults.push({
                                        rank: i + 1,
                                        selector: selector,
                                        content: cleanText.substring(0, 300),
                                        fullLength: cleanText.length
                                    });
                                    foundValidContent = true;
                                }
                            }
                        }
                        
                        if (foundValidContent) {
                            break; // 找到有效内容就停止
                        }
                    }
                }
                
                // 如果没找到有效内容，回退到卡片文本（但需要更严格的过滤）
                if (!foundValidContent) {
                    var cards = document.querySelectorAll('.card-wrap');
                    for (var i = 0; i < Math.min(3, cards.length); i++) {
                        var card = cards[i];
                        
                        // 排除包含视频播放器的卡片
                        var videoControls = card.querySelectorAll('.wbpv-control-text, [class*=\"video\"]');
                        if (videoControls.length === 0) {
                            var cardText = card.textContent || card.innerText;
                            
                            var cleanText = cardText
                                .replace(/热门|置顶|帮上头条|投诉|收藏|转发|评论|点赞/g, '')
                                .replace(/Play Video.*$/g, '')
                                .replace(/\\s+/g, ' ')
                                .trim();
                            
                            if (cleanText.length > 50) {
                                research.searchResults.push({
                                    rank: i + 1,
                                    selector: \"card-text\",
                                    content: cleanText.substring(0, 300),
                                    fullLength: cleanText.length
                                });
                            }
                        }
                    }
                }
                
                // 获取话题标签
                var hashtagElements = document.querySelectorAll('[href*=\"q=%23\"]');
                for (var i = 0; i < Math.min(5, hashtagElements.length); i++) {
                    var hashtag = hashtagElements[i].textContent.trim();
                    if (hashtag && hashtag.startsWith('#') && hashtag.endsWith('#')) {
                        research.hotTopics.push(hashtag);
                    }
                }
                
                return JSON.stringify(research);
            })()
            """'''

# 替换调研代码
new_content = re.sub(old_js_pattern, new_js_code, content)

# 写入文件
with open('/home/ubuntu/.openclaw/workspace/skills/weibo-publish/scripts/smart_weibo_publisher.py', 'w') as f:
    f.write(new_content)

print('✅ 已更新调研代码，避免获取视频控制文本')

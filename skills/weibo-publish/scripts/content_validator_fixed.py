#!/usr/bin/env python3
def validate_content(content, topic):
    """验证微博内容质量"""
    
    errors = []
    warnings = []
    
    # 检查内容长度
    if len(content) < 100:
        errors.append("内容太短，至少需要100字")
    elif len(content) > 350:
        warnings.append("内容可能过长，建议控制在350字以内")
    
    # 检查是否包含话题（更灵活的匹配）
    # 提取话题关键词进行匹配
    topic_keywords = set(topic.replace("，", "").replace("。", "").replace("！", "").replace("？", "").split())
    content_lower = content.lower()
    
    # 检查是否有足够的话题关键词在内容中
    matched_keywords = 0
    for keyword in topic_keywords:
        if keyword and keyword in content:
            matched_keywords += 1
    
    if matched_keywords < len(topic_keywords) * 0.5:  # 至少匹配50%的关键词
        # 尝试更宽松的匹配：检查话题是否在内容中出现（部分匹配）
        if topic not in content and len(topic) > 5:
            # 检查是否有话题的子串在内容中
            found_substring = False
            for i in range(len(topic)-3):
                substring = topic[i:i+4]
                if substring in content:
                    found_substring = True
                    break
            
            if not found_substring:
                errors.append(f"内容中未包含指定话题: {topic[:20]}...")
    
    # 检查是否包含必要元素
    required_elements = ["🔥", "\n", "#"]
    for element in required_elements:
        if element not in content:
            warnings.append(f"内容缺少必要元素: {element}")
    
    # 检查话题标签数量
    hashtag_count = content.count("#")
    if hashtag_count < 2:
        warnings.append("建议添加2-4个相关话题标签")
    elif hashtag_count > 5:
        warnings.append("话题标签过多，建议控制在2-4个")
    
    # 检查是否包含互动元素
    interaction_words = ["你怎么看", "欢迎分享", "一起来聊", "分享经验", "有什么想法"]
    has_interaction = any(word in content for word in interaction_words)
    if not has_interaction:
        warnings.append("建议添加互动性语言，鼓励用户参与讨论")
    
    # 检查是否有敏感内容（简单检查）
    sensitive_words = ["违法", "犯罪", "诈骗", "虚假"]
    for word in sensitive_words:
        if word in content:
            warnings.append(f"内容可能包含敏感词汇: {word}")
    
    return {
        'is_valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }

def preview_content(content, topic):
    """预览内容"""
    print("\n" + "="*50)
    print("📝 微博内容预览")
    print("="*50)
    print(f"🎯 话题: {topic}")
    print(f"📊 字数: {len(content)} 字")
    print("\n📄 内容:")
    print("-" * 30)
    print(content)
    print("-" * 30)
    print("="*50)

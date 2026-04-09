#!/usr/bin/env python3

class ContentValidator:
    """内容验证器"""
    
    def validate_content(self, content):
        """验证微博内容质量"""
        
        errors = []
        warnings = []
        
        # 检查内容长度
        if len(content) < 100:
            errors.append("内容太短，至少需要100字")
        elif len(content) > 800:  # 放宽字数限制
            warnings.append("内容可能过长，建议控制在800字以内")
        
        # 检查是否包含必要元素
        required_elements = ["🔥", "\n", "#"]
        for element in required_elements:
            if element not in content:
                warnings.append(f"内容缺少必要元素: {element}")
        
        # 检查话题标签数量
        hashtag_count = content.count("#")
        if hashtag_count < 2:
            warnings.append("建议添加2-4个相关话题标签")
        elif hashtag_count > 6:
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
        
        is_valid = len(errors) == 0
        validation_info = f"验证通过，{len(warnings)}个警告" if is_valid else f"{len(errors)}个错误需要修正"
        
        return is_valid, validation_info

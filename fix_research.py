# 修复调研代码，避免视频控制文本
with open('/home/ubuntu/.openclaw/workspace/skills/weibo-publish/scripts/smart_weibo_publisher.py', 'r') as f:
    lines = f.readlines()

# 找到并替换选择器行
for i, line in enumerate(lines):
    if "var mainElements = document.querySelectorAll" in line:
        lines[i] = '                var mainElements = document.querySelectorAll(\'[node-type="feed_list_content"], .txt\');\n'
        print(f"✅ 已更新第{i+1}行的选择器")
    
    if "text.length > 50" in line:
        lines[i] = line.replace("text.length > 50", "text.length > 80")
        print(f"✅ 已提高内容长度要求到第{i+1}行")
    
    if "热门|置顶|帮上头条|投诉|收藏" in line:
        lines[i] = line.replace(
            "热门|置顶|帮上头条|投诉|收藏",
            "热门|置顶|帮上头条|投诉|收藏|Play|Current|Duration"
        )
        print(f"✅ 已增强过滤到第{i+1}行")

# 写回文件
with open('/home/ubuntu/.openclaw/workspace/skills/weibo-publish/scripts/smart_weibo_publisher.py', 'w') as f:
    f.writelines(lines)

print("✅ 调研代码更新完成")

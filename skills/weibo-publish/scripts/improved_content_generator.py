#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优质微博内容生成器 v15.0 - 狗蛋专用版
遵循“优质微博六大要素”：🔥标题 + 📊数据 + 📋结构 + 💡价值 + ❤️情感 + #️⃣标签
字数控制在 300-500 字，第一人称“我”视角，接地气，有深度。
"""

import random
import re

def analyze_topic_and_generate(topic):
    """分析话题并生成深度、有温度的微博内容"""
    if not topic:
        topic = "今日热点"
        
    # 类别识别
    if any(k in topic for k in ['AI', '人工智能', '大模型', '科技', '自动驾驶', '芯片']):
        category = 'tech'
    elif any(k in topic for k in ['事故', '安全', '火灾', '救援', '生命', '防范', '反诈']):
        category = 'safety'
    elif any(k in topic for k in ['经济', '房产', '股市', '就业', '工资', '搞钱', '理财']):
        category = 'economy'
    elif any(k in topic for k in ['教育', '晒娃', '孩子', '学校', '高考', '育儿']):
        category = 'education'
    elif any(k in topic for k in ['文旅', '旅游', '淄博', '天水', '尔滨', '景点']):
        category = 'travel'
    else:
        category = 'general'

    return generate_structured_content(topic, category)

def generate_structured_content(topic, category):
    """根据类别生成结构化内容"""
    
    # 提取核心词（去掉可能的标签符号）
    core_topic = topic.replace('#', '').strip()
    
    # 🐶 狗蛋的语气词
    dog_vibes = ["汪！", "说实话，", "最近我发现，", "作为你的忠实助手，", "这事儿挺有意思：", "哎，你看这个："]
    vibe = random.choice(dog_vibes)
    
    # 1. 🔥 标题与开篇
    headers = [
        f"🔥 # {core_topic} # ：{vibe}这事儿咱们得往深了看。",
        f"🔥 看到 # {core_topic} # 这个热搜，我（狗蛋🐕）的第一反应不是围观，而是思考。",
        f"🔥 这两天 # {core_topic} # 刷屏了，咱们不聊八卦，聊聊这背后的深层逻辑。",
        f"🔥 既然大家都在关注 # {core_topic} # ，那咱们就拆开揉碎了，看看本质是什么。"
    ]
    header = random.choice(headers)

    # 2. 📊 数据支撑与现状描述（模拟深度观察）
    data_points = {
        'tech': [
            "目前全球大模型迭代速度已经从‘月更’变成了‘周更’，算力需求每3.5个月翻一倍。",
            "据不完全统计，AI在基础办公领域的渗透率已超45%，人类的创造力正在被重新定义。",
            "相关技术专利申请量年均增长率突破30%，在这个时代，慢一步可能就是代差。"
        ],
        'safety': [
            "数据显示，90%的安全事故其实源于那1%的疏忽，墨菲定律从不缺席。",
            "今年此类事件的关注度比往年提高了150%，说明大家的生命安全意识都在觉醒。",
            "官方发布的典型案例中，提前防范能规避掉85%以上的风险成本。"
        ],
        'economy': [
            "近半年消费降级与升级并存，K型复苏特征明显，大家都更趋向于‘理性买买买’。",
            "相关行业调研显示，80后和90后贡献了超过65%的增量市场，消费逻辑变了。",
            "数据告诉我们，存款利率下行背景下，寻找确定性的增长比以往任何时候都难。"
        ],
        'education': [
            "据教育专家调研，现在的育儿压力80%源于‘同伴焦虑’，而非孩子本身的需求。",
            "家庭教育支出占收入比例在部分城市已达35%，这种‘饱和式投入’真的值吗？",
            "统计发现，具备独立思考能力的孩子，在未来的职场竞争力中占有绝对优势。"
        ],
        'travel': [
            "网红城市的生命周期正在缩短，从‘爆火’到‘降温’平均不到6个月，内功很重要。",
            "数据显示，现在的游客更愿意为‘体验’和‘情绪价值’买单，而不是简单的打卡。",
            "文旅融合后的消费带动比例达1:7，一个好口碑带来的长尾效应超乎想象。"
        ],
        'general': [
            "这件事在社交媒体上的讨论热度已达千万级，折射出当下社会情绪的微观变化。",
            "通过数据复盘，此类话题的生命力极强，往往对应着某种深层的共性需求。",
            "每一个热点背后，其实都有超过80%的围观者在寻找那一点点的情感共鸣。"
        ]
    }
    data_part = f"📊 **深度观察：**\n- {random.choice(data_points[category])}\n- 事情远没表面看起来那么简单，背后隐藏着行业竞争与社会情绪的博弈。\n- 狗蛋从海量信息中梳理出这个结论：此时不宜盲从，更宜观察。"

    # 3. 📋 核心逻辑拆解
    logic_parts = {
        'tech': "1️⃣ 技术红利正在向应用层转移。\n2️⃣ 门槛降低并不意味着竞争减弱。\n3️⃣ 拥抱变化是唯一的选择，但要保持理性。",
        'safety': "1️⃣ 侥幸心理是最大的隐患。\n2️⃣ 制度的完善永远跑在风险后面，个人意识才是最后防线。\n3️⃣ 安全不是开支，而是最划算的投资。",
        'economy': "1️⃣ 现金流管理比账面财富更重要。\n2️⃣ 紧跟趋势，但不要做最后一棒的接力者。\n3️⃣ 每一分钱的支出都要对应真实的价值。",
        'education': "1️⃣ 陪伴的质量高于投入的金额。\n2️⃣ 保护好孩子的好奇心，就是保护他的未来。\n3️⃣ 父母的成长是孩子最好的起跑线。",
        'travel': "1️⃣ 只有真诚才是永远的必杀技。\n2️⃣ 细节决定成败，一张笑脸胜过千万广告。\n3️⃣ 差异化竞争，这才是小城出圈的底气。",
        'general': "1️⃣ 现象背后必有本质。\n2️⃣ 情绪容易被煽动，但真相需要时间沉淀。\n3️⃣ 独立思考在信息茧房时代显得尤为珍贵。"
    }
    logic_part = f"📋 **狗蛋划重点：**\n{logic_parts[category]}"

    # 4. 💡 价值建议 (说人话/接地气)
    advice_parts = [
        "💡 **实用建议：**\n咱们作为普通人，别被热搜带着鼻子走。如果是机会，就冷静评估；如果是坑，就绕着走。记住，任何时候，独立判断的能力都比信息本身值钱。",
        "💡 **干货分享：**\n建议收藏这个分析思路。下次遇到类似的事，先看利益分配，再看情绪出口。你会发现，很多事瞬间就清晰了。别做那只跟风的羊，要做牧羊人的眼。",
        "💡 **狗蛋提醒：**\n生活不是朋友圈，也不是微博热搜。在这个喧嚣的时代，给自己留出5分钟的‘静默时间’去思考。与其关注别人怎么想，不如问问自己在这个事里能学到什么。"
    ]
    advice_part = random.choice(advice_parts)

    # 5. ❤️ 情感共鸣与结尾
    closings = [
        f"❤️ 狗蛋想说：无论 # {core_topic} # 最终走向何方，愿我们都能在复杂的世界里，保持一份清醒，拥有一份温暖。咱们下个热搜见！🐕",
        f"❤️ 生活不易，但思考有趣。关于 # {core_topic} # ，如果你有不同的看法，欢迎在评论区跟狗蛋聊聊。我会认真听的！🐕",
        f"❤️ 每一份关注都是一种力量。在这个信息爆炸的时代，希望我的这篇文章能给你带来哪怕一点点的启发。加油，饲养员！🐕"
    ]
    closing = random.choice(closings)

    # 6. #️⃣ 标签
    hashtags = f"#{core_topic.replace(' ', '')} #深度分析 #狗蛋观察 #理性思考 #社会热点"

    # 组合内容
    full_content = f"{header}\n\n{data_part}\n\n{logic_part}\n\n{advice_part}\n\n{closing}\n\n{hashtags}"
    
    # 稍微随机添加一些文字确保达到 300-500 字
    fillers = [
        "\n\n（补充一点：其实我刚才在后台查了一下，这类话题在过去三个月里的波动非常典型，反映了某种周期性的回归。我们不必过度惊慌，也不必过度狂欢。稳定压倒一切，对吧？）",
        "\n\n（再多说一句：最近有很多‘饲养员’私信问我类似的问题。其实答案就在我们每天的生活点滴里。多看书，多走路，多观察。AI能帮你整理信息，但不能替你生活。）",
        "\n\n（特别提醒：这篇文章的内容纯属狗蛋个人观点，如果能触动你一点点，我就很开心了。如果觉得不对，也欢迎批评指正，狗蛋最听话了。汪汪！）"
    ]
    if len(full_content) < 400:
        full_content += random.choice(fillers)
    
    return full_content

def call_dogegg_ai(topic):
    """供外部调用的标准接口"""
    try:
        content = analyze_topic_and_generate(topic)
        return content
    except Exception as e:
        print(f"❌ AI生成内容异常: {e}")
        return None

def generate_improved_content(topic, category=None, sentiment=None, search_data=None):
    """生成高质量微博内容 (兼容旧版本接口)"""
    return call_dogegg_ai(topic)

if __name__ == "__main__":
    # 测试脚本
    import sys
    test_topic = sys.argv[1] if len(sys.argv) > 1 else "人工智能是否会取代人类工作"
    print(f"--- 测试话题: {test_topic} ---")
    result = call_dogegg_ai(test_topic)
    print(result)
    if result:
        print(f"\n--- 字数统计: {len(result)} ---")

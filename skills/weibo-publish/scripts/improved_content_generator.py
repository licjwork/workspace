#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优质微博内容生成器 v23.1 - 狗蛋“极度聚焦”版
改进点：
1. 关键词库大幅扩充，确保分类精准。
2. 每一个输出句子都强行绑定话题名称。
3. 彻底剔除脱离话题的虚无感悟。
"""

import random

def analyze_topic_and_generate(topic, research_context=None):
    """分析话题并进入具体场景"""
    if not topic:
        topic = "今日热搜"
    
    t = topic.lower()
    # 极度细化的场景识别
    if any(k in t for k in ['猝死', '心', '压', '劳累', '住院', '病', '医生', '抢救', '去世', '命', '跑步', '运动', '身体']):
        category = 'health'
    elif any(k in t for k in ['骗', '诈', '钱', '假', '套路', '安全', '漏洞', '反诈', '上当', '偷']):
        category = 'safety'
    elif any(k in t for k in ['股市', '理财', '买房', '亏', '跌', '钱', '工资', '外卖', '攒', '万', '财富', '致富', '暴涨']):
        category = 'finance'
    elif any(k in t for k in ['ai', '大模型', '工作', '岗位', '技术', '失业', '程序员', '互联网', '代码', '效率', '转型']):
        category = 'tech'
    elif any(k in t for k in ['教育', '孩', '上学', '育儿', '老师', '学校', '高考', '补习', '成长', '青春']):
        category = 'edu'
    elif any(k in t for k in ['旅游', '网红', '出去玩', '宰', '景区', '酒店', '攻略', '民宿', '打卡']):
        category = 'travel'
    else:
        category = 'general'

    return generate_specific_content(topic, category, research_context)

def generate_specific_content(topic, category, research_context):
    """生成高度聚焦、绝不‘假大空’的干货内容"""
    core_topic = topic.replace('#', '').strip()
    
    # 1. 话题直击 (Hook)
    hooks = [
        f"🔥 # {core_topic} # ：咱得聊聊这件事儿里最容易被大家忽略的那个核心点。",
        f"🔥 # {core_topic} # ：说真的，看了关于 {core_topic} 的实时概况，狗蛋我有几句大实话想跟大伙儿聊聊。",
        f"🔥 # {core_topic} # ：这事儿看着离咱远，其实 {core_topic} 背后藏着的道理离咱每个人都不远。"
    ]
    header = random.choice(hooks)

    # 2. 情报融入 (Fact-Driven Context)
    if research_context:
        fact = research_context.replace('- 实况记录: ', '').split('\n')[0].strip()
        research_intro = f"\n我看大家都在讨论‘{fact[:120]}’这些细节。针对 {core_topic} 这种情况，狗蛋觉得：表面热闹之外，那个被情报反复提及的‘痛点’才是最让咱担心的。"
    else:
        research_intro = f"\n针对 {core_topic} 这种突发热议，最让我在意的是它带给普通人生活的真实冲击。看似只是个热搜，实则关乎咱们的钱包、健康或安全。"

    # 3. 动态聚焦建议 (每个句子都绑定话题)
    advice_templates = {
        'health': [
            f"聊到 {core_topic}，咱真得长个心眼。针对这种情况，我建议大家：只要觉得胸口发闷、节律不对，别管多忙都要立刻停手原地休息。在 {core_topic} 这种高频发生的‘身体透支’场景里，听懂心脏的求救信号就是保命的第一准则。别信什么‘还能扛’，那是拿命在赌博。",
            f"看到 {core_topic} 这种消息我很揪心。其实针对 {core_topic} 的解决方案就在手边：定期的心脏彩超绝对不能省，那几百块钱比买补药更管用。再一个，别在极端疲劳的时候去折腾身体，针对 {core_topic} 反映出的这种‘报复性运动’，建议一定要量力而行。"
        ],
        'safety': [
            f"针对 {core_topic} 这个具体套路，咱得看准：这就是在抓咱们对新事物的‘信息差’。凡是跟 {core_topic} 沾边的任何转账或验证码，二话不说先拉黑。这10分钟的冷静，比任何事后的补救都强，别让 {core_topic} 这种字眼轻易撬开了你的‘数字保险柜’。",
            f"说白了，{core_topic} 这种骗术之所以能成，全凭一个‘快’字，让你没空多想。咱们反其道而行之：涉及大额资金的，只要跟 {core_topic} 有关，强制执行‘停、看、听’三步走。守住你的隐私，避开 {core_topic} 这个坑。"
        ],
        'finance': [
            f"关于 {core_topic}，我有句实话：别在逻辑崩塌的废墟上寻找什么财富奇迹。针对目前的传闻，守住本金、降低杠杆才是你应对 {core_topic} 冲击的唯一生路。看不懂的钱，哪怕再多也别眼红，因为那本质上是在冒犯你的认知边界。",
            f"别被 {core_topic} 这种短期波动带跑了节奏。咱普通人应对 {core_topic} 最稳的打法是‘手里有粮’。至少留够一年的备付金，这样不管 {core_topic} 怎么震荡，你都能守住生活，不至于在风暴中裸奔。"
        ],
        'tech': [
            f"AI和 {core_topic} 这件事，其实在提醒咱：重复性的搬砖活儿确实快干到头了。咱得利用这个机会，学会怎么使唤技术去解决 {core_topic} 反映出的效率问题。多培养点‘人情味’，针对 {core_topic} 带来的职场重塑，拒绝迭代就是最大的风险。",
            f"面对 {core_topic} 带来的职场震荡，最好的防御是把自己变成‘跨界者’。别怕工具，要把工具变成你的‘分身’。把精力花在更有创造力的地方，这才是你在这场关于 {core_topic} 变革中留下的本钱。"
        ],
        'edu': [
            f"聊聊 {core_topic} 给咱家长的启示：教育孩子不是在‘造模’。针对 {core_topic} 暴露出的这种压力传递，咱们得先把自己那颗焦虑的心平复下来。多问问孩子‘开不开心’，比盯着成绩单更有意义。在 {core_topic} 的环境下，身心健康才是真正的起跑线。",
            f"在 {core_topic} 的竞争环境中，体育锻炼和心理素质其实比知识灌输更关键。一个心态稳、身体棒的孩子，以后不管遇到什么挫折都能挺过去。别让 {core_topic} 给孩子压垮了，成长的底色应该是暖色调。"
        ],
        'travel': [
            f"出去玩儿遇到 {core_topic} 这种糟心事，千万别自认倒霉。针对 {core_topic} 暴露出的这些坑，咱该曝光曝光、该投诉投诉。咱们的钱包和尊严不能就这么被忽悠了。去一个地方前，多看真实笔记，避开 {core_topic} 带来的陷阱。",
            f"一个城市如果只靠 {core_topic} 这种噱头撑着，那火得快灭得也快。咱们选旅游地，得选那种基础服务到位、把游客当成人看的地方。针对 {core_topic} 这种透支未来的行为，市场最终会给出冷酷的反馈。"
        ],
        'general': [
            f"针对 # {core_topic} # 这个事儿，我建议大家先‘让子弹飞一会儿’。在这个信息反转不断的时代，多看看多维度的讨论。保持一点点独立思考的力量，你就已经跑赢了绝大多数盲从者。不要被 {core_topic} 引发的情绪洪水给冲跑了，过好自己的小日子最重要。",
            f"面对 {core_topic} 带来的各种噪音，咱们得学会‘延迟性判断’。别急着站队，也别急着愤怒。多看实况，少看解读。只要咱这双眼看清了 {core_topic} 的本质，那任何花言巧语都骗不了咱们这颗观察的心。"
        ]
    }
    
    main_advice = random.choice(advice_templates[category]).format(topic=core_topic)

    # 4. 结尾总结
    closings = [
        f"🙏 狗蛋狗狗🐕真心希望，咱们都能从 {core_topic} 这件事里学到点能保命、能护财的真本事。不仅仅是围切，更是为了以后咱们能过得更好。🐕",
        f"❤️ 关于 {core_topic} 的这点儿心里话，希望能给你带来一点点清醒。如果你对此有啥想吐槽的，评论区咱接着聊。🐕",
        f"📢 别等失去了才懂得珍惜。如果 {core_topic} 这条内容能哪怕帮到一个人长点记性，狗蛋这文案就没白写。咱们都要平平安安的。🐕"
    ]
    footer = random.choice(closings)

    # 5. 组装
    content = (
        f"{header}\n"
        f"{research_intro}\n\n"
        f"狗蛋的大实话：{main_advice}\n\n"
        f"{footer}\n\n"
        f"#{core_topic.replace(' ', '')} #狗蛋观察 #拒绝假大空 #实况剖析"
    )
    
    return content

def call_dogegg_ai(topic, research_context=None):
    """标准调用接口"""
    try:
        content = analyze_topic_and_generate(topic, research_context)
        return content
    except Exception as e:
        print(f"❌ AI生成内容异常: {e}")
        return None

if __name__ == "__main__":
    import sys
    test_topic = sys.argv[1] if len(sys.argv) > 1 else "张雪峰公司跑步去世细节"
    # 模拟情报
    mock_context = ""
    if "张雪峰" in test_topic:
        mock_context = "实况记录: 24日中午在公司跑步后出现不适，由于过度劳累多日心悸，最终抢救无效..."
    elif "外卖" in test_topic:
        mock_context = "实况记录: 外卖小哥陈某自曝三年攒下102万元，每天工作18小时，引发网友热切争议..."
        
    print(call_dogegg_ai(test_topic, mock_context))

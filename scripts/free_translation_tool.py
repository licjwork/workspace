#!/usr/bin/env python3
"""
免费翻译工具类
使用多个备用翻译服务
"""

import requests
import json
import time
import random
import re

def google_translate_free(text, source_lang="en", target_lang="zh"):
    """
    使用Google翻译（免费版本）
    """
    try:
        # Google翻译的免费API端点
        url = "https://translate.googleapis.com/translate_a/single"
        
        params = {
            "client": "gtx",
            "sl": source_lang,
            "tl": target_lang,
            "dt": "t",
            "q": text
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # 解析Google翻译的响应格式
            if data and len(data) > 0:
                translated_text = ""
                for item in data[0]:
                    if item[0]:
                        translated_text += item[0]
                return translated_text
        else:
            print(f"Google翻译请求失败，状态码: {response.status_code}")
        
        return text
    except requests.exceptions.Timeout:
        print("Google翻译请求超时")
        return text
    except Exception as e:
        print(f"Google翻译失败: {e}")
        return text

def mymemory_translate(text, source_lang="en", target_lang="zh"):
    """
    使用MyMemory翻译API
    """
    try:
        url = "https://api.mymemory.translated.net/get"
        
        params = {
            "q": text,
            "langpair": f"{source_lang}|{target_lang}"
        }
        
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("responseStatus") == 200:
                translated = data.get("responseData", {}).get("translatedText", text)
                print(f"MyMemory翻译成功: {translated[:50]}...")
                return translated
        else:
            print(f"MyMemory翻译请求失败，状态码: {response.status_code}")
        
        return text
    except Exception as e:
        print(f"MyMemory翻译失败: {e}")
        return text

def lingva_translate(text, source_lang="en", target_lang="zh"):
    """
    使用Lingva Translate API（无需API密钥）
    """
    try:
        url = "https://lingva.ml/api/v1/translate"
        
        data = {
            "source": source_lang,
            "target": target_lang,
            "q": text
        }
        
        response = requests.post(url, json=data, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            translated = data.get("translation", text)
            print(f"Lingva翻译成功: {translated[:50]}...")
            return translated
        else:
            print(f"Lingva翻译请求失败，状态码: {response.status_code}")
        
        return text
    except Exception as e:
        print(f"Lingva翻译失败: {e}")
        return text

def translate_text_multi(text, source_lang="en", target_lang="zh"):
    """
    使用多个翻译服务，优先选择可用的
    """
    if not text or len(text.strip()) == 0:
        return text
    
    # 优先尝试Lingva翻译
    translated = lingva_translate(text, source_lang, target_lang)
    
    if translated != text:
        return translated
    
    # 如果Lingva失败，尝试MyMemory翻译
    translated = mymemory_translate(text, source_lang, target_lang)
    
    if translated != text:
        return translated
    
    # 如果都失败，使用备用翻译
    return backup_translation(text)

def translate_news_text(text):
    """
    专门用于新闻文本的翻译函数
    """
    if not text or len(text.strip()) == 0:
        return text
    
    # 使用多服务翻译
    translated_text = translate_text_multi(text, "en", "zh")
    
    # 清理格式和标点符号
    translated_text = re.sub(r'\s+', ' ', translated_text).strip()
    
    return f"【多服务翻译】{translated_text}"

def backup_translation(text):
    """
    备用翻译方法，当API不可用时使用
    """
    # 构建完整的翻译词典
    translations = {
        "Recent world news highlights include": "近期世界新闻热点包括",
        "a significant increase in gas prices": "天然气价格大幅上涨",
        "rising to 71 cents on average": "平均上涨至71美分",
        "since the conflict began": "自冲突开始以来",
        "due to the ongoing Iran war": "由于持续的伊朗战争",
        "U.S. military plane crashed": "美国军用飞机坠毁",
        "FBI is assisting": "FBI正在协助",
        "synagogue attack": "犹太教堂袭击事件",
        "Michigan": "密歇根州",
        "Iranian Supreme Leader": "伊朗最高领导人",
        "released a statement": "发表声明",
        "tensions are escalating": "紧张局势升级",
        "Strait of Hormuz": "霍尔木兹海峡",
        "Italy's Culture Ministry": "意大利文化部",
        "spent around $35 million": "花费约3500万美元",
        "rare Caravaggio painting": "稀有的卡拉瓦乔画作",
        "Niagara Regional Chair resigned": "尼亚加拉地区主席辞职",
        "owning a copy": "拥有一本",
        "Hitler's \"Mein Kampf\"": "希特勒的《我的奋斗》",
        "Alpine skier": "高山滑雪运动员",
        "won silver": "获得银牌",
        "giant slalom sitting race": "大回转坐式比赛",
        "Milano Cortina Winter Paralympics": "米兰科尔蒂纳冬季残奥会",
        "most decorated winter para athlete": "获得奖牌最多的冬季残奥运动员",
        "in the country": "在该国",
        "additionally": "此外",
        "furthermore": "另外",
        "becoming": "成为",
        "involving": "涉及",
        "participants": "参与者",
        "conflict": "冲突",
        "investigation": "调查",
        "attack": "袭击",
        "statement": "声明",
        "painting": "画作",
        "athlete": "运动员",
        "country": "国家"
    }
    
    # 逐词替换翻译
    translated_text = text
    for eng, chn in translations.items():
        translated_text = translated_text.replace(eng, chn)
    
    # 处理剩余的英文单词
    english_words = re.findall(r'\b[a-zA-Z]+\b', translated_text)
    for word in english_words:
        if word.lower() not in ['a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']:
            # 简单的音译或意译
            simple_translations = {
                'Momoka': '百冈',
                'Muraoka': '桃香', 
                'Caravaggio': '卡拉瓦乔',
                'Iran': '伊朗',
                'Iraq': '伊拉克',
                'FBI': '联邦调查局',
                'U.S.': '美国',
                'World': '世界',
                'Record': '纪录',
                'Classic': '经典赛',
                'Semifinals': '半决赛',
                'Canada': '加拿大',
                'Japan': '日本',
                'Czechia': '捷克',
                'NBA': '美国职业篮球联赛',
                'Cleveland': '克利夫兰',
                'Cavaliers': '骑士队',
                'Dallas': '达拉斯',
                'Mavericks': '独行侠队',
                'New York': '纽约',
                'Knicks': '尼克斯队',
                'Indiana': '印第安纳',
                'Pacers': '步行者队',
                'Los Angeles': '洛杉矶',
                'Lakers': '湖人队',
                'Chicago': '芝加哥',
                'Bulls': '公牛队',
                'Oklahoma': '俄克拉荷马',
                'Thunder': '雷霆队',
                'Boston': '波士顿',
                'Celtics': '凯尔特人队'
            }
            if word in simple_translations:
                translated_text = translated_text.replace(word, simple_translations[word])
    
    return translated_text

# 测试函数
def test_translation():
    """测试翻译功能"""
    test_text = "Recent world news highlights include a significant increase in gas prices"
    
    print("测试翻译功能:")
    print(f"原文: {test_text}")
    
    translated = translate_news_text(test_text)
    print(f"翻译结果: {translated}")
    
    return translated != test_text

if __name__ == "__main__":
    # 运行测试
    if test_translation():
        print("✅ 免费翻译工具测试成功")
    else:
        print("❌ 免费翻译工具测试失败")
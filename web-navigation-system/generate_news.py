#!/usr/bin/env python3
"""
Generate international news data for the navigation system
Follows the heartbeat.md instructions for the定时任务阶段
"""

import json
import subprocess
import sys
import os
from datetime import datetime

def search_news_with_tavily():
    """Use Tavily API to search for latest international news"""
    api_key = "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"
    script_path = "/home/ubuntu/.openclaw/workspace/skills/tavily/scripts/tavily_search.py"
    
    try:
        # Execute Tavily search for international news
        result = subprocess.run([
            sys.executable, script_path,
            "国际最新新闻",
            "--api-key", api_key,
            "--topic", "news",
            "--max-results", "10",
            "--json"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"Tavily search failed: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"Error running Tavily search: {e}")
        return None

def parse_news_with_ai(tavily_results):
    """Use LongCat AI to parse and translate news results"""
    parser_script = "/home/ubuntu/.openclaw/workspace/web-navigation-system/improved_news_parser.py"
    
    try:
        # Prepare the input for the parser
        input_data = json.dumps(tavily_results, ensure_ascii=False)
        
        # Execute the AI parser
        result = subprocess.run([
            sys.executable, parser_script
        ], input=input_data, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"AI parsing failed: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"Error running AI parser: {e}")
        return None

def generate_news_json():
    """Main function to generate news.json following heartbeat instructions"""
    print(f"[{datetime.now()}] Starting news generation process...")
    
    # Step 1: Search with Tavily
    print("Step 1: Searching for international news with Tavily...")
    tavily_results = search_news_with_tavily()
    if not tavily_results:
        print("Failed to get Tavily results")
        return False
    
    print(f"Got {len(tavily_results.get('results', []))} results from Tavily")
    
    # Step 2: Parse with AI
    print("Step 2: Parsing and translating with LongCat AI...")
    parsed_news = parse_news_with_ai(tavily_results)
    if not parsed_news:
        print("Failed to parse news with AI")
        return False
    
    # Step 3: Generate news.json
    print("Step 3: Generating news.json...")
    
    news_data = {
        "timestamp": datetime.now().isoformat(),
        "news_count": len(parsed_news.get('news_list', [])),
        "news_list": parsed_news.get('news_list', [])
    }
    
    output_path = "/home/ubuntu/.openclaw/workspace/web-navigation-system/news.json"
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)
        
        print(f"Successfully generated news.json with {news_data['news_count']} news items")
        return True
        
    except Exception as e:
        print(f"Error writing news.json: {e}")
        return False

if __name__ == "__main__":
    success = generate_news_json()
    sys.exit(0 if success else 1)
#!/usr/bin/env python3
import sys
import os
import json

def read_file_safely(file_path):
    """安全读取文件内容"""
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return {"error": f"文件不存在: {file_path}"}
        
        # 检查文件权限
        if not os.access(file_path, os.R_OK):
            return {"error": f"文件无读取权限: {file_path}"}
        
        # 检查文件大小（避免读取过大的文件）
        file_size = os.path.getsize(file_path)
        if file_size > 1024 * 1024:  # 1MB
            return {"error": f"文件过大: {file_size} bytes"}
        
        # 尝试不同的编码方式
        encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                    return {
                        "success": True,
                        "content": content,
                        "encoding": encoding,
                        "size": len(content)
                    }
            except UnicodeDecodeError:
                continue
        
        return {"error": "无法解码文件，尝试了多种编码方式"}
    
    except Exception as e:
        return {"error": f"读取文件时发生错误: {str(e)}"}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python3 reliable_file_reader.py <文件路径>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    result = read_file_safely(file_path)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

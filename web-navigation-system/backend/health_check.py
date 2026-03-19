#!/usr/bin/env python3
import requests
import json
import time

def send_feishu_alert(message):
    """发送飞书告警消息"""
    try:
        # 这里需要配置飞书webhook地址
        # webhook_url = "你的飞书webhook地址"
        # response = requests.post(webhook_url, json={"msg_type": "text", "content": {"text": message}})
        print(f"飞书告警消息（待配置）: {message}")
    except Exception as e:
        print(f"发送飞书告警失败: {e}")

def check_all_sites_health():
    """检查所有网站的健康状态"""
    try:
        # 获取管理员会话令牌
        login_response = requests.post(
            'http://localhost:5000/api/auth/login',
            json={'username': 'admin', 'password': 'admin123'}
        )
        
        if login_response.status_code != 200:
            print(f"登录失败: {login_response.text}")
            return
        
        session_token = login_response.json().get('session_token')
        
        # 批量检测所有网站
        health_response = requests.post(
            'http://localhost:5000/api/sites/health/check-all',
            headers={'X-Session-Token': session_token}
        )
        
        if health_response.status_code == 200:
            data = health_response.json()
            results = data['results']
            unhealthy_count = data.get('unhealthy_count', 0)
            
            print(f"成功检测 {len(results)} 个网站的健康状态")
            
            # 统计结果
            status_counts = {}
            for result in results:
                status = result['health_status']
                status_counts[status] = status_counts.get(status, 0) + 1
            
            print("健康状态统计:")
            for status, count in status_counts.items():
                print(f"  {status}: {count} 个网站")
            
            # 如果有异常网站，发送告警
            if unhealthy_count > 0:
                alert_message = f"🚨 网站健康检测告警\n检测到 {unhealthy_count} 个网站异常\n请及时检查相关网站。"
                send_feishu_alert(alert_message)
                print(f"已发送 {unhealthy_count} 个网站异常告警")
                
        else:
            print(f"健康检测失败: {health_response.text}")
            
    except Exception as e:
        print(f"检测过程中出错: {e}")

if __name__ == "__main__":
    print(f"开始网站健康检测 - {time.strftime('%Y-%m-%d %H:%M:%S')}")
    check_all_sites_health()
    print(f"检测完成 - {time.strftime('%Y-%m-%d %H:%M:%S')}")

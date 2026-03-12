#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
author: guiying li
date: 2026-03-11
功能：从配置文件(config.json)和环境变量(.env)中读取配置信息
"""

import os
import json
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# 获取当前脚本所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, 'config.json')

def load_json_config():
    """
    从config.json加载配置
    
    Returns:
        dict: 配置字典
    """
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"警告: 配置文件 {CONFIG_FILE} 不存在")
        return {}
    except json.JSONDecodeError as e:
        print(f"错误: 配置文件格式错误 - {e}")
        return {}

# 加载JSON配置
json_config = load_json_config()

# OBS配置信息 - 从环境变量读取敏感信息，从JSON读取非敏感配置
OBS_CONFIG = {
    # OBS云端配置 - 敏感信息从环境变量读取
    'ak': os.getenv('OBS_AK', ''),
    'sk': os.getenv('OBS_SK', ''),
    'server': json_config.get('obs', {}).get('server', 'obs.cn-east-3.myhuaweicloud.com'),
    'bucket_name': json_config.get('obs', {}).get('bucket_name', ''),
    'obs_prefix': json_config.get('obs', {}).get('obs_prefix', 'videos'),
    
    # 本地文件配置
    'local_parent_dir': json_config.get('local', {}).get('parent_dir', os.path.expanduser('~/Downloads/深汕原始数据')),
    
    # 定时任务配置
    'upload_interval': json_config.get('schedule', {}).get('interval', 3600),
    'enable_schedule': json_config.get('schedule', {}).get('enable', True),
    
    # 上传配置
    'max_file_count': json_config.get('upload', {}).get('max_file_count', 0),
    'upload_timeout': json_config.get('upload', {}).get('timeout', 300),
    
    # 日志配置
    'log_level': json_config.get('log', {}).get('level', 'INFO'),
    'log_dir': json_config.get('log', {}).get('dir', 'logs'),
    
    # 视频文件配置
    'video_extensions': json_config.get('video', {}).get('extensions', ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv']),
}

# 验证配置是否完整
def validate_config():
    """
    验证配置是否完整
    
    Returns:
        bool: 配置是否完整
    """
    required_fields = ['ak', 'sk', 'bucket_name']
    for field in required_fields:
        if not OBS_CONFIG.get(field):
            print(f"错误：缺少必要配置项 {field}")
            return False
    return True

def get_config_summary():
    """
    获取配置摘要信息
    
    Returns:
        str: 配置摘要信息
    """
    summary = []
    summary.append("=" * 50)
    summary.append("OBS配置信息")
    summary.append("=" * 50)
    summary.append(f"OBS服务器: {OBS_CONFIG['server']}")
    summary.append(f"存储桶名称: {OBS_CONFIG['bucket_name']}")
    summary.append(f"OBS前缀: {OBS_CONFIG['obs_prefix']}")
    summary.append("-" * 50)
    summary.append(f"本地目录: {OBS_CONFIG['local_parent_dir']}")
    summary.append("-" * 50)
    summary.append(f"定时任务: {'启用' if OBS_CONFIG['enable_schedule'] else '禁用'}")
    summary.append(f"上传间隔: {OBS_CONFIG['upload_interval']} 秒 ({OBS_CONFIG['upload_interval']/60:.1f} 分钟)")
    summary.append(f"每次最大上传: {'不限制' if OBS_CONFIG['max_file_count'] == 0 else OBS_CONFIG['max_file_count']} 个文件")
    summary.append(f"上传超时: {OBS_CONFIG['upload_timeout']} 秒")
    summary.append("-" * 50)
    summary.append(f"日志级别: {OBS_CONFIG['log_level']}")
    summary.append(f"日志目录: {OBS_CONFIG['log_dir']}")
    summary.append("-" * 50)
    summary.append(f"支持的视频格式: {', '.join(OBS_CONFIG['video_extensions'])}")
    summary.append("=" * 50)
    return "\n".join(summary)

if __name__ == '__main__':
    print(get_config_summary())
    print(f"\n配置验证: {'通过' if validate_config() else '失败'}")

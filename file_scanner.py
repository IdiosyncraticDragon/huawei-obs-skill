#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地文件扫描模块
author: guiying li
date: 2026-03-11
功能：扫描本地摄像头文件夹中的视频文件
"""

import os
import logging
from config import OBS_CONFIG
from logger import logger

# 支持的视频文件扩展名
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv']

def is_video_file(filename):
    """
    判断是否为视频文件
    
    Args:
        filename: 文件名
    
    Returns:
        bool: 是否为视频文件
    """
    ext = os.path.splitext(filename)[1].lower()
    return ext in VIDEO_EXTENSIONS

def scan_camera_folders(parent_dir):
    """
    扫描父目录下的摄像头文件夹
    
    Args:
        parent_dir: 父目录路径
    
    Returns:
        list: 摄像头文件夹列表
    """
    camera_folders = []
    
    # 解析波浪号路径
    parent_dir = os.path.expanduser(parent_dir)
    
    if not os.path.exists(parent_dir):
        logger.error(f"父目录不存在: {parent_dir}")
        return camera_folders
    
    try:
        items = os.listdir(parent_dir)
        logger.info(f"开始扫描父目录: {parent_dir}，共发现 {len(items)} 个项目")
        
        for item in items:
            item_path = os.path.join(parent_dir, item)
            if os.path.isdir(item_path):
                camera_folders.append(item)
                logger.info(f"发现摄像头文件夹: {item}")
        
        logger.info(f"扫描完成，发现 {len(camera_folders)} 个摄像头文件夹")
    except Exception as e:
        logger.error(f"扫描摄像头文件夹失败: {e}")
    
    return camera_folders

def scan_video_files(camera_folder):
    """
    扫描摄像头文件夹中的视频文件
    
    Args:
        camera_folder: 摄像头文件夹路径
    
    Returns:
        list: 视频文件路径列表
    """
    video_files = []
    
    try:
        for item in os.listdir(camera_folder):
            item_path = os.path.join(camera_folder, item)
            if os.path.isfile(item_path) and is_video_file(item):
                video_files.append(item_path)
    except Exception as e:
        logger.error(f"扫描视频文件失败: {e}")
    
    return video_files

def get_file_info(local_file, camera_name):
    """
    获取文件信息，包括本地路径和OBS路径
    
    Args:
        local_file: 本地文件路径
        camera_name: 摄像头名称
    
    Returns:
        dict: 文件信息字典
    """
    filename = os.path.basename(local_file)
    obs_key = os.path.join(OBS_CONFIG['obs_prefix'], camera_name, filename).replace('\\', '/')
    
    return {
        'local_path': local_file,
        'obs_key': obs_key,
        'camera_name': camera_name
    }

def scan_all_videos(parent_dir=None):
    """
    扫描所有摄像头文件夹中的视频文件
    
    Args:
        parent_dir: 父目录路径，默认使用配置中的路径
    
    Returns:
        list: 所有视频文件信息列表
    """
    if parent_dir is None:
        parent_dir = OBS_CONFIG['local_parent_dir']
    
    # 解析波浪号路径
    parent_dir = os.path.expanduser(parent_dir)
    camera_folders = scan_camera_folders(parent_dir)
    
    all_videos = []
    camera_file_counts = {}
    
    for camera_name in camera_folders:
        camera_path = os.path.join(parent_dir, camera_name)
        video_files = scan_video_files(camera_path)
        camera_file_counts[camera_name] = len(video_files)
        
        for video_file in video_files:
            file_info = get_file_info(video_file, camera_name)
            all_videos.append(file_info)
    
    logger.info(f"扫描完成，共发现 {len(all_videos)} 个视频文件")
    for camera, count in camera_file_counts.items():
        logger.info(f"  - {camera}: {count} 个视频文件")
    
    return all_videos

if __name__ == '__main__':
    videos = scan_all_videos()
    print(f"\n扫描结果: 发现 {len(videos)} 个视频文件")
    for video in videos:
        print(f"本地路径: {video['local_path']}")
        print(f"OBS路径: {video['obs_key']}")
        print(f"摄像头: {video['camera_name']}")
        print("-" * 30)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志模块
author: guiying li
date: 2026-03-12
功能：提供日志落盘功能，记录所有上传操作
"""

import os
import logging
from datetime import datetime

# 创建logs目录
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 日志文件路径
LOG_FILE = os.path.join(LOG_DIR, f'upload_{datetime.now().strftime("%Y%m%d")}.log')

# 配置日志格式
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def get_logger(name='video_uploader'):
    """
    获取日志记录器
    
    Args:
        name: 日志记录器名称
    
    Returns:
        logging.Logger: 日志记录器实例
    """
    logger = logging.getLogger(name)
    
    # 避免重复添加handler
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.INFO)
    
    # 文件处理器 - 记录所有日志
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    
    # 控制台处理器 - 记录INFO及以上级别
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# 创建全局日志记录器
logger = get_logger()

def log_upload_success(local_file, obs_key, file_size):
    """
    记录上传成功日志
    
    Args:
        local_file: 本地文件路径
        obs_key: OBS中的文件路径
        file_size: 文件大小（字节）
    """
    logger.info(f"上传成功 | 本地文件: {local_file} | OBS路径: {obs_key} | 文件大小: {file_size} 字节")

def log_upload_failed(local_file, obs_key, error_msg):
    """
    记录上传失败日志
    
    Args:
        local_file: 本地文件路径
        obs_key: OBS中的文件路径
        error_msg: 错误信息
    """
    logger.error(f"上传失败 | 本地文件: {local_file} | OBS路径: {obs_key} | 错误: {error_msg}")

def log_delete_success(local_file):
    """
    记录删除本地文件成功日志
    
    Args:
        local_file: 本地文件路径
    """
    logger.info(f"删除本地文件成功: {local_file}")

def log_delete_failed(local_file, error_msg):
    """
    记录删除本地文件失败日志
    
    Args:
        local_file: 本地文件路径
        error_msg: 错误信息
    """
    logger.error(f"删除本地文件失败: {local_file} | 错误: {error_msg}")

def log_scan_result(camera_count, file_count):
    """
    记录扫描结果
    
    Args:
        camera_count: 摄像头数量
        file_count: 文件数量
    """
    logger.info(f"扫描完成 | 摄像头数量: {camera_count} | 视频文件数量: {file_count}")

def log_upload_summary(total_files, success_count, failed_count, deleted_count):
    """
    记录上传摘要
    
    Args:
        total_files: 总文件数
        success_count: 成功上传数
        failed_count: 上传失败数
        deleted_count: 删除本地文件数
    """
    logger.info(f"========== 上传摘要 ==========")
    logger.info(f"总文件数: {total_files}")
    logger.info(f"成功上传: {success_count}")
    logger.info(f"上传失败: {failed_count}")
    logger.info(f"删除本地文件: {deleted_count}")
    logger.info(f"==============================")

if __name__ == '__main__':
    # 测试日志功能
    logger.info("测试日志功能")
    log_upload_success("/test/video.mp4", "videos/camera1/video.mp4", 1024000)
    log_upload_failed("/test/video2.mp4", "videos/camera1/video2.mp4", "网络错误")
    log_delete_success("/test/video.mp4")
    log_scan_result(4, 100)
    log_upload_summary(100, 95, 5, 95)
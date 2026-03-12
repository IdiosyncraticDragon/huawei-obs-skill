#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OBS上传模块
author: guiying li
date: 2026-03-11
功能：将本地视频文件上传到华为云OBS并删除本地文件
"""

import os
import sys
import time
from config import OBS_CONFIG, validate_config
from file_scanner import scan_all_videos
from logger import logger, log_upload_success, log_upload_failed, log_delete_success, log_delete_failed, log_scan_result, log_upload_summary

try:
    from obs import ObsClient
except ImportError:
    logger.error("未安装华为云OBS SDK，请运行: pip install huaweicloud-sdk-python-obs")
    exit(1)

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    logger.warning("未安装tqdm库，将不显示进度条，请运行: pip install tqdm")

def get_obs_client():
    """
    获取OBS客户端实例
    
    Returns:
        ObsClient实例或None
    """
    try:
        client = ObsClient(
            access_key_id=OBS_CONFIG['ak'],
            secret_access_key=OBS_CONFIG['sk'],
            server=OBS_CONFIG['server']
        )
        logger.info("OBS客户端初始化成功")
        return client
    except Exception as e:
        logger.error(f"OBS客户端初始化失败: {e}")
        return None

def upload_file(obs_client, local_file, obs_key):
    """
    上传文件到OBS
    
    Args:
        obs_client: ObsClient实例
        local_file: 本地文件路径
        obs_key: OBS中的文件路径
    
    Returns:
        bool: 上传是否成功
    """
    try:
        logger.info(f"开始上传文件: {local_file} -> {obs_key}")
        response = obs_client.putFile(OBS_CONFIG['bucket_name'], obs_key, local_file)
        if response.status < 300:
            file_size = os.path.getsize(local_file)
            log_upload_success(local_file, obs_key, file_size)
            logger.info(f"文件上传成功: {obs_key}")
            return True
        else:
            log_upload_failed(local_file, obs_key, response.errorMessage)
            logger.error(f"文件上传失败: {response.errorMessage}")
            return False
    except Exception as e:
        log_upload_failed(local_file, obs_key, str(e))
        logger.error(f"上传文件异常: {e}")
        return False

def delete_local_file(local_file):
    """
    删除本地文件
    
    Args:
        local_file: 本地文件路径
    
    Returns:
        bool: 删除是否成功
    """
    try:
        if os.path.exists(local_file):
            os.remove(local_file)
            log_delete_success(local_file)
            logger.info(f"本地文件已删除: {local_file}")
            return True
        else:
            logger.warning(f"本地文件不存在: {local_file}")
            return False
    except Exception as e:
        log_delete_failed(local_file, str(e))
        logger.error(f"删除本地文件失败: {e}")
        return False

def get_file_size(local_file):
    """
    获取文件大小（人类可读格式）
    
    Args:
        local_file: 本地文件路径
    
    Returns:
        str: 文件大小字符串
    """
    try:
        size = os.path.getsize(local_file)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"
    except:
        return "未知"

def upload_videos():
    """
    上传所有视频文件
    
    Returns:
        dict: 上传结果统计
    """
    start_time = time.time()
    logger.info("=" * 50)
    logger.info("开始执行视频上传任务")
    logger.info("=" * 50)
    
    if not validate_config():
        logger.error("配置验证失败，无法上传文件")
        return {'total': 0, 'success': 0, 'failed': 0, 'deleted': 0}
    
    obs_client = get_obs_client()
    if not obs_client:
        logger.error("无法获取OBS客户端，无法上传文件")
        return {'total': 0, 'success': 0, 'failed': 0, 'deleted': 0}
    
    videos = scan_all_videos()
    total_files = len(videos)
    
    if not videos:
        logger.info("没有发现视频文件")
        log_scan_result(len(set(v.get('camera_name', '') for v in videos)), 0)
        return {'total': 0, 'success': 0, 'failed': 0, 'deleted': 0}
    
    cameras = set(v.get('camera_name', '') for v in videos)
    log_scan_result(len(cameras), total_files)
    
    success_count = 0
    fail_count = 0
    deleted_count = 0
    
    logger.info(f"共发现 {total_files} 个视频文件，来自 {len(cameras)} 个摄像头")
    logger.info(f"摄像头列表: {', '.join(cameras)}")
    logger.info("=" * 50)
    
    if HAS_TQDM:
        pbar = tqdm(total=total_files, desc="上传进度", unit="文件", 
                    bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]')
    
    for video in videos:
        local_file = video['local_path']
        obs_key = video['obs_key']
        camera_name = video['camera_name']
        file_size = get_file_size(local_file)
        
        if HAS_TQDM:
            pbar.set_description(f"正在上传: {camera_name[:15]}...")
        
        if upload_file(obs_client, local_file, obs_key):
            success_count += 1
            if delete_local_file(local_file):
                deleted_count += 1
        else:
            fail_count += 1
        
        if HAS_TQDM:
            pbar.update(1)
            pbar.set_postfix({'成功': success_count, '失败': fail_count, '已删除': deleted_count})
    
    if HAS_TQDM:
        pbar.close()
    
    try:
        obs_client.close()
        logger.info("OBS客户端已关闭")
    except Exception as e:
        logger.error(f"关闭OBS客户端失败: {e}")
    
    end_time = time.time()
    duration = end_time - start_time
    
    logger.info("=" * 50)
    logger.info(f"上传任务完成！")
    logger.info(f"总文件数: {total_files}")
    logger.info(f"成功上传: {success_count}")
    logger.info(f"上传失败: {fail_count}")
    logger.info(f"删除本地文件: {deleted_count}")
    logger.info(f"总耗时: {duration:.2f} 秒")
    if success_count > 0:
        logger.info(f"平均速度: {success_count / duration:.2f} 文件/秒")
    logger.info("=" * 50)
    
    log_upload_summary(total_files, success_count, fail_count, deleted_count)
    
    return {
        'total': total_files,
        'success': success_count,
        'failed': fail_count,
        'deleted': deleted_count,
        'duration': duration
    }

if __name__ == '__main__':
    result = upload_videos()
    print(f"\n上传结果:")
    print(f"  总文件数: {result['total']}")
    print(f"  成功上传: {result['success']}")
    print(f"  上传失败: {result['failed']}")
    print(f"  删除本地文件: {result['deleted']}")
    if result.get('duration'):
        print(f"  总耗时: {result['duration']:.2f} 秒")

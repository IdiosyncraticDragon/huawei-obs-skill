#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主脚本
author: guiying li
date: 2026-03-11
功能：启动视频上传到OBS的定时任务
"""

from config import validate_config
from scheduler import UploadScheduler
from logger import logger

def main():
    """
    主函数
    """
    logger.info("=" * 50)
    logger.info("启动视频OBS上传服务")
    logger.info("=" * 50)
    
    if not validate_config():
        logger.error("配置验证失败，服务无法启动")
        return
    
    scheduler = UploadScheduler()
    scheduler.start()
    
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("收到中断信号，正在停止服务...")
        scheduler.stop()
    except Exception as e:
        logger.error(f"服务运行异常: {e}")
        scheduler.stop()

if __name__ == '__main__':
    main()

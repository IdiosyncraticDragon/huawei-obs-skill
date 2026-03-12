---
name: huawei-obs-uploader
description: 华为云 OBS 视频文件自动上传工具。支持定时扫描本地摄像头视频文件，自动上传到华为云 OBS 存储，并删除本地文件。
---

# 华为云 OBS 视频上传 Skill

这是一个华为云 OBS 视频自动上传工具，适用于摄像头视频文件的自动备份场景。

## 功能特性

- 📁 **自动扫描**：定时扫描本地摄像头文件夹中的视频文件
- ☁️ **自动上传**：将视频文件上传到华为云 OBS 对象存储
- 🗑️ **自动清理**：上传成功后自动删除本地文件，节省存储空间
- 📊 **详细日志**：记录所有上传操作和结果，支持问题排查
- ⏰ **定时任务**：支持配置定时上传间隔，无需人工干预
- 🔒 **安全配置**：敏感信息通过环境变量配置，避免泄露

## 适用场景

- 安防摄像头视频自动备份
- 监控视频云端存储
- 本地视频文件自动归档
- 多摄像头视频集中管理

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置文件

复制配置示例：
```bash
cp config.json.example config.json
cp .env.example .env
```

编辑 `.env` 文件，配置华为云 OBS 密钥：
```env
OBS_AK=你的华为云AK
OBS_SK=你的华为云SK
```

编辑 `config.json` 文件，配置 OBS 和本地路径：
```json
{
  "obs": {
    "server": "obs.cn-east-3.myhuaweicloud.com",
    "bucket_name": "你的存储桶名称",
    "obs_prefix": "videos"
  },
  "local": {
    "parent_dir": "~/Videos/cameras"
  },
  "schedule": {
    "enable": true,
    "interval": 3600
  }
}
```

### 3. 运行程序

```bash
# 单次执行上传
python main.py

# 查看配置信息
python config.py
```

## 配置说明

### OBS 配置

| 参数 | 说明 | 默认值 |
|------|------|--------|
| ak | 华为云访问密钥 AK | 从环境变量读取 |
| sk | 华为云访问密钥 SK | 从环境变量读取 |
| server | OBS 服务端点 | obs.cn-east-3.myhuaweicloud.com |
| bucket_name | OBS 存储桶名称 | 必填 |
| obs_prefix | OBS 中文件存储的前缀目录 | videos |

### 本地配置

| 参数 | 说明 | 默认值 |
|------|------|--------|
| local_parent_dir | 本地视频文件根目录 | ~/Downloads/深汕原始数据 |

### 定时任务配置

| 参数 | 说明 | 默认值 |
|------|------|--------|
| enable_schedule | 是否启用定时任务 | true |
| upload_interval | 上传间隔（秒） | 3600（1小时） |

### 支持的视频格式

默认支持：`.mp4`, `.avi`, `.mov`, `.wmv`, `.flv`, `.mkv`

## 目录结构

```
huawei-obs-skill/
├── SKILL.md              # 技能说明文档
├── main.py               # 程序入口
├── uploader.py           # OBS 上传核心模块
├── config.py             # 配置管理模块
├── file_scanner.py       # 文件扫描模块
├── logger.py             # 日志模块
├── requirements.txt      # 依赖列表
├── config.json.example   # 配置文件示例
└── .env.example          # 环境变量示例
```

## 依赖项

```
huaweicloud-sdk-python-obs >= 3.22.12
python-dotenv >= 1.0.0
tqdm >= 4.66.0
```

## 作者

Guiying Li

## 许可证

MIT

# 华为云 OBS 视频自动上传工具

一个功能完整的华为云 OBS 视频文件自动上传工具，支持定时扫描、自动上传、本地文件清理等功能。

## ✨ 功能特性

- **自动扫描**：自动识别指定目录下的所有摄像头文件夹和视频文件
- **断点续传**：稳定的 OBS 上传能力，支持大文件上传
- **自动清理**：上传成功后自动删除本地文件，节省存储空间
- **定时任务**：可配置的定时上传间隔，无人值守自动运行
- **进度显示**：支持 tqdm 进度条，实时查看上传进度
- **详细日志**：完整的操作日志记录，便于问题排查
- **安全配置**：敏感信息通过环境变量管理，避免配置泄露

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置

1. 复制配置文件模板：
```bash
cp config.json.example config.json
cp .env.example .env
```

2. 编辑 `.env` 文件，填入你的华为云 AK/SK：
```env
OBS_AK=your_access_key
OBS_SK=your_secret_key
```

3. 编辑 `config.json`，配置存储桶和本地路径：
```json
{
  "obs": {
    "server": "obs.cn-east-3.myhuaweicloud.com",
    "bucket_name": "your-bucket-name",
    "obs_prefix": "videos"
  },
  "local": {
    "parent_dir": "~/Videos/cameras"
  }
}
```

### 运行

```bash
# 单次执行上传任务
python main.py

# 查看配置信息
python config.py

# 仅扫描文件不上传
python file_scanner.py
```

## 📁 目录结构说明

程序会自动扫描 `local_parent_dir` 下的子目录作为摄像头文件夹，例如：

```
~/Videos/cameras/
├── camera-001/       # 摄像头1的文件夹
│   ├── video1.mp4
│   └── video2.mp4
├── camera-002/       # 摄像头2的文件夹
│   ├── video1.mp4
│   └── video2.mp4
└── camera-003/       # 摄像头3的文件夹
    ├── video1.mp4
    └── video2.mp4
```

上传到 OBS 后的路径结构：
```
bucket/
└── videos/
    ├── camera-001/
    │   ├── video1.mp4
    │   └── video2.mp4
    ├── camera-002/
    │   ├── video1.mp4
    │   └── video2.mp4
    └── camera-003/
        ├── video1.mp4
        └── video2.mp4
```

## ⚙️ 配置详解

### OBS 配置

| 参数 | 说明 |
|------|------|
| server | OBS 服务区域端点，例如：<br>- 北京：obs.cn-north-4.myhuaweicloud.com<br>- 上海：obs.cn-east-3.myhuaweicloud.com<br>- 广州：obs.cn-south-1.myhuaweicloud.com |
| bucket_name | OBS 存储桶名称 |
| obs_prefix | OBS 中存储的根目录前缀 |

### 定时任务配置

```json
"schedule": {
  "enable": true,
  "interval": 3600
}
```
- `enable`：是否启用定时任务模式
- `interval`：两次上传任务的间隔时间，单位秒（默认 3600 秒 = 1 小时）

### 日志配置

日志文件默认保存在 `logs/` 目录下，按天分割，包含：
- 扫描结果（摄像头数量、文件数量）
- 每个文件的上传结果（成功/失败）
- 本地文件删除记录
- 上传统计摘要

## 📝 使用示例

### 单次上传

```bash
$ python main.py
==================================================
开始执行视频上传任务
==================================================
OBS客户端初始化成功
开始扫描父目录: ~/Videos/cameras，共发现 3 个项目
发现摄像头文件夹: camera-001
发现摄像头文件夹: camera-002
发现摄像头文件夹: camera-003
扫描完成，发现 3 个摄像头文件夹
扫描完成，共发现 15 个视频文件
共发现 15 个视频文件，来自 3 个摄像头
摄像头列表: camera-001, camera-002, camera-003
==================================================
上传进度: 100%|██████████| 15/15 [02:35<00:00, 10.3s/文件]
==================================================
上传任务完成！
总文件数: 15
成功上传: 15
上传失败: 0
删除本地文件: 15
总耗时: 155.23 秒
平均速度: 0.10 文件/秒
==================================================
```

### 定时任务模式

设置 `enable: true` 后，程序会常驻内存，每隔指定时间自动执行一次上传任务。

## 🛡️ 安全建议

1. 不要将 AK/SK 直接写入配置文件，使用环境变量或 .env 文件
2. 为 OBS 账户配置最小权限，仅允许上传文件操作
3. 定期轮换访问密钥
4. 日志文件中不会记录敏感信息

## 📄 许可证

MIT License

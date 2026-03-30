# 地图API KEY泄漏检测工具 / Map API Key Leak Detection Tool

## 项目概述 / Project Overview

这是一个基于Python开发的地图API KEY泄漏检测工具，支持高德、百度和腾讯地图服务。该工具可以检测地图API KEY是否存在泄漏风险，通过发送API请求验证KEY是否能成功获取地理信息。

This is a Python-based map API key leak detection tool that supports AMap, Baidu Map, Tencent Map, and Google Maps services. The tool can detect whether a map API key has a leakage risk by sending API requests to verify if the key can successfully obtain geographic information.

## 功能特点 / Features

### 1. 多地图服务支持 / Multiple Map Service Support

- 高德地图 (AMap)
- 百度地图 (Baidu Map)
- 腾讯地图 (Tencent Map)
- Google地图 (Google Maps)

### 2. 多API类型支持 / Multiple API Type Support

- **高德地图**: 步行导航、逆地理编码、小程序定位
- **百度地图**: 地点搜索、iOS版API
- **腾讯地图**: 地点搜索
- **Google地图**: 静态地图、街景、地理编码、路线规划、距离矩阵、地形、时区、地点搜索、自动完成、地点详情、附近搜索、文本搜索、地点照片、最近道路、道路匹配、限速、空气质量、路线计算、航空视图、地址验证、地理定位、Firebase动态链接、Gemini生成式语言、Cloud Vision、Cloud Translation、自定义搜索、花粉预报、地点聚合等31个API端点
- **AMap**: Walking Navigation, Reverse Geocoding, Mini Program Positioning
- **Baidu Map**: Place Search, iOS API
- **Tencent Map**: Place Search
- **Google Maps**: Static Map, Street View, Geocoding, Directions, Distance Matrix, Elevation, Time Zone, Place Search, Autocomplete, Place Details, Nearby Search, Text Search, Place Photo, Nearest Roads, Snap to Roads, Speed Limits, Air Quality, Compute Routes, Aerial View, Address Validation, Geolocation, Firebase Dynamic Links, Gemini Generate, Cloud Vision, Cloud Translation, Custom Search, Pollen Forecast, Places Aggregate, and 31 other API endpoints

### 3. 两种检测模式 / Two Detection Modes

- **单个KEY检测**: 实时检测单个API KEY的有效性
- **批量KEY检测**: 从文件中读取多个KEY进行批量检测
- **Single Key Detection**: Real-time detection of a single API key's validity
- **Batch Key Detection**: Read multiple keys from a file for batch detection

### 4. 详细的检测结果 / Detailed Detection Results

- 检测状态（可用/不可用/错误/无效）
- 真实地理位置信息
- 结果数量统计
- 详细的错误信息
- 每千次请求成本
- 财务风险评估（基于100,000次请求）
- Detection status (Available/Unavailable/Error/Invalid)
- Real geographic location information
- Result count statistics
- Detailed error information
- Cost per 1,000 requests
- Financial risk assessment (based on 100,000 requests)

### 5. 报告生成 / Report Generation

- 批量检测结果可导出为CSV格式
- 包含完整的地理位置信息
- 包含每千次请求成本和财务风险信息
- Batch detection results can be exported to CSV format
- Includes complete geographic location information
- Includes cost per 1,000 requests and financial risk information

### 6. 攻击模拟功能 / Attack Simulation Function

- 可选的攻击模拟功能，可发送大量请求到API端点
- 显示攻击模拟的成功率和估计成本
- 仅支持Google Maps API，避免产生不必要的费用
- Optional attack simulation function that can send a large number of requests to API endpoints
- Displays attack simulation success rate and estimated cost
- Only supports Google Maps API to avoid unnecessary costs

## 安装和运行 / Installation and Running

### 环境要求 / Environment Requirements

- Python 3.6+
- 依赖库: requests
- Python 3.6+
- Dependencies: requests

### 安装依赖 / Install Dependencies

```bash
pip3 install requests
```

### 运行GUI应用程序 / Run GUI Application

```bash
python3 gui.py
```

### 运行命令行版本 / Run Command Line Version

```bash
python3 main.py
```

## 使用说明 / Usage Instructions

### 1. 单个KEY检测 / Single Key Detection

1. 在"单个KEY检测"标签页中，选择地图服务类型
2. 选择API类型
3. 输入要检测的API KEY
4. 点击"开始检测"按钮
5. 在结果区域查看检测结果和地理位置信息
6. In the "Single Key Detection" tab, select the map service type
7. Select the API type
8. Enter the API key to be detected
9. Click the "Start Detection" button
10. View the detection results and geographic location information in the results area

### 2. 批量KEY检测 / Batch Key Detection

1. 准备KEY文件，格式为每行一个KEY，格式如下：
   ```
   service,api_type,key
   amap,walking,your_amap_key
   baidu,search,your_baidu_key
   tencent,search,your_tencent_key
   ```
2. 在"批量KEY检测"标签页中，点击"浏览"按钮选择KEY文件
3. 设置报告输出文件路径（可选，默认为report.csv）
4. 点击"开始检测"按钮
5. 在结果区域查看实时检测进度和结果
6. 检测完成后，点击"导出结果"按钮保存CSV报告
7. Prepare a key file, with one key per line in the following format:
   ```
   service,api_type,key
   amap,walking,your_amap_key
   baidu,search,your_baidu_key
   tencent,search,your_tencent_key
   ```
8. In the "Batch Key Detection" tab, click the "Browse" button to select the key file
9. Set the report output file path (optional, default is report.csv)
10. Click the "Start Detection" button
11. View the real-time detection progress and results in the results area
12. After detection is complete, click the "Export Results" button to save the CSV report

## 检测原理 / Detection Principle

检测工具通过发送API请求，验证KEY是否能成功获取地理信息：

1. 构造符合地图API要求的请求参数
2. 发送HTTP请求到相应的API端点
3. 解析响应结果，判断是否返回有效地理信息
4. 根据结果判断KEY的状态

The detection tool verifies whether a key can successfully obtain geographic information by sending API requests:

1. Construct request parameters that meet the map API requirements
2. Send HTTP requests to the corresponding API endpoints
3. Parse the response results to determine if valid geographic information is returned
4. Determine the key status based on the results

## 结果解释 / Result Interpretation

- **可用**: KEY能够成功返回有效地理信息，可能存在泄漏风险
- **不可用**: KEY无法返回有效地理信息
- **错误**: 检测过程中发生错误
- **无效**: KEY格式或参数无效
- **Available**: The key can successfully return valid geographic information, which may indicate a leakage risk
- **Unavailable**: The key cannot return valid geographic information
- **Error**: An error occurred during detection
- **Invalid**: The key format or parameters are invalid

## 注意事项 / Notes

1. **合法使用**: 仅在有明确授权的情况下运行，遵守API使用条款和速率限制
2. **安全风险**: 请勿将工具用于非法用途
3. **API费用**: 检测过程中会产生API调用，可能产生费用
4. **速率限制**: 工具默认设置了请求延迟，避免触发API速率限制
5. **Legal Use**: Only run with explicit authorization, comply with API terms of service and rate limits
6. **Security Risk**: Do not use the tool for illegal purposes
7. **API Costs**: API calls generated during detection may incur costs
8. **Rate Limits**: The tool is configured with default request delays to avoid triggering API rate limits

## 项目结构 / Project Structure

```
.
├── main.py          # 核心检测功能和命令行界面 / Core detection functions and command line interface
├── gui.py           # GUI应用程序 / GUI application
├── keys.txt         # KEY文件示例 / Key file example
├── report.csv       # 报告文件示例 / Report file example
└── README.md        # 项目说明文档 / Project documentation
```

## 开发说明 / Development Instructions

### 主要函数 / Main Functions

- `detect_key()`: 检测单个KEY / Detect a single key
- `batch_detect()`: 批量检测KEY / Batch detect keys
- `test_map_api()`: 通用地图API测试函数 / General map API testing function

### 扩展支持新的地图服务 / Extend Support for New Map Services

1. 在`test_map_api()`函数中添加新服务的处理逻辑
2. 在GUI的`update_api_types()`函数中添加新服务的API类型
3. 在`API_CONFIG`字典中添加新服务的API URL配置
4. Add processing logic for the new service in the `test_map_api()` function
5. Add API types for the new service in the GUI's `update_api_types()` function
6. Add API URL configuration for the new service in the `API_CONFIG` dictionary

## 许可证 / License

本项目仅供学习和授权测试使用，请勿用于非法用途。

This project is for learning and authorized testing purposes only. Do not use it for illegal purposes.

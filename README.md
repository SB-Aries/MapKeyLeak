# MapKeyLeak
地图API KEY泄漏检测工具，支持高德、百度、谷歌和腾讯地图服务。该工具可以检测地图API KEY是否存在泄漏利用
## 功能特点

### 1. 多地图服务支持

- 高德地图 (AMap)
- 百度地图 (Baidu Map)
- 腾讯地图 (Tencent Map)
- Google地图 (Google Maps)

### 2. 多API类型支持

- **高德地图**: 步行导航、逆地理编码、小程序定位
- **百度地图**: 地点搜索、iOS版API
- **腾讯地图**: 地点搜索
- **Google地图**: 静态地图、街景、地理编码、路线规划、距离矩阵、地形、时区、地点搜索、自动完成、地点详情、附近搜索、文本搜索、地点照片、最近道路、道路匹配、限速、空气质量、路线计算、航空视图、地址验证、地理定位、Firebase动态链接、Gemini生成式语言、Cloud Vision、Cloud Translation、自定义搜索、花粉预报、地点聚合等31个API端点

### 3. 两种检测模式

- **单个KEY检测**: 实时检测单个API KEY的有效性
- **批量KEY检测**: 从文件中读取多个KEY进行批量检测

### 4. 详细的检测结果

- 检测状态（可用/不可用/错误/无效）
- 真实地理位置信息
- 结果数量统计
- 详细的错误信息
- 每千次请求成本
- 财务风险评估（基于100,000次请求）

### 5. 报告生成

- 批量检测结果可导出为CSV格式
- 包含完整的地理位置信息
- 包含每千次请求成本和财务风险信息

### 6. 攻击模拟功能

- 可选的攻击模拟功能，可发送大量请求到API端点
- 显示攻击模拟的成功率和估计成本
- 仅支持Google Maps API，避免产生不必要的费用

## 安装和运行

### 环境要求

- Python 3.6+
- 依赖库: requests, configparser

### 安装依赖

```bash
pip3 install requests configparser
```

### 运行GUI应用程序

```bash
python3 gui.py
```

### 运行命令行版本

```bash
python3 main.py
```

## 使用说明

### 1. 单个KEY检测

1. 在"单个KEY检测"标签页中，选择地图服务类型
2. 选择API类型
3. 输入要检测的API KEY
4. 点击"开始检测"按钮
5. 在结果区域查看检测结果和地理位置信息

### 2. 批量KEY检测

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

## 检测原理

检测工具通过发送API请求，验证KEY是否能成功获取地理信息：

1. 构造符合地图API要求的请求参数
2. 发送HTTP请求到相应的API端点
3. 解析响应结果，判断是否返回有效地理信息
4. 根据结果判断KEY的状态

## 结果解释

- **可用**: KEY能够成功返回有效地理信息，可能存在泄漏风险
- **不可用**: KEY无法返回有效地理信息
- **错误**: 检测过程中发生错误
- **无效**: KEY格式或参数无效

## 配置文件

工具会读取同目录下的`config.ini`文件作为配置。如果文件不存在，会使用默认配置。

### 配置文件格式

```ini
[TEST]
default_keyword = 酒店
default_page_size = 20
default_max_pages = 3
request_delay = 1.0
timeout = 10.0

[BATCH]
input_file = keys.txt
output_file = report.csv
concurrency = 5
detailed_report = True

[AMAP]
key = 你的高德API密钥
base_url_walking = https://restapi.amap.com/v3/direction/walking
base_url_regeo = https://restapi.amap.com/v3/geocode/regeo
base_url_mini = https://restapi.amap.com/v3/geocode/regeo

[BAIDU]
ak = 你的百度API密钥
base_url_search = https://api.map.baidu.com/place/v2/search
base_url_ios = https://api.map.baidu.com/place/v2/search

[TENCENT]
key = 你的腾讯API密钥
base_url_search = https://apis.map.qq.com/ws/place/v1/search
```

## 注意事项

1. **合法使用**: 仅在有明确授权的情况下运行，遵守API使用条款和速率限制
2. **安全风险**: 请勿将工具用于非法用途
3. **API费用**: 检测过程中会产生API调用，可能产生费用
4. **速率限制**: 工具默认设置了请求延迟，避免触发API速率限制

## 项目结构

```
.
├── main.py          # 核心检测功能和命令行界面
├── gui.py           # GUI应用程序
├── config.ini       # 配置文件（可选）
├── keys.txt         # KEY文件示例
├── report.csv       # 报告文件示例
└── README.md        # 项目说明文档
```

## 开发说明

### 主要函数

- `load_config()`: 加载配置文件
- `detect_key()`: 检测单个KEY
- `batch_detect()`: 批量检测KEY
- `test_map_api()`: 通用地图API测试函数

### 扩展支持新的地图服务

1. 在`load_config()`函数中添加新服务的配置
2. 在`test_map_api()`函数中添加新服务的处理逻辑
3. 在GUI的`update_api_types()`函数中添加新服务的API类型

## 许可证

本项目仅供学习和授权测试使用，请勿用于非法用途。

## 联系方式

如有问题或建议，请通过以下方式联系：

- 项目地址: \[GitHub Repository]
- 作者: \[Your Name]
- 邮箱: \[<your_email@example.com>]

## 更新日志

### v1.0.0 (2026-03-30)

- 初始版本发布
- 支持高德、百度和腾讯地图
- 实现单个KEY检测和批量KEY检测
- 实现GUI应用程序
- 支持CSV报告生成

### v1.1.0 (2026-03-30)

- 添加Google地图支持，支持31个API端点
- 添加每千次请求成本和财务风险评估
- 实现可选的攻击模拟功能
- 增强报告生成，包含财务风险信息
- 更新GUI，支持Google地图服务和API类型
- 优化检测结果显示，包含财务风险信息

## 致谢

感谢所有为这个项目做出贡献的开发者和测试人员！

***

**重要声明：** 本工具仅用于授权测试环境，请勿用于非法用途。使用本工具产生的一切后果由使用者自行承担。

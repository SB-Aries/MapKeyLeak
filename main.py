import requests
import time
import json
import os

# 硬编码的API URL配置
API_CONFIG = {
    'test': {
        'default_keyword': '酒店',
        'default_page_size': 20,
        'default_max_pages': 3,
        'request_delay': 1.0,
        'timeout': 10.0
    },
    'batch': {
        'input_file': 'keys.txt',
        'output_file': 'report.csv',
        'concurrency': 5,
        'detailed_report': True
    },
    'amap': {
        'base_url_walking': 'https://restapi.amap.com/v3/direction/walking',
        'base_url_regeo': 'https://restapi.amap.com/v3/geocode/regeo',
        'base_url_mini': 'https://restapi.amap.com/v3/geocode/regeo'
    },
    'baidu': {
        'base_url_search': 'https://api.map.baidu.com/place/v2/search',
        'base_url_ios': 'https://api.map.baidu.com/place/v2/search'
    },
    'tencent': {
        'base_url_search': 'https://apis.map.qq.com/ws/place/v1/search'
    }
}

# 高德地图测试函数
def test_amap_walking(config=None):
    """
    测试高德步行导航API
    """
    if config is None:
        config = API_CONFIG
    
    params = {
        "origin": "116.434307,39.90909",
        "destination": "116.434446,39.90816"
    }
    
    result = test_map_api('amap', 'walking', params, config)
    return result['result_count']

def test_amap_regeo(config=None):
    """
    测试高德逆地理编码API
    """
    if config is None:
        config = API_CONFIG
    
    params = {
        "location": "116.434446,39.90816"
    }
    
    result = test_map_api('amap', 'regeo', params, config)
    return result['result_count']

def test_amap_mini(config=None):
    """
    测试高德小程序定位API
    """
    if config is None:
        config = API_CONFIG
    
    params = {
        "location": "117.19674,39.14784",
        "extensions": "all",
        "s": "rsx",
        "platform": "WXJS",
        "appname": "c589cf63f592ac13bcab35f8cd18f495",
        "sdkversion": "1.2.0",
        "logversion": "2.0"
    }
    
    result = test_map_api('amap', 'mini', params, config)
    return result['result_count']

# 百度地图测试函数
def test_baidu_search(keyword="ATM机", tag="银行", region="北京", page_size=10, max_pages=1, config=None):
    """
    测试百度地点搜索API
    """
    if config is None:
        config = API_CONFIG
    
    params = {
        "query": keyword,
        "tag": tag,
        "region": region,
        "output": "json",
        "page_size": page_size
    }
    
    result = test_map_api('baidu', 'search', params, config, max_pages)
    return result['result_count']

def test_baidu_ios(keyword="ATM机", tag="银行", region="北京", config=None):
    """
    测试百度iOS版API
    """
    if config is None:
        config = API_CONFIG
    
    params = {
        "query": keyword,
        "tag": tag,
        "region": region,
        "output": "json",
        "=iPhone7,2": "",
        "mcode": "com.didapinche.taxi",
        "os": "12.5.6"
    }
    
    result = test_map_api('baidu', 'ios', params, config)
    return result['result_count']

# 腾讯地图测试函数
def test_tencent_search(keyword="酒店", page_size=20, max_pages=3, config=None):
    """
    测试腾讯地点搜索API
    
    参数:
    keyword: 搜索关键词
    page_size: 每页结果数
    max_pages: 最大测试页数
    config: 配置字典（可选）
    """
    if config is None:
        config = API_CONFIG
    
    params = {
        "keyword": keyword,
        "boundary": "nearby(39.908491,116.374328,1000)",
        "page_size": page_size
    }
    
    result = test_map_api('tencent', 'search', params, config, max_pages)
    return result['result_count']

def test_api_pagination_with_limit(keyword="酒店", page_size=20, max_pages=3, config=None):
    """
    测试API分页和结果限制功能（兼容旧接口）
    每次调用只输出前30%的结果（用于测试数据处理逻辑）
    
    参数:
    keyword: 搜索关键词
    page_size: 每页结果数
    max_pages: 最大测试页数
    config: 配置字典（可选）
    """
    return test_tencent_search(keyword, page_size, max_pages, config)

def test_result_processing():
    """
    测试不同地图服务和参数下的结果处理
    """
    # 使用硬编码配置
    config = API_CONFIG
    
    print("\n=== 多地图服务结果处理测试 ===")
    print("=" * 60)
    
    results_summary = []
    test_count = 1
    
    # 测试高德地图
    print(f"\n测试用例 {test_count}: 高德地图 - 步行导航")
    print("-" * 40)
    count = test_amap_walking(config)
    results_summary.append({
        "测试用例": test_count,
        "地图服务": "高德地图",
        "API类型": "步行导航",
        "获取结果总数": count
    })
    test_count += 1
    
    print(f"\n测试用例 {test_count}: 高德地图 - 逆地理编码")
    print("-" * 40)
    count = test_amap_regeo(config)
    results_summary.append({
        "测试用例": test_count,
        "地图服务": "高德地图",
        "API类型": "逆地理编码",
        "获取结果总数": count
    })
    test_count += 1
    
    # 测试百度地图
    print(f"\n测试用例 {test_count}: 百度地图 - 地点搜索")
    print("-" * 40)
    count = test_baidu_search(config=config)
    results_summary.append({
        "测试用例": test_count,
        "地图服务": "百度地图",
        "API类型": "地点搜索",
        "获取结果总数": count
    })
    test_count += 1
    
    print(f"\n测试用例 {test_count}: 百度地图 - iOS版")
    print("-" * 40)
    count = test_baidu_ios(config=config)
    results_summary.append({
        "测试用例": test_count,
        "地图服务": "百度地图",
        "API类型": "iOS版",
        "获取结果总数": count
    })
    test_count += 1
    
    # 测试腾讯地图
    print(f"\n测试用例 {test_count}: 腾讯地图 - 地点搜索")
    print("-" * 40)
    count = test_tencent_search(max_pages=1, config=config)
    results_summary.append({
        "测试用例": test_count,
        "地图服务": "腾讯地图",
        "API类型": "地点搜索",
        "获取结果总数": count
    })
    test_count += 1
    
    # 输出测试总结
    print("\n=== 测试结果总结 ===")
    print(f"共执行 {len(results_summary)} 个测试用例")
    print("\n详细结果:")
    for summary in results_summary:
        print(f"测试用例 {summary['测试用例']}: {summary['地图服务']} - {summary['API类型']} - 获取{summary['获取结果总数']}条")
    
    return results_summary

def test_map_api(map_service, api_type, params, config, max_pages=1):
    """
    通用地图API测试函数（优化版，返回真实地理位置信息）
    
    参数:
    map_service: 地图服务类型 (amap, baidu, tencent, google)
    api_type: API类型 (walking, regeo, mini, search, ios等)
    params: 请求参数
    config: 配置字典
    max_pages: 最大测试页数
    
    返回:
    包含结果数量和地理位置信息的字典
    {"result_count": 结果数量, "locations": 地理位置信息列表, "cost_per_1k": 每千次请求成本}
    """
    # 获取测试通用配置
    test_config = config['test']
    
    result_count = 0
    locations = []
    cost_per_1k = 0.0
    
    # 根据地图服务和API类型获取对应的配置
    if map_service == 'amap':
        service_config = config['amap']
        base_url_key = f'base_url_{api_type}'
        api_key = service_config['key']
        key_param = 'key'
        
        # 获取基础URL
        if base_url_key not in service_config:
            return {"result_count": 0, "locations": [], "cost_per_1k": 0.0}
        
        base_url = service_config[base_url_key]
        
        # 添加API密钥到参数
        params[key_param] = api_key
        
        for page in range(1, max_pages + 1):
            # 根据地图服务添加分页参数
            if api_type == 'search':
                params['page'] = page
            
            try:
                # 发送请求（添加延迟避免触发频率限制）
                time.sleep(test_config['request_delay'])
                
                response = requests.get(base_url, params=params, timeout=test_config['timeout'])
                
                if response.status_code == 200:
                    # 处理不同地图服务的响应，获取真实地理位置信息
                    data = response.json()
                    
                    # 高德地图 - 获取真实地理信息
                    if data.get('status') == '1':
                        if api_type == 'walking':
                            # 步行导航 - 获取路径信息
                            paths = data.get('route', {}).get('paths', [])
                            result_count = len(paths) if paths else 0
                            if paths:
                                for path in paths[:3]:  # 最多显示3条
                                    location_info = {
                                        "type": "walking",
                                        "distance": path.get('distance', '未知'),
                                        "duration": path.get('duration', '未知'),
                                        "origin": params.get('origin', '未知'),
                                        "destination": params.get('destination', '未知')
                                    }
                                    locations.append(location_info)
                        elif api_type in ['regeo', 'mini']:
                            # 逆地理编码 - 获取详细地址
                            regeocode = data.get('regeocode', {})
                            if regeocode and regeocode.get('formatted_address'):
                                result_count = 1
                                location_info = {
                                    "type": "address",
                                    "location": params.get('location', '未知'),
                                    "formatted_address": regeocode.get('formatted_address', '未知'),
                                    "province": regeocode.get('addressComponent', {}).get('province', '未知'),
                                    "city": regeocode.get('addressComponent', {}).get('city', '未知'),
                                    "district": regeocode.get('addressComponent', {}).get('district', '未知')
                                }
                                locations.append(location_info)
                            else:
                                result_count = 0
                        else:
                            # 地点搜索 - 获取POI信息
                            pois = data.get('pois', [])
                            result_count = len(pois)
                            for poi in pois[:3]:  # 最多显示3条
                                location_info = {
                                    "type": "poi",
                                    "name": poi.get('name', '未知'),
                                    "address": poi.get('address', '未知'),
                                    "location": poi.get('location', '未知'),
                                    "type": poi.get('type', '未知')
                                }
                                locations.append(location_info)
                        break  # 检测模式下只需要1次请求
                
                else:
                    break  # HTTP错误，直接返回
                
            except requests.exceptions.Timeout:
                break  # 请求超时
            except requests.exceptions.RequestException as e:
                print(f"网络错误: {e}")
                break  # 网络错误
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}")
                break  # JSON解析错误
            except Exception as e:
                print(f"其他错误: {e}")
                break  # 其他错误
    
    elif map_service == 'baidu':
        service_config = config['baidu']
        base_url_key = f'base_url_{api_type}'
        api_key = service_config['ak']
        key_param = 'ak'
        
        # 获取基础URL
        if base_url_key not in service_config:
            return {"result_count": 0, "locations": [], "cost_per_1k": 0.0}
        
        base_url = service_config[base_url_key]
        
        # 添加API密钥到参数
        params[key_param] = api_key
        
        for page in range(1, max_pages + 1):
            # 根据地图服务添加分页参数
            if api_type == 'search':
                params['page_num'] = page
            
            try:
                # 发送请求（添加延迟避免触发频率限制）
                time.sleep(test_config['request_delay'])
                
                response = requests.get(base_url, params=params, timeout=test_config['timeout'])
                
                if response.status_code == 200:
                    # 处理不同地图服务的响应，获取真实地理位置信息
                    data = response.json()
                    
                    # 百度地图 - 获取真实地理信息
                    if data.get('status') == 0:
                        results = data.get('results', [])
                        result_count = len(results)
                        for result in results[:3]:  # 最多显示3条
                            location_info = {
                                "type": "poi",
                                "name": result.get('name', '未知'),
                                "address": result.get('address', '未知'),
                                "location": f"{result.get('location', {}).get('lat', '未知')},{result.get('location', {}).get('lng', '未知')}",
                                "telephone": result.get('telephone', '未知')
                            }
                            locations.append(location_info)
                        break  # 检测模式下只需要1次请求
                
                else:
                    break  # HTTP错误，直接返回
                
            except requests.exceptions.Timeout:
                break  # 请求超时
            except requests.exceptions.RequestException as e:
                print(f"网络错误: {e}")
                break  # 网络错误
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}")
                break  # JSON解析错误
            except Exception as e:
                print(f"其他错误: {e}")
                break  # 其他错误
    
    elif map_service == 'tencent':
        service_config = config['tencent']
        base_url_key = f'base_url_{api_type}'
        api_key = service_config['key']
        key_param = 'key'
        
        # 获取基础URL
        if base_url_key not in service_config:
            return {"result_count": 0, "locations": [], "cost_per_1k": 0.0}
        
        base_url = service_config[base_url_key]
        
        # 添加API密钥到参数
        params[key_param] = api_key
        
        for page in range(1, max_pages + 1):
            # 根据地图服务添加分页参数
            if api_type == 'search':
                params['page_index'] = page
            
            try:
                # 发送请求（添加延迟避免触发频率限制）
                time.sleep(test_config['request_delay'])
                
                response = requests.get(base_url, params=params, timeout=test_config['timeout'])
                
                if response.status_code == 200:
                    # 处理不同地图服务的响应，获取真实地理位置信息
                    data = response.json()
                    
                    # 腾讯地图 - 获取真实地理信息
                    if data.get('status') == 0:
                        results = data.get('data', [])
                        result_count = len(results)
                        for result in results[:3]:  # 最多显示3条
                            location_info = {
                                "type": "poi",
                                "name": result.get('title', '未知'),
                                "address": result.get('address', '未知'),
                                "location": f"{result.get('location', {}).get('lat', '未知')},{result.get('location', {}).get('lng', '未知')}",
                                "category": result.get('category', '未知')
                            }
                            locations.append(location_info)
                        break  # 检测模式下只需要1次请求
                
                else:
                    break  # HTTP错误，直接返回
                
            except requests.exceptions.Timeout:
                break  # 请求超时
            except requests.exceptions.RequestException as e:
                print(f"网络错误: {e}")
                break  # 网络错误
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}")
                break  # JSON解析错误
            except Exception as e:
                print(f"其他错误: {e}")
                break  # 其他错误
    
    elif map_service == 'google':
        # Google Maps API处理逻辑
        api_key = config['google']['key']
        
        # 检查API类型是否在Google端点列表中
        if api_type not in GOOGLE_ENDPOINTS:
            return {"result_count": 0, "locations": [], "cost_per_1k": 0.0}
        
        endpoint = GOOGLE_ENDPOINTS[api_type]
        endpoint_type = endpoint['type']
        endpoint_url = endpoint['url']
        cost_per_1k = endpoint['cost_per_1k']
        
        # 构建完整URL
        full_url = endpoint_url + api_key
        
        try:
            # 发送请求（添加延迟避免触发频率限制）
            time.sleep(test_config['request_delay'])
            
            if endpoint_type == 'POST':
                # 处理POST请求
                data = endpoint.get('data', '{}')
                response = requests.post(full_url, json=json.loads(data), timeout=test_config['timeout'])
            else:
                # 处理GET和IMG请求
                response = requests.get(full_url, timeout=test_config['timeout'])
            
            # 检查响应状态
            if response.status_code == 200:
                # 处理响应
                response_text = response.text
                
                # 判断是否为JSON响应
                is_json = endpoint_type == 'JSON' or (endpoint_type != 'IMG' and response.headers.get('Content-Type', '').startswith('application/json'))
                
                if is_json:
                    try:
                        data = response.json()
                        
                        # 检查是否成功返回数据
                        if ("status" in data and data["status"] == "OK") or \
                           "shortLink" in data or \
                           "candidates" in data or \
                           "translations" in data or \
                           "snappedPoints" in data or \
                           "models" in data or \
                           "files" in data or \
                           "cachedContents" in data or \
                           "currentConditions" in data or \
                           "routes" in data:
                            result_count = 1
                            # 提取地理位置信息（如果有）
                            if "results" in data and len(data["results"]) > 0:
                                for result in data["results"][:3]:
                                    if "formatted_address" in result:
                                        location_info = {
                                            "type": "address",
                                            "formatted_address": result.get("formatted_address", "未知"),
                                            "location": f"{result.get('geometry', {}).get('location', {}).get('lat', '未知')},{result.get('geometry', {}).get('location', {}).get('lng', '未知')}"
                                        }
                                        locations.append(location_info)
                            elif "routes" in data and len(data["routes"]) > 0:
                                route = data["routes"][0]
                                location_info = {
                                    "type": "route",
                                    "distance": route.get("legs", [{}])[0].get("distance", {}).get("text", "未知"),
                                    "duration": route.get("legs", [{}])[0].get("duration", {}).get("text", "未知")
                                }
                                locations.append(location_info)
                    except json.JSONDecodeError:
                        # 非JSON响应，可能是图片或其他格式
                        if endpoint_type == 'IMG':
                            # 图片响应，视为成功
                            result_count = 1
                else:
                    # 非JSON响应，如图片
                    result_count = 1
        except requests.exceptions.Timeout:
            pass  # 请求超时
        except requests.exceptions.RequestException as e:
            print(f"Google API请求错误: {e}")
        except Exception as e:
            print(f"Google API处理错误: {e}")
    
    else:
        return {"result_count": 0, "locations": [], "cost_per_1k": 0.0}
    
    return {"result_count": result_count, "locations": locations, "cost_per_1k": cost_per_1k}

def analyze_api_response(map_service='tencent', api_type='search', config=None):
    """
    分析API响应结构和数据格式
    
    参数:
    map_service: 地图服务类型 (amap, baidu, tencent)
    api_type: API类型
    config: 配置字典（可选）
    """
    print("\n=== API响应结构分析 ===")
    
    # 加载配置
    if config is None:
        config = API_CONFIG
    
    # 根据地图服务设置最小化测试请求参数
    if map_service == 'amap':
        if api_type == 'walking':
            test_params = {
                "origin": "116.434307,39.90909",
                "destination": "116.434446,39.90816"
            }
        elif api_type in ['regeo', 'mini']:
            test_params = {
                "location": "116.434446,39.90816"
            }
            if api_type == 'mini':
                test_params.update({
                    "extensions": "all",
                    "s": "rsx",
                    "platform": "WXJS",
                    "appname": "c589cf63f592ac13bcab35f8cd18f495",
                    "sdkversion": "1.2.0",
                    "logversion": "2.0"
                })
        else:
            test_params = {
                "keywords": "测试",
                "city": "北京",
                "offset": 1
            }
    
    elif map_service == 'baidu':
        test_params = {
            "query": "ATM机",
            "tag": "银行",
            "region": "北京",
            "output": "json"
        }
        if api_type == 'ios':
            test_params.update({
                "=iPhone7,2": "",
                "mcode": "com.didapinche.taxi",
                "os": "12.5.6"
            })
    
    elif map_service == 'tencent':
        test_params = {
            "keyword": "测试",
            "boundary": "nearby(39.9,116.3,100)",
            "page_size": 1
        }
    
    else:
        print(f"不支持的地图服务: {map_service}")
        return
    
    try:
        # 调用通用测试函数进行分析
        test_map_api(map_service, api_type, test_params, config, max_pages=1)
    except Exception as e:
        print(f"分析失败: {e}")

# Google Maps API端点列表
GOOGLE_ENDPOINTS = {
    "staticmap": {
        "type": "IMG",
        "url": "https://maps.googleapis.com/maps/api/staticmap?center=45,10&zoom=7&size=400x400&key=",
        "cost_per_1k": 2.00
    },
    "streetview": {
        "type": "IMG",
        "url": "https://maps.googleapis.com/maps/api/streetview?size=400x400&location=40.72,-73.98&fov=90&key=",
        "cost_per_1k": 7.00
    },
    "geocode": {
        "type": "JSON",
        "url": "https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,CA&key=",
        "cost_per_1k": 5.00
    },
    "directions": {
        "type": "JSON",
        "url": "https://maps.googleapis.com/maps/api/directions/json?origin=Disneyland&destination=Universal&key=",
        "cost_per_1k": 5.00
    },
    "distancematrix": {
        "type": "JSON",
        "url": "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=DC&destinations=NY&key=",
        "cost_per_1k": 5.00
    },
    "elevation": {
        "type": "JSON",
        "url": "https://maps.googleapis.com/maps/api/elevation/json?locations=39.73,-104.98&key=",
        "cost_per_1k": 5.00
    },
    "timezone": {
        "type": "JSON",
        "url": "https://maps.googleapis.com/maps/api/timezone/json?location=39.6,-119.6&timestamp=1331161200&key=",
        "cost_per_1k": 5.00
    },
    "findplacefromtext": {
        "type": "JSON",
        "url": "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=Museum&inputtype=textquery&fields=name,rating&key=",
        "cost_per_1k": 17.00
    },
    "autocomplete": {
        "type": "JSON",
        "url": "https://maps.googleapis.com/maps/api/place/autocomplete/json?input=Paris&key=",
        "cost_per_1k": 2.83
    },
    "placedetails": {
        "type": "JSON",
        "url": "https://maps.googleapis.com/maps/api/place/details/json?place_id=ChIJN1t_tDeuEmsRUsoyG83frY4&fields=name,rating&key=",
        "cost_per_1k": 17.00
    },
    "nearbysearch": {
        "type": "JSON",
        "url": "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33,151&radius=1500&type=restaurant&key=",
        "cost_per_1k": 32.00
    },
    "textsearch": {
        "type": "JSON",
        "url": "https://maps.googleapis.com/maps/api/place/textsearch/json?query=restaurants+in+Sydney&key=",
        "cost_per_1k": 32.00
    },
    "placephoto": {
        "type": "IMG",
        "url": "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=CnRtAAAATY6p_z_S48W_9Ope963X3ZfM3A&key=",
        "cost_per_1k": 7.00
    },
    "nearestroads": {
        "type": "JSON",
        "url": "https://roads.googleapis.com/v1/nearestRoads?points=60.1,24.9|60.1,24.9&key=",
        "cost_per_1k": 10.00
    },
    "snaptoroads": {
        "type": "JSON",
        "url": "https://roads.googleapis.com/v1/snapToRoads?path=-35.2,149.1|-35.2,149.1&interpolate=true&key=",
        "cost_per_1k": 10.00
    },
    "speedlimits": {
        "type": "JSON",
        "url": "https://roads.googleapis.com/v1/speedLimits?path=38.7,-9.0&key=",
        "cost_per_1k": 20.00
    },
    "airquality": {
        "type": "POST",
        "url": "https://airquality.googleapis.com/v1/currentConditions:lookup?key=",
        "cost_per_1k": 5.00,
        "data": '{"location":{"latitude":40.7128,"longitude":-74.0060}}'
    },
    "computeroutes": {
        "type": "POST",
        "url": "https://routes.googleapis.com/directions/v2:computeRoutes?key=",
        "cost_per_1k": 5.00,
        "data": '{"origin":{"location":{"latLng":{"latitude":37.419734,"longitude":-122.0827784}}},"destination":{"location":{"latLng":{"latitude":37.7749,"longitude":-122.4194}}},"travelMode":"DRIVE"}'
    },
    "aerialview": {
        "type": "POST",
        "url": "https://aerialview.googleapis.com/v1/videos:lookup?key=",
        "cost_per_1k": 16.00,
        "data": '{"location":{"latitude":37.7749,"longitude":-122.4194}}'
    },
    "addressvalidation": {
        "type": "POST",
        "url": "https://addressvalidation.googleapis.com/v1:validateAddress?key=",
        "cost_per_1k": 14.00,
        "data": '{"address":{"regionCode":"US","postalCode":"94043","addressLines":["1600 Amphitheatre Parkway"]}}'
    },
    "geolocation": {
        "type": "POST",
        "url": "https://www.googleapis.com/geolocation/v1/geolocate?key=",
        "cost_per_1k": 5.00,
        "data": '{"considerIp":true}'
    },
    "firebasedynamiclinks": {
        "type": "POST",
        "url": "https://firebasedynamiclinks.googleapis.com/v1/shortLinks?key=",
        "cost_per_1k": 0.00,
        "data": '{"longDynamicLink":"http://example.com"}'
    },
    "geminigenerate": {
        "type": "POST",
        "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=",
        "cost_per_1k": 12.00,
        "data": '{"contents":[{"parts":[{"text":"Hi"}]}]}'
    },
    "geminimodels": {
        "type": "JSON",
        "url": "https://generativelanguage.googleapis.com/v1beta/models?key=",
        "cost_per_1k": 12.00
    },
    "geminifiles": {
        "type": "JSON",
        "url": "https://generativelanguage.googleapis.com/v1beta/files?key=",
        "cost_per_1k": 12.00
    },
    "geminicached": {
        "type": "JSON",
        "url": "https://generativelanguage.googleapis.com/v1beta/cachedContents?key=",
        "cost_per_1k": 12.00
    },
    "cloudvision": {
        "type": "POST",
        "url": "https://vision.googleapis.com/v1/images:annotate?key=",
        "cost_per_1k": 1.50,
        "data": '{"requests":[{"features":[{"type":"LABEL_DETECTION"}],"image":{"source":{"imageUri":"http://pwn.com/img.jpg"}}}]}'
    },
    "cloudtranslation": {
        "type": "JSON",
        "url": "https://translation.googleapis.com/language/translate/v2?q=hello&target=es&key=",
        "cost_per_1k": 20.00
    },
    "customsearch": {
        "type": "JSON",
        "url": "https://www.googleapis.com/customsearch/v1?q=pwned&cx=test&key=",
        "cost_per_1k": 5.00
    },
    "pollenforecast": {
        "type": "POST",
        "url": "https://pollen.googleapis.com/v1/forecast:lookup?key=",
        "cost_per_1k": 5.00,
        "data": '{"location":{"latitude":40.7128,"longitude":-74.0060}}'
    },
    "placesaggregate": {
        "type": "JSON",
        "url": "https://maps.googleapis.com/maps/api/place/aggregate/json?key=",
        "cost_per_1k": 32.00
    }
}



def show_menu():
    """
    显示菜单（优化版，突出批量检测功能）
    """
    print("\n=== 地图API KEY泄漏检测工具 ===")
    print("1. 批量检测KEY（推荐）")
    print("2. 单个KEY检测")
    print("3. 退出程序")
    print("=" * 40)

def show_map_service_menu():
    """
    显示地图服务选择菜单
    """
    print("\n选择地图服务:")
    print("1. 高德地图")
    print("2. 百度地图")
    print("3. 腾讯地图")
    print("4. 返回上级菜单")
    print("=" * 30)

def show_amap_api_menu():
    """
    显示高德地图API选择菜单
    """
    print("\n选择高德地图API类型:")
    print("1. 步行导航")
    print("2. 逆地理编码")
    print("3. 小程序定位")
    print("4. 返回上级菜单")
    print("=" * 30)

def show_baidu_api_menu():
    """
    显示百度地图API选择菜单
    """
    print("\n选择百度地图API类型:")
    print("1. 地点搜索")
    print("2. iOS版API")
    print("3. 返回上级菜单")
    print("=" * 30)

def read_key_file(file_path):
    """
    读取KEY文件，返回KEY列表
    
    参数:
    file_path: KEY文件路径
    
    返回:
    KEY列表，每个元素为字典：{"service": 服务类型, "api_type": API类型, "key": KEY值}
    """
    keys = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split(',')
                if len(parts) != 3:
                    print(f"警告: 第 {line_num} 行格式错误，跳过: {line}")
                    continue
                
                service, api_type, key = parts
                keys.append({
                    "service": service.strip(),
                    "api_type": api_type.strip(),
                    "key": key.strip()
                })
        
        print(f"成功读取 {len(keys)} 个KEY")
        return keys
    except Exception as e:
        print(f"读取KEY文件失败: {e}")
        return []

def detect_key(service, api_type, key, config):
    """
    检测单个KEY是否可用
    
    参数:
    service: 服务类型 (amap, baidu, tencent, google)
    api_type: API类型 (walking, regeo, mini, search, ios等)
    key: API密钥
    config: 配置字典
    
    返回:
    检测结果字典: 包含服务类型、API类型、KEY值、状态、消息、结果数量、地理位置信息和财务风险
    """
    print(f"\n正在检测: {service} - {api_type} - {key[:10]}...")
    
    # 创建临时配置，使用要检测的KEY
    temp_config = config.copy()
    params = {}
    
    # 根据服务类型设置测试参数和配置
    if service == 'amap':
        # 高德地图处理
        if api_type == 'walking':
            params = {
                "origin": "116.434307,39.90909",
                "destination": "116.434446,39.90816"
            }
        elif api_type in ['regeo', 'mini']:
            params = {
                "location": "116.434446,39.90816"
            }
            if api_type == 'mini':
                params.update({
                    "extensions": "all",
                    "s": "rsx",
                    "platform": "WXJS",
                    "appname": "c589cf63f592ac13bcab35f8cd18f495",
                    "sdkversion": "1.2.0",
                    "logversion": "2.0"
                })
        else:
            return {
                "service": service,
                "api_type": api_type,
                "key": key,
                "status": "无效",
                "message": f"不支持的高德API类型: {api_type}",
                "result_count": 0,
                "locations": [],
                "cost_per_1k": 0.0,
                "financial_risk": 0.0
            }
        
        # 更新临时配置中的KEY
        temp_config['amap'] = temp_config['amap'].copy()
        temp_config['amap']['key'] = key
    
    elif service == 'baidu':
        # 百度地图处理
        params = {
            "query": "ATM机",
            "tag": "银行",
            "region": "北京",
            "output": "json"
        }
        if api_type == 'ios':
            params.update({
                "=iPhone7,2": "",
                "mcode": "com.didapinche.taxi",
                "os": "12.5.6"
            })
        
        # 更新临时配置中的KEY
        temp_config['baidu'] = temp_config['baidu'].copy()
        temp_config['baidu']['ak'] = key
    
    elif service == 'tencent':
        # 腾讯地图处理
        params = {
            "keyword": "酒店",
            "boundary": "nearby(39.908491,116.374328,1000)",
            "page_size": 1
        }
        
        # 更新临时配置中的KEY
        temp_config['tencent'] = temp_config['tencent'].copy()
        temp_config['tencent']['key'] = key
    
    elif service == 'google':
        # Google地图处理
        # 对于Google，我们不需要设置额外参数，因为端点配置已经包含了所有必要参数
        params = {}
        
        # 更新临时配置中的KEY
        temp_config['google'] = temp_config['google'].copy()
        temp_config['google']['key'] = key
    
    else:
        return {
            "service": service,
            "api_type": api_type,
            "key": key,
            "status": "无效",
            "message": f"不支持的服务类型: {service}",
            "result_count": 0,
            "locations": [],
            "cost_per_1k": 0.0,
            "financial_risk": 0.0
        }
    
    try:
        # 调用通用测试函数，限制为1页
        result = test_map_api(service, api_type, params, temp_config, max_pages=1)
        result_count = result.get('result_count', 0)
        locations = result.get('locations', [])
        cost_per_1k = result.get('cost_per_1k', 0.0)
        
        # 计算财务风险（假设100,000次请求）
        financial_risk = cost_per_1k * 100.0
        
        if result_count > 0:
            return {
                "service": service,
                "api_type": api_type,
                "key": key,
                "status": "可用",
                "message": "成功获取地理信息",
                "result_count": result_count,
                "locations": locations,
                "cost_per_1k": cost_per_1k,
                "financial_risk": financial_risk
            }
        else:
            return {
                "service": service,
                "api_type": api_type,
                "key": key,
                "status": "不可用",
                "message": "未获取到地理信息",
                "result_count": result_count,
                "locations": [],
                "cost_per_1k": cost_per_1k,
                "financial_risk": 0.0
            }
    except Exception as e:
        return {
            "service": service,
            "api_type": api_type,
            "key": key,
            "status": "错误",
            "message": str(e),
            "result_count": 0,
            "locations": [],
            "cost_per_1k": 0.0,
            "financial_risk": 0.0
        }

def batch_detect(config):
    """
    批量检测KEY
    
    参数:
    config: 配置字典
    """
    print("\n=== 批量KEY检测 ===")
    print("=" * 60)
    
    # 获取批量检测配置
    batch_config = config['batch']
    input_file = batch_config['input_file']
    output_file = batch_config['output_file']
    
    # 读取KEY列表
    keys = read_key_file(input_file)
    if not keys:
        print("没有可用的KEY进行检测")
        return
    
    # 开始检测
    print(f"\n开始检测 {len(keys)} 个KEY...")
    results = []
    
    for key_info in keys:
        result = detect_key(
            key_info['service'],
            key_info['api_type'],
            key_info['key'],
            config
        )
        results.append(result)
    
    # 生成报告
    print("\n=== 检测结果报告 ===")
    print(f"总计: {len(results)} 个KEY")
    
    # 统计结果
    stats = {
        "可用": 0,
        "不可用": 0,
        "错误": 0,
        "无效": 0
    }
    
    for result in results:
        status = result['status']
        if status in stats:
            stats[status] += 1
        else:
            stats[status] = 1
    
    print(f"可用: {stats['可用']}")
    print(f"不可用: {stats['不可用']}")
    print(f"错误: {stats['错误']}")
    print(f"无效: {stats['无效']}")
    
    # 计算总财务风险
    total_financial_risk = 0.0
    for result in results:
        if result['status'] == "可用":
            total_financial_risk += result.get('financial_risk', 0.0)
    
    if total_financial_risk > 0:
        print(f"\n=== 财务风险评估 ===")
        print(f"总财务风险 (100,000次请求): ${total_financial_risk:.2f}")
    
    # 生成输出报告
    print(f"\n生成报告: {output_file}")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            # 写入表头
            f.write("服务类型,API类型,KEY,状态,消息,结果数量,每千次请求成本,财务风险,地理位置信息\n")
            
            # 写入详细结果
            for result in results:
                # 格式化地理位置信息为字符串
                locations_str = ""
                if result['locations']:
                    location_details = []
                    for loc in result['locations']:
                        if loc['type'] == 'walking':
                            loc_str = f"步行导航-{loc.get('distance', '未知')}米-{loc.get('duration', '未知')}秒"
                        elif loc['type'] == 'address':
                            loc_str = f"地址-{loc.get('formatted_address', '未知')}"
                        elif loc['type'] == 'route':
                            loc_str = f"路线-{loc.get('distance', '未知')}-{loc.get('duration', '未知')}"
                        else:  # POI类型
                            loc_str = f"POI-{loc.get('name', '未知')}-{loc.get('address', '未知')}"
                        location_details.append(loc_str)
                    locations_str = "|" .join(location_details)
                
                f.write(f"{result['service']},{result['api_type']},{result['key']},{result['status']},{result['message']},{result['result_count']},{result.get('cost_per_1k', 0.0)},{result.get('financial_risk', 0.0)},{locations_str}\n")
    
        print(f"报告生成成功: {output_file}")
        
        # 显示可用的KEY
        print("\n可用的KEY列表:")
        print("-" * 80)
        for result in results:
            if result['status'] == "可用":
                print(f"{result['service']},{result['api_type']},{result['key']} - 财务风险: ${result.get('financial_risk', 0.0):.2f}")
                # 显示地理位置信息
                if result['locations']:
                    print("  地理位置信息:")
                    for i, location in enumerate(result['locations'], 1):
                        if location['type'] == 'walking':
                            print(f"    {i}. 步行导航: {location.get('distance', '未知')}米, {location.get('duration', '未知')}秒")
                        elif location['type'] == 'address':
                            print(f"    {i}. 地址: {location.get('formatted_address', '未知')}")
                        elif location['type'] == 'route':
                            print(f"    {i}. 路线: {location.get('distance', '未知')}, {location.get('duration', '未知')}")
                        else:  # POI类型
                            print(f"    {i}. POI: {location.get('name', '未知')} - {location.get('address', '未知')}")
    
    except Exception as e:
        print(f"生成报告失败: {e}")
    
    # 执行可选的攻击模拟
    available_results = [r for r in results if r['status'] == '可用']
    if available_results:
        print(f"\n=== 可选的攻击模拟 ===")
        print(f"检测到 {len(available_results)} 个可用的KEY")
        print("这个功能可以模拟对漏洞端点的攻击，证明漏洞的严重性")
        print("注意：这可能会产生实际的API调用费用，请谨慎使用")
        
        simulate_attack = input("是否执行攻击模拟？(y/N): ")
        if simulate_attack.lower() == 'y':
            # 执行攻击模拟
            simulate_attack_on_results(available_results, config)

def simulate_attack_on_results(results, config):
    """
    对可用的KEY执行攻击模拟
    
    参数:
    results: 检测结果列表，只包含可用的KEY
    config: 配置字典
    """
    print("\n=== 开始攻击模拟 ===")
    print("警告：这将发送大量请求到API端点，可能会产生费用")
    print("=" * 60)
    
    # 获取测试通用配置
    test_config = config['test']
    
    # 每个端点的请求数量
    stress_count = 100  # 发送100个请求
    
    for result in results:
        service = result['service']
        api_type = result['api_type']
        key = result['key']
        
        print(f"\n[+] 攻击模拟: {service} - {api_type} - {key[:10]}...")
        
        # 构建请求URL和参数
        if service == 'google':
            # 对于Google，使用端点配置
            if api_type not in GOOGLE_ENDPOINTS:
                print("    无效的Google API类型，跳过")
                continue
            
            endpoint = GOOGLE_ENDPOINTS[api_type]
            endpoint_type = endpoint['type']
            endpoint_url = endpoint['url']
            
            # 构建完整URL
            full_url = endpoint_url + key
            
            # 发送请求
            success_count = 0
            for i in range(stress_count):
                try:
                    if endpoint_type == 'POST':
                        # 处理POST请求
                        data = endpoint.get('data', '{}')
                        response = requests.post(full_url, json=json.loads(data), timeout=test_config['timeout'])
                    else:
                        # 处理GET和IMG请求
                        response = requests.get(full_url, timeout=test_config['timeout'])
                    
                    if response.status_code == 200:
                        success_count += 1
                        
                    # 每10个请求显示一个进度点
                    if (i + 1) % 10 == 0:
                        print(".", end="", flush=True)
                except Exception as e:
                    pass  # 忽略错误，继续发送请求
            
            print(f"\n    完成: {success_count}/{stress_count} 个请求成功")
            print(f"    估计成本: ${(success_count / 1000) * result.get('cost_per_1k', 0.0):.2f}")
        else:
            # 对于其他地图服务，使用detect_key函数的逻辑
            print("    攻击模拟仅支持Google Maps API")
    
    print("\n=== 攻击模拟完成 ===")
    print("注意：这只是一个模拟，实际攻击可能会产生更高的费用")
    print("请及时检查API使用情况和费用")

def show_tencent_api_menu():
    """
    显示腾讯地图API选择菜单
    """
    print("\n选择腾讯地图API类型:")
    print("1. 地点搜索")
    print("2. 返回上级菜单")
    print("=" * 30)

def show_single_key_detect_menu():
    """
    单个KEY检测菜单
    """
    print("\n选择地图服务:")
    print("1. 高德地图")
    print("2. 百度地图")
    print("3. 腾讯地图")
    print("4. Google地图")
    print("5. 返回上级菜单")
    print("=" * 30)

if __name__ == "__main__":
    """
    重要声明：
    1. 仅在有明确授权的情况下运行
    2. 遵守API使用条款和速率限制
    3. 不要用于生产环境
    4. 测试后清理测试数据
    """

    print("=== 地图API KEY泄漏检测工具 ===")
    print("警告：仅用于授权测试环境，请勿用于非法用途")
    print("=" * 60)
    print("检测原理：通过发送API请求，验证KEY是否能成功获取地理信息")
    print("可用KEY定义：能够成功返回有效地理信息的KEY")
    print("=" * 60)

    # 确认授权
    confirm = input("确认您已获得测试授权？(输入 'YES' 继续): ")

    if confirm == "YES":
        print("\n开始检测...")
        
        # 使用硬编码配置
        config = API_CONFIG
        print("已加载硬编码配置")
        
        while True:
            show_menu()
            choice = input("请选择操作 (1-3): ")
            
            if choice == "1":
                # 批量检测KEY
                batch_detect(config)
            
            elif choice == "2":
                # 单个KEY检测
                while True:
                    print("\n单个KEY检测")
                    print("请输入KEY信息（格式：服务类型,API类型,KEY）")
                    print("服务类型: amap, baidu, tencent, google")
                    print("API类型: ")
                    print("  - amap: walking, regeo, mini")
                    print("  - baidu: search, ios")
                    print("  - tencent: search")
                    print("  - google: staticmap, streetview, geocode, directions, distancematrix, elevation, timezone, ")
                    print("            findplacefromtext, autocomplete, placedetails, nearbysearch, textsearch, placephoto,")
                    print("            nearestroads, snaptoroads, speedlimits, airquality, computeroutes, aerialview,")
                    print("            addressvalidation, geolocation, firebasedynamiclinks, geminigenerate, geminimodels,")
                    print("            geminifiles, geminicached, cloudvision, cloudtranslation, customsearch, pollenforecast,")
                    print("            placesaggregate")
                    print("输入 'back' 返回上级菜单")
                    
                    key_input = input("请输入: ").strip()
                    
                    if key_input.lower() == "back":
                        break
                    
                    parts = key_input.split(',')
                    if len(parts) != 3:
                        print("格式错误，请重新输入")
                        continue
                    
                    service, api_type, key = parts
                    service = service.strip()
                    api_type = api_type.strip()
                    key = key.strip()
                    
                    # 调用检测函数
                    result = detect_key(service, api_type, key, config)
                    
                    # 显示检测结果
                    print("\n=== 检测结果 ===")
                    print(f"服务类型: {result['service']}")
                    print(f"API类型: {result['api_type']}")
                    print(f"KEY: {result['key']}")
                    print(f"状态: {result['status']}")
                    print(f"消息: {result['message']}")
                    print(f"结果数量: {result['result_count']}")
                    print(f"每千次请求成本: ${result.get('cost_per_1k', 0.0):.2f}")
                    print(f"财务风险 (100,000次请求): ${result.get('financial_risk', 0.0):.2f}")
                    
                    # 显示地理位置信息
                    if result['locations']:
                        print("\n=== 真实地理位置信息 ===")
                        for i, location in enumerate(result['locations'], 1):
                            print(f"\n位置 {i}:")
                            print(f"  类型: {location.get('type', '未知')}")
                            
                            if location['type'] == 'walking':
                                print(f"  起点: {location.get('origin', '未知')}")
                                print(f"  终点: {location.get('destination', '未知')}")
                                print(f"  距离: {location.get('distance', '未知')}米")
                                print(f"  时长: {location.get('duration', '未知')}秒")
                            elif location['type'] == 'address':
                                print(f"  坐标: {location.get('location', '未知')}")
                                print(f"  完整地址: {location.get('formatted_address', '未知')}")
                                print(f"  省份: {location.get('province', '未知')}")
                                print(f"  城市: {location.get('city', '未知')}")
                                print(f"  区县: {location.get('district', '未知')}")
                            elif location['type'] == 'route':
                                print(f"  距离: {location.get('distance', '未知')}")
                                print(f"  时长: {location.get('duration', '未知')}")
                            else:  # POI类型
                                print(f"  名称: {location.get('name', '未知')}")
                                print(f"  地址: {location.get('address', '未知')}")
                                print(f"  坐标: {location.get('location', '未知')}")
                                if 'category' in location:
                                    print(f"  分类: {location.get('category', '未知')}")
                                elif 'type' in location:
                                    print(f"  类型: {location.get('type', '未知')}")
                                if 'telephone' in location:
                                    print(f"  电话: {location.get('telephone', '未知')}")
                    
                    if result['status'] == "可用":
                        print("\n⚠️  警告：该KEY可能已泄漏，能够成功获取地理信息")
                        if result.get('financial_risk', 0.0) > 0:
                            print(f"💰 财务风险警告：该KEY可能导致 ${result.get('financial_risk', 0.0):.2f} 的损失（基于100,000次请求）")
                    else:
                        print("\n✓ 该KEY无法获取地理信息或已失效")
            
            elif choice == "3":
                # 退出程序
                print("\n退出检测工具。请遵守安全测试规范。")
                break
            
            else:
                print("无效的选择，请重新输入")
    else:
        print("测试已取消。请确保获得合法授权后再进行测试。")
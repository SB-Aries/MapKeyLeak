import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import os
import sys
import csv

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入主脚本的功能
from main import detect_key, read_key_file, API_CONFIG

class MapAPIKeyCheckerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("地图API KEY泄漏检测工具")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # 使用硬编码配置
        self.config = API_CONFIG
        
        # 创建主容器
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题
        self.create_title()
        
        # 创建功能选择标签页
        self.create_tabs()
        
        # 创建底部状态栏
        self.create_status_bar()
    
    def create_title(self):
        """创建应用标题"""
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = ttk.Label(title_frame, text="地图API KEY泄漏检测工具", font=("Arial", 16, "bold"))
        title_label.pack(side=tk.LEFT)
        
        # 添加警告标签
        warning_label = ttk.Label(title_frame, text="仅用于授权测试环境，请勿用于非法用途，一切违规操作后果与作者无关", 
                                 foreground="red", font=("Arial", 10))
        warning_label.pack(side=tk.RIGHT, padx=10)
    
    def create_tabs(self):
        """创建功能选择标签页"""
        self.tab_control = ttk.Notebook(self.main_frame)
        
        # 创建单个KEY检测标签页
        self.single_key_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.single_key_tab, text="单个KEY检测")
        self.create_single_key_detection()
        
        # 创建批量KEY检测标签页
        self.batch_key_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.batch_key_tab, text="批量KEY检测")
        self.create_batch_key_detection()
        
        # 放置标签页控件
        self.tab_control.pack(fill=tk.BOTH, expand=True)
    
    def create_single_key_detection(self):
        """创建单个KEY检测界面"""
        # 创建输入区域
        input_frame = ttk.LabelFrame(self.single_key_tab, text="输入参数", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 服务类型选择
        ttk.Label(input_frame, text="地图类型:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.service_var = tk.StringVar()
        self.service_combobox = ttk.Combobox(input_frame, textvariable=self.service_var, 
                                            values=["高德地图", "百度地图", "腾讯地图", "Google地图"], 
                                            state="readonly", width=20)
        self.service_combobox.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        self.service_combobox.current(0)  # 默认选择高德地图
        
        # API类型选择
        ttk.Label(input_frame, text="API类型:").grid(row=0, column=2, sticky=tk.W, pady=5, padx=5)
        self.api_type_var = tk.StringVar()
        self.api_type_combobox = ttk.Combobox(input_frame, textvariable=self.api_type_var, 
                                             state="readonly", width=20)
        self.api_type_combobox.grid(row=0, column=3, sticky=tk.W, pady=5, padx=5)
        
        # 根据服务类型更新API类型选项
        self.update_api_types()
        self.service_combobox.bind("<<ComboboxSelected>>", lambda event: self.update_api_types())
        
        # KEY输入
        ttk.Label(input_frame, text="API密钥:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.key_entry = ttk.Entry(input_frame, width=60)
        self.key_entry.grid(row=1, column=1, columnspan=3, sticky=tk.W, pady=5, padx=5)
        
        # 检测按钮
        self.detect_button = ttk.Button(input_frame, text="开始检测", 
                                       command=self.detect_single_key)
        self.detect_button.grid(row=2, column=1, pady=10, padx=5, sticky=tk.W)
        
        # 创建结果显示区域
        result_frame = ttk.LabelFrame(self.single_key_tab, text="检测结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        # 结果文本框
        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, width=100, height=20)
        self.result_text.pack(fill=tk.BOTH, expand=True)
    
    def update_api_types(self):
        """根据服务类型更新API类型选项"""
        service_name = self.service_var.get()
        
        # 中文服务名称到英文的映射
        service_mapping = {
            "高德地图": "amap",
            "百度地图": "baidu",
            "腾讯地图": "tencent",
            "Google地图": "google"
        }
        
        # 获取英文服务类型
        service = service_mapping.get(service_name)
        
        api_types = {
            "amap": ["WEB", "jsapi", "小程序"],
            "baidu": ["WEB", "ios"],
            "tencent": ["WEB"],
            "google": ["staticmap", "streetview", "geocode", "directions", "distancematrix", 
                      "elevation", "timezone", "findplacefromtext", "autocomplete", "placedetails",
                      "nearbysearch", "textsearch", "placephoto", "nearestroads", "snaptoroads",
                      "speedlimits", "airquality", "computeroutes", "addressvalidation", "geolocation"
                     ]
        }
        
        self.api_type_combobox['values'] = api_types.get(service, [])
        if api_types.get(service):
            self.api_type_combobox.current(0)
    
    def detect_single_key(self):
        """执行单个KEY检测"""
        # 清空结果文本框
        self.result_text.delete(1.0, tk.END)
        
        # 获取输入参数
        service_name = self.service_var.get()
        api_type = self.api_type_var.get()
        key = self.key_entry.get().strip()
        
        # 验证输入
        if not service_name or not api_type or not key:
            messagebox.showerror("错误", "请填写完整的检测参数")
            return
        
        # 中文服务名称到英文的映射
        service_mapping = {
            "高德地图": "amap",
            "百度地图": "baidu",
            "腾讯地图": "tencent",
            "Google地图": "google"
        }
        
        # 获取英文服务类型
        service = service_mapping.get(service_name)
        if not service:
            messagebox.showerror("错误", f"不支持的服务类型: {service_name}")
            return
        
        # 更新状态
        self.update_status("正在检测KEY...")
        self.detect_button.config(state=tk.DISABLED)
        self.root.update()
        
        try:
            # 调用检测函数
            result = detect_key(service, api_type, key, self.config)
            
            # 显示检测结果
            self.display_single_result(result)
        except Exception as e:
            messagebox.showerror("错误", f"检测过程中发生错误: {str(e)}")
        finally:
            # 恢复状态
            self.update_status("检测完成")
            self.detect_button.config(state=tk.NORMAL)
    
    def display_single_result(self, result):
        """显示单个KEY检测结果"""
        self.result_text.insert(tk.END, "=== 检测结果 ===\n")
        self.result_text.insert(tk.END, f"服务类型: {result['service']}\n")
        self.result_text.insert(tk.END, f"API类型: {result['api_type']}\n")
        self.result_text.insert(tk.END, f"KEY: {result['key']}\n")
        self.result_text.insert(tk.END, f"状态: {result['status']}\n")
        self.result_text.insert(tk.END, f"消息: {result['message']}\n")
        self.result_text.insert(tk.END, f"结果数量: {result['result_count']}\n")
        self.result_text.insert(tk.END, f"每千次请求成本: ${result.get('cost_per_1k', 0.0):.2f}\n")
        self.result_text.insert(tk.END, f"财务风险 (100,000次请求): ${result.get('financial_risk', 0.0):.2f}\n")
        
        # 显示地理位置信息
        if result['locations']:
            self.result_text.insert(tk.END, "\n=== 真实地理位置信息 ===\n")
            for i, location in enumerate(result['locations'], 1):
                self.result_text.insert(tk.END, f"\n位置 {i}:\n")
                self.result_text.insert(tk.END, f"  类型: {location.get('type', '未知')}\n")
                
                if location['type'] == 'walking':
                    self.result_text.insert(tk.END, f"  起点: {location.get('origin', '未知')}\n")
                    self.result_text.insert(tk.END, f"  终点: {location.get('destination', '未知')}\n")
                    self.result_text.insert(tk.END, f"  距离: {location.get('distance', '未知')}米\n")
                    self.result_text.insert(tk.END, f"  时长: {location.get('duration', '未知')}秒\n")
                elif location['type'] == 'address':
                    self.result_text.insert(tk.END, f"  坐标: {location.get('location', '未知')}\n")
                    self.result_text.insert(tk.END, f"  完整地址: {location.get('formatted_address', '未知')}\n")
                    self.result_text.insert(tk.END, f"  省份: {location.get('province', '未知')}\n")
                    self.result_text.insert(tk.END, f"  城市: {location.get('city', '未知')}\n")
                    self.result_text.insert(tk.END, f"  区县: {location.get('district', '未知')}\n")
                elif location['type'] == 'route':
                    self.result_text.insert(tk.END, f"  距离: {location.get('distance', '未知')}\n")
                    self.result_text.insert(tk.END, f"  时长: {location.get('duration', '未知')}\n")
                else:  # POI类型
                    self.result_text.insert(tk.END, f"  名称: {location.get('name', '未知')}\n")
                    self.result_text.insert(tk.END, f"  地址: {location.get('address', '未知')}\n")
                    self.result_text.insert(tk.END, f"  坐标: {location.get('location', '未知')}\n")
                    if 'category' in location:
                        self.result_text.insert(tk.END, f"  分类: {location.get('category', '未知')}\n")
                    elif 'type' in location:
                        self.result_text.insert(tk.END, f"  类型: {location.get('type', '未知')}\n")
                    if 'telephone' in location:
                        self.result_text.insert(tk.END, f"  电话: {location.get('telephone', '未知')}\n")
        
        # 添加警告信息
        if result['status'] == "可用":
            self.result_text.insert(tk.END, "\n⚠️  「+」存在API泄漏\n")
            if result.get('financial_risk', 0.0) > 0:
                self.result_text.insert(tk.END, f"💰  「+」财务风险可能导致 ${result.get('financial_risk', 0.0):.2f} 的损失（基于100,000次请求）\n")
        else:
            self.result_text.insert(tk.END, "\n✓  「-」该KEY无法或已失效\n")
    
    def create_batch_key_detection(self):
        """创建批量KEY检测界面"""
        # 创建文件选择区域
        file_frame = ttk.LabelFrame(self.batch_key_tab, text="文件选择", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 输入文件选择
        ttk.Label(file_frame, text="KEY文件:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.input_file_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.input_file_var, width=60).grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        ttk.Button(file_frame, text="浏览", command=self.browse_input_file).grid(row=0, column=2, pady=5, padx=5, sticky=tk.W)
        
        # 输出文件选择
        ttk.Label(file_frame, text="报告文件:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.output_file_var = tk.StringVar()
        self.output_file_var.set("report.csv")
        ttk.Entry(file_frame, textvariable=self.output_file_var, width=60).grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        ttk.Button(file_frame, text="浏览", command=self.browse_output_file).grid(row=1, column=2, pady=5, padx=5, sticky=tk.W)
        
        # 控制按钮
        button_frame = ttk.Frame(file_frame)
        button_frame.grid(row=2, column=1, pady=10, padx=5, sticky=tk.W)
        
        self.batch_detect_button = ttk.Button(button_frame, text="开始检测", 
                                             command=self.batch_detect_keys)
        self.batch_detect_button.pack(side=tk.LEFT, padx=5)
        
        self.export_button = ttk.Button(button_frame, text="导出结果", 
                                       command=self.export_results, state=tk.DISABLED)
        self.export_button.pack(side=tk.LEFT, padx=5)
        
        # 创建结果显示区域
        result_frame = ttk.LabelFrame(self.batch_key_tab, text="检测结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        # 结果统计区域
        stats_frame = ttk.Frame(result_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.total_label = ttk.Label(stats_frame, text="总计: 0")
        self.total_label.pack(side=tk.LEFT, padx=10)
        
        self.available_label = ttk.Label(stats_frame, text="可用: 0", foreground="green")
        self.available_label.pack(side=tk.LEFT, padx=10)
        
        self.unavailable_label = ttk.Label(stats_frame, text="不可用: 0", foreground="red")
        self.unavailable_label.pack(side=tk.LEFT, padx=10)
        
        self.error_label = ttk.Label(stats_frame, text="错误: 0", foreground="orange")
        self.error_label.pack(side=tk.LEFT, padx=10)
        
        self.invalid_label = ttk.Label(stats_frame, text="无效: 0", foreground="gray")
        self.invalid_label.pack(side=tk.LEFT, padx=10)
        
        # 详细结果文本框
        self.batch_result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, width=100, height=25)
        self.batch_result_text.pack(fill=tk.BOTH, expand=True)
        
        # 存储检测结果
        self.batch_results = []
    
    def browse_input_file(self):
        """浏览选择输入文件"""
        file_path = filedialog.askopenfilename(filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")])
        if file_path:
            self.input_file_var.set(file_path)
    
    def browse_output_file(self):
        """浏览选择输出文件"""
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")])
        if file_path:
            self.output_file_var.set(file_path)
    
    def batch_detect_keys(self):
        """执行批量KEY检测"""
        # 清空结果
        self.batch_result_text.delete(1.0, tk.END)
        self.batch_results = []
        
        # 获取输入文件路径
        input_file = self.input_file_var.get().strip()
        if not input_file:
            messagebox.showerror("错误", "请选择KEY文件")
            return
        
        # 验证文件是否存在
        if not os.path.exists(input_file):
            messagebox.showerror("错误", f"文件不存在: {input_file}")
            return
        
        # 更新状态
        self.update_status("正在读取KEY文件...")
        self.batch_detect_button.config(state=tk.DISABLED)
        self.root.update()
        
        # 读取KEY文件
        keys = read_key_file(input_file)
        if not keys:
            messagebox.showerror("错误", "未读取到有效的KEY")
            self.batch_detect_button.config(state=tk.NORMAL)
            return
        
        # 更新状态
        self.update_status(f"开始检测 {len(keys)} 个KEY...")
        self.root.update()
        
        # 开始检测
        for i, key_info in enumerate(keys):
            # 更新进度
            self.update_status(f"检测中... {i+1}/{len(keys)}")
            self.root.update()
            
            # 调用检测函数
            result = detect_key(
                key_info['service'],
                key_info['api_type'],
                key_info['key'],
                self.config
            )
            self.batch_results.append(result)
            
            # 显示当前结果
            self.display_batch_result(result)
        
        # 检测完成，更新统计信息
        self.update_batch_stats()
        
        # 更新状态
        self.update_status("批量检测完成")
        self.batch_detect_button.config(state=tk.NORMAL)
        self.export_button.config(state=tk.NORMAL)
    
    def display_batch_result(self, result):
        """显示单个批量检测结果"""
        self.batch_result_text.insert(tk.END, f"服务类型: {result['service']} | API类型: {result['api_type']} | KEY: {result['key']} | 状态: {result['status']} | 消息: {result['message']} | 财务风险: ${result.get('financial_risk', 0.0):.2f}\n")
        
        # 显示地理位置信息（如果可用）
        if result['locations'] and result['status'] == "可用":
            for i, location in enumerate(result['locations'][:2]):  # 只显示前2个位置
                if location['type'] == 'walking':
                    loc_str = f"  位置{i+1}: 步行导航-{location.get('distance', '未知')}米-{location.get('duration', '未知')}秒"
                elif location['type'] == 'address':
                    loc_str = f"  位置{i+1}: 地址-{location.get('formatted_address', '未知')}"
                elif location['type'] == 'route':
                    loc_str = f"  位置{i+1}: 路线-{location.get('distance', '未知')}-{location.get('duration', '未知')}"
                else:  # POI类型
                    loc_str = f"  位置{i+1}: POI-{location.get('name', '未知')}-{location.get('address', '未知')}"
                self.batch_result_text.insert(tk.END, f"{loc_str}\n")
    
    def update_batch_stats(self):
        """更新批量检测统计信息"""
        # 统计结果
        stats = {
            "可用": 0,
            "不可用": 0,
            "错误": 0,
            "无效": 0
        }
        
        for result in self.batch_results:
            status = result['status']
            if status in stats:
                stats[status] += 1
            else:
                stats[status] = 1
        
        # 更新标签
        self.total_label.config(text=f"总计: {len(self.batch_results)}")
        self.available_label.config(text=f"可用: {stats['可用']}")
        self.unavailable_label.config(text=f"不可用: {stats['不可用']}")
        self.error_label.config(text=f"错误: {stats['错误']}")
        self.invalid_label.config(text=f"无效: {stats['无效']}")
        
        # 添加统计结果到显示
        self.batch_result_text.insert(tk.END, "\n=== 检测结果报告 ===\n")
        self.batch_result_text.insert(tk.END, f"总计: {len(self.batch_results)} 个KEY\n")
        self.batch_result_text.insert(tk.END, f"可用: {stats['可用']}\n")
        self.batch_result_text.insert(tk.END, f"不可用: {stats['不可用']}\n")
        self.batch_result_text.insert(tk.END, f"错误: {stats['错误']}\n")
        self.batch_result_text.insert(tk.END, f"无效: {stats['无效']}\n")
    
    def export_results(self):
        """导出批量检测结果"""
        if not self.batch_results:
            messagebox.showerror("错误", "没有检测结果可导出")
            return
        
        # 获取输出文件路径
        output_file = self.output_file_var.get().strip()
        if not output_file:
            messagebox.showerror("错误", "请指定报告文件")
            return
        
        try:
            with open(output_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                # 写入表头
                writer.writerow(["服务类型", "API类型", "KEY", "状态", "消息", "结果数量", "每千次请求成本", "财务风险", "地理位置信息"])
                
                # 写入详细结果
                for result in self.batch_results:
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
                    
                    writer.writerow([
                        result['service'],
                        result['api_type'],
                        result['key'],
                        result['status'],
                        result['message'],
                        result['result_count'],
                        result.get('cost_per_1k', 0.0),
                        result.get('financial_risk', 0.0),
                        locations_str
                    ])
            
            messagebox.showinfo("成功", f"报告已生成: {output_file}")
        except Exception as e:
            messagebox.showerror("错误", f"生成报告失败: {str(e)}")
    
    def create_status_bar(self):
        """创建底部状态栏"""
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_status(self, message):
        """更新状态信息"""
        self.status_var.set(message)
        self.root.update()

def main():
    """主函数"""
    # 创建主窗口
    root = tk.Tk()
    
    # 创建GUI应用
    app = MapAPIKeyCheckerGUI(root)
    
    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    main()
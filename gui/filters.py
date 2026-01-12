"""
篩選模組 - 交易記錄篩選功能
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import calendar
from typing import List, Dict, Callable

from gui.ui_components import DateSelector

class FilterPanel:
    """篩選面板類別"""
    
    def __init__(self, parent, category_manager, on_filter_callback: Callable):
        """
        初始化篩選面板
        
        Args:
            parent: 父容器
            category_manager: 分類管理器
            on_filter_callback: 篩選回調函數
        """
        self.parent = parent
        self.category_manager = category_manager
        self.on_filter_callback = on_filter_callback
        
        self.filter_expanded = tk.BooleanVar(value=False)
        
        # 篩選變數 (日期由 DateSelector 管理內部狀態，這裡僅保留 StringVar 用於相容)
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()
        self.type_filter_var = tk.StringVar(value="全部")
        self.category_filter_var = tk.StringVar()
        # 移除關鍵字變數
        
        self.setup_ui()
    
    def setup_ui(self):
        """設定篩選界面"""
        # 篩選標題框架
        filter_title_frame = ttk.Frame(self.parent)
        filter_title_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.toggle_button = ttk.Button(filter_title_frame, text="▼ 進階篩選", 
                                       command=self.toggle_filter)
        self.toggle_button.pack(side=tk.LEFT)
        
        ttk.Button(filter_title_frame, text="清除篩選", 
                  command=self.clear_filters).pack(side=tk.LEFT, padx=(10, 0))
        
        # 快速篩選按鈕
        quick_filter_frame = ttk.Frame(filter_title_frame)
        quick_filter_frame.pack(side=tk.RIGHT)
        
        ttk.Button(quick_filter_frame, text="本月", 
                  command=self.filter_current_month).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_filter_frame, text="本週", 
                  command=self.filter_current_week).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_filter_frame, text="今日", 
                  command=self.filter_today).pack(side=tk.LEFT, padx=2)
        
        # 篩選內容框架
        self.filter_frame = ttk.LabelFrame(self.parent, text="篩選條件", padding="10")
        
        # 建立篩選控制項
        self.create_filter_controls()
    
    def create_filter_controls(self):
        """建立篩選控制項"""
        # 第一行
        row1 = ttk.Frame(self.filter_frame)
        row1.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(row1, text="起始日期:").pack(side=tk.LEFT, padx=(0, 5))
        
        # 使用自訂 DateSelector
        self.start_date_selector = DateSelector(
            row1, 
            on_date_change=lambda date: self.on_date_selected(date, 'start')
        )
        self.start_date_selector.pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Label(row1, text="結束日期:").pack(side=tk.LEFT, padx=(0, 5))
        
        # 使用自訂 DateSelector
        self.end_date_selector = DateSelector(
            row1, 
            on_date_change=lambda date: self.on_date_selected(date, 'end')
        )
        self.end_date_selector.pack(side=tk.LEFT, padx=(0, 15))
        
        # 類型選擇放在第二行，因為 DateSelector 比較寬
        
        # 第二行
        row2 = ttk.Frame(self.filter_frame)
        row2.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(row2, text="類型:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Combobox(row2, textvariable=self.type_filter_var, 
                    values=["全部", "收入", "支出"], state="readonly", width=10).pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Label(row2, text="分類:").pack(side=tk.LEFT, padx=(0, 5))
        self.category_filter_combo = ttk.Combobox(row2, textvariable=self.category_filter_var, 
                                                 state="readonly", width=15)
        self.category_filter_combo.pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Button(row2, text="套用篩選", command=self.apply_filters).pack(side=tk.LEFT, padx=(15, 0))
        
        # 綁定事件 - 即時篩選
        self.type_filter_var.trace('w', self.on_filter_change)
        self.category_filter_var.trace('w', self.on_filter_change)
        
        # 初始化分類選項
        self.update_category_filter_options()
        
        # 初始化日期變數
        self.start_date_var.set(self.start_date_selector.get_date_string())
        self.end_date_var.set(self.end_date_selector.get_date_string())
    
    def toggle_filter(self):
        """切換篩選區域顯示/隱藏"""
        if self.filter_expanded.get():
            self.filter_frame.grid_remove()
            self.toggle_button.config(text="▼ 進階篩選")
            self.filter_expanded.set(False)
        else:
            self.filter_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 10))
            self.toggle_button.config(text="▲ 進階篩選")
            self.filter_expanded.set(True)
    
    def update_category_filter_options(self):
        """更新分類篩選選項"""
        categories = self.category_manager.get_all_categories()
        category_options = ["全部分類"] + [cat['name'] for cat in categories]
        self.category_filter_combo['values'] = category_options
        self.category_filter_combo.set("全部分類")
    
    def clear_filters(self):
        """清除所有篩選條件"""
        # 重置日期為當日
        today = datetime.now().strftime('%Y-%m-%d')
        self.start_date_selector.set_date(today)
        self.end_date_selector.set_date(today)
        self.start_date_var.set(today)
        self.end_date_var.set(today)
            
        self.type_filter_var.set("全部")
        self.category_filter_var.set("全部分類")
        self.apply_filters()
    
    def filter_current_month(self):
        """篩選本月資料"""
        now = datetime.now()
        start_date = f"{now.year}-{now.month:02d}-01"
        last_day = calendar.monthrange(now.year, now.month)[1]
        end_date = f"{now.year}-{now.month:02d}-{last_day}"
        
        self.set_date_range(start_date, end_date)
        self.apply_filters()
    
    def filter_current_week(self):
        """篩選本週資料"""
        now = datetime.now()
        week_start = now - timedelta(days=now.weekday())
        week_end = week_start + timedelta(days=6)
        
        self.set_date_range(week_start.strftime('%Y-%m-%d'), week_end.strftime('%Y-%m-%d'))
        self.apply_filters()
    
    def filter_today(self):
        """篩選今日資料"""
        today = datetime.now().strftime('%Y-%m-%d')
        self.set_date_range(today, today)
        self.apply_filters()
        
    def set_date_range(self, start, end):
        """設定日期範圍"""
        self.start_date_selector.set_date(start)
        self.end_date_selector.set_date(end)
        self.start_date_var.set(start)
        self.end_date_var.set(end)
    
    def on_date_selected(self, date_str, type_):
        """當日期被選擇時"""
        if type_ == 'start':
            self.start_date_var.set(date_str)
        else:
            self.end_date_var.set(date_str)
        self.apply_filters()
    
    def on_filter_change(self, *args):
        """當篩選條件改變時（即時篩選）"""
        self.apply_filters()
    
    def apply_filters(self):
        """套用篩選條件"""
        # 轉換類型為英文
        type_map = {"全部": "all", "收入": "income", "支出": "expense"}
        selected_type = self.type_filter_var.get()
        type_value = type_map.get(selected_type, "all")
        
        filters = {
            'start_date': self.start_date_var.get().strip(),
            'end_date': self.end_date_var.get().strip(),
            'type': type_value,
            'category': self.category_filter_var.get(),
            'keyword': ""  # 已移除關鍵字篩選
        }
        
        # 呼叫回調函數
        if self.on_filter_callback:
            self.on_filter_callback(filters)
    
    def get_filter_values(self) -> Dict:
        """取得當前篩選值"""
        # 轉換類型為英文
        type_map = {"全部": "all", "收入": "income", "支出": "expense"}
        selected_type = self.type_filter_var.get()
        type_value = type_map.get(selected_type, "all")
        
        return {
            'start_date': self.start_date_var.get().strip(),
            'end_date': self.end_date_var.get().strip(),
            'type': type_value,
            'category': self.category_filter_var.get(),
            'keyword': ""
        }

"""
篩選模組 - 交易記錄篩選功能 (CustomTkinter Version)
"""

import tkinter as tk
import customtkinter as ctk
from datetime import datetime, timedelta
import calendar
from typing import List, Dict, Callable

from gui.ui_components import DateSelector, ModernButton, SPACING, COLORS, FONTS

class FilterPanel:
    """篩選面板類別"""
    
    def __init__(self, parent, category_manager, on_filter_callback: Callable, control_parent=None):
        """
        初始化篩選面板
        """
        self.parent = parent
        self.control_parent = control_parent
        self.category_manager = category_manager
        self.on_filter_callback = on_filter_callback
        
        self.filter_expanded = tk.BooleanVar(value=False)
        
        # 篩選變數
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()
        self.type_filter_var = tk.StringVar(value="全部")
        self.category_filter_var = tk.StringVar()
        
        self.setup_ui()
    
    def setup_ui(self):
        """設定篩選界面"""
        
        # 決定控制項放置的位置
        if self.control_parent:
            # 如有提供外部容器 (例如主視窗的按鈕列)
            target_frame = self.control_parent
            
            # 1. 快速篩選按鈕區 (移至最前)
            # 使用 CTkFrame
            quick_filter_frame = ctk.CTkFrame(target_frame, fg_color=COLORS['bg_primary'])
            quick_filter_frame.pack(side=tk.LEFT, padx=(0, 5))
            
            ModernButton(quick_filter_frame, text="本日", style='secondary',
                      command=self.filter_today).pack(side=tk.LEFT, padx=SPACING['xs'])
            ModernButton(quick_filter_frame, text="本週", style='secondary',
                      command=self.filter_current_week).pack(side=tk.LEFT, padx=SPACING['xs'])
            ModernButton(quick_filter_frame, text="本月", style='secondary',
                      command=self.filter_current_month).pack(side=tk.LEFT, padx=SPACING['xs'])
            ModernButton(quick_filter_frame, text="本年", style='secondary',
                      command=self.filter_current_year).pack(side=tk.LEFT, padx=SPACING['xs'])
            
            # 2. 進階篩選按鈕 (移至快速篩選之後)
            self.toggle_button = ModernButton(target_frame, text="▼ 進階篩選", style='secondary',
                                          command=self.toggle_filter)
            self.toggle_button.pack(side=tk.LEFT, padx=(SPACING['xs'], SPACING['xs']))
            
        else:
            # 舊有行為兼容 (雖然現在主要用 control_parent)
            self.toggle_button = ModernButton(self.parent, text="▼ 進階篩選", style='secondary',
                                           command=self.toggle_filter)
            self.toggle_button.pack(side=tk.LEFT)
        
        # 篩選內容框架 (原本是 LabelFrame，現在改為 Frame 因為 CTk 沒有 LabelFrame)
        # 我們手動加標題 Label 在 create_filter_controls
        self.filter_frame = ctk.CTkFrame(self.parent, fg_color=COLORS['bg_card'], corner_radius=10, border_width=1, border_color=COLORS['border'])
        
        # 建立篩選控制項
        self.create_filter_controls()
        
        # 如果是外部控制模式，初始化時就隱藏父容器以釋放空間
        # 並且不需要捕捉 grid_info，因為我們已經在 toggle_filter 中硬編碼還原位置
        if self.control_parent:
            self.parent.grid_remove()
    
    def create_filter_controls(self):
        """建立篩選控制項"""
        # 第一行 (日期)
        row1 = ctk.CTkFrame(self.filter_frame, fg_color=COLORS['bg_card']) # Inside card -> card color
        row1.pack(fill='x', padx=10, pady=(10, 5))
        
        ctk.CTkLabel(row1, text="篩選條件", font=(FONTS['heading'][0], 14, "bold"), text_color=COLORS['text_primary']).pack(side=tk.LEFT, padx=(0, 10))
        
        ctk.CTkLabel(row1, text="起始:", text_color=COLORS['text_secondary']).pack(side=tk.LEFT, padx=(0, 5))
        
        self.start_date_selector = DateSelector(
            row1, 
            on_date_change=lambda date: self.on_date_selected(date, 'start')
        )
        self.start_date_selector.pack(side=tk.LEFT, padx=(0, 15))
        
        ctk.CTkLabel(row1, text="結束:", text_color=COLORS['text_secondary']).pack(side=tk.LEFT, padx=(0, 5))
        
        self.end_date_selector = DateSelector(
            row1, 
            on_date_change=lambda date: self.on_date_selected(date, 'end')
        )
        self.end_date_selector.pack(side=tk.LEFT, padx=(0, 15))
        
        # 第二行 (類型與分類)
        row2 = ctk.CTkFrame(self.filter_frame, fg_color=COLORS['bg_card'])
        row2.pack(fill='x', padx=10, pady=(0, 10))
        
        # 為了對齊，左側留白或放標籤
        dummy_label = ctk.CTkLabel(row2, text="          ", font=(FONTS['heading'][0], 14, "bold")) # 佔位
        dummy_label.pack(side=tk.LEFT, padx=(0, 10))
        dummy_label.configure(text_color=COLORS['bg_card']) # 隱藏文字
        
        ctk.CTkLabel(row2, text="類型:", text_color=COLORS['text_secondary']).pack(side=tk.LEFT, padx=(0, 5))
        
        def on_type_change(choice):
            self.type_filter_var.set(choice)
            self.on_filter_change()

        self.type_combo = ctk.CTkComboBox(row2, variable=self.type_filter_var, 
                    values=["全部", "收入", "支出"], state="readonly", width=100, command=on_type_change)
        self.type_combo.pack(side=tk.LEFT, padx=(0, 15))
        
        ctk.CTkLabel(row2, text="分類:", text_color=COLORS['text_secondary']).pack(side=tk.LEFT, padx=(0, 5))
        
        def on_cat_change(choice):
            self.category_filter_var.set(choice)
            self.on_filter_change()

        self.category_filter_combo = ctk.CTkComboBox(row2, variable=self.category_filter_var, 
                                                 state="readonly", width=140, command=on_cat_change)
        self.category_filter_combo.pack(side=tk.LEFT, padx=(0, 15))
        
        ModernButton(row2, text="套用篩選", style='primary', command=self.apply_filters).pack(side=tk.LEFT, padx=(15, 0))
        ModernButton(row2, text="清除", style='secondary', command=self.clear_filters).pack(side=tk.LEFT, padx=(5, 0))
        
        # 初始化分類選項
        self.update_category_filter_options()
        
        # 初始化日期變數
        self.start_date_var.set(self.start_date_selector.get_date_string())
        self.end_date_var.set(self.end_date_selector.get_date_string())
    
    def toggle_filter(self):
        """切換篩選區域顯示/隱藏"""
        if self.filter_expanded.get():
            # 收起篩選
            self.filter_frame.pack_forget() # CTkFrame inside parent use pack usually? Wait, parent is grid-ed.
            # self.filter_frame 是放在 self.parent 裡的。
            # self.parent (filter_container) 本身使用 grid 在 main_window。
            # self.filter_frame 應該填滿 self.parent。
            
            self.filter_frame.pack_forget() 
            self.toggle_button.configure(text="▼ 進階篩選")
            self.filter_expanded.set(False)
            
            # 若為外部控制模式，連同父容器一起隱藏
            if self.control_parent:
                self.parent.grid_remove()
            
            # 強制更新父容器佈局
            # self.parent.winfo_toplevel().update_idletasks()
        else:
            # 展開篩選
            
            # 若為外部控制模式，先還原父容器
            if self.control_parent:
                # 直接指定 row=2，避開 grid_info 可能的失效問題
                self.parent.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 10))

            # 顯示篩選內容
            # self.parent 是一個空的 container frame。我們把 filter_frame pack 進去。
            self.filter_frame.pack(fill='both', expand=True, padx=2, pady=2)
                
            self.toggle_button.configure(text="▲ 進階篩選")
            self.filter_expanded.set(True)
            
            # 強制更新父容器佈局 (移除 update_idletasks 以減少卡頓)
            # self.parent.winfo_toplevel().update_idletasks()
    
    def update_category_filter_options(self):
        """更新分類篩選選項"""
        categories = self.category_manager.get_all_categories()
        category_options = ["全部分類"] + [cat['name'] for cat in categories]
        self.category_filter_combo.configure(values=category_options)
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
        self.type_combo.set("全部")
        self.category_filter_var.set("全部分類")
        self.category_filter_combo.set("全部分類")
        self.apply_filters()
        
    def filter_current_year(self):
        """篩選本年資料"""
        now = datetime.now()
        start_date = f"{now.year}-01-01"
        end_date = f"{now.year}-12-31"
        self.set_date_range(start_date, end_date)
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
            'keyword': "" 
        }
        
        # 呼叫回調函數
        if self.on_filter_callback:
            self.on_filter_callback(filters)
    
    def get_filter_values(self) -> Dict:
        """取得當前篩選值"""
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

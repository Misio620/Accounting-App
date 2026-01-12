"""
改進的交易對話框 - 包含日期選擇器和分類排序
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import calendar
import re


class ImprovedTransactionDialog:
    """改進的交易記錄新增/編輯對話框"""
    
    def __init__(self, parent, category_manager, transaction_manager, transaction_data=None):
        self.parent = parent
        self.category_manager = category_manager
        self.transaction_manager = transaction_manager
        self.transaction_data = transaction_data
        self.result = None
        
        # 建立對話框視窗
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("新增交易記錄" if transaction_data is None else "編輯交易記錄")
        self.dialog.geometry("400x320")  # 縮小視窗尺寸
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)
        
        self.setup_ui()
        self.center_window()
        
        if transaction_data:
            self.fill_existing_data()
    
    def center_window(self):
        """將對話框置中顯示"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (320 // 2)
        self.dialog.geometry(f"400x320+{x}+{y}")
    
    def setup_ui(self):
        """設定對話框界面"""
        main_frame = ttk.Frame(self.dialog, padding="15")  # 減少內距
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # 內容框架，用於置中
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(expand=True)
        
        # 標題
        title_text = "新增交易記錄" if self.transaction_data is None else "編輯交易記錄"
        title_label = ttk.Label(content_frame, text=title_text, font=("Arial", 12, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))  # 減少下方間距
        
        # 日期選擇（下拉選擇器）
        date_label = ttk.Label(content_frame, text="日期:")
        date_label.grid(row=1, column=0, sticky=tk.E, padx=(0, 10), pady=3)  # 減少垂直間距
        
        date_frame = ttk.Frame(content_frame)
        date_frame.grid(row=1, column=1, sticky=tk.W, pady=3)
        
        current_date = datetime.now()
        
        # 年份
        self.year_var = tk.StringVar(value=str(current_date.year))
        year_combo = ttk.Combobox(date_frame, textvariable=self.year_var, width=6, state="readonly")
        year_combo['values'] = [str(y) for y in range(2018, 2101)]
        year_combo.pack(side=tk.LEFT)
        ttk.Label(date_frame, text="年").pack(side=tk.LEFT, padx=(2, 5))
        
        # 月份
        self.month_var = tk.StringVar(value=str(current_date.month))
        month_combo = ttk.Combobox(date_frame, textvariable=self.month_var, width=4, state="readonly")
        month_combo['values'] = [str(m) for m in range(1, 13)]
        month_combo.pack(side=tk.LEFT)
        ttk.Label(date_frame, text="月").pack(side=tk.LEFT, padx=(2, 5))
        
        # 日期
        self.day_var = tk.StringVar(value=str(current_date.day))
        self.day_combo = ttk.Combobox(date_frame, textvariable=self.day_var, width=4, state="readonly")
        self.day_combo['values'] = [str(d) for d in range(1, 32)]
        self.day_combo.pack(side=tk.LEFT)
        ttk.Label(date_frame, text="日").pack(side=tk.LEFT, padx=(2, 0))
        
        # 綁定年月變化事件
        year_combo.bind('<<ComboboxSelected>>', self.update_day_options)
        month_combo.bind('<<ComboboxSelected>>', self.update_day_options)
        
        # 類型選擇
        type_label = ttk.Label(content_frame, text="類型:")
        type_label.grid(row=2, column=0, sticky=tk.E, padx=(0, 10), pady=3)
        
        self.type_var = tk.StringVar(value="expense")
        type_frame = ttk.Frame(content_frame)
        type_frame.grid(row=2, column=1, sticky=tk.W, pady=3)
        
        ttk.Radiobutton(type_frame, text="收入", variable=self.type_var, 
                       value="income", command=self.on_type_change).pack(side=tk.LEFT)
        ttk.Radiobutton(type_frame, text="支出", variable=self.type_var, 
                       value="expense", command=self.on_type_change).pack(side=tk.LEFT, padx=(20, 0))
        
        # 分類選擇
        category_label = ttk.Label(content_frame, text="分類:")
        category_label.grid(row=3, column=0, sticky=tk.E, padx=(0, 10), pady=3)
        
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(content_frame, textvariable=self.category_var, 
                                          state="readonly", width=25)
        self.category_combo.grid(row=3, column=1, sticky=tk.W, pady=3)
        
        # 金額輸入
        amount_label = ttk.Label(content_frame, text="金額:")
        amount_label.grid(row=4, column=0, sticky=tk.E, padx=(0, 10), pady=3)
        
        amount_frame = ttk.Frame(content_frame)
        amount_frame.grid(row=4, column=1, sticky=tk.W, pady=3)
        
        ttk.Label(amount_frame, text="$").pack(side=tk.LEFT)
        self.amount_var = tk.StringVar()
        amount_entry = ttk.Entry(amount_frame, textvariable=self.amount_var, width=22)
        amount_entry.pack(side=tk.LEFT, padx=(3, 0))
        
        # 備註輸入
        description_label = ttk.Label(content_frame, text="備註:")
        description_label.grid(row=5, column=0, sticky=tk.E, padx=(0, 10), pady=3)
        
        self.description_var = tk.StringVar()
        description_entry = ttk.Entry(content_frame, textvariable=self.description_var, width=30)
        description_entry.grid(row=5, column=1, sticky=tk.W, pady=3)
        
        # 按鈕區域
        button_frame = ttk.Frame(content_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=15)
        
        ttk.Button(button_frame, text="確定", command=self.on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=self.on_cancel).pack(side=tk.LEFT, padx=5)
        
        # 初始載入分類
        self.on_type_change()
        
        # 綁定 Enter 鍵
        self.dialog.bind('<Return>', lambda e: self.on_ok())
        self.dialog.bind('<Escape>', lambda e: self.on_cancel())
    
    def update_day_options(self, event=None):
        """根據年月更新日期選項"""
        try:
            year = int(self.year_var.get())
            month = int(self.month_var.get())
            
            # 計算該月的天數
            max_day = calendar.monthrange(year, month)[1]
            
            # 更新日期選項
            self.day_combo['values'] = [str(d) for d in range(1, max_day + 1)]
            
            # 如果當前選擇的日期超過該月最大天數，調整為最大天數
            current_day = int(self.day_var.get())
            if current_day > max_day:
                self.day_var.set(str(max_day))
        except:
            pass
    
    def on_type_change(self):
        """當類型改變時更新分類選項（按 ID 排序）"""
        transaction_type = self.type_var.get()
        categories = self.category_manager.get_categories_by_type(transaction_type)
        
        # 按分類 ID 排序（ID 通常是按建立順序，如 1, 2, 3...）
        sorted_categories = sorted(categories, key=lambda cat: cat['id'])
        category_names = [f"{cat['id']}: {cat['name']}" for cat in sorted_categories]
        self.category_combo['values'] = category_names
        
        if category_names:
            self.category_combo.set(category_names[0])
    
    def fill_existing_data(self):
        """填入現有交易資料（編輯模式）"""
        data = self.transaction_data
        
        # 解析日期
        date_parts = data['date'].split('-')
        if len(date_parts) == 3:
            self.year_var.set(date_parts[0])
            self.month_var.set(str(int(date_parts[1])))  # 移除前導零
            self.day_var.set(str(int(date_parts[2])))    # 移除前導零
        
        self.type_var.set(data['type'])
        self.amount_var.set(str(data['amount']))
        self.description_var.set(data.get('description', ''))
        
        self.on_type_change()
        
        # 設定對應的分類
        categories = self.category_manager.get_categories_by_type(data['type'])
        for cat in categories:
            if cat['name'] == data['category_name']:
                self.category_combo.set(f"{cat['id']}: {cat['name']}")
                break
    
    def validate_input(self):
        """驗證輸入資料"""
        # 驗證類型
        if not self.type_var.get():
            messagebox.showerror("錯誤", "請選擇類型")
            return False
        
        # 驗證分類
        if not self.category_var.get():
            messagebox.showerror("錯誤", "請選擇分類")
            return False
        
        # 驗證金額
        amount_str = self.amount_var.get().strip()
        if not amount_str:
            messagebox.showerror("錯誤", "請輸入金額")
            return False
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("錯誤", "金額必須大於 0")
                return False
        except ValueError:
            messagebox.showerror("錯誤", "金額格式錯誤")
            return False
        
        return True
    
    def on_ok(self):
        """確定按鈕處理"""
        if not self.validate_input():
            return
        
        try:
            # 組合日期
            year = self.year_var.get()
            month = self.month_var.get().zfill(2)  # 補零
            day = self.day_var.get().zfill(2)      # 補零
            date = f"{year}-{month}-{day}"
            
            category_id = int(self.category_var.get().split(':')[0])
            
            self.result = {
                'date': date,
                'type': self.type_var.get(),
                'category_id': category_id,
                'amount': float(self.amount_var.get().strip()),
                'description': self.description_var.get().strip()
            }
            
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("錯誤", f"資料處理失敗：{str(e)}")
    
    def on_cancel(self):
        """取消按鈕處理"""
        self.result = None
        self.dialog.destroy()

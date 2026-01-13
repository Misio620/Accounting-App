"""
改進的交易對話框 - 包含日期選擇器和分類排序 (CustomTkinter Version)
"""

import tkinter as tk
import customtkinter as ctk
from datetime import datetime
import calendar
from .ui_config import COLORS, FONTS, SPACING, PADDING, ICONS

class ImprovedTransactionDialog:
    """改進的交易記錄新增/編輯對話框 (Modern Style)"""
    
    def __init__(self, parent, category_manager, transaction_manager, transaction_data=None):
        self.parent = parent
        self.category_manager = category_manager
        self.transaction_manager = transaction_manager
        self.transaction_data = transaction_data
        self.result = None
        
        # 建立對話框視窗 (CTkToplevel)
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("新增交易" if transaction_data is None else "編輯交易")
        self.dialog.geometry("450x550")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)
        
        # 確保視窗在最上層
        self.dialog.lift()
        self.dialog.focus_force()
        
        self.setup_ui()
        self.center_window()
        
        if transaction_data:
            self.fill_existing_data()

    def center_window(self):
        """將對話框置中顯示"""
        self.dialog.update_idletasks()
        width = 450
        height = 550
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_ui(self):
        """設定對話框界面"""
        # 主背景
        self.main_frame = ctk.CTkFrame(self.dialog, corner_radius=0, fg_color=COLORS['bg_card'])
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # 標題
        title_text = "新增交易記錄" if self.transaction_data is None else "編輯交易記錄"
        ctk.CTkLabel(
            self.main_frame, 
            text=title_text, 
            font=(FONTS['heading'][0], 20, "bold"),
            text_color=COLORS['text_primary']
        ).pack(pady=(0, 20))
        
        # 1. 日期選擇區
        date_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        date_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(date_frame, text="日期", font=FONTS['body'], width=60, anchor="w").pack(side="left")
        
        current_date = datetime.now()
        
        # 年 (ComboBox)
        self.year_var = tk.StringVar(value=str(current_date.year))
        self.year_combo = ctk.CTkComboBox(
            date_frame, 
            variable=self.year_var, 
            width=80, 
            values=[str(y) for y in range(2020, 2031)],
            command=self.update_day_options
        )
        self.year_combo.pack(side="left", padx=(0, 5))
        
        # 月
        self.month_var = tk.StringVar(value=str(current_date.month))
        self.month_combo = ctk.CTkComboBox(
            date_frame, 
            variable=self.month_var, 
            width=60, 
            values=[str(m) for m in range(1, 13)],
            command=self.update_day_options
        )
        self.month_combo.pack(side="left", padx=(0, 5))
        
        # 日
        self.day_var = tk.StringVar(value=str(current_date.day))
        self.day_combo = ctk.CTkComboBox(
            date_frame, 
            variable=self.day_var, 
            width=60, 
            values=[str(d) for d in range(1, 32)]
        )
        self.day_combo.pack(side="left")

        # 2. 類型選擇
        type_frame_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        type_frame_container.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(type_frame_container, text="類型", font=FONTS['body'], width=60, anchor="w").pack(side="left")
        
        self.type_var = tk.StringVar(value="expense")
        # Radio Buttons
        self.rb_expense = ctk.CTkRadioButton(
            type_frame_container, 
            text="支出", 
            variable=self.type_var, 
            value="expense",
            fg_color=COLORS['danger'],
            command=self.on_type_change
        )
        self.rb_expense.pack(side="left", padx=(0, 20))
        
        self.rb_income = ctk.CTkRadioButton(
            type_frame_container, 
            text="收入", 
            variable=self.type_var, 
            value="income",
            fg_color=COLORS['success'],
            command=self.on_type_change
        )
        self.rb_income.pack(side="left")

        # 3. 分類選擇
        cat_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        cat_frame.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(cat_frame, text="分類", font=FONTS['body'], width=60, anchor="w").pack(side="left")
        
        self.category_var = tk.StringVar()
        self.category_combo = ctk.CTkComboBox(
            cat_frame, 
            variable=self.category_var, 
            width=250,
            state="readonly"
        )
        self.category_combo.pack(side="left", fill="x", expand=True)

        # 4. 金額輸入
        amount_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        amount_frame.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(amount_frame, text="金額", font=FONTS['body'], width=60, anchor="w").pack(side="left")
        
        self.amount_var = tk.StringVar()
        self.amount_entry = ctk.CTkEntry(
            amount_frame, 
            textvariable=self.amount_var, 
            width=250,
            placeholder_text="輸入金額"
        )
        self.amount_entry.pack(side="left", fill="x", expand=True)

        # 5. 備註輸入
        desc_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        desc_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(desc_frame, text="備註", font=FONTS['body'], width=60, anchor="w").pack(side="left")
        
        self.description_var = tk.StringVar()
        self.description_entry = ctk.CTkEntry(
            desc_frame, 
            textvariable=self.description_var, 
            width=250,
            placeholder_text="輸入備註 (選填)"
        )
        self.description_entry.pack(side="left", fill="x", expand=True)

        # 按鈕區域
        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(20, 0))
        
        ctk.CTkButton(
            btn_frame, 
            text="確定", 
            command=self.on_ok,
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_dark'],
            width=100
        ).pack(side="left", padx=(60, 10))
        
        ctk.CTkButton(
            btn_frame, 
            text="取消", 
            command=self.on_cancel,
            fg_color="transparent",
            border_width=1,
            border_color=COLORS['text_secondary'],
            text_color=COLORS['text_primary'],
            width=100
        ).pack(side="left", padx=10)

        # Init functionality
        self.on_type_change()
        
        # Bindings
        # CTk doesn't support bind <Return> on Toplevel consistently, but we can try on entries
        self.amount_entry.bind('<Return>', lambda e: self.on_ok())
        self.description_entry.bind('<Return>', lambda e: self.on_ok())

    def update_day_options(self, event=None):
        try:
            year = int(self.year_var.get())
            month = int(self.month_var.get())
            max_day = calendar.monthrange(year, month)[1]
            # Update values
            new_values = [str(d) for d in range(1, max_day + 1)]
            self.day_combo.configure(values=new_values)
            
            current_day = int(self.day_var.get())
            if current_day > max_day:
                self.day_var.set(str(max_day))
        except:
            pass

    def on_type_change(self):
        transaction_type = self.type_var.get()
        categories = self.category_manager.get_categories_by_type(transaction_type)
        sorted_categories = sorted(categories, key=lambda cat: cat['id'])
        category_names = [f"{cat['id']}: {cat['name']}" for cat in sorted_categories]
        
        self.category_combo.configure(values=category_names)
        if category_names:
            self.category_combo.set(category_names[0])
        else:
            self.category_combo.set("無分類")

    def fill_existing_data(self):
        data = self.transaction_data
        date_parts = data['date'].split('-')
        if len(date_parts) == 3:
            self.year_var.set(date_parts[0])
            self.month_var.set(str(int(date_parts[1])))
            self.day_var.set(str(int(date_parts[2])))
        
        self.type_var.set(data['type'])
        self.amount_var.set(str(data['amount']))
        self.description_var.set(data.get('description', ''))
        
        self.on_type_change() # refresh categories
        
        # Set category
        target_cat = f"{data.get('category_id', '?')}: {data.get('category_name', '?')}"
        # Try to find exact match in current values
        current_values = self.category_combo.cget('values') # cget might not work for values list in CTk?
        # CTkComboBox uses .values
        # But we already set values in on_type_change.
        # Just loop and set
        
        # Wait, data usually has 'category_name' but `on_type_change` sets "ID: Name".
        for val in self.category_combo._values: # access internal list or configured list
            if val.endswith(f": {data.get('category_name', '')}"):
                self.category_combo.set(val)
                break
    
    def on_ok(self):
        try:
            # Validation
            amount_str = self.amount_var.get().strip()
            if not amount_str:
                tk.messagebox.showerror("錯誤", "請輸入金額")
                return
            amount = float(amount_str)
            if amount <= 0:
                tk.messagebox.showerror("錯誤", "金額必須大於 0")
                return
                
            if not self.category_var.get():
                tk.messagebox.showerror("錯誤", "請選擇分類")
                return
                
            # Date
            year = self.year_var.get()
            month = self.month_var.get().zfill(2)
            day = self.day_var.get().zfill(2)
            date = f"{year}-{month}-{day}"
            
            category_id = int(self.category_var.get().split(':')[0])
            
            self.result = {
                'date': date,
                'type': self.type_var.get(),
                'category_id': category_id,
                'amount': amount,
                'description': self.description_var.get().strip()
            }
            self.dialog.destroy()
            
        except ValueError:
             tk.messagebox.showerror("錯誤", "金額格式錯誤")
        except Exception as e:
             tk.messagebox.showerror("錯誤", f"發生錯誤: {e}")

    def on_cancel(self):
        self.result = None
        self.dialog.destroy()

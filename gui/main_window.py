"""
記帳應用程式 - 主視窗界面（乾淨版本）
使用 tkinter 建立桌面應用程式界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from datetime import datetime
import sys
import os
import csv
import json
from collections import defaultdict
import calendar

# 圖表相關 imports
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    
    # 設定中文字體
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# 將專案根目錄加入路徑
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.models import DatabaseManager, CategoryManager, TransactionManager

class TransactionDialog:
    """交易記錄新增/編輯對話框"""
    
    def __init__(self, parent, category_manager, transaction_manager, transaction_data=None):
        self.parent = parent
        self.category_manager = category_manager
        self.transaction_manager = transaction_manager
        self.transaction_data = transaction_data
        self.result = None
        
        # 建立對話框視窗
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("新增交易記錄" if transaction_data is None else "編輯交易記錄")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
        self.center_window()
        
        if transaction_data:
            self.fill_existing_data()
    
    def center_window(self):
        """將對話框置中顯示"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (300 // 2)
        self.dialog.geometry(f"400x300+{x}+{y}")
    
    def setup_ui(self):
        """設定對話框界面"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 日期選擇
        ttk.Label(main_frame, text="日期:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        ttk.Entry(main_frame, textvariable=self.date_var, width=15).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # 類型選擇
        ttk.Label(main_frame, text="類型:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.type_var = tk.StringVar(value="expense")
        type_frame = ttk.Frame(main_frame)
        type_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Radiobutton(type_frame, text="收入", variable=self.type_var, 
                       value="income", command=self.on_type_change).pack(side=tk.LEFT)
        ttk.Radiobutton(type_frame, text="支出", variable=self.type_var, 
                       value="expense", command=self.on_type_change).pack(side=tk.LEFT, padx=(20, 0))
        
        # 分類選擇
        ttk.Label(main_frame, text="分類:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(main_frame, textvariable=self.category_var, 
                                         state="readonly", width=20)
        self.category_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # 金額輸入
        ttk.Label(main_frame, text="金額:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.amount_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.amount_var, width=15).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # 備註輸入
        ttk.Label(main_frame, text="備註:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.description_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.description_var, width=30).grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # 按鈕區域
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="確定", command=self.on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=self.on_cancel).pack(side=tk.LEFT, padx=5)
        
        main_frame.columnconfigure(1, weight=1)
        self.on_type_change()
    
    def on_type_change(self):
        """當類型改變時更新分類選項"""
        transaction_type = self.type_var.get()
        categories = self.category_manager.get_categories_by_type(transaction_type)
        
        category_names = [f"{cat['id']}: {cat['name']}" for cat in categories]
        self.category_combo['values'] = category_names
        
        if category_names:
            self.category_combo.set(category_names[0])
    
    def fill_existing_data(self):
        """填入現有交易資料（編輯模式）"""
        data = self.transaction_data
        self.date_var.set(data['date'])
        self.type_var.set(data['type'])
        self.amount_var.set(str(data['amount']))
        self.description_var.set(data.get('description', ''))
        
        self.on_type_change()
        
        categories = self.category_manager.get_categories_by_type(data['type'])
        for cat in categories:
            if cat['name'] == data['category_name']:
                self.category_combo.set(f"{cat['id']}: {cat['name']}")
                break
    
    def on_ok(self):
        """確定按鈕處理"""
        try:
            if not all([self.date_var.get(), self.type_var.get(), 
                       self.category_var.get(), self.amount_var.get().strip()]):
                messagebox.showerror("錯誤", "請填寫所有必要欄位")
                return
            
            try:
                amount = float(self.amount_var.get().strip())
                if amount <= 0:
                    messagebox.showerror("錯誤", "金額必須大於 0")
                    return
            except ValueError:
                messagebox.showerror("錯誤", "金額格式錯誤")
                return
            
            category_id = int(self.category_var.get().split(':')[0])
            
            self.result = {
                'date': self.date_var.get(),
                'type': self.type_var.get(),
                'category_id': category_id,
                'amount': amount,
                'description': self.description_var.get()
            }
            
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("錯誤", f"輸入驗證失敗：{str(e)}")
    
    def on_cancel(self):
        """取消按鈕處理"""
        self.result = None
        self.dialog.destroy()

class MainWindow:
    """主視窗類別"""
    
    def __init__(self):
        # 初始化資料庫
        self.db_manager = DatabaseManager("accounting.db")
        self.category_manager = CategoryManager(self.db_manager)
        self.transaction_manager = TransactionManager(self.db_manager)
        
        # 建立主視窗
        self.root = tk.Tk()
        self.root.title("個人記帳本")
        self.root.geometry("900x800")
        
        self.current_transactions = []
        
        self.setup_ui()
        self.refresh_data()
    
    def setup_ui(self):
        """設定主界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 標題
        ttk.Label(main_frame, text="個人記帳本", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=3, pady=10)
        
        # 按鈕區域
        self.setup_buttons(main_frame)
        
        # 篩選區域
        self.setup_filters(main_frame)
        
        # 交易記錄列表
        self.setup_transaction_list(main_frame)
        
        # 統計區域
        self.setup_statistics(main_frame)
        
        # 報表區域
        self.setup_reports(main_frame)
        
        # 設定網格權重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        main_frame.rowconfigure(5, weight=1)
    
    def setup_buttons(self, parent):
        """設定按鈕區域"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(button_frame, text="新增交易", command=self.add_transaction).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="編輯交易", command=self.edit_transaction).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刪除交易", command=self.delete_transaction).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="重新整理", command=self.refresh_data).pack(side=tk.LEFT, padx=20)
        
        # 匯出功能按鈕
        export_frame = ttk.Frame(button_frame)
        export_frame.pack(side=tk.RIGHT)
        
        ttk.Button(export_frame, text="匯出 CSV", command=self.export_to_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(export_frame, text="匯出 Excel", command=self.export_to_excel).pack(side=tk.LEFT, padx=5)
    
    def setup_filters(self, parent):
        """設定篩選區域"""
        # 篩選標題框架
        filter_title_frame = ttk.Frame(parent)
        filter_title_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.filter_expanded = tk.BooleanVar(value=False)
        self.toggle_button = ttk.Button(filter_title_frame, text="▼ 進階篩選", command=self.toggle_filter)
        self.toggle_button.pack(side=tk.LEFT)
        
        ttk.Button(filter_title_frame, text="清除篩選", command=self.clear_filters).pack(side=tk.LEFT, padx=(10, 0))
        
        # 篩選內容框架
        self.filter_frame = ttk.LabelFrame(parent, text="篩選條件", padding="10")
        
        # 建立篩選控制項
        self.create_filter_controls()
    
    def create_filter_controls(self):
        """建立篩選控制項"""
        # 第一行
        row1 = ttk.Frame(self.filter_frame)
        row1.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(row1, text="起始日期:").pack(side=tk.LEFT, padx=(0, 5))
        self.start_date_var = tk.StringVar()
        ttk.Entry(row1, textvariable=self.start_date_var, width=12).pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Label(row1, text="結束日期:").pack(side=tk.LEFT, padx=(0, 5))
        self.end_date_var = tk.StringVar()
        ttk.Entry(row1, textvariable=self.end_date_var, width=12).pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Label(row1, text="類型:").pack(side=tk.LEFT, padx=(0, 5))
        self.type_filter_var = tk.StringVar(value="all")
        ttk.Combobox(row1, textvariable=self.type_filter_var, 
                    values=["all", "income", "expense"], state="readonly", width=10).pack(side=tk.LEFT)
        
        # 第二行
        row2 = ttk.Frame(self.filter_frame)
        row2.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(row2, text="分類:").pack(side=tk.LEFT, padx=(0, 5))
        self.category_filter_var = tk.StringVar()
        self.category_filter_combo = ttk.Combobox(row2, textvariable=self.category_filter_var, 
                                                 state="readonly", width=15)
        self.category_filter_combo.pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Label(row2, text="關鍵字:").pack(side=tk.LEFT, padx=(0, 5))
        self.keyword_var = tk.StringVar()
        ttk.Entry(row2, textvariable=self.keyword_var, width=20).pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Button(row2, text="套用篩選", command=self.apply_filters).pack(side=tk.LEFT, padx=(15, 0))
        
        # 綁定事件
        self.keyword_var.trace('w', self.on_filter_change)
        self.type_filter_var.trace('w', self.on_filter_change)
        self.category_filter_var.trace('w', self.on_filter_change)
    
    def setup_transaction_list(self, parent):
        """設定交易記錄列表"""
        list_frame = ttk.LabelFrame(parent, text="交易記錄", padding="5")
        list_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        columns = ('日期', '類型', '分類', '金額', '備註')
        self.transaction_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.transaction_tree.heading(col, text=col)
        
        self.transaction_tree.column('日期', width=100)
        self.transaction_tree.column('類型', width=80)
        self.transaction_tree.column('分類', width=100)
        self.transaction_tree.column('金額', width=100)
        self.transaction_tree.column('備註', width=200)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.transaction_tree.yview)
        self.transaction_tree.configure(yscrollcommand=scrollbar.set)
        
        self.transaction_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
    
    def setup_statistics(self, parent):
        """設定統計區域"""
        stats_frame = ttk.LabelFrame(parent, text="本月統計", padding="10")
        stats_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.income_label = ttk.Label(stats_frame, text="本月收入: $0.00", font=("Arial", 10))
        self.income_label.grid(row=0, column=0, padx=20)
        
        self.expense_label = ttk.Label(stats_frame, text="本月支出: $0.00", font=("Arial", 10))
        self.expense_label.grid(row=0, column=1, padx=20)
        
        self.balance_label = ttk.Label(stats_frame, text="本月結餘: $0.00", font=("Arial", 10, "bold"))
        self.balance_label.grid(row=0, column=2, padx=20)
    
    def setup_reports(self, parent):
        """設定報表區域"""
        report_frame = ttk.LabelFrame(parent, text="統計報表", padding="10")
        report_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # 報表類型選擇
        button_frame = ttk.Frame(report_frame)
        button_frame.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.current_report_type = tk.StringVar(value="year_category")
        
        ttk.Radiobutton(button_frame, text="年分類", variable=self.current_report_type, 
                       value="year_category", command=self.update_report).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(button_frame, text="月分類", variable=self.current_report_type, 
                       value="month_category", command=self.update_report).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(button_frame, text="月收支", variable=self.current_report_type, 
                       value="month_income_expense", command=self.update_report).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(button_frame, text="日收支", variable=self.current_report_type, 
                       value="daily_income_expense", command=self.update_report).pack(side=tk.LEFT, padx=10)
        
        # 時間控制
        control_frame = ttk.Frame(report_frame)
        control_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(control_frame, text="年份:").pack(side=tk.LEFT, padx=(0, 5))
        self.year_var = tk.StringVar(value=str(datetime.now().year))
        year_combo = ttk.Combobox(control_frame, textvariable=self.year_var, width=8, state="readonly")
        
        current_year = datetime.now().year
        year_options = [str(year) for year in range(current_year - 5, current_year + 2)]
        year_combo['values'] = year_options
        year_combo.pack(side=tk.LEFT, padx=(0, 15))
        year_combo.bind('<<ComboboxSelected>>', lambda e: self.update_report())
        
        ttk.Label(control_frame, text="月份:").pack(side=tk.LEFT, padx=(0, 5))
        self.month_var = tk.StringVar(value=str(datetime.now().month))
        month_combo = ttk.Combobox(control_frame, textvariable=self.month_var, width=8, state="readonly")
        month_combo['values'] = [str(i) for i in range(1, 13)]
        month_combo.pack(side=tk.LEFT, padx=(0, 15))
        month_combo.bind('<<ComboboxSelected>>', lambda e: self.update_report())
        
        ttk.Button(control_frame, text="更新報表", command=self.update_report).pack(side=tk.LEFT, padx=15)
        
        # 報表顯示區域
        self.report_display_frame = ttk.Frame(report_frame)
        self.report_display_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        report_frame.columnconfigure(3, weight=1)
        report_frame.rowconfigure(2, weight=1)
        
        self.update_report()
    
    def update_report(self):
        """更新報表顯示"""
        report_type = self.current_report_type.get()
        
        if report_type == "year_category":
            self.show_year_category_chart()
        elif report_type == "month_category":
            self.show_month_category_chart()
        elif report_type == "month_income_expense":
            self.show_month_income_expense_chart()
        elif report_type == "daily_income_expense":
            self.show_daily_income_expense_chart()
    
    def show_year_category_chart(self):
        """顯示年度分類圓餅圖"""
        for widget in self.report_display_frame.winfo_children():
            widget.destroy()
        
        if not MATPLOTLIB_AVAILABLE:
            ttk.Label(self.report_display_frame, text="需要安裝 matplotlib 套件", 
                     font=("Arial", 12)).pack(pady=20)
            ttk.Label(self.report_display_frame, text="執行: pip install matplotlib").pack()
            return
        
        year = int(self.year_var.get())
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        transactions = self.transaction_manager.get_transactions_by_date_range(start_date, end_date)
        
        if not transactions:
            ttk.Label(self.report_display_frame, text="無資料可顯示", 
                     font=("Arial", 12)).pack(pady=20)
            return
        
        # 建立圖表
        fig = Figure(figsize=(12, 6), dpi=80)
        
        if expense_stats:
            ax1 = fig.add_subplot(121)
            
            sorted_expenses = sorted(expense_stats.items(), key=lambda x: x[1], reverse=True)
            labels = [cat for cat, _ in sorted_expenses]
            sizes = [amount for _, amount in sorted_expenses]
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3', '#54A0FF', '#5F27CD']
            
            ax1.pie(sizes, labels=labels, colors=colors[:len(labels)], autopct='%1.1f%%', startangle=90)
            ax1.set_title(f'{month}月支出分類', fontsize=12, fontweight='bold')
        
        if income_stats:
            ax2 = fig.add_subplot(122)
            
            sorted_income = sorted(income_stats.items(), key=lambda x: x[1], reverse=True)
            labels = [cat for cat, _ in sorted_income]
            sizes = [amount for _, amount in sorted_income]
            colors = ['#28a745', '#20c997', '#17a2b8', '#6f42c1', '#e83e8c', '#fd7e14']
            
            ax2.pie(sizes, labels=labels, colors=colors[:len(labels)], autopct='%1.1f%%', startangle=90)
            ax2.set_title(f'{month}月收入分類', fontsize=12, fontweight='bold')
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.report_display_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 統計摘要
        total_income = sum(income_stats.values())
        total_expense = sum(expense_stats.values())
        
        summary_frame = ttk.Frame(self.report_display_frame)
        summary_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(summary_frame, text=f"收入: ${total_income:.2f}", 
                 foreground="green").pack(side=tk.LEFT, padx=20)
        ttk.Label(summary_frame, text=f"支出: ${total_expense:.2f}", 
                 foreground="red").pack(side=tk.LEFT, padx=20)
        ttk.Label(summary_frame, text=f"結餘: ${total_income - total_expense:.2f}").pack(side=tk.LEFT, padx=20)
    
    def show_month_income_expense_chart(self):
        """顯示月度收支長條圖"""
        for widget in self.report_display_frame.winfo_children():
            widget.destroy()
        
        if not MATPLOTLIB_AVAILABLE:
            ttk.Label(self.report_display_frame, text="需要安裝 matplotlib 套件").pack(pady=20)
            return
        
        year = int(self.year_var.get())
        
        # 收集12個月的資料
        months_labels = []
        income_data = []
        expense_data = []
        
        for month in range(1, 13):
            summary = self.transaction_manager.get_monthly_summary(year, month)
            
            if summary['total_income'] > 0 or summary['total_expense'] > 0:
                months_labels.append(f"{month}月")
                income_data.append(summary['total_income'])
                expense_data.append(summary['total_expense'])
        
        if not months_labels:
            ttk.Label(self.report_display_frame, text="無資料可顯示").pack(pady=20)
            return
        
        # 建立圖表
        fig = Figure(figsize=(12, 6), dpi=80)
        ax = fig.add_subplot(111)
        
        x = range(len(months_labels))
        width = 0.35
        
        bars1 = ax.bar([i - width/2 for i in x], income_data, width, label='收入', color='#28a745', alpha=0.8)
        bars2 = ax.bar([i + width/2 for i in x], expense_data, width, label='支出', color='#dc3545', alpha=0.8)
        
        # 在柱子上顯示數值
        for bar in bars1:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + max(income_data + expense_data) * 0.01,
                       f'${height:.0f}', ha='center', va='bottom', fontsize=8)
        
        for bar in bars2:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + max(income_data + expense_data) * 0.01,
                       f'${height:.0f}', ha='center', va='bottom', fontsize=8)
        
        ax.set_title(f'{year}年月度收支對比', fontsize=14, fontweight='bold')
        ax.set_xlabel('月份', fontsize=12)
        ax.set_ylabel('金額 (元)', fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels(months_labels)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.report_display_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 統計摘要
        total_income = sum(income_data)
        total_expense = sum(expense_data)
        
        summary_frame = ttk.Frame(self.report_display_frame)
        summary_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(summary_frame, text=f"年度收入: ${total_income:.2f}", 
                 foreground="green").pack(side=tk.LEFT, padx=20)
        ttk.Label(summary_frame, text=f"年度支出: ${total_expense:.2f}", 
                 foreground="red").pack(side=tk.LEFT, padx=20)
        ttk.Label(summary_frame, text=f"年度結餘: ${total_income - total_expense:.2f}").pack(side=tk.LEFT, padx=20)
    
    def show_daily_income_expense_chart(self):
        """顯示日度收支長條圖"""
        for widget in self.report_display_frame.winfo_children():
            widget.destroy()
        
        if not MATPLOTLIB_AVAILABLE:
            ttk.Label(self.report_display_frame, text="需要安裝 matplotlib 套件").pack(pady=20)
            return
        
        year = int(self.year_var.get())
        month = int(self.month_var.get())
        
        start_date = f"{year}-{month:02d}-01"
        last_day = calendar.monthrange(year, month)[1]
        end_date = f"{year}-{month:02d}-{last_day}"
        
        transactions = self.transaction_manager.get_transactions_by_date_range(start_date, end_date)
        
        if not transactions:
            ttk.Label(self.report_display_frame, text="本月無交易資料").pack(pady=20)
            return
        
        # 統計每日資料
        daily_stats = defaultdict(lambda: {'income': 0, 'expense': 0})
        
        for trans in transactions:
            date = trans['date']
            daily_stats[date][trans['type']] += trans['amount']
        
        # 準備資料
        dates = sorted(daily_stats.keys())
        days = [int(date.split('-')[2]) for date in dates]
        income_data = [daily_stats[date]['income'] for date in dates]
        expense_data = [daily_stats[date]['expense'] for date in dates]
        
        # 建立圖表
        fig = Figure(figsize=(12, 6), dpi=80)
        ax = fig.add_subplot(111)
        
        x = range(len(days))
        width = 0.35
        
        bars1 = ax.bar([i - width/2 for i in x], income_data, width, label='收入', color='#28a745', alpha=0.8)
        bars2 = ax.bar([i + width/2 for i in x], expense_data, width, label='支出', color='#dc3545', alpha=0.8)
        
        # 在柱子上顯示數值
        max_value = max(max(income_data) if income_data else [0], max(expense_data) if expense_data else [0])
        for i, (income, expense) in enumerate(zip(income_data, expense_data)):
            if income > 0:
                ax.text(i - width/2, income + max_value * 0.01,
                       f'${income:.0f}', ha='center', va='bottom', fontsize=7, rotation=90)
            if expense > 0:
                ax.text(i + width/2, expense + max_value * 0.01,
                       f'${expense:.0f}', ha='center', va='bottom', fontsize=7, rotation=90)
        
        ax.set_title(f'{year}年{month}月每日收支', fontsize=14, fontweight='bold')
        ax.set_xlabel('日期', fontsize=12)
        ax.set_ylabel('金額 (元)', fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels([f"{day}日" for day in days], rotation=45)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.report_display_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 統計摘要
        total_income = sum(income_data)
        total_expense = sum(expense_data)
        
        summary_frame = ttk.Frame(self.report_display_frame)
        summary_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(summary_frame, text=f"本月收入: ${total_income:.2f}", 
                 foreground="green").pack(side=tk.LEFT, padx=20)
        ttk.Label(summary_frame, text=f"本月支出: ${total_expense:.2f}", 
                 foreground="red").pack(side=tk.LEFT, padx=20)
        ttk.Label(summary_frame, text=f"本月結餘: ${total_income - total_expense:.2f}").pack(side=tk.LEFT, padx=20)
    
    # 篩選功能方法
    def toggle_filter(self):
        """切換篩選區域顯示/隱藏"""
        if self.filter_expanded.get():
            self.filter_frame.grid_remove()
            self.toggle_button.config(text="▼ 進階篩選")
            self.filter_expanded.set(False)
        else:
            self.filter_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 10))
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
        self.start_date_var.set("")
        self.end_date_var.set("")
        self.type_filter_var.set("all")
        self.category_filter_var.set("全部分類")
        self.keyword_var.set("")
        self.refresh_data()
    
    def on_filter_change(self, *args):
        """當篩選條件改變時（即時篩選）"""
        self.apply_filters()
    
    def apply_filters(self):
        """套用篩選條件"""
        start_date = self.start_date_var.get().strip()
        end_date = self.end_date_var.get().strip()
        transaction_type = self.type_filter_var.get()
        category_filter = self.category_filter_var.get()
        keyword = self.keyword_var.get().strip().lower()
        
        transactions = self.transaction_manager.get_transactions(limit=1000)
        
        filtered_transactions = []
        for trans in transactions:
            if start_date and trans['date'] < start_date:
                continue
            if end_date and trans['date'] > end_date:
                continue
            if transaction_type != "all" and trans['type'] != transaction_type:
                continue
            if category_filter != "全部分類" and trans['category_name'] != category_filter:
                continue
            if keyword and keyword not in str(trans.get('description', '')).lower():
                continue
            
            filtered_transactions.append(trans)
        
        self.display_filtered_transactions(filtered_transactions)
    
    def display_filtered_transactions(self, transactions):
        """顯示篩選後的交易記錄"""
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)
        
        self.current_transactions = transactions
        
        for trans in transactions:
            amount_display = f"${trans['amount']:.2f}"
            if trans['type'] == 'income':
                amount_display = f"+{amount_display}"
            else:
                amount_display = f"-{amount_display}"
            
            type_display = "收入" if trans['type'] == 'income' else "支出"
            
            self.transaction_tree.insert('', 'end', values=(
                trans['date'],
                type_display,
                trans['category_name'],
                amount_display,
                trans.get('description', '')
            ), tags=(str(trans['id']),))
        
        self.update_filtered_statistics(transactions)
    
    def refresh_data(self):
        """重新整理資料顯示"""
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)
        
        transactions = self.transaction_manager.get_transactions(limit=100)
        self.current_transactions = transactions
        
        for trans in transactions:
            amount_display = f"${trans['amount']:.2f}"
            if trans['type'] == 'income':
                amount_display = f"+{amount_display}"
            else:
                amount_display = f"-{amount_display}"
            
            type_display = "收入" if trans['type'] == 'income' else "支出"
            
            self.transaction_tree.insert('', 'end', values=(
                trans['date'],
                type_display,
                trans['category_name'],
                amount_display,
                trans.get('description', '')
            ), tags=(str(trans['id']),))
        
        self.update_statistics()
        
        if hasattr(self, 'category_filter_combo'):
            self.update_category_filter_options()
        
        self.update_report()
    
    def update_statistics(self):
        """更新統計顯示"""
        now = datetime.now()
        summary = self.transaction_manager.get_monthly_summary(now.year, now.month)
        
        self.income_label.config(text=f"本月收入: ${summary['total_income']:.2f}")
        self.expense_label.config(text=f"本月支出: ${summary['total_expense']:.2f}")
        
        balance = summary['balance']
        balance_text = f"本月結餘: ${balance:.2f}"
        balance_color = "green" if balance >= 0 else "red"
        self.balance_label.config(text=balance_text, foreground=balance_color)
    
    def update_filtered_statistics(self, transactions):
        """更新篩選後的統計顯示"""
        total_income = sum(trans['amount'] for trans in transactions if trans['type'] == 'income')
        total_expense = sum(trans['amount'] for trans in transactions if trans['type'] == 'expense')
        balance = total_income - total_expense
        
        self.income_label.config(text=f"篩選收入: ${total_income:.2f}")
        self.expense_label.config(text=f"篩選支出: ${total_expense:.2f}")
        
        balance_text = f"篩選結餘: ${balance:.2f}"
        balance_color = "green" if balance >= 0 else "red"
        self.balance_label.config(text=balance_text, foreground=balance_color)
    
    # 交易管理方法
    def add_transaction(self):
        """新增交易記錄"""
        dialog = TransactionDialog(self.root, self.category_manager, self.transaction_manager)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            data = dialog.result
            success = self.transaction_manager.add_transaction(
                date=data['date'],
                transaction_type=data['type'],
                category_id=data['category_id'],
                amount=data['amount'],
                description=data['description']
            )
            
            if success:
                messagebox.showinfo("成功", "交易記錄新增成功！")
                self.refresh_data()
            else:
                messagebox.showerror("錯誤", "交易記錄新增失敗！")
    
    def edit_transaction(self):
        """編輯選中的交易記錄"""
        selected_item = self.transaction_tree.selection()
        if not selected_item:
            messagebox.showwarning("提醒", "請先選擇要編輯的交易記錄")
            return
        
        transaction_id = int(self.transaction_tree.item(selected_item[0])['tags'][0])
        
        transactions = self.transaction_manager.get_transactions()
        transaction_data = None
        for trans in transactions:
            if trans['id'] == transaction_id:
                transaction_data = trans
                break
        
        if not transaction_data:
            messagebox.showerror("錯誤", "找不到交易記錄")
            return
        
        dialog = TransactionDialog(self.root, self.category_manager, 
                                 self.transaction_manager, transaction_data)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            data = dialog.result
            success = self.transaction_manager.update_transaction(
                transaction_id=transaction_id,
                date=data['date'],
                transaction_type=data['type'],
                category_id=data['category_id'],
                amount=data['amount'],
                description=data['description']
            )
            
            if success:
                messagebox.showinfo("成功", "交易記錄更新成功！")
                self.refresh_data()
            else:
                messagebox.showerror("錯誤", "交易記錄更新失敗！")
    
    def delete_transaction(self):
        """刪除選中的交易記錄"""
        selected_item = self.transaction_tree.selection()
        if not selected_item:
            messagebox.showwarning("提醒", "請先選擇要刪除的交易記錄")
            return
        
        if not messagebox.askyesno("確認", "確定要刪除這筆交易記錄嗎？"):
            return
        
        transaction_id = int(self.transaction_tree.item(selected_item[0])['tags'][0])
        
        success = self.transaction_manager.delete_transaction(transaction_id)
        
        if success:
            messagebox.showinfo("成功", "交易記錄刪除成功！")
            self.refresh_data()
        else:
            messagebox.showerror("錯誤", "交易記錄刪除失敗！")
    
    # 匯出功能方法
    def export_to_csv(self):
        """匯出資料到 CSV 檔案"""
        if not self.current_transactions:
            messagebox.showwarning("提醒", "沒有資料可匯出")
            return
        
        filename = filedialog.asksaveasfilename(
            title="匯出 CSV 檔案",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                
                writer.writerow(['日期', '類型', '分類', '金額', '備註'])
                
                for trans in self.current_transactions:
                    type_display = "收入" if trans['type'] == 'income' else "支出"
                    writer.writerow([
                        trans['date'],
                        type_display,
                        trans['category_name'],
                        trans['amount'],
                        trans.get('description', '')
                    ])
                
                writer.writerow([])
                writer.writerow(['統計摘要'])
                
                total_income = sum(trans['amount'] for trans in self.current_transactions if trans['type'] == 'income')
                total_expense = sum(trans['amount'] for trans in self.current_transactions if trans['type'] == 'expense')
                balance = total_income - total_expense
                
                writer.writerow(['總收入', f'${total_income:.2f}'])
                writer.writerow(['總支出', f'${total_expense:.2f}'])
                writer.writerow(['結餘', f'${balance:.2f}'])
                
                writer.writerow([])
                writer.writerow(['匯出資訊'])
                writer.writerow(['匯出時間', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                writer.writerow(['記錄筆數', len(self.current_transactions)])
            
            messagebox.showinfo("成功", f"資料已成功匯出到：\n{filename}")
            
        except Exception as e:
            messagebox.showerror("錯誤", f"匯出失敗：{str(e)}")
    
    def export_to_excel(self):
        """匯出資料到 Excel 檔案"""
        if not self.current_transactions:
            messagebox.showwarning("提醒", "沒有資料可匯出")
            return
        
        try:
            import openpyxl
            from openpyxl.styles import Font, PatternFill, Alignment
        except ImportError:
            result = messagebox.askyesno("缺少套件", 
                "Excel 匯出需要安裝 openpyxl 套件。\n\n" +
                "請在終端機執行：pip install openpyxl\n\n" +
                "現在要改用 CSV 格式匯出嗎？")
            if result:
                self.export_to_csv()
            return
        
        filename = filedialog.asksaveasfilename(
            title="匯出 Excel 檔案",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            wb = openpyxl.Workbook()
            ws_data = wb.active
            ws_data.title = "交易記錄"
            
            header_font = Font(bold=True, color="FFFFFF")
            header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            
            headers = ['日期', '類型', '分類', '金額', '備註']
            for col, header in enumerate(headers, 1):
                cell = ws_data.cell(row=1, column=col, value=header)
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = Alignment(horizontal='center')
            
            for row, trans in enumerate(self.current_transactions, 2):
                ws_data.cell(row=row, column=1, value=trans['date'])
                ws_data.cell(row=row, column=2, value="收入" if trans['type'] == 'income' else "支出")
                ws_data.cell(row=row, column=3, value=trans['category_name'])
                ws_data.cell(row=row, column=4, value=trans['amount'])
                ws_data.cell(row=row, column=5, value=trans.get('description', ''))
            
            column_widths = [12, 8, 15, 12, 30]
            for col, width in enumerate(column_widths, 1):
                ws_data.column_dimensions[openpyxl.utils.get_column_letter(col)].width = width
            
            wb.save(filename)
            messagebox.showinfo("成功", f"Excel 檔案已成功匯出到：\n{filename}")
            
        except Exception as e:
            messagebox.showerror("錯誤", f"Excel 匯出失敗：{str(e)}")
    
    def run(self):
        """啟動主程式"""
        self.root.mainloop()

def main():
    """主程式入口"""
    try:
        app = MainWindow()
        app.run()
    except Exception as e:
        print(f"程式啟動失敗：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 
    def show_month_category_chart(self):
        """顯示月度分類圓餅圖"""
        for widget in self.report_display_frame.winfo_children():
            widget.destroy()
        
        if not MATPLOTLIB_AVAILABLE:
            ttk.Label(self.report_display_frame, text="需要安裝 matplotlib 套件").pack(pady=20)
            return
        
        year = int(self.year_var.get())
        month = int(self.month_var.get())
        
        start_date = f"{year}-{month:02d}-01"
        last_day = calendar.monthrange(year, month)[1]
        end_date = f"{year}-{month:02d}-{last_day}"
        
        transactions = self.transaction_manager.get_transactions_by_date_range(start_date, end_date)
        
        if not transactions:
            ttk.Label(self.report_display_frame, text="無資料可顯示").pack(pady=20)
            return
        
        # 統計資料
        expense_stats = defaultdict(float)
        income_stats = defaultdict(float)
        
        for trans in transactions:
            if trans['type'] == 'expense':
                expense_stats[trans['category_name']] += trans['amount']
            else:
                income_stats[trans['category_name']] += trans['amount']
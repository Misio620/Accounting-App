"""
獨立報表視窗 - 顯示 4 種統計報表
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import calendar

from .charts import ChartManager, MATPLOTLIB_AVAILABLE
from .ui_config import COLORS, FONTS, SPACING, PADDING, ICONS


class ReportWindow:
    """報表視窗類別"""
    
    def __init__(self, parent, transaction_manager):
        self.parent = parent
        self.transaction_manager = transaction_manager
        self.chart_manager = ChartManager(transaction_manager)
        
        # 建立視窗
        self.window = tk.Toplevel(parent)
        self.window.title(f"{ICONS['chart']} 統計報表")
        self.window.geometry("1200x700")
        self.window.minsize(1000, 600)
        
        # 設定視窗置中
        self.center_window()
        
        self.setup_ui()
    
    def center_window(self):
        """視窗置中"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """設定界面"""
        # 主容器
        main_frame = tk.Frame(self.window, bg=COLORS['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING['loose'], pady=PADDING['loose'])
        
        # 標題區域
        header_frame = tk.Frame(main_frame, bg=COLORS['bg_secondary'], height=70)
        header_frame.pack(fill=tk.X, pady=(0, SPACING['lg']))
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg=COLORS['bg_secondary'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=PADDING['loose'], pady=SPACING['md'])
        
        title_label = tk.Label(
            header_content,
            text=f"{ICONS['chart']} 統計報表",
            font=FONTS['title'],
            fg=COLORS['primary'],
            bg=COLORS['bg_secondary']
        )
        title_label.pack(side=tk.LEFT)
        
        # 關閉按鈕
        close_btn = tk.Button(
            header_content,
            text="✕ 關閉",
            font=FONTS['body'],
            bg=COLORS['danger'],
            fg='white',
            activebackground='#dc2626',
            relief='flat',
            cursor='hand2',
            padx=PADDING['normal'],
            pady=SPACING['sm'],
            command=self.window.destroy
        )
        close_btn.pack(side=tk.RIGHT)
        
        # 控制區域
        control_frame = tk.Frame(main_frame, bg=COLORS['bg_card'], relief='solid', borderwidth=1)
        control_frame.pack(fill=tk.X, pady=(0, SPACING['lg']))
        
        control_content = tk.Frame(control_frame, bg=COLORS['bg_card'])
        control_content.pack(fill=tk.X, padx=PADDING['loose'], pady=PADDING['normal'])
        
        # 報表類型選擇
        type_frame = tk.Frame(control_content, bg=COLORS['bg_card'])
        type_frame.pack(side=tk.LEFT)
        
        tk.Label(
            type_frame,
            text="報表類型：",
            font=FONTS['subheading'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary']
        ).pack(side=tk.LEFT, padx=(0, SPACING['md']))
        
        self.report_type = tk.StringVar(value="year_category")
        
        report_types = [
            ("year_category", "📊 年度分類"),
            ("month_category", "📊 月度分類"),
            ("month_income_expense", "📈 月度收支"),
            ("daily_income_expense", "📈 每日收支")
        ]
        
        for value, text in report_types:
            rb = tk.Radiobutton(
                type_frame,
                text=text,
                variable=self.report_type,
                value=value,
                font=FONTS['body'],
                bg=COLORS['bg_card'],
                activebackground=COLORS['bg_card'],
                selectcolor=COLORS['primary_light'],
                command=self.update_report
            )
            rb.pack(side=tk.LEFT, padx=SPACING['sm'])
        
        # 時間選擇
        time_frame = tk.Frame(control_content, bg=COLORS['bg_card'])
        time_frame.pack(side=tk.RIGHT)
        
        tk.Label(
            time_frame,
            text="年份：",
            font=FONTS['body'],
            bg=COLORS['bg_card']
        ).pack(side=tk.LEFT, padx=(0, SPACING['xs']))
        
        self.year_var = tk.StringVar(value=str(datetime.now().year))
        year_combo = ttk.Combobox(time_frame, textvariable=self.year_var, width=8, state="readonly")
        current_year = datetime.now().year
        year_combo['values'] = [str(year) for year in range(current_year - 5, current_year + 2)]
        year_combo.pack(side=tk.LEFT, padx=(0, SPACING['md']))
        year_combo.bind('<<ComboboxSelected>>', lambda e: self.update_report())
        
        tk.Label(
            time_frame,
            text="月份：",
            font=FONTS['body'],
            bg=COLORS['bg_card']
        ).pack(side=tk.LEFT, padx=(0, SPACING['xs']))
        
        self.month_var = tk.StringVar(value=str(datetime.now().month))
        month_combo = ttk.Combobox(time_frame, textvariable=self.month_var, width=8, state="readonly")
        month_combo['values'] = [str(i) for i in range(1, 13)]
        month_combo.pack(side=tk.LEFT, padx=(0, SPACING['md']))
        month_combo.bind('<<ComboboxSelected>>', lambda e: self.update_report())
        
        # 更新按鈕
        update_btn = tk.Button(
            time_frame,
            text=f"{ICONS['refresh']} 更新",
            font=FONTS['body'],
            bg=COLORS['primary'],
            fg='white',
            activebackground=COLORS['primary_dark'],
            relief='flat',
            cursor='hand2',
            padx=PADDING['normal'],
            pady=SPACING['xs'],
            command=self.update_report
        )
        update_btn.pack(side=tk.LEFT)
        
        # 報表顯示區域
        self.report_display_frame = tk.Frame(
            main_frame,
            bg=COLORS['bg_card'],
            relief='solid',
            borderwidth=1
        )
        self.report_display_frame.pack(fill=tk.BOTH, expand=True)
        
        # 初始顯示
        self.update_report()
    
    def update_report(self):
        """更新報表顯示"""
        # 清除現有內容
        for widget in self.report_display_frame.winfo_children():
            widget.destroy()
        
        if not MATPLOTLIB_AVAILABLE:
            error_frame = tk.Frame(self.report_display_frame, bg=COLORS['bg_card'])
            error_frame.pack(expand=True)
            
            tk.Label(
                error_frame,
                text="⚠️ 圖表功能需要安裝 matplotlib",
                font=FONTS['heading'],
                fg=COLORS['danger'],
                bg=COLORS['bg_card']
            ).pack(pady=SPACING['lg'])
            
            tk.Label(
                error_frame,
                text="請執行: pip install matplotlib",
                font=FONTS['body'],
                fg=COLORS['text_secondary'],
                bg=COLORS['bg_card']
            ).pack()
            return
        
        try:
            report_type = self.report_type.get()
            year = int(self.year_var.get())
            month = int(self.month_var.get())
            
            if report_type == "year_category":
                self.chart_manager.show_year_category_chart(self.report_display_frame, year)
            elif report_type == "month_category":
                self.chart_manager.show_month_category_chart(self.report_display_frame, year, month)
            elif report_type == "month_income_expense":
                self.chart_manager.show_month_income_expense_chart(self.report_display_frame, year)
            elif report_type == "daily_income_expense":
                self.chart_manager.show_daily_income_expense_chart(self.report_display_frame, year, month)
        
        except Exception as e:
            error_frame = tk.Frame(self.report_display_frame, bg=COLORS['bg_card'])
            error_frame.pack(expand=True)
            
            tk.Label(
                error_frame,
                text=f"❌ 報表生成失敗",
                font=FONTS['heading'],
                fg=COLORS['danger'],
                bg=COLORS['bg_card']
            ).pack(pady=SPACING['lg'])
            
            tk.Label(
                error_frame,
                text=str(e),
                font=FONTS['caption'],
                fg=COLORS['text_secondary'],
                bg=COLORS['bg_card']
            ).pack()

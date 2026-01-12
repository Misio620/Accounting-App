"""
主視窗模組 - 個人記帳應用程式主界面
重構版本 - 使用模組化設計
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import sys
import os
import csv

# 匯入資料庫模組
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from database.models import DatabaseManager, CategoryManager, TransactionManager

# 匯入 GUI 模組
from .dialogs import TransactionDialog, CategoryManagementDialog
from .charts import ChartManager, MATPLOTLIB_AVAILABLE
from .filters import FilterPanel
from .ui_config import COLORS, FONTS, SPACING, PADDING, ICONS
from .ui_components import StatCard, ModernButton, SectionFrame

# 匯入工具模組
try:
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from utils.backup import BackupManager, format_file_size
    BACKUP_AVAILABLE = True
except ImportError:
    BACKUP_AVAILABLE = False


class MainWindow:
    """主視窗類別 - 重構版本"""
    
    def __init__(self):
        print("正在初始化個人記帳本...")
        
        # 初始化資料庫
        try:
            self.db_manager = DatabaseManager("accounting.db")
            self.category_manager = CategoryManager(self.db_manager)
            self.transaction_manager = TransactionManager(self.db_manager)
            print("✅ 資料庫初始化完成")
        except Exception as e:
            print(f"❌ 資料庫初始化失敗: {e}")
            messagebox.showerror("資料庫錯誤", f"無法初始化資料庫：{e}")
            sys.exit(1)
        
        # 初始化圖表管理器
        self.chart_manager = ChartManager(self.transaction_manager)
        
        # 初始化備份管理器
        if BACKUP_AVAILABLE:
            self.backup_manager = BackupManager()
        else:
            self.backup_manager = None
        
        # 建立主視窗
        self.root = tk.Tk()
        self.root.title("個人記帳本 v1.1 (重構版)")
        self.root.geometry("1000x800")
        self.root.minsize(800, 600)
        
        self.current_transactions = []
        
        self.setup_ui()
        
        print("✅ 界面初始化完成")
    
    def setup_ui(self):
        """設定主界面"""
        # 建立選單列
        self.setup_menu()
        
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 標題和版本資訊
        header_frame = tk.Frame(main_frame, bg=COLORS['bg_secondary'], height=60)
        header_frame.grid(row=0, column=0, columnspan=3, pady=(0, SPACING['lg']), sticky=(tk.W, tk.E))
        header_frame.pack_propagate(False)
        
        # 內部容器
        header_content = tk.Frame(header_frame, bg=COLORS['bg_secondary'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=PADDING['loose'], pady=SPACING['md'])
        
        title_label = tk.Label(
            header_content,
            text=f"{ICONS['balance']} 個人記帳本",
            font=FONTS['title'],
            fg=COLORS['primary'],
            bg=COLORS['bg_secondary']
        )
        title_label.pack(side=tk.LEFT)
        
        version_label = tk.Label(
            header_content,
            text="v1.1",
            font=FONTS['caption'],
            fg=COLORS['text_light'],
            bg=COLORS['bg_secondary']
        )
        version_label.pack(side=tk.RIGHT, padx=(0, SPACING['md']))
        
        # 按鈕區域
        self.setup_buttons(main_frame)
        
        # 篩選區域 - 使用 FilterPanel 模組
        filter_container = ttk.Frame(main_frame)
        filter_container.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E))
        self.filter_panel = FilterPanel(filter_container, self.category_manager, self.on_filter_applied)
        
        # 交易記錄列表
        self.setup_transaction_list(main_frame)
        
        # 統計區域
        self.setup_statistics(main_frame)
        
        # 報表區域 - 已移除，改為獨立視窗
        # self.setup_reports(main_frame)
        
        # 設定網格權重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)  # 交易列表可擴展
        
        # 綁定快捷鍵
        self.setup_shortcuts()
        
        # UI 建立完成後載入資料
        self.root.after(100, self.refresh_data)
    
    def setup_menu(self):
        """設定選單列"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 檔案選單
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="檔案", menu=file_menu)
        file_menu.add_command(label="匯出 CSV", command=self.export_to_csv, accelerator="Ctrl+S")
        file_menu.add_command(label="匯出 Excel", command=self.export_to_excel)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.on_closing, accelerator="Alt+F4")
        
        # 管理選單
        manage_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="管理", menu=manage_menu)
        manage_menu.add_command(label="分類管理", command=self.open_category_management, accelerator="Ctrl+M")
        manage_menu.add_separator()
        manage_menu.add_command(label="備份資料", command=self.backup_database)
        manage_menu.add_command(label="還原資料", command=self.restore_database)
        
        # 說明選單
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="說明", menu=help_menu)
        help_menu.add_command(label="快捷鍵說明", command=self.show_shortcuts_help)
        help_menu.add_command(label="關於", command=self.show_about)
    
    def setup_shortcuts(self):
        """設定快捷鍵"""
        self.root.bind('<Control-n>', lambda e: self.add_transaction())
        self.root.bind('<F5>', lambda e: self.refresh_data())
        self.root.bind('<Control-s>', lambda e: self.export_to_csv())
    
    def setup_buttons(self, parent):
        """設定按鈕區域"""
        button_frame = tk.Frame(parent, bg=COLORS['bg_primary'])
        button_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=SPACING['md'])
        
        # 左側按鈕
        left_buttons = tk.Frame(button_frame, bg=COLORS['bg_primary'])
        left_buttons.pack(side=tk.LEFT)
        
        ModernButton(
            left_buttons,
            text="新增交易",
            style='primary',
            icon='add',
            command=self.add_transaction
        ).pack(side=tk.LEFT, padx=SPACING['xs'])
        
        # 分隔線
        sep = tk.Frame(left_buttons, width=2, bg=COLORS['border'])
        sep.pack(side=tk.LEFT, padx=SPACING['md'], fill=tk.Y)
        
        ModernButton(
            left_buttons,
            text="重新整理",
            style='secondary',
            icon='refresh',
            command=self.refresh_data
        ).pack(side=tk.LEFT, padx=SPACING['xs'])
        
        ModernButton(
            left_buttons,
            text="統計報表",
            style='secondary',
            icon='chart',
            command=self.open_report_window
        ).pack(side=tk.LEFT, padx=SPACING['xs'])
        
        # 右側匯出按鈕
        export_frame = tk.Frame(button_frame, bg=COLORS['bg_primary'])
        export_frame.pack(side=tk.RIGHT)
        
        ModernButton(
            export_frame,
            text="匯出 CSV",
            style='secondary',
            icon='export',
            command=self.export_to_csv
        ).pack(side=tk.LEFT, padx=SPACING['xs'])
        
        ModernButton(
            export_frame,
            text="匯出 Excel",
            style='success',
            icon='export',
            command=self.export_to_excel
        ).pack(side=tk.LEFT, padx=SPACING['xs'])
    
    def setup_transaction_list(self, parent):
        """設定交易記錄列表"""
        list_frame = ttk.LabelFrame(parent, text="交易記錄", padding="5")
        list_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        columns = ('日期', '類型', '分類', '金額', '備註')
        self.transaction_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        # 設定欄位標題和寬度
        self.transaction_tree.heading('日期', text='日期')
        self.transaction_tree.heading('類型', text='類型')
        self.transaction_tree.heading('分類', text='分類')
        self.transaction_tree.heading('金額', text='金額')
        self.transaction_tree.heading('備註', text='備註')
        
        self.transaction_tree.column('日期', width=100, anchor='center')
        self.transaction_tree.column('類型', width=80, anchor='center')
        self.transaction_tree.column('分類', width=120, anchor='center')
        self.transaction_tree.column('金額', width=120, anchor='center')  # 改為置中
        self.transaction_tree.column('備註', width=280, anchor='center')
        
        # 滾動條
        v_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.transaction_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.transaction_tree.xview)
        self.transaction_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # 放置組件
        self.transaction_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # 設定網格權重
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # 綁定選擇事件
        self.transaction_tree.bind('<<TreeviewSelect>>', self.on_transaction_select)
        self.transaction_tree.bind('<Double-1>', lambda e: self.edit_transaction())
        
        # 操作按鈕區域（選中交易時顯示）
        self.action_frame = tk.Frame(list_frame, bg=COLORS['bg_card'], height=60)
        self.action_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(SPACING['sm'], 0))
        self.action_frame.grid_remove()  # 初始隱藏
        
        action_content = tk.Frame(self.action_frame, bg=COLORS['bg_card'])
        action_content.pack(fill=tk.BOTH, expand=True, padx=PADDING['normal'], pady=SPACING['sm'])
        
        # 左側：選中的交易資訊
        self.selected_info_label = tk.Label(
            action_content,
            text="",
            font=FONTS['body'],
            fg=COLORS['text_secondary'],
            bg=COLORS['bg_card'],
            anchor='w'
        )
        self.selected_info_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 右側：操作按鈕
        button_container = tk.Frame(action_content, bg=COLORS['bg_card'])
        button_container.pack(side=tk.RIGHT)
        
        from .ui_components import ModernButton
        
        ModernButton(
            button_container,
            text="編輯",
            style='secondary',
            icon='edit',
            command=self.edit_transaction
        ).pack(side=tk.LEFT, padx=SPACING['xs'])
        
        ModernButton(
            button_container,
            text="刪除",
            style='danger',
            icon='delete',
            command=self.delete_transaction
        ).pack(side=tk.LEFT, padx=SPACING['xs'])
        
        # 狀態列
        status_frame = ttk.Frame(list_frame)
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        self.status_label = ttk.Label(status_frame, text="準備就緒")
        self.status_label.pack(side=tk.LEFT)
        
        self.record_count_label = ttk.Label(status_frame, text="")
        self.record_count_label.pack(side=tk.RIGHT)
    
    def on_transaction_select(self, event):
        """當選擇交易時顯示操作按鈕"""
        selected = self.transaction_tree.selection()
        if selected:
            # 顯示操作區域
            self.action_frame.grid()
            
            # 取得選中的交易資訊
            item = selected[0]
            values = self.transaction_tree.item(item)['values']
            if values:
                date = values[0]
                trans_type = values[1]
                category = values[2]
                amount = values[3]
                
                info_text = f"已選擇：{date} | {trans_type} | {category} | {amount}"
                self.selected_info_label.config(text=info_text)
        else:
            # 隱藏操作區域
            self.action_frame.grid_remove()

    
    def setup_statistics(self, parent):
        """設定統計區域"""
        stats_frame = tk.Frame(parent, bg=COLORS['bg_primary'])
        stats_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=SPACING['lg'])
        
        # 標題
        title_label = tk.Label(
            stats_frame,
            text=f"{ICONS['chart']} 統計資訊",
            font=FONTS['heading'],
            fg=COLORS['text_primary'],
            bg=COLORS['bg_primary']
        )
        title_label.pack(anchor='w', pady=(0, SPACING['md']))
        
        # 卡片容器
        cards_container = tk.Frame(stats_frame, bg=COLORS['bg_primary'])
        cards_container.pack(fill=tk.X)
        
        # 三個統計卡片 - 改用 grid 以確保均分寬度
        cards_container.grid_columnconfigure(0, weight=1, uniform="stats")
        cards_container.grid_columnconfigure(1, weight=1, uniform="stats")
        cards_container.grid_columnconfigure(2, weight=1, uniform="stats")
        
        self.income_card = StatCard(cards_container, card_type='income')
        self.income_card.grid(row=0, column=0, sticky="nsew", padx=(0, SPACING['sm']))
        
        self.expense_card = StatCard(cards_container, card_type='expense')
        self.expense_card.grid(row=0, column=1, sticky="nsew", padx=SPACING['sm'])
        
        self.balance_card = StatCard(cards_container, card_type='balance')
        self.balance_card.grid(row=0, column=2, sticky="nsew", padx=(SPACING['sm'], 0))
    
    def setup_reports(self, parent):
        """設定報表區域（改為按鈕）"""
        report_frame = tk.Frame(parent, bg=COLORS['bg_primary'])
        report_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=SPACING['lg'])
        
        # 標題
        title_label = tk.Label(
            report_frame,
            text=f"{ICONS['chart']} 統計報表",
            font=FONTS['heading'],
            fg=COLORS['text_primary'],
            bg=COLORS['bg_primary']
        )
        title_label.pack(anchor='w', pady=(0, SPACING['md']))
        
        # 說明和按鈕容器
        content_frame = tk.Frame(
            report_frame,
            bg=COLORS['bg_card'],
            relief='solid',
            borderwidth=1
        )
        content_frame.pack(fill=tk.X)
        
        inner_frame = tk.Frame(content_frame, bg=COLORS['bg_card'])
        inner_frame.pack(fill=tk.X, padx=PADDING['loose'], pady=PADDING['loose'])
        
        # 說明文字
        desc_label = tk.Label(
            inner_frame,
            text="查看詳細的統計報表，包含年度分類、月度分類、月度收支、每日收支等圖表分析",
            font=FONTS['body'],
            fg=COLORS['text_secondary'],
            bg=COLORS['bg_card']
        )
        desc_label.pack(side=tk.LEFT, padx=(0, SPACING['lg']))
        
        # 開啟報表按鈕
        from .ui_components import ModernButton
        ModernButton(
            inner_frame,
            text="開啟報表視窗",
            style='primary',
            icon='chart',
            command=self.open_report_window
        ).pack(side=tk.RIGHT)
    
    # 篩選相關方法
    def on_filter_applied(self, filters: dict):
        """當篩選條件套用時的回調"""
        transactions = self.transaction_manager.get_transactions(limit=1000)
        
        filtered_transactions = []
        for trans in transactions:
            # 日期篩選
            if filters['start_date'] and trans['date'] < filters['start_date']:
                continue
            if filters['end_date'] and trans['date'] > filters['end_date']:
                continue
            
            # 類型篩選
            if filters['type'] != "all" and trans['type'] != filters['type']:
                continue
            
            # 分類篩選
            if filters['category'] != "全部分類" and filters['category'] and trans['category_name'] != filters['category']:
                continue
            
            # 關鍵字篩選
            if filters['keyword'] and filters['keyword'] not in str(trans.get('description', '')).lower():
                continue
            
            filtered_transactions.append(trans)
        
        self.display_transactions(filtered_transactions)
    
    def display_transactions(self, transactions):
        """顯示交易記錄"""
        # 防禦性檢查：確保 transaction_tree 已建立
        if not hasattr(self, 'transaction_tree'):
            return
        
        # 清除現有項目
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
            tags = ('income' if trans['type'] == 'income' else 'expense',)
            
            self.transaction_tree.insert('', 'end', values=(
                trans['date'],
                type_display,
                trans['category_name'],
                amount_display,
                trans.get('description', '')
            ), tags=(str(trans['id']),) + tags)
        
        # 設定顏色
        self.transaction_tree.tag_configure('income', foreground='green')
        self.transaction_tree.tag_configure('expense', foreground='red')
        
        self.update_filtered_statistics(transactions)
        self.record_count_label.config(text=f"共 {len(transactions)} 筆記錄")
        
        # 隱藏操作區域
        if hasattr(self, 'action_frame'):
            self.action_frame.grid_remove()
    
    def refresh_data(self):
        """重新整理資料顯示"""
        try:
            transactions = self.transaction_manager.get_transactions(limit=200)
            self.display_transactions(transactions)
            
            self.update_statistics()
            
            if hasattr(self, 'filter_panel'):
                self.filter_panel.update_category_filter_options()
            
            self.status_label.config(text="資料已更新")
            
        except Exception as e:
            messagebox.showerror("錯誤", f"資料更新失敗：{e}")
            self.status_label.config(text="更新失敗")
    
    def update_statistics(self):
        """更新統計顯示"""
        now = datetime.now()
        summary = self.transaction_manager.get_monthly_summary(now.year, now.month)
        
        # 更新卡片數值
        self.income_card.set_value(summary['total_income'])
        self.expense_card.set_value(summary['total_expense'])
        self.balance_card.set_value(summary['balance'])
    
    def update_filtered_statistics(self, transactions):
        """更新篩選後的統計顯示"""
        total_income = sum(trans['amount'] for trans in transactions if trans['type'] == 'income')
        total_expense = sum(trans['amount'] for trans in transactions if trans['type'] == 'expense')
        balance = total_income - total_expense
        
        # 更新卡片（顯示篩選結果）
        self.income_card.set_value(total_income, f"{ICONS['filter']} 篩選結果")
        self.expense_card.set_value(total_expense, f"{ICONS['filter']} 篩選結果")
        self.balance_card.set_value(balance, f"{ICONS['filter']} 篩選結果")
    
    def open_report_window(self):
        """開啟報表視窗"""
        from .report_window import ReportWindow
        ReportWindow(self.root, self.transaction_manager)
    
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
                self.status_label.config(text="新增記錄成功")
            else:
                messagebox.showerror("錯誤", "交易記錄新增失敗！")
                self.status_label.config(text="新增記錄失敗")
    
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
                self.status_label.config(text="更新記錄成功")
            else:
                messagebox.showerror("錯誤", "交易記錄更新失敗！")
                self.status_label.config(text="更新記錄失敗")
    
    def delete_transaction(self):
        """刪除選中的交易記錄"""
        selected_item = self.transaction_tree.selection()
        if not selected_item:
            messagebox.showwarning("提醒", "請先選擇要刪除的交易記錄")
            return
        
        if not messagebox.askyesno("確認", "確定要刪除這筆交易記錄嗎？\n此操作無法復原。"):
            return
        
        transaction_id = int(self.transaction_tree.item(selected_item[0])['tags'][0])
        
        success = self.transaction_manager.delete_transaction(transaction_id)
        
        if success:
            messagebox.showinfo("成功", "交易記錄刪除成功！")
            self.refresh_data()
            self.status_label.config(text="刪除記錄成功")
        else:
            messagebox.showerror("錯誤", "交易記錄刪除失敗！")
            self.status_label.config(text="刪除記錄失敗")
    
    # 分類管理
    def open_category_management(self):
        """開啟分類管理對話框"""
        dialog = CategoryManagementDialog(self.root, self.category_manager, self.transaction_manager)
        self.root.wait_window(dialog.dialog)
        
        # 重新整理資料以更新分類選項
        self.refresh_data()
    
    # 匯出功能
    def export_to_csv(self):
        """匯出資料到 CSV 檔案"""
        if not self.current_transactions:
            messagebox.showwarning("提醒", "沒有資料可匯出")
            return
        
        filename = filedialog.asksaveasfilename(
            title="匯出 CSV 檔案",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialname=f"記帳資料_{datetime.now().strftime('%Y%m%d')}.csv"
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                
                # 寫入標題
                writer.writerow(['日期', '類型', '分類', '金額', '備註'])
                
                # 寫入交易資料
                for trans in self.current_transactions:
                    type_display = "收入" if trans['type'] == 'income' else "支出"
                    writer.writerow([
                        trans['date'],
                        type_display,
                        trans['category_name'],
                        trans['amount'],
                        trans.get('description', '')
                    ])
                
                # 寫入統計摘要
                writer.writerow([])
                writer.writerow(['統計摘要'])
                
                total_income = sum(trans['amount'] for trans in self.current_transactions if trans['type'] == 'income')
                total_expense = sum(trans['amount'] for trans in self.current_transactions if trans['type'] == 'expense')
                balance = total_income - total_expense
                
                writer.writerow(['總收入', f'${total_income:.2f}'])
                writer.writerow(['總支出', f'${total_expense:.2f}'])
                writer.writerow(['結餘', f'${balance:.2f}'])
                
                # 寫入匯出資訊
                writer.writerow([])
                writer.writerow(['匯出資訊'])
                writer.writerow(['匯出時間', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                writer.writerow(['記錄筆數', len(self.current_transactions)])
            
            messagebox.showinfo("成功", f"資料已成功匯出到：\n{filename}")
            self.status_label.config(text="CSV 匯出成功")
            
        except Exception as e:
            messagebox.showerror("錯誤", f"匯出失敗：{str(e)}")
            self.status_label.config(text="CSV 匯出失敗")
    
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
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialname=f"記帳資料_{datetime.now().strftime('%Y%m%d')}.xlsx"
        )
        
        if not filename:
            return
        
        try:
            wb = openpyxl.Workbook()
            ws_data = wb.active
            ws_data.title = "交易記錄"
            
            # 設定標題樣式
            header_font = Font(bold=True, color="FFFFFF")
            header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            
            headers = ['日期', '類型', '分類', '金額', '備註']
            for col, header in enumerate(headers, 1):
                cell = ws_data.cell(row=1, column=col, value=header)
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = Alignment(horizontal='center')
            
            # 寫入交易資料
            for row, trans in enumerate(self.current_transactions, 2):
                ws_data.cell(row=row, column=1, value=trans['date'])
                ws_data.cell(row=row, column=2, value="收入" if trans['type'] == 'income' else "支出")
                ws_data.cell(row=row, column=3, value=trans['category_name'])
                ws_data.cell(row=row, column=4, value=trans['amount'])
                ws_data.cell(row=row, column=5, value=trans.get('description', ''))
            
            # 調整欄寬
            column_widths = [12, 8, 15, 12, 30]
            for col, width in enumerate(column_widths, 1):
                ws_data.column_dimensions[openpyxl.utils.get_column_letter(col)].width = width
            
            wb.save(filename)
            messagebox.showinfo("成功", f"Excel 檔案已成功匯出到：\n{filename}")
            self.status_label.config(text="Excel 匯出成功")
            
        except Exception as e:
            messagebox.showerror("錯誤", f"Excel 匯出失敗：{str(e)}")
            self.status_label.config(text="Excel 匯出失敗")
    
    # 備份和還原
    def backup_database(self):
        """備份資料庫"""
        if not self.backup_manager:
            messagebox.showerror("錯誤", "備份功能不可用\n請確認 utils/backup.py 存在")
            return
        
        # 執行備份
        success, message = self.backup_manager.backup_database()
        
        if success:
            # 取得檔案大小
            import os
            file_size = os.path.getsize(message)
            size_str = format_file_size(file_size)
            
            messagebox.showinfo("備份成功", 
                f"資料庫已成功備份！\n\n"
                f"備份檔案: {os.path.basename(message)}\n"
                f"檔案大小: {size_str}\n"
                f"位置: backup/")
            self.status_label.config(text="資料庫備份成功")
        else:
            messagebox.showerror("備份失敗", message)
            self.status_label.config(text="備份失敗")
    
    def restore_database(self):
        """還原資料庫"""
        if not self.backup_manager:
            messagebox.showerror("錯誤", "還原功能不可用")
            return
        
        # 列出可用的備份
        backups = self.backup_manager.list_backups()
        
        if not backups:
            messagebox.showwarning("提示", "沒有可用的備份檔案\n\n請先執行備份功能")
            return
        
        # 建立還原對話框
        restore_dialog = tk.Toplevel(self.root)
        restore_dialog.title("還原資料庫")
        restore_dialog.geometry("500x400")
        restore_dialog.transient(self.root)
        restore_dialog.grab_set()
        
        ttk.Label(restore_dialog, text="選擇要還原的備份", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        # 備份列表
        list_frame = ttk.Frame(restore_dialog)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('檔名', '大小', '建立時間')
        backup_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            backup_tree.heading(col, text=col)
        
        backup_tree.column('檔名', width=200)
        backup_tree.column('大小', width=100)
        backup_tree.column('建立時間', width=150)
        
        # 填入備份資料
        for backup in backups:
            backup_tree.insert('', 'end', values=(
                backup['name'],
                format_file_size(backup['size']),
                backup['created_time'].strftime('%Y-%m-%d %H:%M:%S')
            ), tags=(backup['path'],))
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=backup_tree.yview)
        backup_tree.configure(yscrollcommand=scrollbar.set)
        
        backup_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 按鈕
        button_frame = ttk.Frame(restore_dialog)
        button_frame.pack(pady=10)
        
        def do_restore():
            selected = backup_tree.selection()
            if not selected:
                messagebox.showwarning("提示", "請選擇要還原的備份")
                return
            
            backup_path = backup_tree.item(selected[0])['tags'][0]
            
            if not messagebox.askyesno("確認還原", 
                "確定要從備份還原資料庫嗎？\n\n"
                "⚠️ 警告：當前資料庫將被覆蓋！\n"
                "（系統會自動備份當前資料庫）"):
                return
            
            success, msg = self.backup_manager.restore_database(backup_path)
            
            if success:
                messagebox.showinfo("還原成功", 
                    f"{msg}\n\n請重新啟動程式以載入還原的資料")
                restore_dialog.destroy()
                self.status_label.config(text="資料庫已還原")
            else:
                messagebox.showerror("還原失敗", msg)
        
        ttk.Button(button_frame, text="還原", command=do_restore).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=restore_dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    # 說明功能
    def show_shortcuts_help(self):
        """顯示快捷鍵說明"""
        help_text = """
快捷鍵說明

Ctrl+N    新增交易
F5        重新整理
Ctrl+S    匯出 CSV
Ctrl+M    分類管理
Alt+F4    退出程式

提示：
- 點擊交易列表中的「編輯」或「刪除」進行操作
- 雙擊交易記錄也可以快速編輯
        """
        messagebox.showinfo("快捷鍵說明", help_text)
    
    def show_about(self):
        """顯示關於對話框"""
        about_text = """
個人記帳本 v1.1

重構版本 - 模組化設計

功能特色：
• 交易記錄管理
• 分類管理
• 進階篩選
• 統計報表
• 圖表分析
• 資料匯出

開發：Python + tkinter
        """
        messagebox.showinfo("關於", about_text)
    
    def on_closing(self):
        """程式關閉時的處理"""
        if messagebox.askokcancel("退出", "確定要退出個人記帳本嗎？"):
            self.root.destroy()
    
    def run(self):
        """啟動主程式"""
        # 綁定關閉事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 顯示啟動訊息
        self.status_label.config(text="個人記帳本已啟動")
        
        print("🚀 個人記帳本已啟動 (重構版)")
        print("📚 使用說明：")
        print("   - Ctrl+N: 新增交易")
        print("   - Ctrl+E: 編輯交易")
        print("   - Del: 刪除交易")
        print("   - F5: 重新整理")
        print("   - Ctrl+S: 匯出 CSV")
        print("   - Ctrl+M: 分類管理")
        
        # 啟動主迴圈
        self.root.mainloop()

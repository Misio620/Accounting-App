"""
對話框模組 - 交易和分類管理對話框
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from typing import Optional, Dict, Any

# 匯入改進的對話框
from .improved_dialog import ImprovedTransactionDialog

# 使用改進的對話框作為預設
TransactionDialog = ImprovedTransactionDialog


# 舊的 TransactionDialog 已被 ImprovedTransactionDialog 取代
# class TransactionDialog:
#     ...（舊代碼已註解）


class CategoryManagementDialog:
    """分類管理對話框"""
    
    def __init__(self, parent, category_manager, transaction_manager):
        self.parent = parent
        self.category_manager = category_manager
        self.transaction_manager = transaction_manager
        
        # 建立對話框視窗
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("分類管理")
        self.dialog.geometry("600x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
        self.center_window()
        self.load_categories()
    
    def center_window(self):
        """將對話框置中顯示"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"600x500+{x}+{y}")
    
    def setup_ui(self):
        """設定對話框界面"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 標題
        ttk.Label(main_frame, text="分類管理", font=("Arial", 14, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 15))
        
        # 分類列表
        list_frame = ttk.LabelFrame(main_frame, text="現有分類", padding="10")
        list_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # 建立 Treeview
        columns = ('ID', '名稱', '類型', '使用次數')
        self.category_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.category_tree.heading(col, text=col)
        
        self.category_tree.column('ID', width=50, anchor='center')
        self.category_tree.column('名稱', width=150)
        self.category_tree.column('類型', width=100, anchor='center')
        self.category_tree.column('使用次數', width=100, anchor='center')
        
        # 滾動條
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.category_tree.yview)
        self.category_tree.configure(yscrollcommand=scrollbar.set)
        
        self.category_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # 按鈕區域
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="新增分類", command=self.add_category).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="編輯分類", command=self.edit_category).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刪除分類", command=self.delete_category).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="重新整理", command=self.load_categories).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="關閉", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # 設定網格權重
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
    
    def load_categories(self):
        """載入分類列表"""
        # 清除現有項目
        for item in self.category_tree.get_children():
            self.category_tree.delete(item)
        
        # 載入所有分類
        categories = self.category_manager.get_all_categories()
        
        for cat in categories:
            # 計算使用次數
            usage_count = self._get_category_usage_count(cat['id'])
            
            type_display = "收入" if cat['type'] == 'income' else "支出"
            
            self.category_tree.insert('', 'end', values=(
                cat['id'],
                cat['name'],
                type_display,
                usage_count
            ), tags=(str(cat['id']),))
    
    def _get_category_usage_count(self, category_id: int) -> int:
        """取得分類的使用次數"""
        try:
            # 查詢使用此分類的交易數量
            transactions = self.transaction_manager.get_transactions(limit=10000)
            count = sum(1 for trans in transactions 
                       if self._get_category_id_from_transaction(trans) == category_id)
            return count
        except:
            return 0
    
    def _get_category_id_from_transaction(self, transaction: Dict) -> Optional[int]:
        """從交易記錄取得分類 ID"""
        # 需要從分類名稱反查 ID
        categories = self.category_manager.get_all_categories()
        for cat in categories:
            if cat['name'] == transaction.get('category_name'):
                return cat['id']
        return None
    
    def add_category(self):
        """新增分類"""
        dialog = AddCategoryDialog(self.dialog, self.category_manager)
        self.dialog.wait_window(dialog.dialog)
        
        if dialog.result:
            self.load_categories()
    
    def edit_category(self):
        """編輯分類"""
        selected_item = self.category_tree.selection()
        if not selected_item:
            messagebox.showwarning("提醒", "請先選擇要編輯的分類")
            return
        
        category_id = int(self.category_tree.item(selected_item[0])['values'][0])
        category_name = self.category_tree.item(selected_item[0])['values'][1]
        
        messagebox.showinfo("提示", "編輯分類功能開發中...")
    
    def delete_category(self):
        """刪除分類"""
        selected_item = self.category_tree.selection()
        if not selected_item:
            messagebox.showwarning("提醒", "請先選擇要刪除的分類")
            return
        
        values = self.category_tree.item(selected_item[0])['values']
        category_id = int(values[0])
        category_name = values[1]
        usage_count = int(values[3])
        
        # 檢查是否有交易使用此分類
        if usage_count > 0:
            messagebox.showerror("錯誤", 
                f"無法刪除分類「{category_name}」\n\n此分類已被 {usage_count} 筆交易使用。\n請先刪除或修改這些交易的分類。")
            return
        
        # 確認刪除
        if not messagebox.askyesno("確認刪除", 
            f"確定要刪除分類「{category_name}」嗎？\n此操作無法復原。"):
            return
        
        messagebox.showinfo("提示", "刪除分類功能需要在 database/models.py 中新增 delete_category 方法")
        # TODO: 實現刪除功能
        # success = self.category_manager.delete_category(category_id)
        # if success:
        #     messagebox.showinfo("成功", "分類刪除成功！")
        #     self.load_categories()


class AddCategoryDialog:
    """新增分類對話框"""
    
    def __init__(self, parent, category_manager):
        self.parent = parent
        self.category_manager = category_manager
        self.result = None
        
        # 建立對話框視窗
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("新增分類")
        self.dialog.geometry("350x200")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)
        
        self.setup_ui()
        self.center_window()
    
    def center_window(self):
        """將對話框置中顯示"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (350 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (200 // 2)
        self.dialog.geometry(f"350x200+{x}+{y}")
    
    def setup_ui(self):
        """設定對話框界面"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 標題
        ttk.Label(main_frame, text="新增分類", font=("Arial", 12, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 15))
        
        # 分類名稱
        ttk.Label(main_frame, text="分類名稱:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.name_var, width=25).grid(
            row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # 類型選擇
        ttk.Label(main_frame, text="類型:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.type_var = tk.StringVar(value="expense")
        type_frame = ttk.Frame(main_frame)
        type_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Radiobutton(type_frame, text="收入", variable=self.type_var, 
                       value="income").pack(side=tk.LEFT)
        ttk.Radiobutton(type_frame, text="支出", variable=self.type_var, 
                       value="expense").pack(side=tk.LEFT, padx=(20, 0))
        
        # 按鈕區域
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="確定", command=self.on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=self.on_cancel).pack(side=tk.LEFT, padx=5)
        
        # 設定欄位調整
        main_frame.columnconfigure(1, weight=1)
        
        # 綁定 Enter 鍵
        self.dialog.bind('<Return>', lambda e: self.on_ok())
        self.dialog.bind('<Escape>', lambda e: self.on_cancel())
    
    def on_ok(self):
        """確定按鈕處理"""
        name = self.name_var.get().strip()
        
        if not name:
            messagebox.showerror("錯誤", "請輸入分類名稱")
            return
        
        category_type = self.type_var.get()
        
        # 新增分類
        success = self.category_manager.add_category(name, category_type)
        
        if success:
            self.result = {'name': name, 'type': category_type}
            messagebox.showinfo("成功", "分類新增成功！")
            self.dialog.destroy()
        else:
            messagebox.showerror("錯誤", f"分類「{name}」已存在")
    
    def on_cancel(self):
        """取消按鈕處理"""
        self.result = None
        self.dialog.destroy()

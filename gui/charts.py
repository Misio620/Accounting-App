"""
圖表模組 - 統計圖表生成功能
"""

import tkinter as tk
from tkinter import ttk
from collections import defaultdict
import calendar
import math
from typing import Dict, List, Tuple, Optional

try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MultipleLocator
    
    # 設定中文字體
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class ChartManager:
    """圖表管理類別"""
    
    # 現代化配色方案（8色）
    # 現代化配色方案（12色循環）
    DEFAULT_COLORS = [
        '#3b82f6',  # 藍色
        '#10b981',  # 綠色
        '#f59e0b',  # 橙色
        '#8b5cf6',  # 紫色
        '#ec4899',  # 粉色
        '#06b6d4',  # 青色
        '#f97316',  # 深橙
        '#6366f1',  # 靛藍
        '#14b8a6',  # 青綠
        '#f43f5e',  # 玫瑰紅
        '#84cc16',  # 萊姆綠
        '#0ea5e9',  # 天空藍
    ]
    
    # 分類顏色映射表 (名稱 -> 顏色索引)
    _category_color_map = {}
    
    def __init__(self, transaction_manager):
        self.transaction_manager = transaction_manager
        
    def get_category_color(self, category_name: str) -> str:
        """取得分類對應的固定顏色"""
        # 如果這個分類還沒有分配顏色，分配一個
        if category_name not in self._category_color_map:
            # 使用名稱的雜湊值加上現有映射長度來決定顏色，確保順序大致固定但有隨機性
            # 或者簡單地按出現順序分配
            self._category_color_map[category_name] = len(self._category_color_map) % len(self.DEFAULT_COLORS)
            
        color_index = self._category_color_map[category_name]
        return self.DEFAULT_COLORS[color_index]
    
    def create_pie_chart(self, data: Dict[str, float], title: str) -> Figure:
        """
        建立圓餅圖
        
        Args:
            data: 分類資料 {分類名稱: 金額}
            title: 圖表標題
        
        Returns:
            Figure: matplotlib 圖表物件
        """
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError("需要安裝 matplotlib")
        
        if not data:
            return None
        
        # 排序資料
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        labels = [cat for cat, _ in sorted_data]
        sizes = [amount for _, amount in sorted_data]
        
        # 根據分類名稱獲取固定顏色
        colors = [self.get_category_color(label) for label in labels]
        
        # 建立圖表
        fig = Figure(figsize=(10, 5), dpi=80)
        ax = fig.add_subplot(111)
        
        # 突出最大項
        explode = [0.05 if i == 0 else 0 for i in range(len(labels))]
        
        # 只顯示百分比，不顯示金額
        def make_autopct(pct):
            return f'{pct:.1f}%' if pct > 3 else ''
        
        # 在圓餅圖上顯示分類名稱和百分比
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels,  # 顯示分類名稱
            colors=colors,  # 使用固定的分類顏色
            autopct=make_autopct,
            startangle=90,
            explode=explode,
            shadow=True,
            textprops={'fontsize': 16, 'weight': 'bold'},  # 分類名稱字體
            labeldistance=1.1,  # 標籤距離圓心的比例（避免超出）
            pctdistance=0.75  # 百分比距離圓心的比例
        )
        
        # 設定百分比文字樣式
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(14)
            autotext.set_weight('bold')
        
        # 使用圖例顯示分類名稱和金額（在右側）
        legend_labels = [f'{label}: ${amount:,.0f}' for label, amount in zip(labels, sizes)]
        ax.legend(legend_labels, loc='center left', bbox_to_anchor=(1.2, 0.5), 
                 fontsize=16, frameon=True, fancybox=True, shadow=True)
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        
        fig.tight_layout()
        return fig
    
    @staticmethod
    def create_bar_chart(income_data: List[float], expense_data: List[float], 
                        labels: List[str], title: str, y_interval: Optional[int] = None,
                        bar_width: float = 0.6) -> Figure:
        """
        建立長條圖（收支對比）
        
        Args:
            income_data: 收入資料列表
            expense_data: 支出資料列表
            labels: 標籤列表
            title: 圖表標題
            y_interval: Y 軸刻度間隔（可選）
            bar_width: 直條寬度（預設 0.6）
        
        Returns:
            Figure: matplotlib 圖表物件
        """
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError("需要安裝 matplotlib")
        
        if not labels:
            return None
        
        # 建立圖表
        fig = Figure(figsize=(12, 6), dpi=80)
        ax = fig.add_subplot(111)
        
        # 設定 x 軸位置（使用整數位置，確保對齊）
        x_positions = list(range(len(labels)))
        # bar_width 從參數傳入
        
        # 只繪製支出直條（單一直條，像參考圖片）
        bars = ax.bar(
            x_positions,  # 直接使用 x_positions，直條中心對齊刻度
            expense_data, 
            bar_width, 
            label='支出', 
            color='#ef4444',
            alpha=0.9,
            edgecolor='none'
        )
        
        # 如果需要顯示收入，可以用不同顏色的直條
        # 這裡先只顯示支出，符合參考圖片
        
        # 在柱子上顯示數值
        max_value = max(expense_data) if expense_data else 1
        
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + max_value * 0.01,
                       f'${height:.0f}', ha='center', va='bottom', fontsize=14, fontweight='bold')
        
        ax.set_title(title, fontsize=15, fontweight='bold', pad=20)
        ax.set_xlabel('', fontsize=12)
        ax.set_ylabel('金額 (元)', fontsize=12, fontweight='bold')
        ax.set_xticks(x_positions)  # 使用 x_positions 設定刻度
        ax.set_xticklabels(labels, fontsize=12)
        ax.tick_params(axis='y', labelsize=12)  # 設定 Y 軸刻度字體大小
        # ax.legend(fontsize=12, framealpha=0.9)  # 移除圖例
        ax.grid(True, alpha=0.2, axis='y', linestyle='--')
        
        # 設定 Y 軸刻度間隔
        if y_interval:
            # 計算最大值，並確保 Y 軸上限是間隔的倍數
            # 這樣可以保證刻度線能顯示出來
            current_max = max(expense_data) if expense_data else 0
            if current_max > 0:
                # 無條件進位到下一個間隔倍數
                top_limit = math.ceil(current_max / y_interval) * y_interval
                # 如果計算出的上限等於最大值（剛好整除），多加一個間隔以留白
                if top_limit == current_max:
                    top_limit += y_interval
                ax.set_ylim(0, top_limit)
                
            ax.yaxis.set_major_locator(MultipleLocator(y_interval))
        else:
            # 確保 y 軸從 0 開始
            ax.set_ylim(bottom=0)
        
        fig.tight_layout()
        return fig
    
    def show_year_category_chart(self, parent_frame, year: int) -> None:
        """顯示年度分類圓餅圖"""
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        transactions = self.transaction_manager.get_transactions_by_date_range(start_date, end_date)
        
        if not transactions:
            no_data_label = tk.Label(parent_frame, text="無交易資料", 
                                     font=('Microsoft YaHei', 40), fg='#94a3b8', bg='#FFFFFF')
            no_data_label.pack(expand=True)
            return
        
        # 統計分類資料
        expense_stats = defaultdict(float)
        
        for trans in transactions:
            if trans['type'] == 'expense':
                expense_stats[trans['category_name']] += trans['amount']
        
        if not expense_stats:
            no_data_label = tk.Label(parent_frame, text="無交易資料", 
                                     font=('Microsoft YaHei', 40), fg='#94a3b8', bg='#FFFFFF')
            no_data_label.pack(expand=True)
            return
        
        # 建立圓餅圖
        fig = self.create_pie_chart(expense_stats, f'{year}年支出分類')
        
        if fig:
            canvas = FigureCanvasTkAgg(fig, parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def show_month_category_chart(self, parent_frame, year: int, month: int) -> None:
        """顯示月度分類圓餅圖"""
        start_date = f"{year}-{month:02d}-01"
        last_day = calendar.monthrange(year, month)[1]
        end_date = f"{year}-{month:02d}-{last_day}"
        
        transactions = self.transaction_manager.get_transactions_by_date_range(start_date, end_date)
        
        if not transactions:
            no_data_label = tk.Label(parent_frame, text="無交易資料", 
                                     font=('Microsoft YaHei', 40), fg='#94a3b8', bg='#FFFFFF')
            no_data_label.pack(expand=True)
            return
        
        # 統計資料
        expense_stats = defaultdict(float)
        
        for trans in transactions:
            if trans['type'] == 'expense':
                expense_stats[trans['category_name']] += trans['amount']
        
        if not expense_stats:
            no_data_label = tk.Label(parent_frame, text="無交易資料", 
                                     font=('Microsoft YaHei', 40), fg='#94a3b8', bg='#FFFFFF')
            no_data_label.pack(expand=True)
            return
        
        # 建立圓餅圖
        fig = self.create_pie_chart(expense_stats, f'{year}年{month}月支出分類')
        
        if fig:
            canvas = FigureCanvasTkAgg(fig, parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def show_month_income_expense_chart(self, parent_frame, year: int) -> None:
        """顯示月度收支長條圖 + 月度列表"""
        # 收集12個月的資料
        months_labels = []
        income_data = []
        expense_data = []
        monthly_details = []  # 儲存月度明細
        
        for month in range(1, 13):
            summary = self.transaction_manager.get_monthly_summary(year, month)
            balance = summary['total_income'] - summary['total_expense']
            
            if summary['total_income'] > 0 or summary['total_expense'] > 0:
                months_labels.append(f"{month}月")
                income_data.append(summary['total_income'])
                expense_data.append(summary['total_expense'])
                monthly_details.append({
                    'month': month,
                    'label': f"{year}年{month:02d}月",
                    'balance': balance
                })
        
        if not months_labels:
            no_data_label = tk.Label(parent_frame, text="無交易資料", 
                                     font=('Microsoft YaHei', 40), fg='#94a3b8', bg='#FFFFFF')
            no_data_label.pack(expand=True)
            return
        
        # 計算年度總計
        year_total = sum(i - e for i, e in zip(income_data, expense_data))
        
        # 上方：年度總計標籤
        header_frame = tk.Frame(parent_frame, bg='#F8FAFC')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        year_total_text = f"年總計：${year_total:,.0f}" if year_total >= 0 else f"年總計：-${abs(year_total):,.0f}"
        year_total_color = '#10b981' if year_total >= 0 else '#ef4444'
        
        tk.Label(header_frame, text=year_total_text, font=('Microsoft YaHei', 16, 'bold'),
                 fg=year_total_color, bg='#F8FAFC').pack(side=tk.RIGHT, padx=20)
        
        # 中間：長條圖
        fig = self.create_bar_chart(income_data, expense_data, months_labels, 
                                    f'{year}年月度收支', y_interval=5000)
        
        if fig:
            canvas = FigureCanvasTkAgg(fig, parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.X, expand=False, pady=(0, 10))
        
        # 下方：月度明細列表 (可捲動)
        list_frame = tk.Frame(parent_frame, bg='#FFFFFF')
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # 建立 Canvas + Scrollbar
        canvas_scroll = tk.Canvas(list_frame, bg='#FFFFFF', highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas_scroll.yview)
        scrollable_frame = tk.Frame(canvas_scroll, bg='#FFFFFF')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))
        )
        
        canvas_scroll.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas_scroll.configure(yscrollcommand=scrollbar.set)
        
        canvas_scroll.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 填充月度明細 (倒序顯示，最近的月份在上方)
        for detail in reversed(monthly_details):
            row = tk.Frame(scrollable_frame, bg='#FFFFFF')
            row.pack(fill=tk.X, padx=15, pady=8)
            
            # 左側色塊
            color_block = tk.Frame(row, bg='#3b82f6', width=4, height=30)
            color_block.pack(side=tk.LEFT, padx=(0, 10))
            
            # 月份標籤
            tk.Label(row, text=detail['label'], font=('Microsoft YaHei', 14),
                    bg='#FFFFFF', fg='#334155').pack(side=tk.LEFT)
            
            # 金額
            balance = detail['balance']
            amount_text = f"${balance:,.0f}" if balance >= 0 else f"-${abs(balance):,.0f}"
            amount_color = '#10b981' if balance >= 0 else '#ef4444'
            tk.Label(row, text=amount_text, font=('Microsoft YaHei', 14, 'bold'),
                    bg='#FFFFFF', fg=amount_color).pack(side=tk.RIGHT)
    
    def show_daily_income_expense_chart(self, parent_frame, year: int, month: int) -> None:
        """顯示日度收支長條圖 + 日度列表"""
        start_date = f"{year}-{month:02d}-01"
        last_day = calendar.monthrange(year, month)[1]
        end_date = f"{year}-{month:02d}-{last_day}"
        
        transactions = self.transaction_manager.get_transactions_by_date_range(start_date, end_date)
        
        if not transactions:
            no_data_label = tk.Label(parent_frame, text="無交易資料", 
                                     font=('Microsoft YaHei', 40), fg='#94a3b8', bg='#FFFFFF')
            no_data_label.pack(expand=True)
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
        day_labels = [f"{day}日" for day in days]
        
        # 計算月度明細
        daily_details = []
        for date in dates:
            day = int(date.split('-')[2])
            balance = daily_stats[date]['income'] - daily_stats[date]['expense']
            daily_details.append({
                'day': day,
                'label': f"{month}月{day:02d}日",
                'balance': balance
            })
        
        # 計算月度總計
        month_total = sum(i - e for i, e in zip(income_data, expense_data))
        
        # 上方：月度總計標籤
        header_frame = tk.Frame(parent_frame, bg='#F8FAFC')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        month_total_text = f"月總計：${month_total:,.0f}" if month_total >= 0 else f"月總計：-${abs(month_total):,.0f}"
        month_total_color = '#10b981' if month_total >= 0 else '#ef4444'
        
        tk.Label(header_frame, text=month_total_text, font=('Microsoft YaHei', 16, 'bold'),
                 fg=month_total_color, bg='#F8FAFC').pack(side=tk.RIGHT, padx=20)
        
        # 中間：長條圖 (高度固定)
        fig = self.create_bar_chart(income_data, expense_data, day_labels, 
                                    f'{year}年{month}月每日收支', y_interval=500, bar_width=0.4)
        
        if fig:
            ax = fig.axes[0]
            ax.set_xticklabels(day_labels, rotation=45)
            fig.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.X, expand=False, pady=(0, 10))
        
        # 下方：日度明細列表 (可捲動)
        list_frame = tk.Frame(parent_frame, bg='#FFFFFF')
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas_scroll = tk.Canvas(list_frame, bg='#FFFFFF', highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas_scroll.yview)
        scrollable_frame = tk.Frame(canvas_scroll, bg='#FFFFFF')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))
        )
        
        canvas_scroll.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas_scroll.configure(yscrollcommand=scrollbar.set)
        
        canvas_scroll.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 填充日度明細 (倒序顯示)
        for detail in reversed(daily_details):
            row = tk.Frame(scrollable_frame, bg='#FFFFFF')
            row.pack(fill=tk.X, padx=15, pady=6)
            
            color_block = tk.Frame(row, bg='#3b82f6', width=4, height=24)
            color_block.pack(side=tk.LEFT, padx=(0, 10))
            
            tk.Label(row, text=detail['label'], font=('Microsoft YaHei', 13),
                    bg='#FFFFFF', fg='#334155').pack(side=tk.LEFT)
            
            balance = detail['balance']
            amount_text = f"${balance:,.0f}" if balance >= 0 else f"-${abs(balance):,.0f}"
            amount_color = '#10b981' if balance >= 0 else '#ef4444'
            tk.Label(row, text=amount_text, font=('Microsoft YaHei', 13, 'bold'),
                    bg='#FFFFFF', fg=amount_color).pack(side=tk.RIGHT)

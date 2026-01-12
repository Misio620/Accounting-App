"""
美化的 UI 元件
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import calendar
from .ui_config import COLORS, FONTS, SPACING, PADDING, ICONS, STAT_CARD_CONFIG


class StatCard(tk.Frame):
    """統計卡片元件"""
    
    def __init__(self, parent, card_type='income', **kwargs):
        super().__init__(parent, **kwargs)
        
        config = STAT_CARD_CONFIG[card_type]
        
        # 設定卡片樣式
        self.config(
            bg=config['bg'],
            relief='solid',
            borderwidth=1,
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS['border']
        )
        
        # 內容框架
        content = tk.Frame(self, bg=config['bg'])
        content.pack(fill=tk.BOTH, expand=True, padx=PADDING['loose'], pady=PADDING['loose'])
        
        # 標題 (已移除圖標)
        title_label = tk.Label(
            content,
            text=config['title'],
            font=FONTS['subheading'],
            bg=config['bg'],
            fg=COLORS['text_secondary']
        )
        title_label.pack(anchor='center', pady=(0, SPACING['sm']))
        
        # 金額顯示
        self.value_label = tk.Label(
            content,
            text='$0.00',
            font=FONTS['number_large'],
            bg=config['bg'],
            fg=config['color']
        )
        self.value_label.pack(anchor='center', pady=(SPACING['sm'], 0))
        
        # 趨勢顯示（預留）
        self.trend_label = tk.Label(
            content,
            text='',
            font=FONTS['caption'],
            bg=config['bg'],
            fg=COLORS['text_light']
        )
        self.trend_label.pack(anchor='center', pady=(SPACING['xs'], 0))
    
    def set_value(self, value, trend=None):
        """設定卡片數值"""
        self.value_label.config(text=f'${value:,.2f}')
        if trend:
            self.trend_label.config(text=trend)


class ModernButton(tk.Button):
    """現代化按鈕元件"""
    
    def __init__(self, parent, text='', style='primary', icon=None, **kwargs):
        # 準備文字（加入圖標）
        if icon and icon in ICONS:
            display_text = f"{ICONS[icon]} {text}"
        else:
            display_text = text
        
        # 根據樣式設定顏色
        if style == 'primary':
            bg = COLORS['primary']
            fg = '#ffffff'
            active_bg = COLORS['primary_dark']
        elif style == 'success':
            bg = COLORS['success']
            fg = '#ffffff'
            active_bg = '#059669'
        elif style == 'danger':
            bg = COLORS['danger']
            fg = '#ffffff'
            active_bg = '#dc2626'
        else:  # secondary
            bg = COLORS['bg_secondary']
            fg = COLORS['text_primary']
            active_bg = COLORS['border']
        
        super().__init__(
            parent,
            text=display_text,
            bg=bg,
            fg=fg,
            activebackground=active_bg,
            activeforeground=fg,
            font=FONTS['body'],
            relief='flat',
            cursor='hand2',
            padx=PADDING['normal'],
            pady=SPACING['sm'],
            **kwargs
        )
        
        # 綁定懸停效果
        self.default_bg = bg
        self.hover_bg = active_bg
        
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
    
    def _on_enter(self, event):
        self.config(bg=self.hover_bg)
    
    def _on_leave(self, event):
        self.config(bg=self.default_bg)


class SectionFrame(tk.Frame):
    """區塊框架（帶標題）"""
    
    def __init__(self, parent, title='', icon=None, **kwargs):
        super().__init__(parent, bg=COLORS['bg_primary'], **kwargs)
        
        # 標題列
        header = tk.Frame(self, bg=COLORS['bg_primary'])
        header.pack(fill=tk.X, pady=(0, SPACING['md']))
        
        # 標題文字
        title_text = f"{ICONS.get(icon, '')} {title}" if icon else title
        title_label = tk.Label(
            header,
            text=title_text,
            font=FONTS['heading'],
            bg=COLORS['bg_primary'],
            fg=COLORS['text_primary']
        )
        title_label.pack(side=tk.LEFT)
        
        # 內容框架
        self.content = tk.Frame(
            self,
            bg=COLORS['bg_card'],
            relief='solid',
            borderwidth=1,
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS['border']
        )
        self.content.pack(fill=tk.BOTH, expand=True)
        
        # 內部填充
        self.inner = tk.Frame(self.content, bg=COLORS['bg_card'])
        self.inner.pack(fill=tk.BOTH, expand=True, padx=PADDING['loose'], pady=PADDING['loose'])


class StyledLabel(tk.Label):
    """樣式化標籤"""
    
    def __init__(self, parent, text='', style='body', color='primary', **kwargs):
        font = FONTS.get(style, FONTS['body'])
        
        if color == 'primary':
            fg = COLORS['text_primary']
        elif color == 'secondary':
            fg = COLORS['text_secondary']
        elif color == 'success':
            fg = COLORS['success']
        elif color == 'danger':
            fg = COLORS['danger']
        else:
            fg = COLORS['text_primary']
        
        super().__init__(
            parent,
            text=text,
            font=font,
            fg=fg,
            bg=COLORS['bg_primary'],
            **kwargs
        )


def create_separator(parent, orient='horizontal'):
    """建立分隔線"""
    if orient == 'horizontal':
        sep = tk.Frame(parent, height=1, bg=COLORS['border'])
        sep.pack(fill=tk.X, pady=SPACING['md'])
    else:
        sep = tk.Frame(parent, width=1, bg=COLORS['border'])
        sep.pack(fill=tk.Y, padx=SPACING['md'])
    return sep


class DateSelector(tk.Frame):
    """年月日選擇器元件"""
    
    def __init__(self, parent, initial_date=None, on_date_change=None, **kwargs):
        super().__init__(parent, bg=COLORS['bg_primary'], **kwargs)
        
        self.on_date_change = on_date_change
        
        # 當前時間作為預設值
        current_date = initial_date if initial_date else datetime.now()
        
        # 年份 Combobox
        self.year_var = tk.StringVar(value=str(current_date.year))
        self.year_combo = ttk.Combobox(self, textvariable=self.year_var, width=5, state="readonly")
        self.year_combo['values'] = [str(y) for y in range(2018, 2101)]
        self.year_combo.pack(side=tk.LEFT)
        tk.Label(self, text="年", bg=COLORS['bg_primary']).pack(side=tk.LEFT, padx=(2, 5))
        
        # 月份 Combobox
        self.month_var = tk.StringVar(value=str(current_date.month))
        self.month_combo = ttk.Combobox(self, textvariable=self.month_var, width=3, state="readonly")
        self.month_combo['values'] = [str(m) for m in range(1, 13)]
        self.month_combo.pack(side=tk.LEFT)
        tk.Label(self, text="月", bg=COLORS['bg_primary']).pack(side=tk.LEFT, padx=(2, 5))
        
        # 日期 Combobox
        self.day_var = tk.StringVar(value=str(current_date.day))
        self.day_combo = ttk.Combobox(self, textvariable=self.day_var, width=3, state="readonly")
        self.day_combo['values'] = [str(d) for d in range(1, 32)]
        self.day_combo.pack(side=tk.LEFT)
        tk.Label(self, text="日", bg=COLORS['bg_primary']).pack(side=tk.LEFT, padx=(2, 0))
        
        # 綁定事件
        self.year_combo.bind('<<ComboboxSelected>>', self._update_days)
        self.month_combo.bind('<<ComboboxSelected>>', self._update_days)
        self.day_combo.bind('<<ComboboxSelected>>', self._notify_change)
        
        # 初始化天數
        self._update_days()
    
    def _update_days(self, event=None):
        """根據年月更新天數"""
        try:
            year = int(self.year_var.get())
            month = int(self.month_var.get())
            
            # 獲取該月最大天數
            _, max_day = calendar.monthrange(year, month)
            
            # 更新日期選項
            self.day_combo['values'] = [str(d) for d in range(1, max_day + 1)]
            
            # 檢查當前選擇是否有效
            current_day = int(self.day_var.get())
            if current_day > max_day:
                self.day_var.set(str(max_day))
                
            self._notify_change()
        except ValueError:
            pass
            
    def _notify_change(self, event=None):
        """通知外部日期變更"""
        if self.on_date_change:
            self.on_date_change(self.get_date_string())
            
    def get_date_string(self):
        """取得 YYYY-MM-DD 格式日期字串"""
        try:
            year = self.year_var.get()
            month = self.month_var.get().zfill(2)
            day = self.day_var.get().zfill(2)
            return f"{year}-{month}-{day}"
        except:
            return ""
            
    def set_date(self, date_str):
        """設定日期 (YYYY-MM-DD)"""
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            self.year_var.set(str(date_obj.year))
            self.month_var.set(str(date_obj.month))
            self.day_var.set(str(date_obj.day))
            self._update_days()
            self._notify_change()
        except ValueError:
            pass

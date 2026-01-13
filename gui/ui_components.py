"""
美化的 UI 元件 (CustomTkinter Version)
"""

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from datetime import datetime
import calendar
from .ui_config import COLORS, FONTS, SPACING, PADDING, ICONS, STAT_CARD_CONFIG, BUTTON_STYLES

class StatCard(ctk.CTkFrame):
    """統計卡片元件"""
    
    def __init__(self, parent, card_type='income', **kwargs):
        config = STAT_CARD_CONFIG[card_type]
        
        # 初始化 CTkFrame (背景色、圓角)
        super().__init__(
            parent, 
            fg_color=config['bg'], 
            corner_radius=10, 
            border_width=1,
            border_color=COLORS['border'],
            **kwargs
        )
        
        # 標題
        title_label = ctk.CTkLabel(
            self,
            text=config['title'],
            font=(FONTS['subheading'][0], FONTS['subheading'][1], 'bold'), # CTk font tuple
            text_color=COLORS['text_secondary']
        )
        title_label.pack(anchor='center', pady=(PADDING['normal'], SPACING['sm']))
        
        # 金額顯示
        self.value_label = ctk.CTkLabel(
            self,
            text='$0.00',
            font=(FONTS['number_large'][0], 24, 'bold'),
            text_color=config['color']
        )
        self.value_label.pack(anchor='center', pady=(0, 0))
        
        # 趨勢顯示（預留）
        self.trend_label = ctk.CTkLabel(
            self,
            text='',
            font=(FONTS['caption'][0], FONTS['caption'][1]),
            text_color=COLORS['text_light']
        )
        self.trend_label.pack(anchor='center', pady=(SPACING['xs'], PADDING['normal']))
    
    def set_value(self, value, trend=None):
        """設定卡片數值"""
        self.value_label.configure(text=f'${value:,.0f}') # 整數顯示
        if trend:
            self.trend_label.configure(text=trend)


class ModernButton(ctk.CTkButton):
    """現代化按鈕元件"""
    
    def __init__(self, parent, text='', style='primary', icon=None, **kwargs):
        # 準備文字（加入圖標）
        if icon and icon in ICONS:
            display_text = f"{ICONS[icon]} {text}"
        else:
            display_text = text
        
        # 取得樣式設定
        btn_style = BUTTON_STYLES.get(style, BUTTON_STYLES['primary'])
        
        border_width = btn_style.get('border_width', 0)
        border_color = btn_style.get('border_color', None)
        
        # 處理自定義高度
        height = kwargs.pop('height', 36)
        anchor = btn_style.get('anchor', 'center')
        
        super().__init__(
            parent,
            text=display_text,
            fg_color=btn_style['fg_color'],
            text_color=btn_style['text_color'],
            hover_color=btn_style['hover_color'],
            font=(FONTS['body'][0], 14),
            corner_radius=8,
            height=height,
            anchor=anchor,
            border_width=border_width,
            border_color=border_color,
            cursor='hand2',
            **kwargs
        )


class SectionFrame(ctk.CTkFrame):
    """區塊框架（帶標題）"""
    
    def __init__(self, parent, title='', icon=None, **kwargs):
        super().__init__(parent, fg_color=COLORS['bg_card'], corner_radius=10, **kwargs)
        
        # 即使內容是白色，背景也是白色，這裡做一個內部 padding 容器
        self.grid_columnconfigure(0, weight=1)
        
        # 標題列
        header_text = f"{ICONS.get(icon, '')} {title}" if icon else title
        self.title_label = ctk.CTkLabel(
            self,
            text=header_text,
            font=(FONTS['heading'][0], 16, 'bold'),
            text_color=COLORS['text_primary'],
            anchor='w'
        )
        self.title_label.pack(fill='x', padx=PADDING['normal'], pady=(PADDING['normal'], SPACING['sm']))
        
        # 內容框架
        self.content = ctk.CTkFrame(self, fg_color=COLORS['bg_card'])
        self.content.pack(fill='both', expand=True, padx=PADDING['normal'], pady=(0, PADDING['normal']))


class StyledLabel(ctk.CTkLabel):
    """樣式化標籤"""
    
    def __init__(self, parent, text='', style='body', color='primary', **kwargs):
        # 字體適配
        f_info = FONTS.get(style, FONTS['body'])
        font_tuple = (f_info[0], f_info[1])
        if len(f_info) > 2:
            font_tuple = (f_info[0], f_info[1], f_info[2])
            
        # 顏色適配
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
            font=font_tuple,
            text_color=fg,
            **kwargs
        )


def create_separator(parent, orient='horizontal'):
    """建立分隔線"""
    if orient == 'horizontal':
        sep = ctk.CTkFrame(parent, height=2, fg_color=COLORS['border'])
        sep.pack(fill='x', pady=SPACING['md'])
    else:
        sep = ctk.CTkFrame(parent, width=2, fg_color=COLORS['border'])
        sep.pack(fill='y', padx=SPACING['md'])
    return sep


class DateSelector(ctk.CTkFrame):
    """年月日選擇器元件 (CTk Version)"""
    
    def __init__(self, parent, initial_date=None, on_date_change=None, **kwargs):
        super().__init__(parent, fg_color=None, **kwargs)
        
        self.on_date_change = on_date_change
        
        # 當前時間作為預設值
        current_date = initial_date if initial_date else datetime.now()
        
        # 年份 Combobox
        self.year_var = ctk.StringVar(value=str(current_date.year))
        years = [str(y) for y in range(2018, 2101)]
        self.year_combo = ctk.CTkComboBox(
            self, variable=self.year_var, values=years, width=80, 
            command=self._update_days, state="readonly"
        )
        self.year_combo.pack(side=tk.LEFT, padx=(0, 2))
        ctk.CTkLabel(self, text="年", width=20).pack(side=tk.LEFT)
        
        # 月份 Combobox
        self.month_var = ctk.StringVar(value=str(current_date.month))
        months = [str(m) for m in range(1, 13)]
        self.month_combo = ctk.CTkComboBox(
            self, variable=self.month_var, values=months, width=60,
            command=self._update_days, state="readonly"
        )
        self.month_combo.pack(side=tk.LEFT, padx=(5, 2))
        ctk.CTkLabel(self, text="月", width=20).pack(side=tk.LEFT)
        
        # 日期 Combobox
        self.day_var = ctk.StringVar(value=str(current_date.day))
        days = [str(d) for d in range(1, 32)]
        self.day_combo = ctk.CTkComboBox(
            self, variable=self.day_var, values=days, width=60,
            command=self._notify_change, state="readonly"
        )
        self.day_combo.pack(side=tk.LEFT, padx=(5, 2))
        ctk.CTkLabel(self, text="日", width=20).pack(side=tk.LEFT)
        
        # 初始化天數
        # self._update_days() # CTkComboBox command might be triggered on set? No.
    
    def _update_days(self, selection=None):
        """根據年月更新天數"""
        try:
            year = int(self.year_var.get())
            month = int(self.month_var.get())
            
            # 獲取該月最大天數
            _, max_day = calendar.monthrange(year, month)
            
            # 更新日期選項
            new_values = [str(d) for d in range(1, max_day + 1)]
            self.day_combo.configure(values=new_values)
            
            # 檢查當前選擇是否有效
            current_day = int(self.day_var.get())
            if current_day > max_day:
                self.day_var.set(str(max_day))
                
            self._notify_change()
        except ValueError:
            pass
            
    def _notify_change(self, selection=None):
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
            self._update_days() # Update values list logic
            # self._notify_change() # Do not notify on programmatic set to avoid loops? Or yes? Usually yes.
        except ValueError:
            pass

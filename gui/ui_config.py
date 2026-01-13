"""
UI 配置檔案 - 統一的顏色、字體、間距設定
"""

# 配色方案 (Modern Minimalist - Light Theme Optimized)
COLORS = {
    # 主色 (macOS Blue / CTk Theme Blue)
    'primary': '#3B8ED0',       
    'primary_light': '#60A5FA', 
    'primary_dark': '#1F6AA5',  
    
    # 功能色
    'success': '#2CC985',      # 現代感綠
    'danger': '#EE5555',       # 柔和紅
    'warning': '#FFAA00',      # 暖橘
    'info': '#409CFF',         # 亮藍
    
    # 背景色
    'bg_primary': '#F3F4F6',   # 淺灰 (Dashboard 背景)
    'bg_secondary': '#FFFFFF', # 輔助背景
    'bg_dark': '#2B2B2B',
    'bg_card': '#FFFFFF',
    
    # Sidebar 專用色
    'sidebar_bg': '#1E293B',        # 深藍灰 (Slate 800)
    'sidebar_text': '#94A3B8',      # 淺灰文字 (Slate 400)
    'sidebar_text_active': '#FFFFFF', # 亮白文字
    'sidebar_selected': '#334155',  # 選中背景 (Slate 700)
    'sidebar_hover': '#334155',     # 懸停背景
    
    # 文字色
    'text_primary': '#1E293B', # 深色主文
    'text_secondary': '#64748B', # 次要文字
    'text_light': '#94A3B8',

    # 邊框色
    'border': '#E2E8F0',
    'border_light': '#F1F5F9',
    
    # 圖表配色（8色）
    'chart_colors': [
        '#3b82f6',  # 藍
        '#10b981',  # 綠
        '#f59e0b',  # 橙
        '#8b5cf6',  # 紫
        '#ec4899',  # 粉
        '#06b6d4',  # 青
        '#f97316',  # 深橙
        '#6366f1',  # 靛藍
    ]
}

# 字體設定
FONTS = {
    'title': ('Microsoft YaHei UI', 24, 'bold'),
    'heading': ('Microsoft YaHei UI', 16, 'bold'),
    'subheading': ('Microsoft YaHei UI', 14, 'bold'),
    'body': ('Microsoft YaHei UI', 12),
    'caption': ('Microsoft YaHei UI', 10),
    'number': ('Consolas', 14, 'bold'),
    'number_large': ('Consolas', 20, 'bold'),
}

# 間距系統
SPACING = {
    'xs': 4,
    'sm': 8,
    'md': 16,
    'lg': 24,
    'xl': 32,
    'xxl': 48,
}

PADDING = {
    'tight': 8,
    'normal': 16,
    'loose': 24,
    'extra': 32,
}

# 圖標
ICONS = {
    'income': '💰',
    'expense': '💸',
    'balance': '💵',
    'category': '📁',
    'chart': '📊',
    'calendar': '📅',
    'filter': '🔍',
    'export': '📤',
    'backup': '💾',
    'settings': '⚙️',
    'add': '➕',
    'edit': '✏️',
    'delete': '🗑️',
    'refresh': '🔄',
    'success': '✅',
    'warning': '⚠️',
    'error': '❌',
    'info': 'ℹ️',
    'up': '↑',
    'down': '↓',
    'dollar': '💲',
}

# 按鈕樣式配置 (CTk 適配)
BUTTON_STYLES = {
    'primary': {
        'fg_color': COLORS['primary'],
        'text_color': '#ffffff',
        'hover_color': COLORS['primary_dark'],
    },
    'success': {
        'fg_color': COLORS['success'],
        'text_color': '#ffffff',
        'hover_color': '#25AD71',
    },
    'danger': {
        'fg_color': COLORS['danger'],
        'text_color': '#ffffff',
        'hover_color': '#CF4444',
    },
    'secondary': {
        'fg_color': '#FFFFFF',
        'text_color': COLORS['text_primary'],
        'hover_color': '#F1F5F9',
        'border_width': 1,
        'border_color': COLORS['border'],
    },
    'sidebar': {
        'fg_color': 'transparent',
        'text_color': '#94A3B8',
        'hover_color': '#334155',
        'anchor': 'w',
    },
    'sidebar_active': {
        'fg_color': '#334155',
        'text_color': '#FFFFFF',
        'hover_color': '#334155',
        'anchor': 'w',
        'border_color': COLORS['primary'],
        'border_width': 0, # Left border handled manually or via compound
    }
}

# 卡片樣式
CARD_STYLE = {
    'bg': COLORS['bg_card'],
    'border': COLORS['border'],
    'relief': 'solid',
    'borderwidth': 1,
    'padding': PADDING['loose'],
}

# 統計卡片配置
STAT_CARD_CONFIG = {
    'income': {
        'icon': ICONS['income'],
        'title': '本月收入',
        'color': COLORS['success'],
        'bg': '#d1fae5',
    },
    'expense': {
        'icon': ICONS['expense'],
        'title': '本月支出',
        'color': COLORS['danger'],
        'bg': '#fee2e2',
    },
    'balance': {
        'icon': ICONS['balance'],
        'title': '本月結餘',
        'color': COLORS['primary'],
        'bg': '#dbeafe',
    }
}

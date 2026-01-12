"""
UI 配置檔案 - 統一的顏色、字體、間距設定
"""

# 配色方案
COLORS = {
    # 主色
    'primary': '#2563eb',
    'primary_light': '#3b82f6',
    'primary_dark': '#1e40af',
    
    # 功能色
    'success': '#10b981',      # 綠色（收入）
    'danger': '#ef4444',       # 紅色（支出）
    'warning': '#f59e0b',      # 橙色
    'info': '#06b6d4',         # 青色
    
    # 背景色
    'bg_primary': '#ffffff',
    'bg_secondary': '#f8fafc',
    'bg_dark': '#1e293b',
    'bg_card': '#ffffff',
    
    # 文字色
    'text_primary': '#0f172a',
    'text_secondary': '#64748b',
    'text_light': '#94a3b8',
    
    # 邊框色
    'border': '#e2e8f0',
    'border_light': '#f1f5f9',
    
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
    'title': ('Microsoft YaHei UI', 22, 'bold'),
    'heading': ('Microsoft YaHei UI', 14, 'bold'),
    'subheading': ('Microsoft YaHei UI', 12, 'bold'),
    'body': ('Microsoft YaHei UI', 11),
    'caption': ('Microsoft YaHei UI', 9),
    'number': ('Consolas', 12, 'bold'),
    'number_large': ('Consolas', 16, 'bold'),
}

# 間距系統
SPACING = {
    'xs': 4,
    'sm': 8,
    'md': 12,
    'lg': 16,
    'xl': 24,
    'xxl': 32,
}

PADDING = {
    'tight': 8,
    'normal': 12,
    'loose': 16,
    'extra': 20,
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
}

# 按鈕樣式配置
BUTTON_STYLES = {
    'primary': {
        'bg': COLORS['primary'],
        'fg': '#ffffff',
        'active_bg': COLORS['primary_dark'],
        'padding': (10, 20),
    },
    'success': {
        'bg': COLORS['success'],
        'fg': '#ffffff',
        'active_bg': '#059669',
        'padding': (10, 20),
    },
    'danger': {
        'bg': COLORS['danger'],
        'fg': '#ffffff',
        'active_bg': '#dc2626',
        'padding': (10, 20),
    },
    'secondary': {
        'bg': COLORS['bg_secondary'],
        'fg': COLORS['text_primary'],
        'active_bg': COLORS['border'],
        'padding': (10, 20),
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

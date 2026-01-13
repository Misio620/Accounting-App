# 個人記帳本 💰

> 使用 Python + CustomTkinter 開發的現代化桌面記帳軟體

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ 功能特色

### 🏠 Dashboard 首頁
- 統計卡片即時顯示收入/支出/結餘
- 交易列表快速瀏覽
- 期間篩選：本日、本週、本月、本年、所有紀錄

### 📊 報表分析
- **年分類**：年度支出分類圓餅圖
- **月分類**：月度支出分類圓餅圖
- **月收支**：12 個月收支趨勢 + 月度明細列表
- **日收支**：每日收支長條圖 + 日度明細列表

### 💾 資料管理
- SQLite 本地資料庫儲存
- CSV / Excel 匯出
- 分類管理（新增/編輯/刪除）

## 📸 截圖預覽

| 首頁 Dashboard | 報表分析 |
|----------------|----------|
| 統計卡片 + 交易列表 | 圖表 + 明細列表 |

## 🚀 快速開始

### 安裝依賴
```bash
pip install -r requirements.txt
```

### 執行程式
```bash
python main.py
```

## ⌨️ 快捷鍵

| 快捷鍵 | 功能 |
|--------|------|
| `Ctrl+N` | 新增交易 |
| `Ctrl+E` | 編輯交易 |
| `Del` | 刪除交易 |
| `F5` | 重新整理 |
| `Ctrl+S` | 匯出 CSV |
| `Ctrl+M` | 分類管理 |

## 📁 專案結構

```
Accounting App/
├── main.py                 # 程式入口
├── requirements.txt        # 依賴清單
├── database/
│   └── models.py           # 資料庫模型
└── gui/
    ├── main_window.py      # 主視窗 (Dashboard)
    ├── dialogs.py          # 對話框
    ├── charts.py           # 圖表模組
    ├── filters.py          # 篩選器
    ├── ui_config.py        # UI 配置
    └── ui_components.py    # UI 元件
```

## 🛠️ 技術棧

| 類別 | 技術 |
|------|------|
| 語言 | Python 3.9+ |
| UI 框架 | CustomTkinter |
| 圖表 | Matplotlib |
| 資料庫 | SQLite |
| 匯出 | openpyxl (Excel) |

## 📋 環境需求

- Python 3.9 或更高版本
- Windows 10 / 11
- 建議螢幕解析度：1280 x 720+

## 📝 開發歷程

詳見 [DEVELOPMENT_LOG.md](DEVELOPMENT_LOG.md)

## 📄 License

MIT License
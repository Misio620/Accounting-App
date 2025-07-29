# 個人記帳應用程式

使用 Python + tkinter 開發的桌面記帳軟體，具備完整的圖表報表功能。

## 🎯 功能特色

- ✅ 交易記錄管理（新增、編輯、刪除）
- ✅ 進階篩選和搜尋功能
- ✅ 圓餅圖報表（年度/月度分類統計）
- ✅ 長條圖報表（月度/日度收支對比）
- ✅ CSV/Excel 資料匯出功能
- ✅ SQLite 資料庫儲存

## 📦 安裝需求

```bash
pip install matplotlib openpyxl
```

## 🚀 使用方法

```bash
python main.py
```

## 📁 專案結構

```
accounting_app/
├── database/
│   ├── __init__.py
│   └── models.py          # 資料庫模型
├── gui/
│   ├── __init__.py
│   └── main_window.py     # 主視窗界面
├── main.py                # 程式入口
├── requirements.txt       # 相依套件
├── README.md             # 專案說明
└── .gitignore            # Git 忽略檔案
```

## 📊 圖表功能

- **圓餅圖**：顯示分類支出/收入占比
- **長條圖**：顯示月度/日度收支對比
- **統計摘要**：自動計算總收入、總支出、結餘

## 🛠️ 開發工具

- Python 3.9+
- tkinter (GUI)
- matplotlib (圖表)
- openpyxl (Excel 匯出)
- SQLite (資料庫)
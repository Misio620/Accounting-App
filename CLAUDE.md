# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案概述

個人記帳本應用程式 - 使用 Python + tkinter 開發的桌面記帳軟體，支援交易記錄管理、圖表報表分析、資料匯出等功能。

## 常用開發指令

### 環境檢查與設定

```bash
# 檢查開發環境完整性（必須先執行）
python setup_check.py

# 測試基本資料庫功能
python test_basic.py

# 安裝相依套件
pip install -r requirements.txt
```

### 執行應用程式

```bash
# 啟動主程式
python main.py
```

### 測試與開發

```bash
# 單元測試（測試資料庫功能）
python test_basic.py

# 環境診斷（檢查檔案完整性、Python 模組、資料庫狀態）
python setup_check.py
```

## 架構設計

### 模組結構

專案採用 **三層架構**：

1. **資料層 (database/)**: 處理 SQLite 資料庫操作
2. **UI 層 (clean_main_window.py)**: tkinter GUI 界面和使用者互動
3. **應用層 (main.py)**: 程式入口點和初始化

### 資料庫架構

使用 **SQLite** 作為資料儲存，包含兩個核心資料表：

- **categories**: 分類管理（收入/支出分類）
- **transactions**: 交易記錄（日期、類型、金額、分類、備註）

索引優化：在 `date`、`type`、`category_id` 欄位建立索引提升查詢效能。

### 三個管理器類別

定義在 `database/models.py`：

- **DatabaseManager**: 負責資料庫連接和初始化
- **CategoryManager**: 分類的 CRUD 操作
- **TransactionManager**: 交易記錄的 CRUD 操作和統計查詢

### UI 元件設計

`clean_main_window.py` 包含：

- **MainWindow**: 主視窗（交易列表、篩選、統計）
- **TransactionDialog**: 新增/編輯交易的對話框
- 圖表功能（使用 matplotlib，可選）

### 匯入注意事項

- `clean_main_window.py` 需要從正確路徑匯入資料庫模組
- 預期匯入路徑：`from database.models import DatabaseManager, CategoryManager, TransactionManager`
- 如果檔案中使用 `from database_models import ...`，應修正為 `from database.models import ...`

## 資料流程

1. **啟動** → `main.py` 匯入並執行 `MainWindow`
2. **初始化** → `DatabaseManager` 建立/開啟 `accounting.db`，插入預設分類
3. **使用者操作** → UI 呼叫 `TransactionManager` 或 `CategoryManager` 方法
4. **資料持久化** → 透過 SQLite 儲存在 `accounting.db`

## 開發注意事項

### 快捷鍵支援

應用程式包含以下快捷鍵（定義在 `clean_main_window.py`）：

- `Ctrl+N`: 新增交易
- `Ctrl+E`: 編輯交易
- `Del`: 刪除交易
- `F5`: 重新整理
- `Ctrl+S`: 匯出 CSV

### 圖表功能

- matplotlib 是**可選依賴**
- 程式會檢查 `MATPLOTLIB_AVAILABLE` 標誌決定是否啟用圖表功能
- 圖表類型：圓餅圖（分類占比）、長條圖（收支對比）

### 資料匯出

支援兩種格式：
- **CSV**: 使用標準庫 `csv` 模組
- **Excel**: 需安裝 `openpyxl` 套件

### 預設分類

資料庫初始化時會自動建立 10 個預設分類：
- 收入：薪資、獎金、副業收入、其他收入
- 支出：飲食、交通、購物、娛樂、醫療、其他支出

## 檔案位置

- **主程式**: `main.py`
- **主視窗**: `clean_main_window.py`
- **資料庫模型**: `database/models.py`
- **資料庫檔案**: `accounting.db`（執行時自動建立）
- **測試檔案**: `test_basic.py`、`test_simple.db`（測試用）
- **備份目錄**: `backup/`（建議定期備份 accounting.db）

## 故障排除

如遇到匯入錯誤或模組找不到：
1. 執行 `python setup_check.py` 診斷問題
2. 檢查 `database/__init__.py` 是否存在
3. 確認匯入路徑是否正確（`database.models` 而非 `database_models`）

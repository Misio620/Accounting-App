# 個人記帳本 - 開發歷程記錄

> 此文件記錄了整個專案從初版到現在的完整開發過程，包含 UI 重構、Bug 修復、功能迭代等詳細說明。

---

## 專案概覽

| 項目 | 說明 |
|------|------|
| **專案名稱** | 個人記帳本 (Personal Accounting App) |
| **技術棧** | Python + CustomTkinter + SQLite + Matplotlib |
| **開發期間** | 2025-10 ~ 2026-01 |
| **當前版本** | v2.0 Dashboard |

---

## 開發階段一：初版建立 (2025-10)

### 架構設計

採用**三層架構**：

1. **資料層 (`database/`)**: SQLite 資料庫操作
2. **UI 層 (`gui/`)**: tkinter GUI 界面
3. **應用層 (`main.py`)**: 程式入口點

### 資料庫設計

兩個核心資料表：
- **categories**: 分類管理（收入/支出分類）
- **transactions**: 交易記錄（日期、類型、金額、分類、備註）

### 管理器模式

定義在 `database/models.py`：
- **DatabaseManager**: 資料庫連接和初始化
- **CategoryManager**: 分類的 CRUD 操作
- **TransactionManager**: 交易記錄的 CRUD 操作和統計查詢

---

## 開發階段二：Bug 修復 (2025-10-29)

### 🔴 問題 1：匯入路徑錯誤（嚴重）

**原始程式碼**:
```python
from database_models import DatabaseManager, CategoryManager, TransactionManager
```

**修正後**:
```python
from database.models import DatabaseManager, CategoryManager, TransactionManager
```

### 🟡 問題 2：show_year_category_chart() 方法實現錯誤

- 方法名稱與實現不符（寫成長條圖而非圓餅圖）
- 未定義的 `month` 變數導致 NameError
- 錯誤訊息與實際功能不符

**修正內容**:
1. ✅ 將統計邏輯從「每日收支」改為「分類金額」
2. ✅ 將圖表類型從「長條圖」改為「圓餅圖」
3. ✅ 移除未定義的 `month` 變數
4. ✅ 更正錯誤訊息

---

## 開發階段三：UI 現代化重構 (2026-01)

### 技術遷移

| 項目 | 變更前 | 變更後 |
|------|--------|--------|
| UI 框架 | tkinter | CustomTkinter |
| 佈局 | 傳統視窗式 | Dashboard 側邊欄式 |
| 主題 | 預設 | Modern Minimalist (Light) |

### 主要變更

#### 1. Dashboard 風格介面
- 固定寬度側邊欄 (240px)
- 內容區域自適應
- 統計卡片 (收入/支出/結餘)

#### 2. 視圖管理系統
- 首頁 (Dashboard)
- 報表分析 (4 種報表內嵌顯示)
- 資料管理 (匯出/備份/分類)

#### 3. 報表功能重構
- 從彈出視窗改為**內嵌頁面顯示**
- 4 種報表：年分類、月分類、月收支、日收支
- 年月切換即時更新圖表
- 無資料時顯示「無交易資料」(40pt 置中)

#### 4. 快捷篩選功能
- 首頁整合交易列表
- 期間篩選：本日、本週、本月、本年、所有紀錄

### 解決的技術問題

| 問題 | 解決方案 |
|------|----------|
| CTkComboBox 與 StringVar 連接失效 | 將變數儲存到各視圖的 parent 物件 |
| 報表視圖切換後變數被覆蓋 | switch_view 中更新 current_report_type |
| 圖表與列表比例不均 | 圖表使用 `expand=False` 固定高度 |

---

## 專案結構

```
Accounting App/
├── main.py                    # 程式入口
├── requirements.txt           # 依賴清單
├── README.md                  # 專案說明
├── DEVELOPMENT_LOG.md         # 開發歷程 (本文件)
├── .gitignore                 # Git 忽略規則
│
├── database/
│   ├── __init__.py
│   └── models.py              # 資料庫模型
│
├── gui/
│   ├── __init__.py
│   ├── main_window.py         # 主視窗 (52KB)
│   ├── dialogs.py             # 對話框
│   ├── charts.py              # 圖表模組
│   ├── filters.py             # 篩選器
│   ├── ui_config.py           # UI 配置 (顏色/字體/間距)
│   ├── ui_components.py       # UI 元件 (StatCard/ModernButton)
│   ├── report_window.py       # 報表視窗 (舊版，保留參考)
│   ├── improved_dialog.py     # 改進對話框 (開發備份)
│   └── main_window_backup_classic.py  # 經典版備份
│
├── utils/
│   └── backup.py              # 備份工具
│
├── tests/                     # 測試目錄
│
└── 開發工具腳本/
    ├── check_db.py            # 資料庫檢查
    ├── check_program.py       # 程式檢查
    ├── cleanup.py             # 清理工具
    ├── setup_check.py         # 環境檢查
    ├── run_tests.py           # 測試執行器
    └── test_*.py              # 各種測試腳本
```

---

## 快捷鍵

| 快捷鍵 | 功能 |
|--------|------|
| `Ctrl+N` | 新增交易 |
| `Ctrl+E` | 編輯交易 |
| `Del` | 刪除交易 |
| `F5` | 重新整理 |
| `Ctrl+S` | 匯出 CSV |
| `Ctrl+M` | 分類管理 |

---

## 依賴套件

```txt
customtkinter
matplotlib (可選，用於圖表)
openpyxl (可選，用於 Excel 匯出)
```

---

## 環境需求

- Python 3.9+
- Windows 10/11
- 建議螢幕解析度：1280x720+

---

## 故障排除

### 問題：Python 命令無法執行
**解決**：確認 Python 已安裝並加入 PATH，或使用 `py main.py` 執行

### 問題：看不到圖表
**解決**：安裝 matplotlib `pip install matplotlib`

### 問題：匯入錯誤
**解決**：確認匯入路徑為 `database.models` 而非 `database_models`

---

## 版本歷史

| 版本 | 日期 | 說明 |
|------|------|------|
| v1.0 | 2025-10 | 初版，基礎功能 |
| v1.0.1 | 2025-10-29 | 修復匯入路徑和圖表方法 |
| v2.0 | 2026-01-13 | CustomTkinter 重構，Dashboard 風格 |

---

## 未來規劃

### 短期
- [ ] 增加更多圖表類型
- [ ] 支援深色模式

### 中期
- [ ] 預算管理功能
- [ ] 匯出 PDF 報表

### 長期
- [ ] 多帳戶支援
- [ ] 雲端同步

---

*最後更新：2026-01-13*

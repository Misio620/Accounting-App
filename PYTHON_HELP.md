# Python 環境問題排查指南

## 🔍 問題診斷

你的 terminal 無法執行 `python` 命令，可能的原因：

### 1. Python 未安裝
### 2. Python 未加入環境變數 PATH
### 3. 使用了錯誤的命令名稱

---

## ✅ 解決方案

### 方案一：使用啟動腳本（最簡單）⭐

**直接雙擊執行：**
```
start.bat
```

這個腳本會自動尋找 Python 並啟動程式。

---

### 方案二：直接雙擊 main.py

1. 在檔案總管中找到 `main.py`
2. 直接雙擊 `main.py`
3. 如果已安裝 Python，程式會自動啟動

---

### 方案三：檢查 Python 安裝

**開啟 PowerShell 或 CMD，嘗試以下命令：**

```powershell
# 嘗試 1
python --version

# 嘗試 2
python3 --version

# 嘗試 3
py --version

# 嘗試 4
where python
```

**如果都顯示錯誤，表示 Python 未安裝或未加入 PATH。**

---

### 方案四：安裝/重新安裝 Python

#### 步驟 1：下載 Python
1. 前往 https://www.python.org/downloads/
2. 下載最新版本（建議 Python 3.11 或 3.12）

#### 步驟 2：安裝 Python
1. 執行下載的安裝檔
2. **重要：勾選 "Add Python to PATH"** ✅
3. 點擊 "Install Now"
4. 等待安裝完成

#### 步驟 3：驗證安裝
開啟新的 terminal（重要：必須是新的），執行：
```bash
python --version
```

應該顯示類似：
```
Python 3.11.x
```

---

### 方案五：手動加入 PATH（進階）

如果 Python 已安裝但無法執行：

#### Windows 10/11:
1. 按 `Win + X`，選擇「系統」
2. 點擊「進階系統設定」
3. 點擊「環境變數」
4. 在「系統變數」中找到 `Path`
5. 點擊「編輯」
6. 點擊「新增」
7. 加入 Python 路徑，例如：
   ```
   C:\Users\你的使用者名稱\AppData\Local\Programs\Python\Python311
   C:\Users\你的使用者名稱\AppData\Local\Programs\Python\Python311\Scripts
   ```
8. 點擊「確定」
9. **重新開啟 terminal**

---

## 🚀 快速啟動方法

### 方法 1：使用 start.bat（推薦）
```
雙擊 start.bat
```

### 方法 2：使用 py 命令
```bash
py main.py
```

### 方法 3：使用完整路徑
```bash
C:\Users\你的使用者名稱\AppData\Local\Programs\Python\Python311\python.exe main.py
```

### 方法 4：直接雙擊
```
雙擊 main.py
```

---

## 📋 檢查清單

完成以下檢查：

- [ ] Python 已安裝
- [ ] Python 版本 ≥ 3.9
- [ ] Python 已加入 PATH
- [ ] 可以執行 `python --version`
- [ ] 可以執行 `pip --version`

---

## 🔧 常見問題

### Q: 執行 python 顯示「不是內部或外部命令」
**A:** Python 未加入 PATH，使用 `start.bat` 或重新安裝 Python（記得勾選 Add to PATH）

### Q: 雙擊 main.py 閃退
**A:** 程式可能有錯誤，使用 `start.bat` 啟動可以看到錯誤訊息

### Q: 顯示「找不到模組」
**A:** 需要安裝依賴：
```bash
pip install matplotlib openpyxl
```

### Q: 我不確定 Python 是否已安裝
**A:** 
1. 開啟 CMD
2. 輸入 `py --version`
3. 如果顯示版本號，表示已安裝
4. 如果顯示錯誤，表示未安裝

---

## 💡 建議的啟動方式

**對於你的情況，建議：**

1. **最簡單：** 直接雙擊 `start.bat`
2. **次選：** 直接雙擊 `main.py`
3. **如果都不行：** 重新安裝 Python（記得勾選 Add to PATH）

---

## 📞 需要更多幫助？

如果以上方法都不行，請提供：
1. 執行 `py --version` 的結果
2. 執行 `where python` 的結果
3. 你的 Windows 版本
4. 是否有安裝過 Python

我會根據這些資訊提供更具體的解決方案。

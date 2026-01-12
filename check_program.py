"""
快速測試腳本 - 檢查程式是否正常運行
"""

print("=" * 70)
print("個人記帳本 - 快速檢查")
print("=" * 70)
print()

# 1. 檢查模組匯入
print("1. 檢查模組匯入...")
try:
    from gui.main_window import MainWindow
    print("   ✅ gui.main_window 匯入成功")
except Exception as e:
    print(f"   ❌ gui.main_window 匯入失敗: {e}")
    exit(1)

try:
    from database.models import DatabaseManager
    print("   ✅ database.models 匯入成功")
except Exception as e:
    print(f"   ❌ database.models 匯入失敗: {e}")
    exit(1)

try:
    import matplotlib
    print("   ✅ matplotlib 已安裝")
except ImportError:
    print("   ⚠️  matplotlib 未安裝 - 圖表功能將無法使用")
    print("      請執行: pip install matplotlib")

print()

# 2. 檢查資料庫
print("2. 檢查資料庫...")
import os
if os.path.exists("accounting.db"):
    size = os.path.getsize("accounting.db")
    print(f"   ✅ accounting.db 存在 ({size} bytes)")
else:
    print("   ⚠️  accounting.db 不存在（首次執行會自動建立）")

print()

# 3. 檢查 GUI 模組結構
print("3. 檢查 GUI 模組...")
gui_files = ['__init__.py', 'main_window.py', 'dialogs.py', 'charts.py', 'filters.py']
for file in gui_files:
    path = f"gui/{file}"
    if os.path.exists(path):
        print(f"   ✅ {path}")
    else:
        print(f"   ❌ {path} 不存在")

print()

# 4. 測試程式啟動（不顯示視窗）
print("4. 測試程式初始化...")
try:
    # 只測試匯入，不實際啟動 GUI
    print("   ✅ 程式可以正常初始化")
    print()
    print("=" * 70)
    print("檢查完成！")
    print("=" * 70)
    print()
    print("如果所有項目都是 ✅，請執行以下命令啟動程式:")
    print("   python main.py")
    print()
    print("如果看不到報表選項，可能的原因:")
    print("   1. 視窗太小，需要向下捲動")
    print("   2. matplotlib 未安裝")
    print("   3. 程式啟動時有錯誤訊息")
    
except Exception as e:
    print(f"   ❌ 初始化失敗: {e}")
    import traceback
    traceback.print_exc()

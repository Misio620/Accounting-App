"""
快速測試 UI 美化版本
"""

print("測試 UI 美化版本...")
print()

try:
    from gui.main_window import MainWindow
    print("✅ 主視窗匯入成功")
    
    print("\n正在啟動程式...")
    app = MainWindow()
    print("✅ 程式初始化成功")
    
    print("\n🎨 UI 美化版本已啟動！")
    print("請查看程式視窗，應該看到：")
    print("  - 💵 大標題圖標")
    print("  - 彩色按鈕（藍色/綠色/紅色）")
    print("  - 三個統計卡片（💰💸💵）")
    print("  - 更美觀的圖表配色")
    print()
    
    app.run()
    
except Exception as e:
    print(f"❌ 錯誤: {e}")
    import traceback
    traceback.print_exc()

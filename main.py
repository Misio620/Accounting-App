#!/usr/bin/env python3
"""
個人記帳本應用程式
主程式入口點

使用方法：
python main.py
"""

import sys
import os

# 確保可以找到專案模組
sys.path.insert(0, os.path.dirname(__file__))

try:
    from clean_main_window import MainWindow
except ImportError as e:
    print(f"錯誤：找不到主視窗模組 - {e}")
    print("請確認 clean_main_window.py 檔案存在且語法正確")
    print("\n嘗試其他導入方式...")
    try:
        import clean_main_window
        MainWindow = clean_main_window.MainWindow
        print("✅ 使用替代方式導入成功")
    except Exception as e2:
        print(f"❌ 替代導入也失敗：{e2}")
        sys.exit(1)

def main():
    """主程式"""
    print("啟動個人記帳本...")
    
    try:
        # 建立並執行主視窗
        app = MainWindow()
        app.run()
        
    except KeyboardInterrupt:
        print("\n程式被使用者中斷")
    except Exception as e:
        print(f"程式執行錯誤：{e}")
        import traceback
        traceback.print_exc()
        input("按 Enter 鍵退出...")

if __name__ == "__main__":
    main()
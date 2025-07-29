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

from gui.main_window import MainWindow

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
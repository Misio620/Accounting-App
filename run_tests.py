"""
執行所有測試的主腳本
"""

import sys
import os

# 將專案根目錄加入路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# 匯入測試模組
from tests.test_database import run_tests as run_database_tests


def main():
    """執行所有測試"""
    print("="*70)
    print("個人記帳應用程式 - 單元測試")
    print("="*70)
    print()
    
    all_success = True
    
    # 執行資料庫測試
    print("📊 執行資料庫模組測試...")
    print("-"*70)
    result = run_database_tests()
    
    if not result.wasSuccessful():
        all_success = False
    
    print()
    print("="*70)
    if all_success:
        print("✅ 所有測試通過！")
    else:
        print("❌ 部分測試失敗，請檢查上方錯誤訊息")
    print("="*70)
    
    return 0 if all_success else 1


if __name__ == '__main__':
    sys.exit(main())

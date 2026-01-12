"""
專案清理工具
自動刪除不需要的檔案
"""

import os
import shutil
from datetime import datetime

# 要刪除的檔案
FILES_TO_DELETE = [
    'clean_main_window.py',
    'clean_main_window.py.backup',
    'clean_main_window_fixed.py',
    'fix_clean_main_window.py',
    'fix_structure.py',
    'test_basic.py',
    'test_fixes.py',
    'test_modules.py',
    'test_simple.db',
    'Github_personal access token.txt',
    'NUL',
    'gui/accounting.db',
    'gui/report_window.py.backup',
    '__pycache__/accounting.db',
]

# 要刪除的目錄
DIRS_TO_DELETE = [
    '__pycache__',
    'gui/__pycache__',
    'database/__pycache__',
    'tests/__pycache__',
    'utils/__pycache__',
]


def main():
    """執行清理"""
    print("=" * 70)
    print("專案清理工具")
    print("=" * 70)
    print()
    
    # 確認
    print("⚠️  警告：此操作將刪除以下檔案和目錄：")
    print()
    print("檔案:")
    for file in FILES_TO_DELETE:
        if os.path.exists(file):
            print(f"  - {file}")
    
    print("\n目錄:")
    for dir in DIRS_TO_DELETE:
        if os.path.exists(dir):
            print(f"  - {dir}/")
    
    print()
    response = input("確定要繼續嗎？(yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("已取消清理")
        return
    
    print()
    print("=" * 70)
    print("開始清理...")
    print("=" * 70)
    print()
    
    deleted_files = 0
    deleted_dirs = 0
    failed = []
    
    # 刪除檔案
    print("刪除檔案:")
    for file in FILES_TO_DELETE:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"  ✅ 已刪除: {file}")
                deleted_files += 1
            except Exception as e:
                print(f"  ❌ 刪除失敗: {file} - {e}")
                failed.append(file)
        else:
            print(f"  ⏭️  不存在: {file}")
    
    print()
    print("刪除目錄:")
    for dir in DIRS_TO_DELETE:
        if os.path.exists(dir):
            try:
                shutil.rmtree(dir)
                print(f"  ✅ 已刪除: {dir}/")
                deleted_dirs += 1
            except Exception as e:
                print(f"  ❌ 刪除失敗: {dir}/ - {e}")
                failed.append(dir)
        else:
            print(f"  ⏭️  不存在: {dir}/")
    
    # 摘要
    print()
    print("=" * 70)
    print("清理完成！")
    print("=" * 70)
    print(f"已刪除檔案: {deleted_files} 個")
    print(f"已刪除目錄: {deleted_dirs} 個")
    
    if failed:
        print(f"\n失敗項目: {len(failed)} 個")
        for item in failed:
            print(f"  - {item}")
    
    print()
    print("建議:")
    print("  1. 執行 'python main.py' 確認程式正常運行")
    print("  2. 執行 'python run_tests.py' 確認測試通過")
    print("  3. 提交變更到 Git")


if __name__ == '__main__':
    main()

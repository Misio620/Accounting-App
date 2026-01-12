#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
開發環境檢查腳本
檢查專案檔案完整性和開發環境準備狀況
"""

import os
import sys
import importlib

# 設定 Windows 控制台編碼
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass

def check_project_files():
    """檢查專案檔案完整性"""
    print("📁 檢查專案檔案...")
    
    required_files = {
        'main.py': '主程式入口',
        'database/__init__.py': '資料庫套件',
        'database/models.py': '資料庫模型',
        'test_basic.py': '基本測試',
        'requirements.txt': '套件需求',
        'README.md': '專案說明'
    }
    
    missing_files = []
    
    for filename, description in required_files.items():
        if os.path.exists(filename):
            print(f"✅ {filename} - {description}")
        else:
            print(f"❌ {filename} - {description} (缺失)")
            missing_files.append(filename)
    
    # 檢查主視窗檔案
    if os.path.exists('clean_main_window.py'):
        print("✅ clean_main_window.py - 主視窗界面")
    else:
        print("⚠️  clean_main_window.py - 主視窗界面 (需要創建)")
        missing_files.append('clean_main_window.py')
    
    return missing_files

def check_python_modules():
    """檢查 Python 模組可用性"""
    print("\n🐍 檢查 Python 環境...")
    
    # 基本模組
    basic_modules = {
        'tkinter': 'GUI 框架 (必需)',
        'sqlite3': '資料庫 (必需)',
        'datetime': '日期處理 (必需)',
        'csv': 'CSV 匯出 (必需)'
    }
    
    # 可選模組
    optional_modules = {
        'matplotlib': '圖表功能 (可選)',
        'openpyxl': 'Excel 匯出 (可選)'
    }
    
    missing_basic = []
    missing_optional = []
    
    print("  基本模組:")
    for module, description in basic_modules.items():
        try:
            importlib.import_module(module)
            print(f"  ✅ {module} - {description}")
        except ImportError:
            print(f"  ❌ {module} - {description}")
            missing_basic.append(module)
    
    print("  可選模組:")
    for module, description in optional_modules.items():
        try:
            importlib.import_module(module)
            print(f"  ✅ {module} - {description}")
        except ImportError:
            print(f"  ⚠️  {module} - {description}")
            missing_optional.append(module)
    
    return missing_basic, missing_optional

def check_database():
    """檢查資料庫狀態"""
    print("\n💾 檢查資料庫...")
    
    if os.path.exists('accounting.db'):
        size = os.path.getsize('accounting.db')
        print(f"✅ accounting.db 存在 ({size:,} bytes)")
        
        # 嘗試連接資料庫
        try:
            import sqlite3
            conn = sqlite3.connect('accounting.db')
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            print(f"   資料表: {', '.join(tables)}")
            
            if 'categories' in tables and 'transactions' in tables:
                print("   ✅ 基本資料表結構完整")
                return True
            else:
                print("   ⚠️  資料表結構不完整")
                return False
                
        except Exception as e:
            print(f"   ❌ 資料庫連接失敗: {e}")
            return False
    else:
        print("ℹ️   accounting.db 不存在 (初次執行時會自動建立)")
        return None

def test_basic_functionality():
    """測試基本功能"""
    print("\n🧪 測試基本功能...")
    
    try:
        # 嘗試導入資料庫模組
        from database.models import DatabaseManager, CategoryManager, TransactionManager
        print("✅ 資料庫模組導入成功")
        
        # 測試資料庫初始化
        db_manager = DatabaseManager("test_setup.db")
        category_manager = CategoryManager(db_manager)
        transaction_manager = TransactionManager(db_manager)
        
        # 測試分類查詢
        categories = category_manager.get_all_categories()
        print(f"✅ 分類查詢成功 ({len(categories)} 個分類)")
        
        # 清理測試檔案
        if os.path.exists("test_setup.db"):
            os.remove("test_setup.db")
        
        return True
        
    except ImportError as e:
        print(f"❌ 模組導入失敗: {e}")
        return False
    except Exception as e:
        print(f"❌ 功能測試失敗: {e}")
        return False

def create_missing_files():
    """創建缺失的檔案"""
    print("\n🔧 檢查必要檔案...")
    
    # 檢查 .gitignore
    if not os.path.exists('.gitignore'):
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Database files (optional)
test_*.db

# IDE
.vscode/
.idea/
*.swp

# System
.DS_Store
Thumbs.db

# Logs
*.log

# Backup
backup/
"""
        with open('.gitignore', 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        print("✅ 創建 .gitignore")
    
    # 檢查 backup 資料夾
    if not os.path.exists('backup'):
        os.makedirs('backup')
        print("✅ 創建 backup 資料夾")

def generate_next_steps(missing_files, missing_basic, missing_optional, db_status):
    """生成下一步建議"""
    print("\n" + "="*50)
    print("📋 開發狀態摘要與下一步建議")
    print("="*50)
    
    if missing_basic:
        print("🚨 關鍵問題需要解決:")
        for module in missing_basic:
            if module == 'tkinter':
                print(f"   - {module}: 需要完整的 Python 安裝")
            else:
                print(f"   - {module}: 標準庫缺失，請檢查 Python 安裝")
    
    if missing_files:
        print("📁 缺失檔案:")
        for file in missing_files:
            if file == 'clean_main_window.py':
                print(f"   - {file}: 需要從原始文件複製主視窗代碼")
            else:
                print(f"   - {file}: 需要創建此檔案")
    
    if missing_optional:
        print("💡 建議安裝 (增強功能):")
        for module in missing_optional:
            print(f"   - pip install {module}")
    
    # 根據狀態給出具體建議
    if not missing_files and not missing_basic:
        if db_status is None:
            print("\n🎯 下一步: 初始化應用程式")
            print("   執行: python test_basic.py")
        elif db_status:
            print("\n🚀 準備就緒! 可以開始開發")
            print("   執行: python main.py")
        else:
            print("\n🔧 需要修復資料庫")
            print("   執行: python test_basic.py")
    else:
        print("\n⚠️  請先解決上述問題，然後重新執行此檢查")
    
    print("\n📚 完整開發指南請參考: development_guide.md")

def main():
    """主檢查函數"""
    print("🔍 個人記帳應用程式 - 開發環境檢查")
    print("="*50)
    
    # 1. 檢查檔案
    missing_files = check_project_files()
    
    # 2. 檢查 Python 環境
    missing_basic, missing_optional = check_python_modules()
    
    # 3. 檢查資料庫
    db_status = check_database()
    
    # 4. 測試基本功能
    if not missing_basic and 'database/models.py' not in missing_files:
        functionality_ok = test_basic_functionality()
    else:
        functionality_ok = False
    
    # 5. 創建必要檔案
    create_missing_files()
    
    # 6. 生成建議
    generate_next_steps(missing_files, missing_basic, missing_optional, db_status)
    
    return len(missing_files) == 0 and len(missing_basic) == 0

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎉 開發環境檢查完成 - 準備就緒!")
    else:
        print("\n⚠️  開發環境需要調整，請按照建議進行修正")
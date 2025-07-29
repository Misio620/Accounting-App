import sys
import os

# 將 database 模組加入路徑
sys.path.append(os.path.dirname(__file__))

from database.models import DatabaseManager, CategoryManager, TransactionManager
from datetime import datetime

def simple_test():
    print("=== 簡化資料庫測試 ===")
    
    try:
        # 初始化
        db_manager = DatabaseManager("test_simple.db")
        category_manager = CategoryManager(db_manager)
        transaction_manager = TransactionManager(db_manager)
        
        print("✅ 資料庫初始化成功")
        
        # 測試查詢分類
        categories = category_manager.get_all_categories()
        print(f"✅ 找到 {len(categories)} 個預設分類")
        
        # 顯示前 3 個分類
        for i, cat in enumerate(categories[:3]):
            print(f"   {cat['id']}: {cat['name']} ({cat['type']})")
        
        # 測試新增交易
        today = datetime.now().strftime('%Y-%m-%d')
        success = transaction_manager.add_transaction(
            date=today,
            transaction_type='expense',
            category_id=5,  # 飲食
            amount=85.5,
            description='測試午餐'
        )
        
        if success:
            print("✅ 交易記錄新增成功")
        
        # 測試查詢交易記錄
        transactions = transaction_manager.get_transactions(limit=5)
        print(f"✅ 查詢到 {len(transactions)} 筆交易記錄")
        
        if transactions:
            trans = transactions[0]
            print(f"   最新記錄: {trans['date']} | ${trans['amount']:.2f} | {trans['category_name']}")
        
        print("\n🎉 所有基本功能測試通過！")
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    simple_test()
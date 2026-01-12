"""
資料庫模組測試
測試 DatabaseManager, CategoryManager, TransactionManager
"""

import unittest
import os
import sys
from datetime import datetime

# 將專案根目錄加入路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database.models import DatabaseManager, CategoryManager, TransactionManager


class TestDatabaseManager(unittest.TestCase):
    """測試 DatabaseManager 類別"""
    
    def setUp(self):
        """每個測試前執行"""
        self.test_db = "test_database.db"
        # 如果測試資料庫存在，先刪除
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        
        self.db_manager = DatabaseManager(self.test_db)
    
    def tearDown(self):
        """每個測試後執行"""
        # 清理測試資料庫
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_database_initialization(self):
        """測試資料庫初始化"""
        # 檢查資料庫檔案是否建立
        self.assertTrue(os.path.exists(self.test_db))
    
    def test_get_connection(self):
        """測試取得資料庫連接"""
        conn = self.db_manager.get_connection()
        self.assertIsNotNone(conn)
        
        # 檢查資料表是否存在
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        self.assertIn('categories', tables)
        self.assertIn('transactions', tables)
        
        conn.close()
    
    def test_default_categories_created(self):
        """測試預設分類是否建立"""
        category_manager = CategoryManager(self.db_manager)
        categories = category_manager.get_all_categories()
        
        # 應該有 10 個預設分類
        self.assertEqual(len(categories), 10)
        
        # 檢查收入分類
        income_categories = [cat for cat in categories if cat['type'] == 'income']
        self.assertEqual(len(income_categories), 4)
        
        # 檢查支出分類
        expense_categories = [cat for cat in categories if cat['type'] == 'expense']
        self.assertEqual(len(expense_categories), 6)


class TestCategoryManager(unittest.TestCase):
    """測試 CategoryManager 類別"""
    
    def setUp(self):
        """每個測試前執行"""
        self.test_db = "test_category.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        
        self.db_manager = DatabaseManager(self.test_db)
        self.category_manager = CategoryManager(self.db_manager)
    
    def tearDown(self):
        """每個測試後執行"""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_get_all_categories(self):
        """測試取得所有分類"""
        categories = self.category_manager.get_all_categories()
        
        self.assertIsInstance(categories, list)
        self.assertEqual(len(categories), 10)
        
        # 檢查第一個分類的結構
        if categories:
            cat = categories[0]
            self.assertIn('id', cat)
            self.assertIn('name', cat)
            self.assertIn('type', cat)
    
    def test_get_categories_by_type_income(self):
        """測試取得收入分類"""
        income_categories = self.category_manager.get_categories_by_type('income')
        
        self.assertEqual(len(income_categories), 4)
        
        # 所有分類都應該是收入類型
        for cat in income_categories:
            self.assertEqual(cat['type'], 'income')
    
    def test_get_categories_by_type_expense(self):
        """測試取得支出分類"""
        expense_categories = self.category_manager.get_categories_by_type('expense')
        
        self.assertEqual(len(expense_categories), 6)
        
        # 所有分類都應該是支出類型
        for cat in expense_categories:
            self.assertEqual(cat['type'], 'expense')
    
    def test_add_category_success(self):
        """測試新增分類成功"""
        result = self.category_manager.add_category('投資收入', 'income')
        
        self.assertTrue(result)
        
        # 驗證分類已新增
        categories = self.category_manager.get_categories_by_type('income')
        category_names = [cat['name'] for cat in categories]
        self.assertIn('投資收入', category_names)
    
    def test_add_category_duplicate(self):
        """測試新增重複分類"""
        # 第一次新增應該成功
        result1 = self.category_manager.add_category('測試分類', 'expense')
        self.assertTrue(result1)
        
        # 第二次新增相同名稱應該失敗
        result2 = self.category_manager.add_category('測試分類', 'expense')
        self.assertFalse(result2)
    
    def test_add_category_invalid_type(self):
        """測試新增無效類型的分類"""
        with self.assertRaises(ValueError):
            self.category_manager.add_category('測試', 'invalid_type')


class TestTransactionManager(unittest.TestCase):
    """測試 TransactionManager 類別"""
    
    def setUp(self):
        """每個測試前執行"""
        self.test_db = "test_transaction.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        
        self.db_manager = DatabaseManager(self.test_db)
        self.category_manager = CategoryManager(self.db_manager)
        self.transaction_manager = TransactionManager(self.db_manager)
        
        # 取得預設分類 ID
        income_cats = self.category_manager.get_categories_by_type('income')
        expense_cats = self.category_manager.get_categories_by_type('expense')
        
        self.income_category_id = income_cats[0]['id'] if income_cats else None
        self.expense_category_id = expense_cats[0]['id'] if expense_cats else None
    
    def tearDown(self):
        """每個測試後執行"""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def test_add_transaction_success(self):
        """測試新增交易成功"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        result = self.transaction_manager.add_transaction(
            date=today,
            transaction_type='expense',
            category_id=self.expense_category_id,
            amount=100.50,
            description='測試交易'
        )
        
        self.assertTrue(result)
        
        # 驗證交易已新增
        transactions = self.transaction_manager.get_transactions()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['amount'], 100.50)
        self.assertEqual(transactions[0]['description'], '測試交易')
    
    def test_add_transaction_invalid_amount(self):
        """測試新增無效金額的交易"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        with self.assertRaises(ValueError):
            self.transaction_manager.add_transaction(
                date=today,
                transaction_type='expense',
                category_id=self.expense_category_id,
                amount=-50,  # 負數金額
                description='無效交易'
            )
    
    def test_add_transaction_invalid_type(self):
        """測試新增無效類型的交易"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        with self.assertRaises(ValueError):
            self.transaction_manager.add_transaction(
                date=today,
                transaction_type='invalid',  # 無效類型
                category_id=self.expense_category_id,
                amount=100,
                description='無效交易'
            )
    
    def test_get_transactions(self):
        """測試取得交易列表"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 新增多筆交易
        self.transaction_manager.add_transaction(today, 'income', self.income_category_id, 5000, '薪資')
        self.transaction_manager.add_transaction(today, 'expense', self.expense_category_id, 100, '午餐')
        self.transaction_manager.add_transaction(today, 'expense', self.expense_category_id, 50, '交通')
        
        transactions = self.transaction_manager.get_transactions()
        
        self.assertEqual(len(transactions), 3)
        
        # 檢查交易結構
        trans = transactions[0]
        self.assertIn('id', trans)
        self.assertIn('date', trans)
        self.assertIn('type', trans)
        self.assertIn('amount', trans)
        self.assertIn('description', trans)
        self.assertIn('category_name', trans)
    
    def test_update_transaction(self):
        """測試更新交易"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 新增交易
        self.transaction_manager.add_transaction(today, 'expense', self.expense_category_id, 100, '原始描述')
        
        # 取得交易 ID
        transactions = self.transaction_manager.get_transactions()
        transaction_id = transactions[0]['id']
        
        # 更新交易
        result = self.transaction_manager.update_transaction(
            transaction_id=transaction_id,
            date=today,
            transaction_type='expense',
            category_id=self.expense_category_id,
            amount=200,
            description='更新後描述'
        )
        
        self.assertTrue(result)
        
        # 驗證更新
        transactions = self.transaction_manager.get_transactions()
        self.assertEqual(transactions[0]['amount'], 200)
        self.assertEqual(transactions[0]['description'], '更新後描述')
    
    def test_delete_transaction(self):
        """測試刪除交易"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 新增交易
        self.transaction_manager.add_transaction(today, 'expense', self.expense_category_id, 100, '測試')
        
        # 取得交易 ID
        transactions = self.transaction_manager.get_transactions()
        transaction_id = transactions[0]['id']
        
        # 刪除交易
        result = self.transaction_manager.delete_transaction(transaction_id)
        self.assertTrue(result)
        
        # 驗證刪除
        transactions = self.transaction_manager.get_transactions()
        self.assertEqual(len(transactions), 0)
    
    def test_get_monthly_summary(self):
        """測試月度統計"""
        today = datetime.now()
        date_str = today.strftime('%Y-%m-%d')
        
        # 新增交易
        self.transaction_manager.add_transaction(date_str, 'income', self.income_category_id, 5000, '薪資')
        self.transaction_manager.add_transaction(date_str, 'expense', self.expense_category_id, 1000, '房租')
        self.transaction_manager.add_transaction(date_str, 'expense', self.expense_category_id, 500, '飲食')
        
        # 取得月度統計
        summary = self.transaction_manager.get_monthly_summary(today.year, today.month)
        
        self.assertEqual(summary['total_income'], 5000)
        self.assertEqual(summary['total_expense'], 1500)
        self.assertEqual(summary['balance'], 3500)


def run_tests():
    """執行所有測試"""
    # 建立測試套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 加入測試
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseManager))
    suite.addTests(loader.loadTestsFromTestCase(TestCategoryManager))
    suite.addTests(loader.loadTestsFromTestCase(TestTransactionManager))
    
    # 執行測試
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    result = run_tests()
    
    # 顯示測試結果摘要
    print("\n" + "="*70)
    print("測試結果摘要")
    print("="*70)
    print(f"執行測試數: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失敗: {len(result.failures)}")
    print(f"錯誤: {len(result.errors)}")
    print("="*70)
    
    # 如果有失敗或錯誤，返回非零退出碼
    sys.exit(not result.wasSuccessful())

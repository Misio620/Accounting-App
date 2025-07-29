"""
記帳應用程式 - 資料庫模型
提供 SQLite 資料庫的連接管理和基本 CRUD 操作
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    """資料庫管理類別"""
    
    def __init__(self, db_path: str = "accounting.db"):
        """
        初始化資料庫管理器
        
        Args:
            db_path: 資料庫檔案路徑
        """
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """取得資料庫連接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 讓查詢結果可以用欄位名稱存取
        return conn
    
    def init_database(self):
        """初始化資料庫表格和預設資料"""
        conn = self.get_connection()
        try:
            # 建立分類表
            conn.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 建立交易記錄表
            conn.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE NOT NULL,
                    type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
                    category_id INTEGER NOT NULL,
                    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
                    description TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                )
            ''')
            
            # 建立索引提升查詢效能
            conn.execute('CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(type)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_transactions_category ON transactions(category_id)')
            
            # 插入預設分類（如果不存在）
            self._insert_default_categories(conn)
            
            conn.commit()
            print("資料庫初始化完成")
            
        except sqlite3.Error as e:
            print(f"資料庫初始化錯誤：{e}")
            conn.rollback()
        finally:
            conn.close()
    
    def _insert_default_categories(self, conn: sqlite3.Connection):
        """插入預設分類"""
        default_categories = [
            # 收入分類
            ('薪資', 'income'),
            ('獎金', 'income'),
            ('副業收入', 'income'),
            ('其他收入', 'income'),
            # 支出分類
            ('飲食', 'expense'),
            ('交通', 'expense'),
            ('購物', 'expense'),
            ('娛樂', 'expense'),
            ('醫療', 'expense'),
            ('其他支出', 'expense')
        ]
        
        for name, category_type in default_categories:
            try:
                conn.execute(
                    'INSERT OR IGNORE INTO categories (name, type) VALUES (?, ?)',
                    (name, category_type)
                )
            except sqlite3.Error as e:
                print(f"插入預設分類 '{name}' 失敗：{e}")

class CategoryManager:
    """分類管理類別"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def get_all_categories(self) -> List[Dict]:
        """取得所有分類"""
        conn = self.db_manager.get_connection()
        try:
            cursor = conn.execute(
                'SELECT id, name, type FROM categories ORDER BY type, name'
            )
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"查詢分類錯誤：{e}")
            return []
        finally:
            conn.close()
    
    def get_categories_by_type(self, category_type: str) -> List[Dict]:
        """取得指定類型的分類"""
        if category_type not in ['income', 'expense']:
            raise ValueError("分類類型必須是 'income' 或 'expense'")
        
        conn = self.db_manager.get_connection()
        try:
            cursor = conn.execute(
                'SELECT id, name, type FROM categories WHERE type = ? ORDER BY name',
                (category_type,)
            )
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"查詢 {category_type} 分類錯誤：{e}")
            return []
        finally:
            conn.close()
    
    def add_category(self, name: str, category_type: str) -> bool:
        """新增分類"""
        if category_type not in ['income', 'expense']:
            raise ValueError("分類類型必須是 'income' 或 'expense'")
        
        conn = self.db_manager.get_connection()
        try:
            conn.execute(
                'INSERT INTO categories (name, type) VALUES (?, ?)',
                (name, category_type)
            )
            conn.commit()
            print(f"成功新增分類：{name}")
            return True
        except sqlite3.IntegrityError:
            print(f"分類 '{name}' 已存在")
            return False
        except sqlite3.Error as e:
            print(f"新增分類錯誤：{e}")
            return False
        finally:
            conn.close()

class TransactionManager:
    """交易記錄管理類別"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def add_transaction(self, date: str, transaction_type: str, 
                       category_id: int, amount: float, description: str = '') -> bool:
        """
        新增交易記錄
        
        Args:
            date: 交易日期 (YYYY-MM-DD)
            transaction_type: 交易類型 ('income' 或 'expense')
            category_id: 分類ID
            amount: 金額
            description: 備註
        """
        if transaction_type not in ['income', 'expense']:
            raise ValueError("交易類型必須是 'income' 或 'expense'")
        
        if amount <= 0:
            raise ValueError("金額必須大於 0")
        
        conn = self.db_manager.get_connection()
        try:
            # 驗證分類是否存在且類型匹配
            cursor = conn.execute(
                'SELECT type FROM categories WHERE id = ?',
                (category_id,)
            )
            category = cursor.fetchone()
            
            if not category:
                raise ValueError(f"分類 ID {category_id} 不存在")
            
            if category['type'] != transaction_type:
                raise ValueError(f"分類類型不匹配：分類是 {category['type']}，但交易類型是 {transaction_type}")
            
            # 插入交易記錄
            conn.execute('''
                INSERT INTO transactions (date, type, category_id, amount, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (date, transaction_type, category_id, round(amount, 2), description))
            
            conn.commit()
            print(f"成功新增交易記錄：{transaction_type} ${amount:.2f}")
            return True
            
        except sqlite3.Error as e:
            print(f"新增交易記錄錯誤：{e}")
            return False
        finally:
            conn.close()
    
    def get_transactions(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """取得交易記錄列表"""
        conn = self.db_manager.get_connection()
        try:
            cursor = conn.execute('''
                SELECT 
                    t.id,
                    t.date,
                    t.type,
                    t.amount,
                    t.description,
                    c.name as category_name
                FROM transactions t
                LEFT JOIN categories c ON t.category_id = c.id
                ORDER BY t.date DESC, t.created_at DESC
                LIMIT ? OFFSET ?
            ''', (limit, offset))
            
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"查詢交易記錄錯誤：{e}")
            return []
        finally:
            conn.close()
    
    def get_transactions_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """取得指定日期範圍的交易記錄"""
        conn = self.db_manager.get_connection()
        try:
            cursor = conn.execute('''
                SELECT 
                    t.id,
                    t.date,
                    t.type,
                    t.amount,
                    t.description,
                    c.name as category_name
                FROM transactions t
                LEFT JOIN categories c ON t.category_id = c.id
                WHERE t.date >= ? AND t.date <= ?
                ORDER BY t.date DESC, t.created_at DESC
            ''', (start_date, end_date))
            
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"查詢日期範圍交易記錄錯誤：{e}")
            return []
        finally:
            conn.close()
    
    def update_transaction(self, transaction_id: int, date: str, 
                          transaction_type: str, category_id: int, 
                          amount: float, description: str = '') -> bool:
        """更新交易記錄"""
        if transaction_type not in ['income', 'expense']:
            raise ValueError("交易類型必須是 'income' 或 'expense'")
        
        if amount <= 0:
            raise ValueError("金額必須大於 0")
        
        conn = self.db_manager.get_connection()
        try:
            # 驗證分類類型匹配
            cursor = conn.execute(
                'SELECT type FROM categories WHERE id = ?',
                (category_id,)
            )
            category = cursor.fetchone()
            
            if not category:
                raise ValueError(f"分類 ID {category_id} 不存在")
            
            if category['type'] != transaction_type:
                raise ValueError(f"分類類型不匹配")
            
            # 更新交易記錄
            cursor = conn.execute('''
                UPDATE transactions 
                SET date = ?, type = ?, category_id = ?, amount = ?, description = ?
                WHERE id = ?
            ''', (date, transaction_type, category_id, round(amount, 2), description, transaction_id))
            
            if cursor.rowcount == 0:
                print(f"交易記錄 ID {transaction_id} 不存在")
                return False
            
            conn.commit()
            print(f"成功更新交易記錄 ID {transaction_id}")
            return True
            
        except sqlite3.Error as e:
            print(f"更新交易記錄錯誤：{e}")
            return False
        finally:
            conn.close()
    
    def delete_transaction(self, transaction_id: int) -> bool:
        """刪除交易記錄"""
        conn = self.db_manager.get_connection()
        try:
            cursor = conn.execute(
                'DELETE FROM transactions WHERE id = ?',
                (transaction_id,)
            )
            
            if cursor.rowcount == 0:
                print(f"交易記錄 ID {transaction_id} 不存在")
                return False
            
            conn.commit()
            print(f"成功刪除交易記錄 ID {transaction_id}")
            return True
            
        except sqlite3.Error as e:
            print(f"刪除交易記錄錯誤：{e}")
            return False
        finally:
            conn.close()
    
    def get_monthly_summary(self, year: int, month: int) -> Dict:
        """取得月度統計摘要"""
        # 計算該月的起始和結束日期
        start_date = f"{year:04d}-{month:02d}-01"
        if month == 12:
            end_date = f"{year+1:04d}-01-01"
        else:
            end_date = f"{year:04d}-{month+1:02d}-01"
        
        conn = self.db_manager.get_connection()
        try:
            # 查詢收入總額
            cursor = conn.execute('''
                SELECT COALESCE(SUM(amount), 0) as total_income
                FROM transactions
                WHERE type = 'income' AND date >= ? AND date < ?
            ''', (start_date, end_date))
            total_income = cursor.fetchone()['total_income']
            
            # 查詢支出總額
            cursor = conn.execute('''
                SELECT COALESCE(SUM(amount), 0) as total_expense
                FROM transactions
                WHERE type = 'expense' AND date >= ? AND date < ?
            ''', (start_date, end_date))
            total_expense = cursor.fetchone()['total_expense']
            
            # 計算結餘
            balance = total_income - total_expense
            
            return {
                'year': year,
                'month': month,
                'total_income': float(total_income),
                'total_expense': float(total_expense),
                'balance': float(balance)
            }
            
        except sqlite3.Error as e:
            print(f"查詢月度統計錯誤：{e}")
            return {
                'year': year,
                'month': month,
                'total_income': 0.0,
                'total_expense': 0.0,
                'balance': 0.0
            }
        finally:
            conn.close()

# 測試用的示例函數
def test_database():
    """測試資料庫功能"""
    print("=== 測試資料庫功能 ===")
    
    # 初始化資料庫
    db_manager = DatabaseManager("test_accounting.db")
    category_manager = CategoryManager(db_manager)
    transaction_manager = TransactionManager(db_manager)
    
    # 測試查詢分類
    print("\n1. 查詢所有分類：")
    categories = category_manager.get_all_categories()
    for cat in categories:
        print(f"  {cat['id']}: {cat['name']} ({cat['type']})")
    
    # 測試新增交易記錄
    print("\n2. 新增測試交易記錄：")
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 新增一筆收入
    success = transaction_manager.add_transaction(
        date=today,
        transaction_type='income',
        category_id=1,  # 薪資
        amount=50000,
        description='月薪'
    )
    
    # 新增一筆支出
    success = transaction_manager.add_transaction(
        date=today,
        transaction_type='expense',
        category_id=5,  # 飲食
        amount=120,
        description='午餐'
    )
    
    # 測試查詢交易記錄
    print("\n3. 查詢交易記錄：")
    transactions = transaction_manager.get_transactions(limit=10)
    for trans in transactions:
        print(f"  {trans['date']} | {trans['type']} | ${trans['amount']:.2f} | {trans['category_name']} | {trans['description']}")
    
    # 測試月度統計
    print("\n4. 查詢本月統計：")
    now = datetime.now()
    summary = transaction_manager.get_monthly_summary(now.year, now.month)
    print(f"  收入：${summary['total_income']:.2f}")
    print(f"  支出：${summary['total_expense']:.2f}")
    print(f"  結餘：${summary['balance']:.2f}")
    
    print("\n測試完成！")

if __name__ == "__main__":
    test_database()
    
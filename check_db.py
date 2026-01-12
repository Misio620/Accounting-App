"""
檢查資料庫中的交易記錄
"""
from database.models import DatabaseManager, TransactionManager

db = DatabaseManager('accounting.db')
tm = TransactionManager(db)
trans = tm.get_transactions()

print(f'交易數量: {len(trans)}')
print()

if trans:
    print('最近的交易：')
    for t in trans[:5]:
        print(f'{t["date"]} {t["type"]} {t["category_name"]} ${t["amount"]:.2f}')
else:
    print('沒有交易記錄')

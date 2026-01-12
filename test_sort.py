"""
測試分類排序
"""
from database.models import DatabaseManager, CategoryManager
import re

db = DatabaseManager('accounting.db')
cm = CategoryManager(db)

print("=== 支出分類（原始順序）===")
cats = cm.get_categories_by_type('expense')
for c in cats:
    print(f"ID: {c['id']}, 名稱: {c['name']}")

print("\n=== 測試排序邏輯 ===")

# 測試當前的排序邏輯
def sort_key_name(cat):
    name = cat['name']
    match = re.match(r'^(\d+)', name)
    if match:
        return (0, int(match.group(1)), name)
    else:
        return (1, 0, name)

sorted_by_name = sorted(cats, key=sort_key_name)
print("\n按名稱排序（當前邏輯）:")
for c in sorted_by_name:
    print(f"ID: {c['id']}, 名稱: {c['name']}")

# 測試按 ID 排序
sorted_by_id = sorted(cats, key=lambda c: c['id'])
print("\n按 ID 排序:")
for c in sorted_by_id:
    print(f"ID: {c['id']}, 名稱: {c['name']}")

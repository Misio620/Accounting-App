#!/usr/bin/env python3
"""
Test script to verify the fixes
"""

import sys
import os

print("=" * 50)
print("Testing fixes for accounting_app")
print("=" * 50)

# Test 1: Import database modules
print("\n[Test 1] Import database modules...")
try:
    from database.models import DatabaseManager, CategoryManager, TransactionManager
    print("PASS: Database modules imported successfully")
except ImportError as e:
    print(f"FAIL: {e}")
    sys.exit(1)

# Test 2: Import main window
print("\n[Test 2] Import main window...")
try:
    sys.path.insert(0, os.path.dirname(__file__))
    from clean_main_window import MainWindow, TransactionDialog
    print("PASS: MainWindow imported successfully")
except ImportError as e:
    print(f"FAIL: {e}")
    sys.exit(1)

# Test 3: Check DatabaseManager initialization
print("\n[Test 3] Initialize database...")
try:
    db_manager = DatabaseManager("test_fixes.db")
    print("PASS: Database initialized successfully")
except Exception as e:
    print(f"FAIL: {e}")
    sys.exit(1)

# Test 4: Check managers
print("\n[Test 4] Initialize managers...")
try:
    category_manager = CategoryManager(db_manager)
    transaction_manager = TransactionManager(db_manager)
    print("PASS: Managers initialized successfully")
except Exception as e:
    print(f"FAIL: {e}")
    sys.exit(1)

# Test 5: Check categories
print("\n[Test 5] Query categories...")
try:
    categories = category_manager.get_all_categories()
    print(f"PASS: Found {len(categories)} categories")
except Exception as e:
    print(f"FAIL: {e}")
    sys.exit(1)

# Test 6: Check MainWindow has the fixed method
print("\n[Test 6] Check show_year_category_chart method exists...")
try:
    assert hasattr(MainWindow, 'show_year_category_chart')
    print("PASS: show_year_category_chart method exists")
except AssertionError:
    print("FAIL: show_year_category_chart method not found")
    sys.exit(1)

print("\n" + "=" * 50)
print("All tests passed!")
print("=" * 50)

# Cleanup
if os.path.exists("test_fixes.db"):
    os.remove("test_fixes.db")
    print("\nCleanup: test database removed")

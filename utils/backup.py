"""
備份和還原工具模組
"""

import os
import shutil
from datetime import datetime
from typing import List, Optional, Tuple


class BackupManager:
    """資料庫備份管理器"""
    
    def __init__(self, db_path: str = "accounting.db", backup_dir: str = "backup"):
        """
        初始化備份管理器
        
        Args:
            db_path: 資料庫檔案路徑
            backup_dir: 備份目錄路徑
        """
        self.db_path = db_path
        self.backup_dir = backup_dir
        
        # 確保備份目錄存在
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
    
    def backup_database(self, custom_name: Optional[str] = None) -> Tuple[bool, str]:
        """
        備份資料庫
        
        Args:
            custom_name: 自訂備份檔名（可選）
        
        Returns:
            (成功與否, 備份檔案路徑或錯誤訊息)
        """
        try:
            # 檢查資料庫檔案是否存在
            if not os.path.exists(self.db_path):
                return False, f"資料庫檔案不存在: {self.db_path}"
            
            # 生成備份檔名
            if custom_name:
                backup_filename = f"{custom_name}.db"
            else:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_filename = f"accounting_backup_{timestamp}.db"
            
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            # 複製資料庫檔案
            shutil.copy2(self.db_path, backup_path)
            
            return True, backup_path
            
        except Exception as e:
            return False, f"備份失敗: {str(e)}"
    
    def list_backups(self) -> List[dict]:
        """
        列出所有備份檔案
        
        Returns:
            備份檔案列表，每個項目包含: name, path, size, created_time
        """
        backups = []
        
        try:
            if not os.path.exists(self.backup_dir):
                return backups
            
            for filename in os.listdir(self.backup_dir):
                if filename.endswith('.db'):
                    filepath = os.path.join(self.backup_dir, filename)
                    
                    # 取得檔案資訊
                    stat = os.stat(filepath)
                    
                    backups.append({
                        'name': filename,
                        'path': filepath,
                        'size': stat.st_size,
                        'created_time': datetime.fromtimestamp(stat.st_mtime)
                    })
            
            # 按建立時間排序（最新的在前）
            backups.sort(key=lambda x: x['created_time'], reverse=True)
            
        except Exception as e:
            print(f"列出備份失敗: {e}")
        
        return backups
    
    def restore_database(self, backup_path: str) -> Tuple[bool, str]:
        """
        從備份還原資料庫
        
        Args:
            backup_path: 備份檔案路徑
        
        Returns:
            (成功與否, 訊息)
        """
        try:
            # 檢查備份檔案是否存在
            if not os.path.exists(backup_path):
                return False, f"備份檔案不存在: {backup_path}"
            
            # 備份當前資料庫（以防萬一）
            if os.path.exists(self.db_path):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                temp_backup = f"{self.db_path}.before_restore_{timestamp}"
                shutil.copy2(self.db_path, temp_backup)
            
            # 還原資料庫
            shutil.copy2(backup_path, self.db_path)
            
            return True, f"資料庫已從備份還原: {backup_path}"
            
        except Exception as e:
            return False, f"還原失敗: {str(e)}"
    
    def delete_backup(self, backup_path: str) -> Tuple[bool, str]:
        """
        刪除備份檔案
        
        Args:
            backup_path: 備份檔案路徑
        
        Returns:
            (成功與否, 訊息)
        """
        try:
            if not os.path.exists(backup_path):
                return False, "備份檔案不存在"
            
            os.remove(backup_path)
            return True, "備份檔案已刪除"
            
        except Exception as e:
            return False, f"刪除失敗: {str(e)}"
    
    def auto_backup_check(self, days: int = 7) -> Tuple[bool, str]:
        """
        檢查是否需要自動備份
        
        Args:
            days: 多少天內沒有備份就需要備份
        
        Returns:
            (是否需要備份, 訊息)
        """
        backups = self.list_backups()
        
        if not backups:
            return True, "沒有任何備份，建議立即備份"
        
        latest_backup = backups[0]
        days_since_backup = (datetime.now() - latest_backup['created_time']).days
        
        if days_since_backup >= days:
            return True, f"距離上次備份已 {days_since_backup} 天，建議備份"
        
        return False, f"上次備份: {latest_backup['created_time'].strftime('%Y-%m-%d %H:%M:%S')}"
    
    def get_backup_size_total(self) -> int:
        """
        取得所有備份的總大小
        
        Returns:
            總大小（bytes）
        """
        total_size = 0
        backups = self.list_backups()
        
        for backup in backups:
            total_size += backup['size']
        
        return total_size


def format_file_size(size_bytes: int) -> str:
    """
    格式化檔案大小
    
    Args:
        size_bytes: 檔案大小（bytes）
    
    Returns:
        格式化的字串（如 "1.5 MB"）
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


# 測試程式碼
if __name__ == "__main__":
    print("=== 備份管理器測試 ===\n")
    
    backup_mgr = BackupManager()
    
    # 測試備份
    print("1. 建立備份...")
    success, message = backup_mgr.backup_database()
    print(f"   結果: {message}\n")
    
    # 列出備份
    print("2. 列出所有備份:")
    backups = backup_mgr.list_backups()
    for backup in backups:
        print(f"   - {backup['name']}")
        print(f"     大小: {format_file_size(backup['size'])}")
        print(f"     時間: {backup['created_time'].strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 檢查是否需要自動備份
    print("3. 檢查自動備份:")
    need_backup, msg = backup_mgr.auto_backup_check(days=7)
    print(f"   {msg}")
    print(f"   需要備份: {'是' if need_backup else '否'}\n")
    
    # 總大小
    total_size = backup_mgr.get_backup_size_total()
    print(f"4. 備份總大小: {format_file_size(total_size)}")

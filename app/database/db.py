import sqlite3
import os

# 預設資料庫路徑 (instance/database.db)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
DB_PATH = os.path.join(INSTANCE_DIR, 'database.db')

def get_db_connection():
    """
    建立並回傳一個 SQLite 資料庫連線。
    使用 sqlite3.Row 讓查詢結果可以像字典一樣操作。
    """
    if not os.path.exists(INSTANCE_DIR):
        os.makedirs(INSTANCE_DIR)
        
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # 確保 Foreign Key 約束有啟用
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

import sqlite3
import logging
from app.database.db import get_db_connection

class Recipe:
    @staticmethod
    def create(title, content=None, image_path=None, is_favorite=False, notes=None):
        """
        新增一筆食譜記錄。
        參數:
            title (str): 食譜標題
            content (str): 食譜內容
            image_path (str): 圖片路徑
            is_favorite (bool): 是否為我的最愛
            notes (str): 烹飪筆記
        回傳:
            int: 新增的食譜 ID，若失敗則回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO recipes (title, content, image_path, is_favorite, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, content, image_path, is_favorite, notes))
            conn.commit()
            recipe_id = cursor.lastrowid
            conn.close()
            return recipe_id
        except sqlite3.Error as e:
            logging.error(f"Error creating recipe: {e}")
            return None

    @staticmethod
    def get_all(search_query=None, is_favorite=None, tag_id=None):
        """
        取得所有食譜記錄，支援條件過濾。
        參數:
            search_query (str): 搜尋關鍵字
            is_favorite (bool): 過濾我的最愛
            tag_id (int): 過濾特定標籤
        回傳:
            list: 包含 sqlite3.Row 的列表
        """
        try:
            conn = get_db_connection()
            query = "SELECT DISTINCT r.* FROM recipes r"
            params = []
            
            if tag_id is not None:
                query += " JOIN recipe_tags rt ON r.id = rt.recipe_id"
                
            conditions = []
            if search_query:
                conditions.append("(r.title LIKE ? OR r.content LIKE ?)")
                params.extend([f"%{search_query}%", f"%{search_query}%"])
                
            if is_favorite is not None:
                conditions.append("r.is_favorite = ?")
                params.append(is_favorite)
                
            if tag_id is not None:
                conditions.append("rt.tag_id = ?")
                params.append(tag_id)
                
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
                
            query += " ORDER BY r.created_at DESC"
            
            recipes = conn.execute(query, params).fetchall()
            conn.close()
            return recipes
        except sqlite3.Error as e:
            logging.error(f"Error getting recipes: {e}")
            return []

    @staticmethod
    def get_by_id(recipe_id):
        """
        取得單筆食譜記錄。
        參數:
            recipe_id (int): 食譜 ID
        回傳:
            sqlite3.Row: 食譜資料，找不到時回傳 None
        """
        try:
            conn = get_db_connection()
            recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
            conn.close()
            return recipe
        except sqlite3.Error as e:
            logging.error(f"Error getting recipe {recipe_id}: {e}")
            return None

    @staticmethod
    def update(recipe_id, title=None, content=None, image_path=None, is_favorite=None, notes=None):
        """
        更新指定的食譜記錄。
        參數:
            recipe_id (int): 食譜 ID
            title (str): 食譜標題
            content (str): 食譜內容
            image_path (str): 圖片路徑
            is_favorite (bool): 是否為我的最愛
            notes (str): 烹飪筆記
        回傳:
            bool: 是否更新成功
        """
        try:
            conn = get_db_connection()
            fields = []
            params = []
            
            if title is not None:
                fields.append("title = ?")
                params.append(title)
            if content is not None:
                fields.append("content = ?")
                params.append(content)
            if image_path is not None:
                fields.append("image_path = ?")
                params.append(image_path)
            if is_favorite is not None:
                fields.append("is_favorite = ?")
                params.append(is_favorite)
            if notes is not None:
                fields.append("notes = ?")
                params.append(notes)
                
            fields.append("updated_at = CURRENT_TIMESTAMP")
                
            if not fields:
                conn.close()
                return False
                
            query = f"UPDATE recipes SET {', '.join(fields)} WHERE id = ?"
            params.append(recipe_id)
            
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except sqlite3.Error as e:
            logging.error(f"Error updating recipe {recipe_id}: {e}")
            return False

    @staticmethod
    def delete(recipe_id):
        """
        刪除指定的食譜記錄。
        參數:
            recipe_id (int): 食譜 ID
        回傳:
            bool: 是否刪除成功
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except sqlite3.Error as e:
            logging.error(f"Error deleting recipe {recipe_id}: {e}")
            return False

import sqlite3
import logging
from app.database.db import get_db_connection

class Tag:
    @staticmethod
    def create(name):
        """
        新增一個標籤，若已存在則回傳既有標籤 ID。
        參數:
            name (str): 標籤名稱
        回傳:
            int: 標籤 ID
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO tags (name) VALUES (?)', (name,))
                conn.commit()
                tag_id = cursor.lastrowid
            except sqlite3.IntegrityError:
                # 標籤名稱不可重複，若重複則直接取得既有的
                tag = conn.execute('SELECT id FROM tags WHERE name = ?', (name,)).fetchone()
                tag_id = tag['id']
            conn.close()
            return tag_id
        except sqlite3.Error as e:
            logging.error(f"Error creating tag {name}: {e}")
            return None

    @staticmethod
    def get_all():
        """
        取得所有標籤清單。
        回傳:
            list: 包含 sqlite3.Row 的標籤列表
        """
        try:
            conn = get_db_connection()
            tags = conn.execute('SELECT * FROM tags ORDER BY name ASC').fetchall()
            conn.close()
            return tags
        except sqlite3.Error as e:
            logging.error(f"Error getting tags: {e}")
            return []

    @staticmethod
    def add_tag_to_recipe(recipe_id, tag_id):
        """
        為食譜加入一個標籤關聯。
        參數:
            recipe_id (int): 食譜 ID
            tag_id (int): 標籤 ID
        回傳:
            bool: 是否新增成功
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO recipe_tags (recipe_id, tag_id)
                    VALUES (?, ?)
                ''', (recipe_id, tag_id))
                conn.commit()
                success = True
            except sqlite3.IntegrityError:
                # 若已存在則忽略
                success = False
            conn.close()
            return success
        except sqlite3.Error as e:
            logging.error(f"Error adding tag {tag_id} to recipe {recipe_id}: {e}")
            return False

    @staticmethod
    def remove_tag_from_recipe(recipe_id, tag_id):
        """
        從食譜移除一個標籤關聯。
        參數:
            recipe_id (int): 食譜 ID
            tag_id (int): 標籤 ID
        回傳:
            bool: 是否刪除成功
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM recipe_tags
                WHERE recipe_id = ? AND tag_id = ?
            ''', (recipe_id, tag_id))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except sqlite3.Error as e:
            logging.error(f"Error removing tag {tag_id} from recipe {recipe_id}: {e}")
            return False

    @staticmethod
    def get_tags_for_recipe(recipe_id):
        """
        取得指定食譜的所有標籤。
        參數:
            recipe_id (int): 食譜 ID
        回傳:
            list: 包含 sqlite3.Row 的標籤列表
        """
        try:
            conn = get_db_connection()
            tags = conn.execute('''
                SELECT t.* FROM tags t
                JOIN recipe_tags rt ON t.id = rt.tag_id
                WHERE rt.recipe_id = ?
                ORDER BY t.name ASC
            ''', (recipe_id,)).fetchall()
            conn.close()
            return tags
        except sqlite3.Error as e:
            logging.error(f"Error getting tags for recipe {recipe_id}: {e}")
            return []

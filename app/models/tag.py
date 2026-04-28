from app.database.db import get_db_connection
import sqlite3

class Tag:
    @staticmethod
    def create(name):
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

    @staticmethod
    def get_all():
        conn = get_db_connection()
        tags = conn.execute('SELECT * FROM tags ORDER BY name ASC').fetchall()
        conn.close()
        return tags

    @staticmethod
    def add_tag_to_recipe(recipe_id, tag_id):
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

    @staticmethod
    def remove_tag_from_recipe(recipe_id, tag_id):
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

    @staticmethod
    def get_tags_for_recipe(recipe_id):
        conn = get_db_connection()
        tags = conn.execute('''
            SELECT t.* FROM tags t
            JOIN recipe_tags rt ON t.id = rt.tag_id
            WHERE rt.recipe_id = ?
            ORDER BY t.name ASC
        ''', (recipe_id,)).fetchall()
        conn.close()
        return tags

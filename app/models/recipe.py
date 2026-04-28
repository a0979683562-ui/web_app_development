from app.database.db import get_db_connection

class Recipe:
    @staticmethod
    def create(title, content=None, image_path=None, is_favorite=False, notes=None):
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

    @staticmethod
    def get_all(search_query=None, is_favorite=None, tag_id=None):
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

    @staticmethod
    def get_by_id(recipe_id):
        conn = get_db_connection()
        recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
        conn.close()
        return recipe

    @staticmethod
    def update(recipe_id, title, content=None, image_path=None, is_favorite=None, notes=None):
        conn = get_db_connection()
        # 為了支援部分更新，動態組裝 SET 條件
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

    @staticmethod
    def delete(recipe_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success

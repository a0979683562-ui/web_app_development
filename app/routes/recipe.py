import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from werkzeug.utils import secure_filename
from app.models.recipe import Recipe
from app.models.tag import Tag

bp = Blueprint('recipe', __name__)

def save_image(file):
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        # Create uploads folder if it doesn't exist
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return f"uploads/{filename}"
    return None

@bp.route('/')
@bp.route('/recipes')
def index():
    search_query = request.args.get('q', '')
    is_favorite = request.args.get('fav', type=bool)
    tag_id = request.args.get('tag_id', type=int)
    
    recipes = Recipe.get_all(search_query=search_query, is_favorite=is_favorite, tag_id=tag_id)
    tags = Tag.get_all()
    
    return render_template('recipes/index.html', recipes=recipes, tags=tags, request=request)

@bp.route('/recipes/new')
def new_recipe():
    tags = Tag.get_all()
    return render_template('recipes/new.html', tags=tags)

@bp.route('/recipes', methods=['POST'])
def create_recipe():
    title = request.form.get('title')
    content = request.form.get('content')
    is_favorite = 'is_favorite' in request.form
    notes = request.form.get('notes')
    
    if not title:
        flash('請輸入食譜標題', 'danger')
        return redirect(url_for('recipe.new_recipe'))
        
    image_path = save_image(request.files.get('image'))
    recipe_id = Recipe.create(title, content, image_path, is_favorite, notes)
    
    if recipe_id:
        selected_tags = request.form.getlist('tags')
        # Add new tags if provided
        new_tags = request.form.get('new_tags')
        if new_tags:
            for nt in new_tags.split(','):
                nt = nt.strip()
                if nt:
                    tid = Tag.create(nt)
                    selected_tags.append(str(tid))
                    
        for tag_id in selected_tags:
            Tag.add_tag_to_recipe(recipe_id, int(tag_id))
            
        flash('新增成功！', 'success')
        return redirect(url_for('recipe.index'))
    else:
        flash('新增失敗，請稍後再試', 'danger')
        return redirect(url_for('recipe.new_recipe'))

@bp.route('/recipes/<int:id>')
def recipe_detail(id):
    recipe = Recipe.get_by_id(id)
    if not recipe:
        abort(404)
        
    tags = Tag.get_tags_for_recipe(id)
    return render_template('recipes/detail.html', recipe=recipe, tags=tags)

@bp.route('/recipes/<int:id>/edit')
def edit_recipe(id):
    recipe = Recipe.get_by_id(id)
    if not recipe:
        abort(404)
        
    all_tags = Tag.get_all()
    current_tags = [t['id'] for t in Tag.get_tags_for_recipe(id)]
    
    return render_template('recipes/edit.html', recipe=recipe, all_tags=all_tags, current_tags=current_tags)

@bp.route('/recipes/<int:id>/update', methods=['POST'])
def update_recipe(id):
    recipe = Recipe.get_by_id(id)
    if not recipe:
        abort(404)
        
    title = request.form.get('title')
    content = request.form.get('content')
    is_favorite = 'is_favorite' in request.form
    notes = request.form.get('notes')
    
    if not title:
        flash('請輸入食譜標題', 'danger')
        return redirect(url_for('recipe.edit_recipe', id=id))
        
    file = request.files.get('image')
    image_path = save_image(file) if file and file.filename != '' else recipe['image_path']
    
    success = Recipe.update(id, title, content, image_path, is_favorite, notes)
    
    if success:
        # Update tags
        current_tags = Tag.get_tags_for_recipe(id)
        for t in current_tags:
            Tag.remove_tag_from_recipe(id, t['id'])
            
        selected_tags = request.form.getlist('tags')
        new_tags = request.form.get('new_tags')
        if new_tags:
            for nt in new_tags.split(','):
                nt = nt.strip()
                if nt:
                    tid = Tag.create(nt)
                    selected_tags.append(str(tid))
                    
        for tag_id in selected_tags:
            Tag.add_tag_to_recipe(id, int(tag_id))
            
        flash('更新成功！', 'success')
    else:
        flash('更新失敗，請稍後再試', 'danger')
        
    return redirect(url_for('recipe.recipe_detail', id=id))

@bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    if Recipe.delete(id):
        flash('食譜已刪除', 'success')
    else:
        flash('刪除失敗', 'danger')
    return redirect(url_for('recipe.index'))

@bp.route('/recipes/<int:id>/notes', methods=['POST'])
def update_notes(id):
    notes = request.form.get('notes')
    if Recipe.update(id, notes=notes):
        flash('筆記已更新', 'success')
    else:
        flash('筆記更新失敗', 'danger')
    return redirect(url_for('recipe.recipe_detail', id=id))

@bp.route('/recipes/<int:id>/favorite', methods=['POST'])
def toggle_favorite(id):
    recipe = Recipe.get_by_id(id)
    if not recipe:
        abort(404)
        
    new_status = not recipe['is_favorite']
    if Recipe.update(id, is_favorite=new_status):
        status_text = '已加入最愛' if new_status else '已取消最愛'
        flash(status_text, 'success')
        
    return redirect(request.referrer or url_for('recipe.index'))

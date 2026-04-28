from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

bp = Blueprint('recipe', __name__)

@bp.route('/')
@bp.route('/recipes')
def index():
    """
    [GET] / 或 /recipes
    顯示食譜列表。
    支援透過 GET 參數 `search_query`, `is_favorite`, `tag_id` 進行過濾。
    渲染 templates/recipes/index.html
    """
    pass

@bp.route('/recipes/new')
def new_recipe():
    """
    [GET] /recipes/new
    顯示新增食譜表單頁面。
    渲染 templates/recipes/new.html
    """
    pass

@bp.route('/recipes', methods=['POST'])
def create_recipe():
    """
    [POST] /recipes
    接收新增食譜表單提交。
    處理圖片上傳，寫入 DB，然後重導向到首頁。
    """
    pass

@bp.route('/recipes/<int:id>')
def recipe_detail(id):
    """
    [GET] /recipes/<id>
    顯示單筆食譜的詳情（包含烹飪筆記）。
    渲染 templates/recipes/detail.html
    若找不到食譜則 abort(404)。
    """
    pass

@bp.route('/recipes/<int:id>/edit')
def edit_recipe(id):
    """
    [GET] /recipes/<id>/edit
    顯示編輯食譜的表單頁面。
    預載入既有食譜的資料。
    渲染 templates/recipes/edit.html
    """
    pass

@bp.route('/recipes/<int:id>/update', methods=['POST'])
def update_recipe(id):
    """
    [POST] /recipes/<id>/update
    接收編輯食譜表單提交。
    更新 DB 資料（與圖片），然後重導向回詳情頁。
    """
    pass

@bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    [POST] /recipes/<id>/delete
    接收刪除食譜的請求。
    從 DB 刪除該筆資料後，重導向回首頁。
    """
    pass

@bp.route('/recipes/<int:id>/notes', methods=['POST'])
def update_notes(id):
    """
    [POST] /recipes/<id>/notes
    專門用來更新烹飪筆記的路由。
    更新完成後重導向回詳情頁。
    """
    pass

@bp.route('/recipes/<int:id>/favorite', methods=['POST'])
def toggle_favorite(id):
    """
    [POST] /recipes/<id>/favorite
    切換食譜的「我的最愛」狀態。
    完成後重導向回原本所在的頁面 (referrer)。
    """
    pass

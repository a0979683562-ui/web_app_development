# 路由設計文件 (API Design)

本文件描述食譜收藏系統的 Flask 路由規劃，包含前端頁面與後端邏輯的對應關係，並列出需要實作的 Jinja2 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 / 食譜列表 | `GET` | `/` <br> `/recipes` | `recipes/index.html` | 顯示所有食譜，支援搜尋 (`q`)、標籤 (`tag_id`) 與最愛 (`fav`) 查詢參數過濾。 |
| 新增食譜頁面 | `GET` | `/recipes/new` | `recipes/new.html` | 顯示新增食譜的空白表單頁面。 |
| 建立食譜 | `POST` | `/recipes` | — | 接收新增表單，存入資料庫並重導向至首頁或詳情頁。 |
| 食譜詳情 | `GET` | `/recipes/<id>` | `recipes/detail.html` | 顯示單筆食譜的完整圖文與筆記。 |
| 編輯食譜頁面 | `GET` | `/recipes/<id>/edit` | `recipes/edit.html` | 顯示編輯表單，並帶入該食譜既有資料。 |
| 更新食譜 | `POST` | `/recipes/<id>/update` | — | 接收編輯表單，更新資料庫並重導向至詳情頁。 |
| 刪除食譜 | `POST` | `/recipes/<id>/delete` | — | 刪除食譜，重導向至首頁。 |
| 更新烹飪筆記 | `POST` | `/recipes/<id>/notes` | — | 接收筆記欄位更新，重導向回詳情頁。 |
| 切換我的最愛 | `POST` | `/recipes/<id>/favorite` | — | 切換最愛狀態，重導向回當前頁面 (列表或詳情)。 |

---

## 2. 每個路由的詳細說明

### `GET /` 與 `GET /recipes`
- **輸入**：URL 查詢參數 `search_query` (字串)、`is_favorite` (布林)、`tag_id` (整數)
- **處理邏輯**：呼叫 `Recipe.get_all()` 取得符合條件的食譜列表。
- **輸出**：渲染 `recipes/index.html`。
- **錯誤處理**：若無資料則於模板顯示「找不到食譜」。

### `GET /recipes/new`
- **輸入**：無
- **處理邏輯**：準備所需資料 (如：所有標籤 `Tag.get_all()`) 供表單選擇。
- **輸出**：渲染 `recipes/new.html`。

### `POST /recipes`
- **輸入**：表單欄位 `title`, `content`, `image` (檔案), `is_favorite`, `notes`, `tags` (陣列)
- **處理邏輯**：
  1. 驗證 `title` 是否為空。若空則 flash 錯誤。
  2. 處理圖片上傳並取得路徑。
  3. 呼叫 `Recipe.create()` 新增記錄。
  4. 針對選取的 `tags`，呼叫 `Tag.add_tag_to_recipe()`。
- **輸出**：成功後重導向至 `GET /recipes`；失敗則重導向回 `GET /recipes/new`。

### `GET /recipes/<id>`
- **輸入**：URL 參數 `id`
- **處理邏輯**：呼叫 `Recipe.get_by_id(id)` 與 `Tag.get_tags_for_recipe(id)`。
- **輸出**：渲染 `recipes/detail.html`。
- **錯誤處理**：若 `Recipe` 不存在，回傳 404 頁面。

### `GET /recipes/<id>/edit`
- **輸入**：URL 參數 `id`
- **處理邏輯**：呼叫 `Recipe.get_by_id(id)` 取出資料供表單使用。
- **輸出**：渲染 `recipes/edit.html`。
- **錯誤處理**：若 `Recipe` 不存在，回傳 404 頁面。

### `POST /recipes/<id>/update`
- **輸入**：表單欄位 `title`, `content`, `image` 等。
- **處理邏輯**：更新對應 ID 的資料，若有新圖片則處理上傳並取代舊路徑。更新關聯標籤。
- **輸出**：重導向至 `GET /recipes/<id>`。

### `POST /recipes/<id>/delete`
- **輸入**：URL 參數 `id`
- **處理邏輯**：呼叫 `Recipe.delete(id)` 刪除記錄。
- **輸出**：重導向至 `GET /recipes`。

### `POST /recipes/<id>/notes`
- **輸入**：URL 參數 `id`，表單欄位 `notes`
- **處理邏輯**：呼叫 `Recipe.update()` 單純更新筆記。
- **輸出**：重導向至 `GET /recipes/<id>`。

### `POST /recipes/<id>/favorite`
- **輸入**：URL 參數 `id`
- **處理邏輯**：取得當前最愛狀態並反轉，呼叫 `Recipe.update()`。
- **輸出**：重導向回發送請求的前一頁 (`request.referrer`)。

---

## 3. Jinja2 模板清單

所有的模板將放置於 `app/templates/` 目錄下：

- `base.html`：**(Base Template)** 包含全站共用的 `<head>`、導覽列 (Navbar)、Footer 與 Flash 訊息區塊。所有其他頁面都將繼承此模板。
- `recipes/index.html`：食譜列表頁（含搜尋列與過濾選項）。
- `recipes/detail.html`：食譜詳情頁（含烹飪筆記顯示與編輯區塊）。
- `recipes/new.html`：新增食譜的表單頁面。
- `recipes/edit.html`：編輯食譜的表單頁面（結構類似 `new.html`，但帶有預設值）。
- `404.html`：(全域) 找不到頁面的錯誤提示畫面。

# 流程圖文件 (Flowchart)

根據 PRD (與 Flask + SQLite 架構規劃)，以下為食譜收藏系統的使用者流程圖與系統序列圖。

## 1. 使用者流程圖（User Flow）

此流程圖描述使用者從進入網站開始，主要功能的操作路徑與頁面跳轉邏輯。

```mermaid
flowchart LR
    Start([使用者開啟網頁]) --> Home[首頁 - 食譜列表]
    
    Home --> Search[關鍵字搜尋 / 標籤過濾 / 我的最愛]
    Search --> Home
    
    Home -->|點擊新增| CreateForm[新增食譜表單頁面]
    CreateForm -->|填寫並送出| SaveCreate[儲存至資料庫]
    SaveCreate --> Home
    
    Home -->|點擊特定食譜| Detail[食譜詳情頁面]
    
    Detail -->|點擊編輯| EditForm[編輯食譜表單頁面]
    EditForm -->|修改並送出| SaveEdit[更新至資料庫]
    SaveEdit --> Detail
    
    Detail -->|編輯筆記| NoteForm[編輯烹飪筆記]
    NoteForm -->|儲存| Detail
    
    Detail -->|點擊最愛| ToggleFav[加入/取消我的最愛]
    ToggleFav --> Detail
    
    Detail -->|點擊刪除| DeleteConfirm{確認刪除？}
    DeleteConfirm -->|是| DeleteAction[從資料庫刪除]
    DeleteAction --> Home
    DeleteConfirm -->|否| Detail
```

## 2. 系統序列圖（Sequence Diagram）

此序列圖描述「使用者點擊新增食譜」到「資料存入資料庫」的完整後端資料流與互動流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask 路由
    participant DB as SQLite 資料庫
    
    User->>Browser: 填寫新增食譜表單（標題、圖文、標籤）並送出
    Browser->>Flask: POST /recipes
    Flask->>Flask: 驗證表單資料
    Flask->>DB: INSERT INTO recipes (title, content, tags...)
    DB-->>Flask: 寫入成功
    Flask-->>Browser: HTTP 302 重導向到首頁
    Browser->>User: 顯示最新食譜列表
```

## 3. 功能清單對照表

以下表格列出系統主要功能、對應的 URL 路徑與 HTTP 方法：

| 功能名稱 | 功能說明 | URL 路徑 | HTTP 方法 |
| :--- | :--- | :--- | :--- |
| **首頁 / 食譜列表** | 顯示所有食譜，支援關鍵字、標籤與最愛篩選 | `/` 或 `/recipes` | `GET` |
| **檢視食譜詳情** | 顯示特定食譜的完整圖文與烹飪筆記 | `/recipes/<id>` | `GET` |
| **新增食譜頁面** | 顯示新增食譜的空白表單 | `/recipes/new` | `GET` |
| **新增食譜處理** | 接收表單資料，寫入資料庫並處理圖片上傳 | `/recipes` | `POST` |
| **編輯食譜頁面** | 顯示編輯食譜的表單並帶入原有資料 | `/recipes/<id>/edit` | `GET` |
| **編輯食譜處理** | 接收修改後的表單資料，更新至資料庫 | `/recipes/<id>/edit` 或 POST 到特定路由 | `POST` |
| **刪除食譜** | 從資料庫刪除特定食譜與相關圖片 | `/recipes/<id>/delete` | `POST` |
| **新增/編輯筆記** | 更新特定食譜的烹飪筆記內容 | `/recipes/<id>/notes` | `POST` |
| **切換我的最愛** | 將特定食譜標記為最愛，或取消最愛標記 | `/recipes/<id>/favorite` | `POST` |

> 註：由於目前尚未找到 `docs/ARCHITECTURE.md`，上述流程與架構基於 PRD 中提及的 Flask、Jinja2 與 SQLite 預設實作模式進行設計。

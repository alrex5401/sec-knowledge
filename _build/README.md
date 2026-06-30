# sec-knowledge build 工具

把 HackMD 文章 markdown 轉成站內文章頁（純離線、產出進 repo、CSP 維持 `'self'`）。

## 依賴
```sh
python3 -m pip install --user markdown
```

## 用法
1. 下載 HackMD raw markdown 到 `articles/{name}.md`：
   ```sh
   curl -sL "https://hackmd.io/@alrex5401/<SLUG>/download" -o articles/{name}.md
   ```
2. （首次）把文章頁樣式加進 `css/brand.css`（冪等）：
   ```sh
   python3 _build/add_article_css.py
   ```
3. 轉換成文章頁：
   ```sh
   python3 _build/build_article.py {isms|cissp}
   ```
   自動：清理 HackMD frontmatter／`<script>`／開頭 About Me → 用 `curl` 把圖片下載到 `assets/{name}/`（解決 macOS python urllib 的 SSL CA 問題）→ python-markdown 轉 HTML → 套 brand 淺色模板＋出處標示 → 產 `articles/{name}.html`。

## 新增文章
在 `build_article.py` 的 `__main__` 加一個 `convert(name, title, desc, source_url, attribution)` 分支。
- 含外部素材的文章（如 CISSP 用 WUSON／Wentz Wu 課程圖）**務必填 `attribution`** 標示出處（著作權閘門）。
- 純自有原創文章 `attribution=None`。

## 注意
- 圖片一律下載到本地、不 hotlink，才能維持 `img-src 'self'` 的嚴格 CSP。
- `articles/*.md`（HackMD 原始源）保留供重建；部署時可在 `.gitignore` 排除 `*.md` 與 `_build/`（非上線必需）。

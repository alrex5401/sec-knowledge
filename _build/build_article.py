#!/usr/bin/env python3
"""把 sec-knowledge/articles/{name}.md 轉成站內文章頁 {name}.html。
- 清理 HackMD frontmatter / <script> / adsense <ins>
- 圖片用 curl 下載到 assets/{name}/、改本地相對路徑（CSP 維持 'self'）
- md -> html（python-markdown）
- 套站模板（brand 淺色 + 文章樣式 + 出處標示 + 返回連結）
"""
import re, os, sys, subprocess
from pathlib import Path
import markdown

BASE = Path("/Users/alrex5401/Documents/VS/sec-knowledge")

def convert(name, title, desc, source_url, attribution=None):
    md = (BASE / "articles" / f"{name}.md").read_text(encoding="utf-8")
    md = re.sub(r"^---\n.*?\n---\n", "", md, count=1, flags=re.S)
    md = re.sub(r"<script.*?</script>", "", md, flags=re.S)
    md = re.sub(r"<ins\b.*?</ins>", "", md, flags=re.S)
    md = re.sub(r"\(adsbygoogle[^\n]*\n", "", md)
    # 移除開頭重複的作者自介（站模板已有 article-meta、且避免露出 gmail）
    md = re.sub(r"^\s*#+\s*About Me\b.*?(?=\n#)", "", md, count=1, flags=re.S | re.I)
    # 移除內文開頭與頁面標題重複的第一個 H1（站模板已有 <h1>）
    md = re.sub(r"^\s*#\s+.+?\n", "", md, count=1)
    imgdir = BASE / "assets" / name
    imgdir.mkdir(parents=True, exist_ok=True)
    seen = {}
    cnt = [0]
    def dl(u):
        if u in seen:
            return seen[u]
        cnt[0] += 1
        ext = os.path.splitext(u.split("?")[0])[1].lower()
        if not ext or len(ext) > 5 or not ext.startswith("."):
            ext = ".png"
        fn = f"img{cnt[0]:02d}{ext}"
        dest = imgdir / fn
        if dest.exists() and dest.stat().st_size > 0:
            seen[u] = f"../assets/{name}/{fn}"   # 已下載、冪等跳過（不重複抓圖）
            return seen[u]
        subprocess.run(["curl", "-sL", "--max-time", "40", "-A", "Mozilla/5.0 (Macintosh)",
                        "-o", str(dest), u], capture_output=True)
        if dest.exists() and dest.stat().st_size > 0:
            seen[u] = f"../assets/{name}/{fn}"
        else:
            print("   圖下載失敗:", u[:70])
            seen[u] = u
        return seen[u]
    def repl(m):
        u = m.group(2)
        return m.group(1) + dl(u) + m.group(3) if u.startswith("http") else m.group(0)
    md = re.sub(r"(!\[[^\]]*\]\()([^)\s]+)(\))", repl, md)
    ok = sum(1 for v in seen.values() if v.startswith("../"))
    print(f"{name}: 圖片 {len(seen)} 張、成功下載 {ok}、失敗 {len(seen)-ok}")
    md_inst = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "attr_list", "sane_lists", "nl2br"])
    body = md_inst.convert(md)
    toc_html = getattr(md_inst, "toc", "")
    toc_block = ""
    if toc_html and "<li" in toc_html:
        toc_block = f'<details class="toc-box" open>\n  <summary>目錄</summary>\n  {toc_html}</details>\n  '
    attr_block = f'<div class="attribution">{attribution}</div>\n  ' if attribution else ""
    page = f'''<!DOCTYPE html>
<html lang="zh-Hant-TW">
<head>
<meta charset="UTF-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; connect-src 'none'; img-src 'self' data:; style-src 'self' 'unsafe-inline'">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="author" content="葉柏毅 Alex Yeh">
<title>{title}｜仆洛宅資安筆記</title>
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://blog.angelz13.com/articles/{name}.html">
<meta property="og:image" content="https://blog.angelz13.com/assets/avatar.png">
<link rel="icon" type="image/png" href="../assets/avatar.png">
<link rel="apple-touch-icon" href="../assets/avatar.png">
<link rel="stylesheet" href="../css/brand.css">
</head>
<body>
<div class="page">
  <a class="back-link" href="../index.html">← 返回資安筆記</a>
  <div class="kicker">SEC NOTES</div>
  <h1>{title}</h1>
  <p class="article-meta">作者：葉柏毅 Alex Yeh ｜ 原文：<a href="{source_url}" rel="noopener" target="_blank">HackMD</a></p>
  {attr_block}{toc_block}<article class="article-body">
{body}
  </article>
  <footer>
    <p>仆洛宅 · 資安知識筆記 · <a href="../index.html">blog.angelz13.com</a></p>
    <p>內容為作者整理之學習筆記、非官方判定，亦不構成資安顧問建議。</p>
  </footer>
</div>
</body>
</html>'''
    (BASE / "articles" / f"{name}.html").write_text(page, encoding="utf-8")
    print(f"{name}.html 產生（{len(page)} 字元）")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "isms"
    if target == "isms":
        convert("isms",
                "ISO 27001:2022／ISMS 認證流程導覽",
                "ISO 27001:2022／ISMS 認證流程實務：里程碑、審查前檢查、A.5–A.18 稽核重點、稽核回答技巧、2013→2022 版本變更比對。",
                "https://hackmd.io/@alrex5401/ISMS",
                None)
    elif target == "cissp":
        convert("cissp",
                "CISSP 八大領域筆記",
                "CISSP 八大領域整理：治理與風險、資產安全、安全工程與密碼學、網路、IAM、安全評鑑、維運、軟體開發安全；對比矩陣、記憶口訣與自測。",
                "https://hackmd.io/@alrex5401/CISSP",
                "本篇 CISSP 八大領域筆記整理自 <strong>WUSON（Wentz Wu）</strong>課程教材、經授權公開分享；圖表版權屬原作者，在此致謝。完整原始筆記見 <a href=\"https://hackmd.io/@alrex5401/CISSP\" rel=\"noopener\" target=\"_blank\">HackMD</a>。")

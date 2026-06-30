#!/usr/bin/env python3
from pathlib import Path
css = Path("/Users/alrex5401/Documents/VS/sec-knowledge/css/brand.css")
t = css.read_text(encoding="utf-8")
MARKER = "── 文章頁 ─"
if MARKER in t:
    print("文章樣式已存在、不重複加")
else:
    article_css = """

/* ── 文章頁 ───────────────────────── */
.article-meta { color: var(--sub); font-size: 0.85rem; margin: 0 0 16px; }
.article-meta a { color: var(--accent); }
.attribution {
  border-left: 3px solid var(--warn);
  background: rgba(179, 130, 63, 0.08);
  border-radius: 0 12px 12px 0;
  padding: 10px 16px;
  font-size: 0.85rem;
  color: var(--sub);
  margin: 0 0 22px;
}
.article-body { font-size: 0.98rem; }
.article-body h1 { font-size: 1.4rem; margin: 30px 0 10px; }
.article-body h2 {
  font-size: 1.25rem;
  margin: 32px 0 12px;
  border-bottom: 1px solid var(--card-border);
  padding-bottom: 6px;
  letter-spacing: 0.03em;
}
.article-body h3 { font-size: 1.08rem; margin: 24px 0 8px; }
.article-body h4 { font-size: 0.98rem; margin: 18px 0 6px; color: var(--accent); }
.article-body p { margin: 12px 0; }
.article-body img {
  max-width: 100%;
  height: auto;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(55, 69, 97, 0.1);
  margin: 14px 0;
}
.article-body table {
  border-collapse: collapse;
  width: 100%;
  margin: 16px 0;
  font-size: 0.88rem;
  display: block;
  overflow-x: auto;
}
.article-body th, .article-body td {
  border: 1px solid var(--card-border);
  padding: 8px 12px;
  text-align: left;
}
.article-body th { background: rgba(90, 106, 147, 0.08); font-weight: 700; }
.article-body code {
  background: rgba(55, 69, 97, 0.06);
  padding: 2px 6px;
  border-radius: 5px;
  font-size: 0.86em;
  font-family: ui-monospace, Menlo, monospace;
}
.article-body pre {
  background: rgba(55, 69, 97, 0.06);
  padding: 14px 16px;
  border-radius: 10px;
  overflow-x: auto;
}
.article-body pre code { background: none; padding: 0; }
.article-body blockquote {
  border-left: 3px solid var(--accent);
  background: rgba(223, 230, 242, 0.4);
  margin: 14px 0;
  padding: 10px 16px;
  border-radius: 0 12px 12px 0;
  color: var(--sub);
}
.article-body ul, .article-body ol { padding-left: 1.5em; }
.article-body li { margin: 5px 0; }
.article-body a { color: var(--accent); word-break: break-word; }
.article-body hr { border: none; border-top: 1px solid var(--card-border); margin: 28px 0; }
"""
    css.write_text(t + article_css, encoding="utf-8")
    print("文章樣式已加進 brand.css")

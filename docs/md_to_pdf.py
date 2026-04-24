import markdown
import os

# Read markdown
with open("项目汇报文档.md", "r", encoding="utf-8") as f:
    md_text = f.read()

# Convert to HTML
html_body = markdown.markdown(md_text, extensions=["tables", "fenced_code"])

# Wrap with basic styling
html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>项目汇报文档</title>
<style>
body {{
    font-family: "Segoe UI", "Microsoft YaHei", "PingFang SC", sans-serif;
    font-size: 14px;
    line-height: 1.8;
    color: #333;
    max-width: 900px;
    margin: 40px auto;
    padding: 0 20px;
}}
h1 {{ font-size: 24px; border-bottom: 2px solid #2c3e50; padding-bottom: 8px; margin-top: 30px; }}
h2 {{ font-size: 20px; border-bottom: 1px solid #ddd; padding-bottom: 6px; margin-top: 24px; }}
h3 {{ font-size: 16px; margin-top: 20px; }}
table {{ border-collapse: collapse; width: 100%; margin: 16px 0; }}
th, td {{ border: 1px solid #ccc; padding: 8px 12px; text-align: left; }}
th {{ background: #f5f5f5; font-weight: 600; }}
code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: Consolas, monospace; }}
pre {{ background: #f8f8f8; padding: 12px; border-radius: 6px; overflow-x: auto; }}
pre code {{ background: none; padding: 0; }}
ul, ol {{ margin: 8px 0; padding-left: 24px; }}
li {{ margin: 4px 0; }}
hr {{ border: none; border-top: 1px solid #eee; margin: 24px 0; }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

with open("项目汇报文档.html", "w", encoding="utf-8") as f:
    f.write(html)

print("HTML generated: 项目汇报文档.html")

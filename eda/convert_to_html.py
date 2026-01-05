import markdown
import os

# HTML Template with CSS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        .content {{
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1, h2, h3 {{ color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
        img {{ max-width: 100%; height: auto; display: block; margin: 20px auto; border: 1px solid #ddd; border-radius: 4px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        code {{ background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px; font-family: 'Courier New', Courier, monospace; }}
        pre {{ background-color: #f4f4f4; padding: 15px; border-radius: 4px; overflow-x: auto; }}
    </style>
</head>
<body>
    <div class="content">
        {body}
    </div>
</body>
</html>
"""

def convert_md_to_html(md_file_path):
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    # Convert Markdown to HTML
    html_body = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])
    
    # Generate Title from filename
    title = os.path.basename(md_file_path).replace('.md', '')
    
    # Wrap in template
    full_html = HTML_TEMPLATE.format(title=title, body=html_body)
    
    # Save as .html
    html_file_path = md_file_path.replace('.md', '.html')
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Converted: {md_file_path} -> {html_file_path}")

# List of files to convert
files_to_convert = [
    'eda/eda_step1_report.md',
    'eda/eda_step2_report.md',
    'eda/introduction_analysis_guideline.md',
    'eda/libs/install_guide.md',
    'eda/vis/visualization_guide.md'
]

for file_path in files_to_convert:
    if os.path.exists(file_path):
        convert_md_to_html(file_path)
    else:
        print(f"File not found: {file_path}")

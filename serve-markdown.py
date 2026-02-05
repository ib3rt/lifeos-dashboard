#!/usr/bin/env python3
"""
Simple Markdown File Server for Life OS
Serves all markdown files from the docs-viewer directory
"""

from flask import Flask, send_from_directory, jsonify, render_template_string
import os

app = Flask(__name__)
DOCS_DIR = os.path.dirname(os.path.abspath(__file__))

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>📚 Life OS Markdown Files</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Inter', sans-serif; 
            background: #0a0a0f; 
            color: #e0e0e0;
            padding: 40px;
        }
        h1 { color: #6366f1; margin-bottom: 30px; }
        .file { 
            padding: 15px; 
            margin: 10px 0;
            background: #1a1a25;
            border-radius: 10px;
            border: 1px solid #333;
        }
        .file a { 
            color: #6366f1; 
            text-decoration: none;
            font-size: 16px;
        }
        .file:hover { border-color: #6366f1; }
        .folder { color: #888; font-size: 12px; margin-bottom: 5px; }
    </style>
</head>
<body>
    <h1>📚 Life OS Markdown Files</h1>
    <p>Total files: {{ files|length }}</p>
    {% for folder, file_list in folders.items() %}
    <div class="folder">📁 {{ folder }}</div>
    {% for f in file_list %}
    <div class="file">
        <a href="/file/{{ f.path }}">{{ f.name }}</a>
    </div>
    {% endfor %}
    {% endfor %}
</body>
</html>
'''

FILE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>{{ filename }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Inter', sans-serif; 
            background: #0a0a0f; 
            color: #e0e0e0;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px;
        }
        h1 { color: #6366f1; margin-bottom: 20px; }
        pre { 
            background: #1a1a25; 
            padding: 20px; 
            border-radius: 10px;
            overflow-x: auto;
        }
        a { color: #6366f1; }
    </style>
</head>
<body>
    <a href="/">← Back to files</a>
    <h1>{{ filename }}</h1>
    <pre>{{ content }}</pre>
</body>
</html>
'''

@app.route('/')
def index():
    files = []
    folders = {}
    
    for root, dirs, filenames in os.walk(DOCS_DIR):
        for f in filenames:
            if f.endswith('.md'):
                path = os.path.join(root, f)
                rel_path = os.path.relpath(path, DOCS_DIR)
                folder = os.path.dirname(rel_path)
                if folder == '.':
                    folder = 'Root'
                
                if folder not in folders:
                    folders[folder] = []
                folders[folder].append({'name': f, 'path': rel_path})
    
    return render_template_string(HTML_TEMPLATE, files=files, folders=folders)

@app.route('/file/<path:filepath>')
def serve_file(filepath):
    full_path = os.path.join(DOCS_DIR, filepath)
    if os.path.exists(full_path):
        with open(full_path, 'r') as f:
            content = f.read()
        return render_template_string(FILE_TEMPLATE, filename=filepath, content=content)
    return 'File not found', 404

if __name__ == '__main__':
    print('🚀 Starting Markdown Server...')
    print('📚 URL: http://localhost:5000')
    app.run(host='0.0.0.0', port=5000, debug=True)

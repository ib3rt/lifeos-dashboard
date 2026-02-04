#!/usr/bin/env python3
"""
Generate search index for markdown files in the workspace.
Scans recursively for *.md files and creates a JSON index.
"""

import json
import os
import re
from pathlib import Path

WORKSPACE_PATH = "/home/ubuntu/.openclaw/workspace"
OUTPUT_PATH = "/home/ubuntu/.openclaw/workspace/docs-viewer/search-index.json"

def extract_title(content):
    """Extract the first H1 or H2 heading as title."""
    lines = content.split('\n')
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('# '):
            return stripped[2:].strip()
        elif stripped.startswith('## '):
            return stripped[3:].strip()
    return None

def extract_excerpt(content, query=None, max_length=300):
    """Extract a preview excerpt from the content."""
    # Remove markdown syntax
    text = re.sub(r'#{1,6}\s+', '', content)
    text = re.sub(r'\*\*|__', '', text)
    text = re.sub(r'\*|_', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', text)
    text = re.sub(r'`[^`]+`', '', text)
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'>', '', text)
    text = re.sub(r'[-*+]\s+', '', text)
    text = re.sub(r'\d+\.\s+', '', text)
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    if len(text) > max_length:
        text = text[:max_length].rsplit(' ', 1)[0] + '...'
    
    return text

def get_file_tree(files):
    """Build a hierarchical file tree from flat file list."""
    tree = []
    path_map = {}
    
    for file_path in sorted(files):
        rel_path = os.path.relpath(file_path, WORKSPACE_PATH)
        parts = rel_path.split(os.sep)
        
        current = tree
        for i, part in enumerate(parts[:-1]):
            existing = next((item for item in current if item.get('name') == part and item.get('type') == 'folder'), None)
            if not existing:
                new_folder = {
                    'type': 'folder',
                    'name': part,
                    'path': os.path.sep.join(parts[:i+1]),
                    'children': []
                }
                current.append(new_folder)
                current = new_folder['children']
            else:
                current = existing['children']
        
        # Add file to the last folder or root
        file_name = parts[-1]
        current.append({
            'type': 'file',
            'name': file_name,
            'path': rel_path
        })
    
    # Sort tree: folders first, then files, both alphabetically
    def sort_tree(nodes):
        nodes.sort(key=lambda x: (0 if x['type'] == 'folder' else 1, x['name'].lower()))
        for node in nodes:
            if node.get('children'):
                sort_tree(node['children'])
    
    sort_tree(tree)
    return tree

def scan_markdown_files():
    """Scan workspace for all markdown files."""
    files = []
    
    for root, dirs, filenames in os.walk(WORKSPACE_PATH):
        # Skip hidden and system directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', '.git']]
        
        for filename in filenames:
            if filename.endswith('.md'):
                file_path = os.path.join(root, filename)
                files.append(file_path)
    
    return files

def build_index():
    """Build the complete search index."""
    print("Scanning for markdown files...")
    files = scan_markdown_files()
    print(f"Found {len(files)} markdown files")
    
    index_data = {
        'version': '1.0',
        'generated': os.path.getmtime(WORKSPACE_PATH) if os.path.exists(WORKSPACE_PATH) else None,
        'files': [],
        'fileTree': get_file_tree(files)
    }
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            rel_path = os.path.relpath(file_path, WORKSPACE_PATH)
            title = extract_title(content)
            excerpt = extract_excerpt(content)
            
            # Count approximate words
            word_count = len(content.split())
            
            # Get file stats
            stat = os.stat(file_path)
            
            index_data['files'].append({
                'path': rel_path,
                'title': title or rel_path,
                'excerpt': excerpt,
                'wordCount': word_count,
                'modified': int(stat.st_mtime)
            })
        except Exception as e:
            print(f"Warning: Could not process {file_path}: {e}")
    
    # Sort files by path
    index_data['files'].sort(key=lambda x: x['path'])
    
    # Write index
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    
    print(f"Index written to {OUTPUT_PATH}")
    print(f"Indexed {len(index_data['files'])} files")

if __name__ == '__main__':
    build_index()

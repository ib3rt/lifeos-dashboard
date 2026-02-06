#!/bin/bash
# Knowledge Curator Agent - Shell-based implementation
# Uses curl to call LLM APIs directly

# Configuration
WORKSPACE="/home/ubuntu/.openclaw/workspace"
ARTICLES_DIR="$WORKSPACE/brands/b3rt-dev/content/articles"
API_ENDPOINT="${MOONSHOT_API_ENDPOINT:-https://api.moonshot.cn/v1}"
API_KEY="${MOONSHOT_API_KEY:-}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Ensure directory exists
mkdir -p "$ARTICLES_DIR"

# Function to call LLM API
call_llm() {
    local prompt="$1"
    local model="${2:-kimi-k2.5}"
    
    curl -s "$API_ENDPOINT/chat/completions" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $API_KEY" \
        -d "{
            \"model\": \"$model\",
            \"messages\": [
                {\"role\": \"system\", \"content\": \"You are a world-class technical writer. Create comprehensive articles in markdown format. Use prose-heavy writing, minimal lists, include specific examples.\"},
                {\"role\": \"user\", \"content\": \"$prompt\"}
            ],
            \"temperature\": 0.7,
            \"max_tokens\": 4000
        }" | jq -r '.choices[0].message.content'
}

# Function to generate article
generate_article() {
    local topic="$1"
    local template="${2:-life-os-intro}"
    
    log_info "Curating: $topic"
    log_info "Template: $template"
    
    # Create slug
    slug=$(echo "$topic" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9 ]/-/g' | tr -s '-' | tr -d ' ')
    filename="${slug}.md"
    filepath="$ARTICLES_DIR/$filename"
    
    # Generate content based on template
    case "$template" in
        "life-os-intro")
            prompt="Write a comprehensive introduction about '$topic' for Life OS users. Include: compelling hook, 3-4 key sections with substantive paragraphs, concrete examples, summary with next steps. Write in markdown. Minimum 800 words."
            ;;
        "technical-guide")
            prompt="Write a complete technical guide about '$topic' covering: prerequisites, step-by-step implementation, code examples, best practices, troubleshooting tips. Markdown format. 1000+ words."
            ;;
        "tutorial")
            prompt="Create a step-by-step tutorial for '$topic'. Include: learning objectives, prerequisites, lesson modules, practice projects. Markdown format. 1000+ words."
            ;;
        *)
            prompt="Write an informative article about '$topic'. Markdown format, 800+ words."
            ;;
    esac
    
    # Call LLM
    log_info "Generating content..."
    content=$(call_llm "$prompt")
    
    if [ -z "$content" ] || [ "$content" = "null" ]; then
        log_error "Failed to generate content"
        return 1
    fi
    
    # Add front matter
    date=$(date '+%B %d, %Y')
    read_time=$(echo "$content" | wc -w)
    read_time=$((read_time / 200))
    [ $read_time -lt 1 ] && read_time=1
    
    full_content="---
title: \"$topic\"
date: \"$date\"
read_time: \"$read_time min read\"
category: \"Life OS\"
tags: [\"Life OS\", \"Automation\", \"AI\"]
---

$content"
    
    # Save article
    echo "$full_content" > "$filepath"
    
    # Generate HTML
    generate_html "$filepath" "$topic" "$read_time"
    
    log_success "Created: $filepath"
    log_success "HTML: ${filepath%.md}.html"
}

# Function to generate HTML from markdown
generate_html() {
    local md_file="$1"
    local title="$2"
    local read_time="$3"
    
    # Read content
    content=$(cat "$md_file")
    
    # Convert markdown to HTML (simplified)
    html_body=$(echo "$content" | sed -E '
        s/^### (.+)$/<h3>\1<\/h3>/
        s/^## (.+)$/<h2>\1<\/h2>/
        s/^# (.+)$/<h1>\1<\/h1>/
        s/\*\*(.+?)\*\*/<strong>\1<\/strong>/
        s/\*(.+?)\*/<em>\1<\/em>/
        s/`(.+?)`/<code>\1<\/code>/
        s/^- (.+)$/<li>\1<\/li>/
    ' | awk '
        /^<h[1-3]>/ || /^<ul>/ || /^<li>/ || /^<pre>/ { in_list=0; print }
        /^<\/ul>/ { print; next }
        /^<li>/ { 
            if (!in_list) { print "<ul>"; in_list=1 }
            print; next
        }
        NF > 0 && !/^</ { 
            if (in_list) { print "</ul>"; in_list=0 }
            print "<p>" $0 "</p>"
        }
        /^</ { print }
    ' | sed 's/<p><\/p>//' | tr -s '\n')
    
    # Create full HTML
    cat > "${md_file%.md}.html" << EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$title | b3rt.dev</title>
    <link rel="stylesheet" href="/design-system.css">
</head>
<body>
    <nav class="glass-nav">
        <div class="nav-container">
            <a href="/" class="nav-logo">🦞 b3rt</a>
            <div class="nav-links">
                <a href="/articles">Articles</a>
                <a href="/templates">Templates</a>
                <a href="/journey">Journey</a>
            </div>
        </div>
    </nav>

    <main class="container">
        <a href="/articles" class="back-link">← Back to Articles</a>
        
        <article class="article-content">
            <header class="article-header">
                <span class="article-category">Life OS</span>
                <h1 class="article-title">$title</h1>
                <div class="article-meta">
                    <span>📖 $read_time min read</span>
                    <span>✍️ By b3rt</span>
                </div>
            </header>
            
            <div class="article-body">
$(echo "$html_body" | sed '1,/---$/d')
            </div>
        </article>
    </main>

    <footer>
        <p>Built with ❤️ using Life OS</p>
    </footer>
</body>
</html>
EOF
}

# Batch generate
batch_generate() {
    local topic="$1"
    local count="${2:-5}"
    
    log_info "Batch generating $count articles on: $topic"
    
    for i in $(seq 1 $count); do
        subtopic="$topic - Part $i"
        generate_article "$subtopic" "life-os-intro"
    done
}

# Main
case "$1" in
    "generate"|"create")
        topic="$2"
        template="${3:-life-os-intro}"
        generate_article "$topic" "$template"
        ;;
    "batch")
        topic="$2"
        count="${3:-5}"
        batch_generate "$topic" "$count"
        ;;
    "help"|"--help"|"-h")
        echo "🦞 Knowledge Curator Agent"
        echo ""
        echo "Usage:"
        echo "  $0 generate \"Topic Name\" [template]"
        echo "  $0 batch \"Topic\" [count]"
        echo "  $0 help"
        echo ""
        echo "Templates:"
        echo "  life-os-intro    General introductions"
        echo "  technical-guide  Developer documentation"
        echo "  tutorial         Step-by-step guides"
        echo ""
        echo "Examples:"
        echo "  $0 generate \"AI Automation Guide\""
        echo "  $0 generate \"API Integration\" technical-guide"
        echo "  $0 batch \"Machine Learning\" 5"
        ;;
    *)
        echo "Unknown command: $1"
        echo "Use: $0 help"
        exit 1
        ;;
esac

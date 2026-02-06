# Content Pipeline

## Pipeline Stages

```
IDEA → OUTLINE → DRAFT → EDIT → OPTIMIZE → APPROVE → PUBLISH → PROMOTE → ANALYZE
```

## Stage Details

### 1. Ideation Stage
**Inputs:** Keywords, trends, audience feedback, competitor analysis
**Outputs:** Content ideas list
**Tools:** `generate_ideas.py`

### 2. Outline Stage
**Inputs:** Approved idea, target keyword
**Outputs:** Content structure, H2/H3 hierarchy
**Tools:** `create_outline.py`

### 3. Draft Stage
**Inputs:** Outline, tone, length, audience
**Outputs:** First draft
**Tools:** `generate_content.py` (AI-assisted)

### 4. Edit Stage
**Inputs:** Draft, style guide, brand voice
**Outputs:** Edited version
**Tools:** `edit_content.py`

### 5. Optimize Stage
**Inputs:** Edited draft, SEO requirements
**Outputs:** SEO-optimized content
**Tools:** `optimize_seo.py`

### 6. Approve Stage
**Inputs:** Optimized content
**Outputs:** Approved content ready for publishing
**Tools:** `approval_workflow.py`

### 7. Publish Stage
**Inputs:** Approved content, scheduling info
**Outputs:** Published content on platforms
**Tools:** `publish_*.py` platform scripts

### 8. Promote Stage
**Inputs:** Published content, promotion channels
**Outputs:** Social posts, newsletter, community shares
**Tools:** `promote_content.py`

### 9. Analyze Stage
**Inputs:** Published content metrics
**Outputs:** Performance report, insights
**Tools:** `analyze_performance.py`

## Quality Gates

| Stage | Gate Criteria |
|-------|---------------|
| Ideation | Min 5 ideas, diverse topics |
| Outline | 80% keyword coverage, logical flow |
| Draft | Min word count, structure compliance |
| Edit | Grammar check, brand voice match |
| Optimize | SEO score > 80, readability > 60 |
| Publish | All platforms ready, schedule confirmed |

## Workflow Commands

```bash
# Start new content piece
python tools/content/new_content.py --idea "your idea here"

# Move to next stage
python tools/content/promote.py --id CONTENT_ID --stage next

# Check pipeline status
python tools/content/pipeline_status.py

# Bulk operations
python tools/content/bulk_promote.py --stage draft --count 10
```

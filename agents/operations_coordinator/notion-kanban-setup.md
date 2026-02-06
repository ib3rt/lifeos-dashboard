# Notion Kanban Setup Guide

> **Mission:** Life OS Project Management Infrastructure  
> **Status:** Ready for deployment  
> **Maintainer:** The Mechanic ⚙️

---

## 1. Notion API Overview

### Current Capabilities (API Version 2025-09-03)

| Feature | Status | Notes |
|---------|--------|-------|
| Database Creation | ✅ Supported | Create databases with initial data sources |
| Page Automation | ✅ Supported | Create/update pages via API |
| Relation Properties | ✅ Supported | Link databases bidirectionally |
| Rollup Properties | ✅ Supported | Aggregate data from related databases |
| Webhooks | ✅ Supported | Real-time event notifications (March 2025 update) |
| Status Properties | ❌ Not Supported | Cannot create via API; use Select as workaround |
| Formula Properties | ✅ Supported | Compute values dynamically |

### Key API Endpoints

```
Base URL: https://api.notion.com/v1

POST   /v1/databases              # Create database
PATCH  /v1/databases/{id}         # Update database
GET    /v1/databases/{id}         # Retrieve database
POST   /v1/pages                  # Create page
PATCH  /v1/pages/{id}             # Update page
GET    /v1/pages/{id}             # Retrieve page
POST   /v1/search                 # Search workspace
```

---

## 2. Integration Token Setup

### Step 1: Create Integration

1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Click "New integration"
3. Name: `Life OS - Kanban Controller`
4. Associated workspace: Select your workspace
5. Enable capabilities:
   - ✅ Read content
   - ✅ Update content
   - ✅ Insert content
   - ✅ Read user information (optional)
6. Click "Save"

### Step 2: Copy Internal Integration Token

```bash
# Store securely - this is your API key
NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Step 3: Share Database with Integration

1. Create a parent page for your Life OS (or use existing)
2. Click "..." (more) on the page → "Add connections"
3. Select `Life OS - Kanban Controller`

### Step 4: Get Parent Page ID

```bash
# From page URL: https://www.notion.so/Workspace-Name-PAGE_ID
# Extract the last 32-character segment
PARENT_PAGE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 3. Database Schema

### 3.1 Projects Database

```json
{
  "parent": {
    "page_id": "YOUR_PARENT_PAGE_ID"
  },
  "title": [
    {
      "type": "text",
      "text": {
        "content": "📁 Projects"
      }
    }
  ],
  "is_inline": true,
  "description": [
    {
      "type": "text",
      "text": {
        "content": "Life OS project tracking - high-level initiatives and goals"
      }
    }
  ],
  "icon": {
    "type": "emoji",
    "emoji": "📁"
  },
  "initial_data_source": {
    "properties": {
      "Name": {
        "title": {}
      },
      "Status": {
        "select": {
          "options": [
            { "name": "🔵 Backlog", "color": "blue" },
            { "name": "🟡 In Progress", "color": "yellow" },
            { "name": "🟠 Review", "color": "orange" },
            { "name": "🟢 Complete", "color": "green" },
            { "name": "⚫ Archived", "color": "gray" }
          ]
        }
      },
      "Priority": {
        "select": {
          "options": [
            { "name": "🔴 Critical", "color": "red" },
            { "name": "🟠 High", "color": "orange" },
            { "name": "🟡 Medium", "color": "yellow" },
            { "name": "🟢 Low", "color": "green" },
            { "name": "⚪ Trivial", "color": "gray" }
          ]
        }
      },
      "Assigned Agent": {
        "select": {
          "options": [
            { "name": "🧠 The Architect", "color": "purple" },
            { "name": "⚙️ The Mechanic", "color": "blue" },
            { "name": "🔍 The Scout", "color": "green" },
            { "name": "🎨 The Artisan", "color": "pink" },
            { "name": "🎯 The Operator", "color": "orange" },
            { "name": "📊 The Analyst", "color": "yellow" }
          ]
        }
      },
      "Due Date": {
        "date": {}
      },
      "Start Date": {
        "date": {}
      },
      "Progress": {
        "number": {
          "format": "percent"
        }
      },
      "Tasks": {
        "relation": {
          "data_source_id": "TASKS_DATA_SOURCE_ID",
          "type": "dual_property",
          "dual_property": {
            "synced_property_name": "Project"
          }
        }
      },
      "Tasks Completed": {
        "rollup": {
          "relation_property_name": "Tasks",
          "rollup_property_name": "Complete",
          "function": "checked"
        }
      },
      "Task Count": {
        "rollup": {
          "relation_property_name": "Tasks",
          "rollup_property_name": "Name",
          "function": "count"
        }
      },
      "Description": {
        "rich_text": {}
      },
      "Tags": {
        "multi_select": {
          "options": [
            { "name": "🤖 AI/ML", "color": "purple" },
            { "name": "🏠 Home", "color": "green" },
            { "name": "💼 Work", "color": "blue" },
            { "name": "📚 Learning", "color": "yellow" },
            { "name": "💪 Health", "color": "red" },
            { "name": "💰 Finance", "color": "green" },
            { "name": "🎮 Gaming", "color": "pink" },
            { "name": "🔧 System", "color": "gray" }
          ]
        }
      },
      "Created": {
        "created_time": {}
      },
      "Last Updated": {
        "last_edited_time": {}
      }
    }
  }
}
```

### 3.2 Tasks Database

```json
{
  "parent": {
    "page_id": "YOUR_PARENT_PAGE_ID"
  },
  "title": [
    {
      "type": "text",
      "text": {
        "content": "✅ Tasks"
      }
    }
  ],
  "is_inline": true,
  "description": [
    {
      "type": "text",
      "text": {
        "content": "Actionable tasks linked to projects"
      }
    }
  ],
  "icon": {
    "type": "emoji",
    "emoji": "✅"
  },
  "initial_data_source": {
    "properties": {
      "Name": {
        "title": {}
      },
      "Status": {
        "select": {
          "options": [
            { "name": "🔵 Backlog", "color": "blue" },
            { "name": "🟡 In Progress", "color": "yellow" },
            { "name": "🟠 Review", "color": "orange" },
            { "name": "🟢 Complete", "color": "green" },
            { "name": "⚫ Archived", "color": "gray" }
          ]
        }
      },
      "Priority": {
        "select": {
          "options": [
            { "name": "🔴 Critical", "color": "red" },
            { "name": "🟠 High", "color": "orange" },
            { "name": "🟡 Medium", "color": "yellow" },
            { "name": "🟢 Low", "color": "green" },
            { "name": "⚪ Trivial", "color": "gray" }
          ]
        }
      },
      "Assigned Agent": {
        "select": {
          "options": [
            { "name": "🧠 The Architect", "color": "purple" },
            { "name": "⚙️ The Mechanic", "color": "blue" },
            { "name": "🔍 The Scout", "color": "green" },
            { "name": "🎨 The Artisan", "color": "pink" },
            { "name": "🎯 The Operator", "color": "orange" },
            { "name": "📊 The Analyst", "color": "yellow" }
          ]
        }
      },
      "Due Date": {
        "date": {}
      },
      "Project": {
        "relation": {
          "data_source_id": "PROJECTS_DATA_SOURCE_ID",
          "type": "dual_property",
          "dual_property": {
            "synced_property_name": "Tasks"
          }
        }
      },
      "Complete": {
        "checkbox": {}
      },
      "Estimated Hours": {
        "number": {
          "format": "number"
        }
      },
      "Actual Hours": {
        "number": {
          "format": "number"
        }
      },
      "Description": {
        "rich_text": {}
      },
      "Notes": {
        "rich_text": {}
      },
      "Tags": {
        "multi_select": {
          "options": [
            { "name": "🤖 AI/ML", "color": "purple" },
            { "name": "🏠 Home", "color": "green" },
            { "name": "💼 Work", "color": "blue" },
            { "name": "📚 Learning", "color": "yellow" },
            { "name": "💪 Health", "color": "red" },
            { "name": "💰 Finance", "color": "green" },
            { "name": "🎮 Gaming", "color": "pink" },
            { "name": "🔧 System", "color": "gray" }
          ]
        }
      },
      "Created": {
        "created_time": {}
      },
      "Last Updated": {
        "last_edited_time": {}
      }
    }
  }
}
```

---

## 4. Sample API Calls

### 4.1 Create Projects Database

```bash
curl -X POST 'https://api.notion.com/v1/databases' \
  -H 'Authorization: Bearer YOUR_NOTION_TOKEN' \
  -H 'Notion-Version: 2025-09-03' \
  -H 'Content-Type: application/json' \
  -d '{
    "parent": {
      "page_id": "YOUR_PARENT_PAGE_ID"
    },
    "title": [
      {
        "type": "text",
        "text": {
          "content": "📁 Projects"
        }
      }
    ],
    "is_inline": true,
    "icon": {
      "type": "emoji",
      "emoji": "📁"
    },
    "initial_data_source": {
      "properties": {
        "Name": {
          "title": {}
        },
        "Status": {
          "select": {
            "options": [
              { "name": "🔵 Backlog", "color": "blue" },
              { "name": "🟡 In Progress", "color": "yellow" },
              { "name": "🟠 Review", "color": "orange" },
              { "name": "🟢 Complete", "color": "green" }
            ]
          }
        },
        "Priority": {
          "select": {
            "options": [
              { "name": "🔴 Critical", "color": "red" },
              { "name": "🟠 High", "color": "orange" },
              { "name": "🟡 Medium", "color": "yellow" },
              { "name": "🟢 Low", "color": "green" }
            ]
          }
        },
        "Assigned Agent": {
          "select": {
            "options": [
              { "name": "⚙️ The Mechanic", "color": "blue" },
              { "name": "🧠 The Architect", "color": "purple" }
            ]
          }
        },
        "Due Date": {
          "date": {}
        },
        "Description": {
          "rich_text": {}
        },
        "Tags": {
          "multi_select": {
            "options": [
              { "name": "🔧 System", "color": "gray" },
              { "name": "🤖 AI/ML", "color": "purple" }
            ]
          }
        },
        "Created": {
          "created_time": {}
        }
      }
    }
  }'
```

**Response:**
```json
{
  "object": "database",
  "id": "projects-database-id",
  "data_sources": [
    {
      "id": "projects-data-source-id",
      "object": "data_source"
    }
  ]
}
```

Save the `data_sources[0].id` as `PROJECTS_DATA_SOURCE_ID`.

### 4.2 Create Tasks Database (with Relation)

```bash
curl -X POST 'https://api.notion.com/v1/databases' \
  -H 'Authorization: Bearer YOUR_NOTION_TOKEN' \
  -H 'Notion-Version: 2025-09-03' \
  -H 'Content-Type: application/json' \
  -d '{
    "parent": {
      "page_id": "YOUR_PARENT_PAGE_ID"
    },
    "title": [
      {
        "type": "text",
        "text": {
          "content": "✅ Tasks"
        }
      }
    ],
    "is_inline": true,
    "icon": {
      "type": "emoji",
      "emoji": "✅"
    },
    "initial_data_source": {
      "properties": {
        "Name": {
          "title": {}
        },
        "Status": {
          "select": {
            "options": [
              { "name": "🔵 Backlog", "color": "blue" },
              { "name": "🟡 In Progress", "color": "yellow" },
              { "name": "🟠 Review", "color": "orange" },
              { "name": "🟢 Complete", "color": "green" }
            ]
          }
        },
        "Project": {
          "relation": {
            "data_source_id": "PROJECTS_DATA_SOURCE_ID",
            "type": "dual_property",
            "dual_property": {
              "synced_property_name": "Tasks"
            }
          }
        },
        "Complete": {
          "checkbox": {}
        },
        "Due Date": {
          "date": {}
        },
        "Assigned Agent": {
          "select": {
            "options": [
              { "name": "⚙️ The Mechanic", "color": "blue" }
            ]
          }
        },
        "Description": {
          "rich_text": {}
        },
        "Created": {
          "created_time": {}
        }
      }
    }
  }'
```

### 4.3 Create a Project

```bash
curl -X POST 'https://api.notion.com/v1/pages' \
  -H 'Authorization: Bearer YOUR_NOTION_TOKEN' \
  -H 'Notion-Version: 2025-09-03' \
  -H 'Content-Type: application/json' \
  -d '{
    "parent": {
      "data_source_id": "PROJECTS_DATA_SOURCE_ID"
    },
    "properties": {
      "Name": {
        "title": [
          {
            "text": {
              "content": "Set up Notion Kanban Board"
            }
          }
        ]
      },
      "Status": {
        "select": {
          "name": "🟢 Complete"
        }
      },
      "Priority": {
        "select": {
          "name": "🔴 Critical"
        }
      },
      "Assigned Agent": {
        "select": {
          "name": "⚙️ The Mechanic"
        }
      },
      "Due Date": {
        "date": {
          "start": "2026-02-02"
        }
      },
      "Description": {
        "rich_text": [
          {
            "text": {
              "content": "Create kanban infrastructure for Life OS project management"
            }
          }
        ]
      },
      "Tags": {
        "multi_select": [
          { "name": "🔧 System" }
        ]
      }
    }
  }'
```

### 4.4 Create a Task (Linked to Project)

```bash
curl -X POST 'https://api.notion.com/v1/pages' \
  -H 'Authorization: Bearer YOUR_NOTION_TOKEN' \
  -H 'Notion-Version: 2025-09-03' \
  -H 'Content-Type: application/json' \
  -d '{
    "parent": {
      "data_source_id": "TASKS_DATA_SOURCE_ID"
    },
    "properties": {
      "Name": {
        "title": [
          {
            "text": {
              "content": "Research Notion API capabilities"
            }
          }
        ]
      },
      "Status": {
        "select": {
          "name": "🟢 Complete"
        }
      },
      "Project": {
        "relation": [
          {
            "id": "PROJECT_PAGE_ID"
          }
        ]
      },
      "Complete": {
        "checkbox": true
      },
      "Assigned Agent": {
        "select": {
          "name": "⚙️ The Mechanic"
        }
      },
      "Due Date": {
        "date": {
          "start": "2026-02-02"
        }
      }
    }
  }'
```

### 4.5 Update Status (Move Kanban Card)

```bash
curl -X PATCH 'https://api.notion.com/v1/pages/TASK_PAGE_ID' \
  -H 'Authorization: Bearer YOUR_NOTION_TOKEN' \
  -H 'Notion-Version: 2025-09-03' \
  -H 'Content-Type: application/json' \
  -d '{
    "properties": {
      "Status": {
        "select": {
          "name": "🟡 In Progress"
        }
      }
    }
  }'
```

### 4.6 Query Tasks by Status

```bash
curl -X POST 'https://api.notion.com/v1/databases/TASKS_DATA_SOURCE_ID/query' \
  -H 'Authorization: Bearer YOUR_NOTION_TOKEN' \
  -H 'Notion-Version: 2025-09-03' \
  -H 'Content-Type: application/json' \
  -d '{
    "filter": {
      "property": "Status",
      "select": {
        "equals": "🟡 In Progress"
      }
    },
    "sorts": [
      {
        "property": "Due Date",
        "direction": "ascending"
      }
    ]
  }'
```

---

## 5. Webhook Setup (Real-time Updates)

### 5.1 Create Webhook Subscription

1. Go to Integration settings → Webhooks tab
2. Click "Add webhook"
3. Endpoint URL: `https://your-server.com/notion-webhook`
4. Events to subscribe:
   - `page.created` - New tasks/projects created
   - `page.updated` - Status changes, edits
   - `page.deleted` - Items removed
   - `comment.created` - New comments (requires comment capability)

### 5.2 Webhook Verification

When you create a webhook, Notion sends a verification request:

```json
{
  "verification_token": "verify_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

Your endpoint must return a 200 response with the token in the body.

### 5.3 Webhook Event Payload Example

```json
{
  "data": {
    "object": "page",
    "id": "page-id",
    "properties": {
      "Status": {
        "select": {
          "name": "🟢 Complete"
        }
      }
    }
  },
  "type": "page.updated",
  "timestamp": "2026-02-02T15:00:00.000Z"
}
```

### 5.4 Signature Validation

```python
import hmac
import hashlib

def validate_webhook(payload_body, signature, verification_token):
    expected = hmac.new(
        verification_token.encode(),
        payload_body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)

# Usage:
# signature = request.headers.get('X-Notion-Signature')
# if validate_webhook(request.body, signature, VERIFICATION_TOKEN):
#     process_webhook(request.json)
```

---

## 6. Automation Ideas

### 6.1 Auto-Assign New Tasks

```python
# When a task is created without an agent, assign based on tags
if not task.get('Assigned Agent'):
    if '🔧 System' in task.get('Tags', []):
        assign_agent(task, '⚙️ The Mechanic')
    elif '🤖 AI/ML' in task.get('Tags', []):
        assign_agent(task, '🧠 The Architect')
```

### 6.2 Status Change Notifications

```python
# When status changes to Complete, notify relevant agents
if old_status != new_status and new_status == '🟢 Complete':
    notify_agent(
        agent=task['Assigned Agent'],
        message=f"✅ Task completed: {task['Name']}"
    )
```

### 6.3 Due Date Reminders

```python
# Daily check for tasks due within 24h
due_soon = query_tasks(
    filter={
        'due_date': {'on_or_before': 'tomorrow'},
        'status': {'not_equals': '🟢 Complete'}
    }
)
for task in due_soon:
    notify_agent(task['Assigned Agent'], f"⏰ Due soon: {task['Name']}")
```

### 6.4 Progress Calculation

```python
# Update project progress based on completed tasks
def update_project_progress(project_id):
    tasks = get_project_tasks(project_id)
    total = len(tasks)
    completed = sum(1 for t in tasks if t['Complete'])
    progress = (completed / total * 100) if total > 0 else 0
    
    update_page(project_id, {
        'Progress': {'number': progress / 100}
    })
```

### 6.5 Agent Workload Dashboard

```python
# Query tasks per agent for workload balancing
def get_agent_workload():
    agents = ['⚙️ The Mechanic', '🧠 The Architect', ...]
    workload = {}
    for agent in agents:
        workload[agent] = query_tasks(
            filter={
                'Assigned Agent': {'equals': agent},
                'Status': {'equals': '🟡 In Progress'}
            }
        )
    return workload
```

---

## 7. Views Configuration

### 7.1 Kanban Board View (By Status)

**Manual setup in Notion UI:**
1. Open database → "+ New view"
2. Select "Board"
3. Group by: `Status`
4. Card preview: Show `Name`, `Priority`, `Due Date`, `Assigned Agent`

### 7.2 Calendar View (By Due Date)

1. "+ New view" → "Calendar"
2. Date property: `Due Date`
3. Display: `Name`, `Status`, `Assigned Agent`

### 7.3 Table View (All Properties)

1. Default view - shows all columns
2. Sort: `Due Date` ascending
3. Filter: `Status` is not `⚫ Archived`

### 7.4 Agent View (Filtered by Assigned Agent)

1. "+ New view" → "Table"
2. Filter: `Assigned Agent` equals `⚙️ The Mechanic`
3. Group by: `Status`

---

## 8. Environment Variables

```bash
# .env file
NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_VERSION=2025-09-03
PROJECTS_DATA_SOURCE_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
TASKS_DATA_SOURCE_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
PARENT_PAGE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
WEBHOOK_SECRET=verify_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 9. Quick Reference

### Status Options
| Emoji | Status | Use Case |
|-------|--------|----------|
| 🔵 | Backlog | Not yet started, queued |
| 🟡 | In Progress | Actively being worked on |
| 🟠 | Review | Awaiting review/approval |
| 🟢 | Complete | Finished |
| ⚫ | Archived | Cancelled or no longer relevant |

### Priority Levels
| Emoji | Priority | Response Time |
|-------|----------|---------------|
| 🔴 | Critical | Immediate |
| 🟠 | High | Within 24h |
| 🟡 | Medium | Within 3 days |
| 🟢 | Low | Within 1 week |
| ⚪ | Trivial | As time permits |

### Agent Assignments
| Agent | Emoji | Specialty |
|-------|-------|-----------|
| The Architect | 🧠 | Design, strategy, planning |
| The Mechanic | ⚙️ | Operations, infrastructure |
| The Scout | 🔍 | Research, exploration |
| The Artisan | 🎨 | Creative, visual work |
| The Operator | 🎯 | Execution, implementation |
| The Analyst | 📊 | Data, reporting, insights |

---

## 10. Troubleshooting

| Issue | Solution |
|-------|----------|
| 401 Unauthorized | Check token, verify integration has access to page |
| 403 Forbidden | Enable required capabilities in integration settings |
| 404 Not Found | Verify page/database IDs are correct |
| 429 Rate Limited | Implement exponential backoff (3 req/sec limit) |
| Status property fails | Use Select instead (Status not creatable via API) |
| Relation not working | Ensure both data sources exist and IDs are correct |
| Webhook not firing | Check endpoint URL, verify subscription is active |

---

*Document version: 1.0*  
*Created: 2026-02-02*  
*Next review: On API changes or new requirements*

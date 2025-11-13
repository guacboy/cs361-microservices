# Group 15 Microservices
## Data Reports Microservice
## Login Microservice
## Suggestion Microservice

### How to REQUEST Data (Submit Suggestions)
You can submit suggestions programmatically by writing directly to the `suggestion.txt` file:

```python
import json
from datetime import datetime

# example programmatic submission
suggestion_data = {
    "suggestion": "Add user profile customization features",
    "timestamp": datetime.now().isoformat(),
    "has_attachment": False,
    "attachment_path": None
}

with open("suggestion.txt", "a", encoding="utf-8") as f:
    f.write(json.dumps(suggestion_data) + "\n")
```

Supported file attachments:
- **Images**: JPG, JPEG, PNG
- **Documents**: PDF, DOC, DOCX, TXT

### How to RECEIVE Data (Process and Access Suggestions)

#### Starting the Receiver Service

1. Run the receiver service (run this first):
   ```bash
   python receive.py
   ```

2. The service will:
   - Start monitoring `suggestion.txt` for new submissions
   - Process suggestions into the database (`data.json`)
   - Display real-time updates in the console

#### Accessing Processed Data

##### Method 1: Real-time Console Output

The receiver service provides continuous updates:

```
==================================================
latest suggestions in database
==================================================
🟢 id: 3 | status: new      | date: 2024-01-15T14:30:45
   suggestion: We should add dark mode to the application...
   📎 attachment: /path/to/screenshot.png
--------------------------------------------------
```

##### Method 2: Direct Database Access

Read directly from `data.json`:

```python
import json

# example call to read all suggestions
with open('data.json', 'r', encoding='utf-8') as f:
    suggestions_data = json.load(f)

# access specific suggestion properties
for suggestion in suggestions_data:
    print(f"ID: {suggestion['id']}")
    print(f"Status: {suggestion['status']}")
    print(f"Suggestion: {suggestion['suggestion']}")
    print(f"Date Added: {suggestion['date_added']}")
    print(f"Has Attachment: {suggestion['has_attachment']}")
```

### Data Structure

Each suggestion in `data.json` contains:

```json
{
  "id": 1,
  "suggestion": "User's suggestion text",
  "date_added": "2024-01-15T14:30:45.123456",
  "status": "new",
  "has_attachment": false,
  "attachment_path": null,
  "submission_timestamp": "2024-01-15T14:30:45.123456"
}
```
# Group 15 Microservices
## CSV Report Generator Microservice

### Installation

Install the required dependencies:
```bash
pip install pandas watchdog
```
or
```bash
pip install -r requirements.txt
```

### How to REQUEST Data (Submit CSV File)

#### Method 1: Direct File Path Writing

Write a CSV file path directly to `report.txt`. The GUI will automatically detect this and generate a report.

```python
# write file path to report.txt
with open('report.txt', 'w') as f:
    f.write("/path/to/your/data.csv")
```

#### Method 2: Command Line Request

```bash
# write file path to report.txt
echo "/path/to/your/data.csv" > report.txt
```

### How to RECEIVE Data (Access Report)

#### Starting the Receiver Service

1. Run both services (order doesn't matter):
   ```bash
   python receive.py
   python report.py
   ```

2. The services will:
   - Start monitoring `report.txt` for a path to a CSV file
   - Displays real-time updates in the console and `report.txt`

#### Example Call
```python
def read_report():
    """
    Read report.txt and print content to console.
    """
    with open('report.txt', 'r') as f:
        content = f.read()
    print(content)
```

#### Example Data

```
Dataset Summary Report
==================================================

File: sample data(Sheet1).csv

Data Preview (first 5 rows):
   ID           Name  Age
0   1       John Doe   32
1   2     Jane Smith   28
2   3    Bob Johnson   45
3   4    Alice Brown   29
4   5  Carlie Wilson   35
============================================================
```

### UML Sequence Diagram
![CSV Report Generator Microservice](ReportGeneratorUML.png)

## Login Microservice

### Installation

Install the required dependencies:
    pip install fastapi uvicorn pydantic

### How to REQUEST Data (Authenticate a login with the user's credentials)

Start the uvicorn server
   uvicorn main:app --reload --port 8000 

Send a POST request with a JSON body containing the user's credentials to the /login endpoint.

    credentials = {
        "username": "Thayer",
        "password": "12345678"
    }

    def api_login(username, password):
        # This sends the request to the microservice
        response = requests.post(
            "http://localhost:8000/login",
            json={"username": username, "password": password}
        )
        return response

### How to RECEIVE Data (Process and Access User Credentials)

Receives the response back from the server, validating the status and extracting the session token or an error message.

    def process_login_response(response):
    # This processes the data received from the microservice
    if response.status_code == 200:
        data = response.json()
        print(f"Login SUCCESS! User ID: {data['user_id']}")
        print(f"Session Token: {data['session_token']}")
        return data['session_token']
    elif response.status_code == 401:
        data = response.json()
        print(f"Login FAILED. Error: {data['detail']}")
        return None
    else:
        print("Error connecting to microservice.")
        return None

### UML Sequence Diagram
<img width="1024" height="1024" alt="Login Microservice UML Diagram" src="https://github.com/user-attachments/assets/50aeae50-8d76-448a-8f1a-4ddc19514e5a" />

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

1. Run the receiver service (run this first before suggestion.py):
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

### UML Sequence Diagram
![Suggestion Microservice](suggestion-microservice-UML.png)

# Contributions
**Dylan**: Developed the REQUEST and RECEIVE services for the CSV Report Generator Microservice and the Suggestion Microservice.

**Yasser**: Created UML diagram for CSV Report Generator Microservice, tested and created video demo for the CSV Report Generator Microservice.

**Thayer**: Created the REQUEST and RECEIVE services for the Login Microservice, updated README for Login Microservice.

**Sid**: Created UML diagram for Login Microservice, tested and created video demo for the Login Microservice, and updated README for Login Microservice.

**Kylee**: Created UML diagram for Suggestion Microservice and created video demonstration for Suggestion Microservice.

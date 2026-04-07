---
name: google-sheets-editing
description: Fast programmatic editing of Google Sheets via gspread API. Use when creating or editing shared Google Sheets, adding dropdowns, conditional formatting, or any spreadsheet work. Triggers on "Google Sheets", "shared document", "shared spreadsheet", "tracker sheet", "gspread".
---

# Google Sheets Editing via gspread

## Why This Exists

Editing Google Sheets through Playwright (clicking menus, typing into cells) is extremely slow. Instead, use the `gspread` Python library to make edits programmatically in seconds.

## New Computer Setup

When working on a new computer for the first time:

1. Install the Python libraries:
   ```
   pip install gspread google-auth google-auth-oauthlib
   ```
2. Copy the service account key file `brain-based-mental-health-60cf6761995a.json` into the project root. This file is gitignored for security, so it must be transferred manually (e.g. USB drive, secure file share, or download from Google Cloud Console > IAM > Service Accounts > Keys).

### Required Libraries
- `gspread`
- `google-auth`
- `google-auth-oauthlib`

### Service Account
- **JSON key file:** `brain-based-mental-health-60cf6761995a.json` (in project root, gitignored)
- **Service account email:** `tcfasd@brain-based-mental-health.iam.gserviceaccount.com`
- **Google Cloud project:** `498429460821`
- **APIs enabled:** Google Sheets API, Google Drive API

### Security
- The service account can ONLY access sheets explicitly shared with its email
- It cannot browse, see, or access anything else on the user's Google Drive
- The JSON key file is gitignored — never commit it

## How to Connect

```python
import gspread
from google.oauth2.service_account import Credentials

scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('brain-based-mental-health-60cf6761995a.json', scopes=scopes)
gc = gspread.authorize(creds)

# Open by key (from the URL)
sheet = gc.open_by_key('SPREADSHEET_ID').sheet1
```

## Common Operations

### Read all data
```python
data = sheet.get_all_values()
```

### Write to cells
```python
sheet.update(values=[['Hello', 'World']], range_name='A1:B1')
```

### Formatting (via batch_update)
```python
requests = [{
    'repeatCell': {
        'range': {'sheetId': 0, 'startRowIndex': 0, 'endRowIndex': 1, 'startColumnIndex': 0, 'endColumnIndex': 5},
        'cell': {'userEnteredFormat': {'backgroundColor': {'red': 0.357, 'green': 0.478, 'blue': 0.416}}},
        'fields': 'userEnteredFormat.backgroundColor'
    }
}]
spreadsheet.batch_update({'requests': requests})
```

### Data validation (dropdowns)
```python
requests = [{
    'setDataValidation': {
        'range': {'sheetId': 0, 'startRowIndex': 2, 'endRowIndex': 6, 'startColumnIndex': 4, 'endColumnIndex': 5},
        'rule': {
            'condition': {'type': 'ONE_OF_LIST', 'values': [{'userEnteredValue': v} for v in ['--', 'Sent', 'In Progress', 'Received', 'Finalized']]},
            'showCustomUi': True, 'strict': True
        }
    }
}]
spreadsheet.batch_update({'requests': requests})
```

### Conditional formatting
```python
requests = [{
    'addConditionalFormatRule': {
        'rule': {
            'ranges': [{'sheetId': 0, 'startRowIndex': 2, 'endRowIndex': 6, 'startColumnIndex': 0, 'endColumnIndex': 5}],
            'booleanRule': {
                'condition': {'type': 'CUSTOM_FORMULA', 'values': [{'userEnteredValue': '=$E3="Sent"'}]},
                'format': {'backgroundColor': {'red': 1.0, 'green': 0.973, 'blue': 0.882}}
            }
        },
        'index': 0
    }
}]
spreadsheet.batch_update({'requests': requests})
```

## Known Shared Sheets

| Sheet | ID | Purpose |
|---|---|---|
| Feedback Task Tracker | `1jeaJ4VTYqXjxvbJ8L2CZsGfLK4ni4SkWc0WZjBEpx7k` | Track feedback status across reviewers |

## Sharing a New Sheet with the Service Account

For any new Google Sheet the user wants me to edit:
1. Open the sheet in Google
2. Click Share
3. Add `tcfasd@brain-based-mental-health.iam.gserviceaccount.com` as Editor
4. Uncheck "Notify people"
5. Click Share

## Workflow

1. **Always use gspread** for Google Sheets work — never Playwright
2. Read current data first to understand the layout
3. Make edits via API calls
4. Confirm changes by reading back the data

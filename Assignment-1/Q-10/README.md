# Q10 - Tkinter Assignment Tracker with File Persistence

## Problem

Create a Tkinter GUI application to manage student assignment
submissions.

The application supports:

- Adding students
- Adding assignment submissions
- Updating marks
- Filtering pending/completed assignments
- Exporting CSV reports
- JSON file persistence
- Input validation

## File

12402080601054_Assignment1_Q10.py

## Requirements

- Python 3.10 or above
- Tkinter
- JSON
- CSV

No external packages are required.

## Run

python 12402080601054_Assignment1_Q10.py

## Data File

The program stores data in:

assignment_data.json

The file is automatically created when data is saved.

## CSV Report

The application can export:

- Enrollment
- Name
- Assignment
- Status
- Marks
- Remarks

## GUI Widgets

The application uses:

- Label
- Entry
- Button
- Combobox
- Treeview
- Scrollbar
- LabelFrame

## Main Features

### Add Student

Adds a student using enrollment number and name.

### Add Submission

Adds an assignment, marks, status and remarks.

### Update Marks

Updates marks of a selected submission.

### Filtering

Records can be filtered by:

- All
- Pending
- Completed

### CSV Export

All assignment records can be exported to a CSV file.

### Persistence

Student and submission data is stored locally
using JSON.

## Validation

The program validates:

- Enrollment number
- Student name
- Assignment name
- Marks
- Duplicate students
- Existing students
- File operations

## Complexity

Filtering:
O(r)

CSV generation:
O(r)

Space:
O(r)

where r is the number of assignment records.

## Testing

The program should be tested with:

1. Normal student addition
2. Duplicate enrollment
3. Invalid enrollment
4. Assignment submission
5. Pending assignment
6. Completed assignment
7. Marks update
8. Filtering
9. CSV export
10. JSON persistence

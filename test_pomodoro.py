import pytest
import project as app
 
 
# Test written data matches with the read data
def test_save_tasks(tmp_path):
    # Point the FILE NAME to save at pytest temporary test folder
    app.FILE_NAME = tmp_path / "tasks.csv"
 
    # Create test data with 2 tasks
    app.tasks = [
        {"Task": "Write Test Functions", "Focus": 25, "Rest": 10, "Status": "done"},
        {"Task": "Run Tests", "Focus": 5, "Rest": 0, "Status": "ongoing"},
    ]
 
    # Write tasks to csv file
    app.save_tasks()
 
    # Read them
    tasks = app.load_tasks()
 
    # Check if values are correct
    assert tasks[0]["Task"] == "Write Test Functions"
    assert tasks[1]["Task"] == "Run Tests"
    assert tasks[0]["Focus"] == 25
    assert tasks[1]["Focus"] == 5
    assert tasks[0]["Rest"] == 10
    assert tasks[1]["Rest"] == 0
    assert tasks[0]["Status"] == "done"
    assert tasks[1]["Status"] == "ongoing"
 
 
# Test FileNotFoundError is raised when there is no file yet
def test_load_tasks(tmp_path):
    app.FILE_NAME = tmp_path / "does_not_exist.csv"

    with pytest.raises(FileNotFoundError):
        app.load_tasks()

# Test only ongoing tasks with focus minutes above 0 can rest
def test_restable_tasks():
    app.tasks = [
        {"Task": "A", "Focus": 25, "Rest": 0, "Status": "done"},
        {"Task": "B", "Focus": 0, "Rest": 0, "Status": "ongoing"},
        {"Task": "C", "Focus": 25, "Rest": 0, "Status": "ongoing"},
    ]

    names = [task["Task"] for task in app.restable_tasks()]
    assert names == ["C"]
# Chiikawa Pomodoro CLI

#### Description:

Chiikawa Pomodoro CLI is a terminal app that combines a to-do list with a Pomodoro timer, themed around Chiikawa, the hamster character from the anime Chiikawa. The Pomodoro technique splits work into a focus block (25 minutes here) followed by a short rest (5 minutes). With the app, the user can add up to five tasks, run a focus session on a task, take a rest after it, mark tasks as done, and see a summary of the focus and rest minutes for each task. Everything is saved to a CSV file, so the user's tasks and minutes are still there the next time the program starts.

When it starts, the program shows Chiikawa ASCII art and the main menu. The user moves with the arrow keys and presses Enter to choose one of seven options:

1. Add tasks
2. Remove tasks
3. Show a summary
4. Start a focus session
5. Start a rest session
6. Mark tasks done
7. Quit

Every screen shows a "back to menu (enter)" hint, and pressing Enter on an empty line takes the user back to the main menu. When a timer finishes, a desktop notification with the Chiikawa icon pops up, so the user can look away from the terminal while working.

## Installation & Set Up

### Requirements

- Python 3.14 or later
- questionary
- notify-py
- tabulate
- pytest

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/bibib4p/chiikawa-pomodoro-cli.git
   cd chiikawa-pomodoro-cli
   ```

2. Install the required libraries:

   ```
   pip install -r requirements.txt
   ```

### Running the Program

```
python pomodoro.py
```

### Running the Tests

```
pytest test_pomodoro.py
```

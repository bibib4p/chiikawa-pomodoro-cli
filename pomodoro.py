import time, sys, os, csv
import questionary
from notifypy import Notify
from tabulate import tabulate

actions = {
    1: "Add tasks",
    2: "Remove tasks",
    3: "Show Summary",
    4: "Start a 25 min focus session",
    5: "Start a 5 min rest session",
    6: "Mark tasks done",
    7: "Quit",
}

ICON_PATH = "pomodoro_icon.jpg"
FILE_NAME = "tasks.csv"

MAX_TASK = 5
FOCUS_MINUTES = 25
REST_MINUTES = 5

# Column labels for the CSV file
COLUMNS = ["Task", "Focus", "Rest", "Status"]

# Each task is a dictionary
tasks = []


def main():
    # Declare as global for reassignment
    global tasks

    # Try loading tasks from existing file
    try:
        # Reassigns tasks
        tasks = load_tasks()

    # Catch Error for First Time, file does not exist
    except FileNotFoundError:
        pass

    # Ctrl + C or Ctrl + D, quits whole program
    try:
        while True:
            clear_screen()
            show_menu()
            choice = ask_choice()
            clear_screen()
            # Hint is shown once at the top of every action
            show_back_hint()
            match choice:
                case 1:
                    if len(tasks) < MAX_TASK:
                        add_tasks()
                    else:
                        print(f"You reached the task limit of {MAX_TASK}.")
                        pause()
                case 2:
                    if tasks:
                        remove_tasks()
                    else:
                        print("No tasks yet.")
                        pause()
                case 3:
                    if tasks:
                        show_summary()
                    else:
                        print("No tasks yet.")
                    pause()
                case 4:
                    if has_ongoing():
                        start_focus_session()
                    else:
                        print("Add tasks first to focus on them.")
                        pause()
                case 5:
                    if not has_ongoing():
                        print("Add tasks first to focus on them.")
                        pause()
                    elif not restable_tasks():
                        print("Do a focus session first.")
                        pause()
                    else:
                        start_rest_session()
                case 6:
                    if has_ongoing():
                        mark_tasks_done()
                    else:
                        print("No ongoing tasks to mark.")
                        pause()
                case 7:
                    quit()
            save_tasks()

    except (KeyboardInterrupt, EOFError):
        quit()


"""-------------------------------------------------- HELPER FUNCTIONS --------------------------------------------------"""


# Save tasks to CSV File
def save_tasks():
    with open(FILE_NAME, "w") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(tasks)


# Load tasks from CSV File
def load_tasks():
    with open(FILE_NAME) as file:
        loaded = list(csv.DictReader(file))

    # Everything in a CSV is text, so Focus and Rest are turned back into numbers
    for task in loaded:
        task["Focus"] = int(task["Focus"])
        task["Rest"] = int(task["Rest"])
    return loaded


# Quit Program
def quit():
    # Save when user quit the program with Ctrl + C/ Ctrl + D
    save_tasks()

    # For . . . animation
    print("\nQuitting", end=" ")
    for i in range(3):
        print(".", end=" ", flush=True)
        time.sleep(0.5)
    print("\n")
    sys.exit()


# Check if user pressed Enter on an empty line. Returns True for yes, False for no
def cancel(text):
    return text == ""


# Prints the "back to menu" hint
def show_back_hint():
    print("\nback to menu (enter)\n")


# Clears the terminal screen
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# Waits for Enter so the user can read the result before the menu comes back
def pause():
    print()
    input()


# Tasks that are not done yet
def ongoing_tasks():
    return [task for task in tasks if task["Status"] == "ongoing"]


# Only ongoing tasks that already have focus minutes can take a rest
def restable_tasks():
    return [task for task in ongoing_tasks() if task["Focus"] > 0]


# Shows a table of the given tasks, numbered 1, 2, 3... in the order they are shown
def show_tasks(shown):
    rows = [[number, task["Task"]] for number, task in enumerate(shown, start=1)]
    print("Ongoing Task")
    print(tabulate(rows, headers=["No.", "Task"], tablefmt="pretty"))
    print()


# Check if there is at least 1 ongoing task. Returns True for yes, False for no
def has_ongoing():
    # any() is True if at least one task is ongoing
    return any(task["Status"] == "ongoing" for task in tasks)


# Ask a y/n question until user answers properly. Returns True for yes, False for no
def ask_yes_no(question):
    answer = input(question + " (y/n) ").strip().lower()
    while answer not in ["y", "yes", "n", "no"]:
        print("Please enter y or n")
        answer = input(question + " (y/n) ").strip().lower()
    return answer in ["y", "yes"]


# Alerts user with a popup notification
def alert(session_type):
    # Different message depending on session type
    if session_type == "Focus":
        title = "Focus session done!"
        message = "Time to take a break"
    else:
        title = "Rest is over!"
        message = "Time to get back to focus"

    noti = Notify()
    noti.title = title
    noti.message = message
    noti.application_name = "Pomodoro"
    noti.icon = str(ICON_PATH)
    noti.send()


"""-------------------------------------------------- MAIN ACTION FUNCTIONS --------------------------------------------------"""


def show_menu():
    print(r"""
                               ⢀⣀⣀⡀
                ⣀⣤⣤⣤⣴⣦⣶⣴⣦⣦⣤⣤⣤⣰⣿⠟⠉⠙⣷
       ⢀⣤⡴⢶⣦⣤⣴⣾⠿⠛⠛⠋⠉⠉⠁      ⠈⠉⠋  ⣠⣿⠁
       ⣿⡟  ⠘⣿⡟                   ⠛⠻⢧⣄⡀
       ⢿⣄⡀  ⠈                       ⠈⠻⣦⡄
     ⢀⣤⠆⠉⠉                            ⠈⢿⣦
    ⣠⡿⠁                        ⣀⡀       ⢻⣷⡀
   ⣴⡟              ⢀⣠⠤          ⠈⠓       ⢻⣧
  ⣸⡿              ⠠⠏                     ⠈⣿⡆
 ⢰⣿⠃                           ⢀⡴⢶⣤⡀      ⢸⡇
 ⢸⡟                ⣠⡤⢤⣄        ⣿⣅⣀⣸⣷ ⢀⣀⡀  ⢸⡇
 ⢸⡇               ⣼⣏ ⢀⣹⡇       ⢿⣯⣭⠾⠋⣴ ⣴⢀⡠ ⣸⡇
 ⢸⡇            ⢀ ⢀⢻⣿⣟⣫⡽⠁   ⢀        ⡟ ⠿⠈⠗⢀⣿⠃
 ⠘⣷⡀        ⢀⢀⣤ ⣤ ⣰⡆⠈    ⣤⣤⠾⢦⡴⠂      ⠒⠂⠁⢀⣾⠇
⢠⣶⠿⣧⡀        ⢸⡇⠸⡟ ⠙⠱     ⢸⣇⣀⡾      ⢀⣠⣄⡀⣀⣾⠋
⣿⡇⢠⣿⣷⡄       ⠠⠅ ⠠ ⠈       ⢩⡭       ⣿⠋⠉⢻⡟
⠘⠷⣼⣿⠈⠻⢦⡀         ⣠⡶⢶⣤              ⠛⠂⢀⣼⡇
  ⠸⣿⡄            ⠏  ⣿⡇             ⢺⡿⠟⠉
   ⢻⣿⡀            ⠰⠾⠛             ⣴⡿⠁
    ⢻⣿⣦                         ⢠⣾⡟                                     __
     ⠙⠻⣷⣄                    ⣀⣤⣾⠟⠋       .-----.-----.--------.-----.--|  |.-----.----.-----.
       ⠈⠙⠿⣶⣤⣀⡀       ⢀⣀⣀⣀ ⣠⣴⠾⠛⠉          |  _  |  _  |        |  _  |  _  ||  _  |   _|  _  |
           ⠉⠙⠛⠛⠲⣶ ⠘⢿⣟⠛⠛⢿⣯⣤⣾⠇             |   __|_____|__|__|__|_____|_____||_____|__| |_____|
                ⠙⠳⠶⠾⠃   ⠈⠁               |__|
    """)


def ask_choice():
    # Each option shows the action text on screen but returns its number
    choices = [questionary.Choice(title=text, value=number) for number, text in actions.items()]

    # unsafe_ask lets Ctrl + C raise KeyboardInterrupt, so main() still quits and saves properly
    return questionary.select(
        "˗ˏˋ MAIN MENU ˎˊ˗\n", choices=choices, qmark="", pointer="♡", instruction=" "
    ).unsafe_ask()


def add_tasks():
    while len(tasks) < MAX_TASK:
        task = input("Enter a task: ").strip()
        if cancel(task):
            break

        # Focus and Rest Time are added as 0 for default
        tasks.append({"Task": task, "Focus": 0, "Rest": 0, "Status": "ongoing"})

        if len(tasks) == MAX_TASK:
            print(f"You reached the task limit of {MAX_TASK}.")
            pause()
            break

        # Asks user if they want to add more
        if not ask_yes_no("Do you wish to add another task?"):
            break


def remove_tasks():
    while tasks:
        rows = [[number, task["Task"], task["Status"]] for number, task in enumerate(tasks, start=1)]
        print(tabulate(rows, headers=["No.", "Task", "Status"], tablefmt="pretty"))
        print()

        text = input("Enter task number to remove (or 'all' to remove every task): ").strip().lower()
        if cancel(text):
            break

        if text == "all":
            if ask_yes_no(f"Remove all {len(tasks)} task(s)?"):
                tasks.clear()
                print("Removed all tasks.")
                pause()
                break
            continue

        try:
            number = int(text)
        except ValueError:
            print("Please enter a number!")
            continue

        # Check valid task number
        if not 1 <= number <= len(tasks):
            print("Please enter a valid task number!")
            continue

        # List positions start at 0, task numbers at 1
        del tasks[number - 1]

        # Asks user if they want to remove more
        if tasks and not ask_yes_no("Remove another task?"):
            break


def mark_tasks_done():
    # Rebuilt every loop so the numbers stay 1, 2, 3... after a task is marked done
    while has_ongoing():
        shown = ongoing_tasks()
        show_tasks(shown)
        text = input("Enter task number to mark done: ").strip()
        if cancel(text):
            break

        try:
            number = int(text)
        except ValueError:
            print("Please enter a number!")
            continue

        # Check valid task number
        if not 1 <= number <= len(shown):
            print("Please enter a valid task number!")
            continue

        # Update status to "done"
        task = shown[number - 1]
        task["Status"] = "done"
        print(f"Marked as done: {task['Task']}")

        # Pause so the message can be read
        if not has_ongoing():
            pause()
            break

        # Asks user if they want to mark done more. Continue loop for yes
        if not ask_yes_no("Mark another task as done?"):
            break


def start_focus_session():
    shown = ongoing_tasks()
    show_tasks(shown)
    while True:
        text = input("Enter task number to focus on: ").strip()
        if cancel(text):
            break

        try:
            number = int(text)
        except ValueError:
            print("Please enter a number!")
            continue

        # Check valid task number
        if not 1 <= number <= len(shown):
            print("Please enter a valid task number!")
            continue

        # Add the minutes the timer returns to this task's Focus value
        task = shown[number - 1]
        task["Focus"] += timer(task["Task"], FOCUS_MINUTES, "Focus")
        pause()

        break


def start_rest_session():
    # Only ongoing tasks that already have focus minutes
    shown = restable_tasks()
    show_tasks(shown)
    while True:
        text = input("Enter task number to start resting: ").strip()
        if cancel(text):
            break

        try:
            number = int(text)
        except ValueError:
            print("Please enter a number!")
            continue

        # Check valid task number
        if not 1 <= number <= len(shown):
            print("Please enter a valid task number!")
            continue

        task = shown[number - 1]
        if task["Focus"] < FOCUS_MINUTES:
            print(f"Please do a focus session of {FOCUS_MINUTES} mins first.\n")
            continue

        # Add the minutes the timer returns to this task's Rest value
        task["Rest"] += timer(task["Task"], REST_MINUTES, "Rest")
        pause()

        break


def timer(task, total_minutes, session_type):
    print("-------------------------------------")
    # Turn minutes to seconds for count down
    total_seconds = total_minutes * 60

    # When session is stopped early
    try:
        # Keep looping till time/ seconds turn to 0
        while total_seconds > 0:

            # Calculating leftover minutes and seconds
            minutes = total_seconds // 60
            seconds = total_seconds % 60

            print(f"{task} | {minutes:02d}:{seconds:02d}", end="\r", flush=True)

            time.sleep(1)
            total_seconds -= 1
        alert(session_type)

    except (KeyboardInterrupt, EOFError):
        print("\nSession stopped early.\n")

    # Calculate whole minutes completed (unfinished minute is ignored)
    minutes_done = min((total_minutes * 60 - total_seconds) // 60, total_minutes)

    if minutes_done > 0:
        print(f"\nYou {session_type.lower()}ed for a total of {minutes_done} min\n")

    return minutes_done


def show_summary():
    rows = [
        [number, task["Task"], task["Focus"], task["Rest"], task["Status"]]
        for number, task in enumerate(tasks, start=1)
    ]
    print(tabulate(rows, headers=["No.", "Task", "Focus", "Rest", "Status"], tablefmt="pretty"))


if __name__ == "__main__":
    main()
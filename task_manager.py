import json
import os
from datetime import datetime

# file to store tasks
TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from file"""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """Save tasks to file"""
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def display_menu():
    """Display main menu"""
    print("\n" + "="*50)
    print("       PERSONAL TASK MANAGER")
    print("\nStay organized and track your daily tasks!")
    print("\nWhat would you like to do?")
    print("\n 1. Add a new task")
    print(" 2. View all tasks")
    print(" 3. Mark task as complete")
    print(" 4. Help & Instructions")
    print(" 5. Exit")
    print("\nTip: Type 'help' at any time for assistance")
    print("-"*50)

def add_task(tasks):
    """Add a new task"""
    print("\n" + "="*50)
    print("       ADD NEW TASK")
    print("="*50)
    print("\nEnter your task description below.")
    print("-"*50)

    description = input("\nTask description: ").strip()

    if description.lower() == 'help':
        show_help()
        return add_task(tasks) # Go back to the add_task prompt

    elif description.lower() == 'cancel':
        print("\nReturning to menu...")
        return

    if not description:
        print("\n ERROR: Task description cannot be empty!")
        print("Please try again.")
        input("\nPress Enter to continue...")
        return add_task(tasks)

    task = {
        "id": len(tasks) + 1,
        "description": description,
        "complete": False,
        "date_added": datetime.now().strftime("%B %d, %Y")
    }

    tasks.append(task)
    save_tasks(tasks)

    print("\n TASK ADDED SUCCESSFULLY!")
    print(f"\nWhat would you like to do next?")
    print(" 1. Add another task")
    print(" 2. View all tasks")
    print(" 3. Return to main menu")

    choice = input("\nEnter your choice (1-3): ").strip()

    if choice == '1':
        add_task(tasks)
    elif choice == '2':
        view_tasks(tasks)
    else:
        return

def view_tasks(tasks):
    """View all tasks"""
    print("\n" + "="*50)
    print("       YOUR TASK LIST")
    print("="*50)

    if not tasks:
        print("\nYou currently have no tasks.")
        print("\nGet started by adding a task!")
        print("\nWhat would you like to do?")
        print(" 1. Add a task")
        print(" 2. Return to Main Menu")

        choice = input("\nEnter your choice (1-2): ").strip()
        if choice == '1':
            add_task(tasks)
        return

    incomplete = [t for t in tasks if not t['complete']]
    complete = [t for t in tasks if t['complete']]

    print(f"\nYou have {len(tasks)} tasks ({len(complete)} completed, {len(incomplete)} incomplete)")
    print("-"*50)

    if incomplete:
        print("\nINCOMPLETE TASKS:")
        for task in incomplete:
            print(f" {task['id']}. {task['description']}")

    if complete:
        print("\nCOMPLETED TASKS:")
        for task in complete:
            print(f" {task['id']}. {task['description']}")

    print("\n" + "="*50)
    print("\nOPTIONS:")
    print(" - Enter task number for details")
    print(" - Type 'menu' to return to Main Menu")

    choice = input("\nYour choice: ").strip()

    if choice.lower() == 'menu':
        return

    if choice.isdigit():
        task_id = int(choice)
        show_task_details(tasks, task_id)

def show_task_details(tasks, task_id):
    """Show details for a specific task"""
    task = next((t for t in tasks if t['id'] == task_id), None)

    if not task:
        print("\nERROR: Invalid task number")
        input("\nPress Enter to continue...")
        return view_tasks(tasks)

    print("\n" + "="*50)
    print("       TASK DETAILS")
    print("="*50)
    print(f"\nTask #{task['id']}")
    print(f"\nDescription: {task['description']}")
    print(f"Status:       {'Complete' if task['complete'] else 'Incomplete'}")
    print(f"Date Added:   {task['date_added']}")
    print("\n" + "="*50)
    print("\nACTIONS:")
    print(" 1. Mark as complete")
    print(" 2. View all tasks")
    print(" 3. Return to Main Menu")

    choice = input("\nEnter your choice (1-3): ").strip()

    if choice == '1':
        mark_complete_direct(tasks, task_id)
    elif choice == '2':
        view_tasks(tasks)
    else:
        return

def mark_complete(tasks):
    """Mark a task as complete"""
    print("\n" + "="*50)
    print("       MARK TASK AS COMPLETE")
    print("="*50)

    incomplete = [t for t in tasks if not t['complete']]

    if not incomplete:
        print("\nYou have no incomplete tasks!")
        input("\nPress Enter to return to menu...")
        return

    print("\nCurrent incomplete tasks:")
    for task in incomplete:
        print(f"  {task['id']}. {task['description']}")

    print("\n" + "="*50)
    choice = input("\nWhich task did you complete? (or 'cancel'): ").strip()

    if choice.lower() == 'help':
        show_help()
        return mark_complete(tasks) # Go back to the mark_complete prompt

    elif choice.lower() == 'cancel':
        print("\nReturning to menu...")
        return

    if not choice.isdigit():
        print("\nERROR: Please enter a valid task number")
        input("\nPress Enter to try again...")
        return mark_complete(tasks)

    task_id = int(choice)
    mark_complete_direct(tasks, task_id)

def mark_complete_direct(tasks, task_id):
    """Confirm and mark task complete"""
    task = next((t for t in tasks if t['id'] == task_id), None)

    if not task:
        print("\nERROR: Invalid task number:")
        input("\nPress Enter to continue...")
        return

    if task['complete']:
        print("\nThis task is already complete!")
        input("\nPress Enter to continue...")
        return

    print("\n" + "="*50)
    print("       CONFIRM ACTION")
    print("="*50)
    print(f"\nYou selected: ")
    print(f"  Task #{task['id']}: '{task['description']}")
    print("\n" + "-"*50)
    print("\nMark this task as complete?")
    print("\nNote: Completed tasks will be moved to your")
    print("'Completed' list. You can still view them later.")
    print("-"*50)

    confirm = input("\nAre you sure? (y/n): ").strip().lower()

    if confirm == 'y':
        task['complete'] = True
        save_tasks(tasks)

        print("\n" + "="*50)
        print("        TASK MARKED AS COMPLETE!")
        print("="*50)
        print(f"\n'{task['description']}' has been marked as complete.")
        print("\nGreat job! Keep up the good work!")
        print("\nWhat would you like to do next?")
        print(" 1. Mark another task complete")
        print(" 2. View all tasks")
        print(" 3. Return to Main Menu")

        choice = input("\nEnter your choice (1-3): ")

        if choice == '1':
            mark_complete(tasks)
        elif choice == '2':
            view_tasks(tasks)
    else:
        print("\nAction cancelled.")
        input("/nPress Enter to return to menu...")

def show_help():
    """Show help and instructions"""
    print("\n" + "="*50)
    print("       HELP & INSTRUCTIONS")
    print("="*50)
    print("\nHOW TO USE TASK MANAGER:")
    print("\nADDING A TASK")
    print(" 1. Select 'Add a new task' from the main menu")
    print(" 2. Enter you task description")
    print(" 3. Press ENTER to save")
    print("\nVIEWING YOUR TASKS")
    print(" 1. Select 'View all tasks' from the main menu")
    print(" 2. Enter the number of the task you finished")
    print(" 3. Confirm your selection")
    print("\n" + "-"*50)
    print("\nTIPS:")
    print(" - Type 'menu' anytime to return to main menu")
    print(" - Type 'cancel' to go back without saving")
    print(" - All tasks are saved automatically")

    input("\nPress any key to return...")

def main():
    """Main program loop"""
    tasks = load_tasks()

    while True:
        display_menu()
        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            mark_complete(tasks)
        elif choice == '4' or choice.lower() == 'help':
            show_help()
        elif choice == '5':
            print("\nThank you for using Task Manager!")
            print("Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter 1-5.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()

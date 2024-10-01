import json
import os
import tkinter as tk
from tkinter import messagebox

# Common Functions (shared between CLI and GUI)
def load_tasks():
    """Load tasks from the shared data file."""
    data_path = os.path.join(os.path.dirname(__file__), 'tasks.json')
    try:
        with open(data_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    """Save tasks to the shared data file."""
    data_path = os.path.join(os.path.dirname(__file__), 'tasks.json')
    with open(data_path, 'w') as file:
        json.dump(tasks, file, indent=4)

# CLI Version Functions
def add_task_cli(tasks, description, priority="Low"):
    tasks.append({'description': description, 'completed': False, 'priority': priority})
    save_tasks(tasks)

def view_tasks_cli(tasks):
    if not tasks:
        print("No tasks available!")
        return
    for idx, task in enumerate(tasks, start=1):
        status = "✔" if task['completed'] else "✘"
        print(f"{idx}. [{status}] {task['description']} (Priority: {task['priority']})")

def complete_task_cli(tasks, task_id):
    tasks[task_id - 1]['completed'] = True
    save_tasks(tasks)

def delete_task_cli(tasks, task_id):
    tasks.pop(task_id - 1)
    save_tasks(tasks)

def run_cli():
    tasks = load_tasks()
    while True:
        print("\nTo-Do List App (CLI)")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Quit")

        choice = input("Choose an option: ")

        if choice == '1':
            description = input("Enter task description: ")
            priority = input("Enter priority (Low, Medium, High): ")
            add_task_cli(tasks, description, priority)
        elif choice == '2':
            view_tasks_cli(tasks)
        elif choice == '3':
            task_id = int(input("Enter task number to complete: "))
            complete_task_cli(tasks, task_id)
        elif choice == '4':
            task_id = int(input("Enter task number to delete: "))
            delete_task_cli(tasks, task_id)
        elif choice == '5':
            print("Exiting CLI...")
            break
        else:
            print("Invalid option. Please try again.")

# GUI Version Functions
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App (GUI)")
        self.tasks = load_tasks()

        # Create UI elements
        self.task_entry = tk.Entry(self.root, width=40)
        self.task_entry.pack(pady=10)

        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task_gui)
        self.add_button.pack(pady=5)

        self.task_listbox = tk.Listbox(self.root, width=50, height=10)
        self.task_listbox.pack(pady=10)
        self.update_task_listbox()

        self.complete_button = tk.Button(self.root, text="Complete Task", command=self.complete_task_gui)
        self.complete_button.pack(pady=5)

        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task_gui)
        self.delete_button.pack(pady=5)

    def update_task_listbox(self):
        """Update the listbox with the current tasks."""
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✔" if task['completed'] else "✘"
            self.task_listbox.insert(tk.END, f"{task['description']} [{status}]")

    def add_task_gui(self):
        """Add a task in the GUI."""
        task_desc = self.task_entry.get()
        if task_desc:
            self.tasks.append({'description': task_desc, 'completed': False})
            save_tasks(self.tasks)
            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Task description cannot be empty")

    def complete_task_gui(self):
        """Mark a selected task as completed."""
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            self.tasks[selected_task_index[0]]['completed'] = True
            save_tasks(self.tasks)
            self.update_task_listbox()
        else:
            messagebox.showwarning("Selection Error", "No task selected")

    def delete_task_gui(self):
        """Delete a selected task."""
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            del self.tasks[selected_task_index[0]]
            save_tasks(self.tasks)
            self.update_task_listbox()
        else:
            messagebox.showwarning("Selection Error", "No task selected")

def run_gui():
    """Initialize the GUI version of the app."""
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()

# Main Program
def main():
    print("Welcome to the To-Do List App")
    print("1. Command-Line Interface (CLI)")
    print("2. Graphical User Interface (GUI)")
    
    choice = input("Choose an option (1 or 2): ")
    
    if choice == '1':
        run_cli()
    elif choice == '2':
        run_gui()
    else:
        print("Invalid choice. Please restart the program and choose either 1 or 2.")

if __name__ == "__main__":
    main()

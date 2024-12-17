import tkinter as tk
from tkinter import messagebox

# Data storage (mock database)
users = {}  # username: {'password': str, 'role': str}
quizzes = []  # List of quizzes with {'question': str, 'answer': str}
scores = {}  # username: {'quiz': score}

# Color palette
BG_LIGHT = "#F7F7FF"
TEXT_COLOR = "#FFFFFF"
BUTTON_TEXT_COLOR = "#FFFFFF"
BG_MAIN = "#F6F5F5"
BG_HEADER = "#EE99C2"
BG_ACCENT = "#FFE3CA"
TEXT_COLOR = "#0C359E"
BUTTON_TEXT_COLOR = "#0C359E"

# Fonts
HEADER_FONT = ("Arial", 18, "bold")
LABEL_FONT = ("Arial", 12)
BUTTON_FONT = ("Arial", 14, "bold")

# Functions
def register_user():
    def submit_registration():
        username = username_entry.get()
        password = password_entry.get()
        role = role_var.get()

        if username in users:
            messagebox.showerror("Error", "Username already exists!")
        elif not username or not password or not role:
            messagebox.showerror("Error", "All fields are required!")
        else:
            users[username] = {'password': password, 'role': role}
            scores[username] = {}
            messagebox.showinfo("Success", "Registration successful!")
            register_window.destroy()

    register_window = tk.Toplevel(root)
    register_window.title("Register")
    register_window.geometry("400x400")
    register_window.configure(bg=BG_MAIN)

    tk.Label(register_window, text="Register", bg=BG_MAIN, font=HEADER_FONT, fg=TEXT_COLOR).pack(pady=10)

    tk.Label(register_window, text="Username:", bg=BG_MAIN, font=LABEL_FONT, fg=TEXT_COLOR).pack(pady=5)
    username_entry = tk.Entry(register_window, font=LABEL_FONT, bg=BG_LIGHT)
    username_entry.pack(pady=5)

    tk.Label(register_window, text="Password:", bg=BG_MAIN, font=LABEL_FONT, fg=TEXT_COLOR).pack(pady=5)
    password_entry = tk.Entry(register_window, show="*", font=LABEL_FONT, bg=BG_LIGHT)
    password_entry.pack(pady=5)

    tk.Label(register_window, text="Role:", bg=BG_MAIN, font=LABEL_FONT, fg=TEXT_COLOR).pack(pady=5)
    role_var = tk.StringVar()
    tk.Radiobutton(register_window, text="Teacher", variable=role_var, value="teacher", bg=BG_MAIN, font=LABEL_FONT, fg=TEXT_COLOR, selectcolor=BG_LIGHT).pack()
    tk.Radiobutton(register_window, text="Student", variable=role_var, value="student", bg=BG_MAIN, font=LABEL_FONT, fg=TEXT_COLOR, selectcolor=BG_LIGHT).pack()

    tk.Button(register_window, text="Register", command=submit_registration, font=BUTTON_FONT, bg=BG_ACCENT, fg=BUTTON_TEXT_COLOR).pack(pady=10)

def login_user():
    def submit_login():
        username = username_entry.get()
        password = password_entry.get()

        if username not in users or users[username]['password'] != password:
            messagebox.showerror("Error", "Invalid username or password!")
        else:
            role = users[username]['role']
            messagebox.showinfo("Success", f"Welcome, {role.capitalize()} {username}!")
            login_window.destroy()
            if role == "teacher":
                teacher_dashboard(username)
            elif role == "student":
                student_dashboard(username)

    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("400x300")
    login_window.configure(bg=BG_MAIN)

    tk.Label(login_window, text="Login", bg=BG_MAIN, font=HEADER_FONT, fg=TEXT_COLOR).pack(pady=10)

    tk.Label(login_window, text="Username:", bg=BG_MAIN, font=LABEL_FONT, fg=TEXT_COLOR).pack(pady=5)
    username_entry = tk.Entry(login_window, font=LABEL_FONT, bg=BG_LIGHT)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password:", bg=BG_MAIN, font=LABEL_FONT, fg=TEXT_COLOR).pack(pady=5)
    password_entry = tk.Entry(login_window, show="*", font=LABEL_FONT, bg=BG_LIGHT)
    password_entry.pack(pady=5)

    tk.Button(login_window, text="Login", command=submit_login, font=BUTTON_FONT, bg=BG_ACCENT, fg=BUTTON_TEXT_COLOR).pack(pady=10)

def teacher_dashboard(username):
    def add_quiz():
        question = question_entry.get()
        answer = answer_entry.get().strip().lower()
        if not question or not answer:
            messagebox.showerror("Error", "Question and answer cannot be empty!")
        else:
            quizzes.append({'question': question, 'answer': answer})
            question_entry.delete(0, tk.END)
            answer_entry.delete(0, tk.END)
            update_quiz_list()

    def delete_quiz():
        selected = quiz_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No question selected!")
        else:
            quizzes.pop(selected[0])
            update_quiz_list()

    def update_quiz():
        selected = quiz_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No question selected!")
            return

        question = question_entry.get()
        answer = answer_entry.get().strip().lower()
        if not question or not answer:
            messagebox.showerror("Error", "Question and answer cannot be empty!")
        else:
            quizzes[selected[0]] = {'question': question, 'answer': answer}
            update_quiz_list()
            messagebox.showinfo("Success", "Quiz updated successfully!")
            question_entry.delete(0, tk.END)
            answer_entry.delete(0, tk.END)

    def update_quiz_list():
        quiz_listbox.delete(0, tk.END)
        for quiz in quizzes:
            quiz_listbox.insert(tk.END, quiz['question'])

    def view_scores():
        scores_window = tk.Toplevel(dashboard)
        scores_window.title("Student Scores")
        scores_window.geometry("400x300")
        scores_window.configure(bg=BG_LIGHT)

        tk.Label(scores_window, text="Student Scores", bg=BG_LIGHT, font=HEADER_FONT, fg=TEXT_COLOR).pack(pady=10)

        for student, score_data in scores.items():
            for quiz, score in score_data.items():
                tk.Label(scores_window, text=f"{student}: {score}/{len(quizzes)}", bg=BG_LIGHT, font=LABEL_FONT, fg=TEXT_COLOR).pack()

    dashboard = tk.Toplevel(root)
    dashboard.title(f"Teacher Dashboard - {username}")
    dashboard.geometry("600x700")
    dashboard.configure(bg=BG_HEADER)

    tk.Label(dashboard, text="Manage Quizzes", bg=BG_HEADER, font=HEADER_FONT, fg=TEXT_COLOR).pack(pady=10)

    question_entry = tk.Entry(dashboard, font=LABEL_FONT, bg=BG_LIGHT)
    answer_entry = tk.Entry(dashboard, font=LABEL_FONT, bg=BG_LIGHT)

    tk.Label(dashboard, text="Question:", bg=BG_HEADER, font=LABEL_FONT, fg=TEXT_COLOR).pack(pady=5)
    question_entry.pack(pady=5)

    tk.Label(dashboard, text="Answer:", bg=BG_HEADER, font=LABEL_FONT, fg=TEXT_COLOR).pack(pady=5)
    answer_entry.pack(pady=5)

    tk.Button(dashboard, text="Add Quiz", command=add_quiz, font=BUTTON_FONT, bg=BG_ACCENT, fg=BUTTON_TEXT_COLOR).pack(pady=5)
    tk.Button(dashboard, text="Update Quiz", command=update_quiz, font=BUTTON_FONT, bg=BG_ACCENT, fg=BUTTON_TEXT_COLOR).pack(pady=5)

    quiz_listbox = tk.Listbox(dashboard, font=LABEL_FONT, bg=BG_LIGHT)
    quiz_listbox.pack(pady=10)

    tk.Button(dashboard, text="Delete Selected Quiz", command=delete_quiz, font=BUTTON_FONT, bg=BG_ACCENT, fg=BUTTON_TEXT_COLOR).pack(pady=5)
    tk.Button(dashboard, text="View Scores", command=view_scores, font=BUTTON_FONT, bg=BG_ACCENT, fg=BUTTON_TEXT_COLOR).pack(pady=10)

def student_dashboard(username):
    def take_quiz():
        if not quizzes:
            messagebox.showinfo("No Quizzes", "No quizzes available!")
            return

        def submit_answer():
            score = 0
            for i, entry in enumerate(answer_entries):
                if entry.get().strip().lower() == quizzes[i]['answer']:
                    score += 1

            scores[username]['quiz'] = score
            messagebox.showinfo("Quiz Submitted", f"You scored {score}/{len(quizzes)}!")
            quiz_window.destroy()

        quiz_window = tk.Toplevel(dashboard)
        quiz_window.title("Take Quiz")
        quiz_window.geometry("400x300")
        quiz_window.configure(bg=BG_LIGHT)

        answer_entries = []
        for i, quiz in enumerate(quizzes):
            tk.Label(quiz_window, text=f"{i + 1}. {quiz['question']}", bg=BG_LIGHT, font=LABEL_FONT, fg=TEXT_COLOR).pack()
            entry = tk.Entry(quiz_window, font=LABEL_FONT, bg=BG_LIGHT)
            entry.pack(pady=5)
            answer_entries.append(entry)

        tk.Button(quiz_window, text="Submit", command=submit_answer, font=BUTTON_FONT, bg=BG_ACCENT, fg=BUTTON_TEXT_COLOR).pack(pady=10)

    dashboard = tk.Toplevel(root)
    dashboard.title(f"Student Dashboard - {username}")
    dashboard.geometry("600x400")
    dashboard.configure(bg=BG_HEADER)

    tk.Button(dashboard, text="Take Quiz", command=take_quiz, font=BUTTON_FONT, bg=BG_ACCENT, fg=BUTTON_TEXT_COLOR).pack(pady=10)

# Main GUI
root = tk.Tk()
root.title("Quiz System")
root.geometry("400x300")
root.configure(bg=BG_HEADER)

welcome_label = tk.Label(root, text="Welcome \n to the \n Quiz System", font=HEADER_FONT, bg=BG_HEADER, fg=TEXT_COLOR)
welcome_label.pack(pady=20)

tk.Button(root, text="Register", command=register_user, font=BUTTON_FONT, bg=BG_ACCENT, fg=BUTTON_TEXT_COLOR).pack(pady=10)

tk.Button(root, text="Login", command=login_user, font=BUTTON_FONT, bg=BG_ACCENT, fg=BUTTON_TEXT_COLOR).pack(pady=10)

root.mainloop()

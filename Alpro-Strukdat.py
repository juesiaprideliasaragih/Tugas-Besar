import tkinter as tk
from tkinter import messagebox

# Data storage (mock database)
users = {}  # username: {'password': str, 'role': str}
quizzes = []  # List of quizzes with {'question': str, 'answer': str}
scores = {}  # username: {'quiz': score}

# Color palette
BG_MAIN = "#FBB4A5"
BG_HEADER = "#FB9EC6"
BG_ACCENT = "#FFE893"
BG_LIGHT = "#FCFFC1"
TEXT_COLOR = "#34495e"

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
    register_window.geometry("400x300")
    register_window.configure(bg=BG_MAIN)

    tk.Label(register_window, text="Username:", bg=BG_MAIN, font=("Arial", 12, "bold"), fg=TEXT_COLOR).pack(pady=5)
    username_entry = tk.Entry(register_window, font=("Arial", 12))
    username_entry.pack(pady=5)

    tk.Label(register_window, text="Password:", bg=BG_MAIN, font=("Arial", 12, "bold"), fg=TEXT_COLOR).pack(pady=5)
    password_entry = tk.Entry(register_window, show="*", font=("Arial", 12))
    password_entry.pack(pady=5)

    tk.Label(register_window, text="Role:", bg=BG_MAIN, font=("Arial", 12, "bold"), fg=TEXT_COLOR).pack(pady=5)
    role_var = tk.StringVar()
    tk.Radiobutton(register_window, text="Teacher", variable=role_var, value="teacher", bg=BG_MAIN, font=("Arial", 12), fg=TEXT_COLOR, selectcolor=BG_LIGHT).pack()
    tk.Radiobutton(register_window, text="Student", variable=role_var, value="student", bg=BG_MAIN, font=("Arial", 12), fg=TEXT_COLOR, selectcolor=BG_LIGHT).pack()

    tk.Button(register_window, text="Register", command=submit_registration, font=("Arial", 12), bg=BG_ACCENT, fg=TEXT_COLOR).pack(pady=10)

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

    tk.Label(login_window, text="Username:", bg=BG_MAIN, font=("Arial", 12, "bold"), fg=TEXT_COLOR).pack(pady=5)
    username_entry = tk.Entry(login_window, font=("Arial", 12))
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password:", bg=BG_MAIN, font=("Arial", 12, "bold"), fg=TEXT_COLOR).pack(pady=5)
    password_entry = tk.Entry(login_window, show="*", font=("Arial", 12))
    password_entry.pack(pady=5)

    tk.Button(login_window, text="Login", command=submit_login, font=("Arial", 12), bg=BG_ACCENT, fg=TEXT_COLOR).pack(pady=10)

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

        tk.Label(scores_window, text="Student Scores", bg=BG_LIGHT, font=("Arial", 14, "bold"), fg=TEXT_COLOR).pack(pady=10)

        for student, score_data in scores.items():
            for quiz, score in score_data.items():
                tk.Label(scores_window, text=f"{student}: {score}/{len(quizzes)}", bg=BG_LIGHT, font=("Arial", 12)).pack()

    dashboard = tk.Toplevel(root)
    dashboard.title(f"Teacher Dashboard - {username}")
    dashboard.geometry("600x700")
    dashboard.configure(bg=BG_HEADER)

    # Create frame to hold the quiz management section
    frame = tk.Frame(dashboard, bg=BG_HEADER)
    frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Manage Quizzes:", bg=BG_HEADER, font=("Arial", 14, "bold"), fg=TEXT_COLOR).pack()

    tk.Label(frame, text="Question:", bg=BG_HEADER, font=("Arial", 12), fg=TEXT_COLOR).pack(pady=5)
    question_entry = tk.Entry(frame, width=50, font=("Arial", 12))
    question_entry.pack(pady=5)

    tk.Label(frame, text="Answer:", bg=BG_HEADER, font=("Arial", 12), fg=TEXT_COLOR).pack(pady=5)
    answer_entry = tk.Entry(frame, width=50, font=("Arial", 12))
    answer_entry.pack(pady=5)

    tk.Button(frame, text="Add Quiz", command=add_quiz, font=("Arial", 12), bg=BG_ACCENT, fg=TEXT_COLOR).pack(pady=5)
    tk.Button(frame, text="Update Quiz", command=update_quiz, font=("Arial", 12), bg=BG_ACCENT, fg=TEXT_COLOR).pack(pady=5)

    quiz_listbox = tk.Listbox(frame, width=50, font=("Arial", 12))
    quiz_listbox.pack(pady=5)
    update_quiz_list()

    tk.Button(frame, text="Delete Selected Quiz", command=delete_quiz, font=("Arial", 12), bg=BG_ACCENT, fg=TEXT_COLOR).pack(pady=5)

    # Create another frame for the "View Scores" button
    score_frame = tk.Frame(dashboard, bg=BG_HEADER)
    score_frame.pack(pady=10, fill=tk.X)

    # View Scores Button with padding to ensure it is visible
    tk.Button(score_frame, text="View Scores", command=view_scores, font=("Arial", 12), bg=BG_ACCENT, fg=TEXT_COLOR).pack(pady=15)
   
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
            tk.Label(quiz_window, text=f"{i + 1}. {quiz['question']}", bg=BG_LIGHT, font=("Arial", 12)).pack()
            entry = tk.Entry(quiz_window, font=("Arial", 12))
            entry.pack(pady=5)
            answer_entries.append(entry)

        tk.Button(quiz_window, text="Submit", command=submit_answer, font=("Arial", 12), bg=BG_ACCENT, fg=TEXT_COLOR).pack(pady=10)

    dashboard = tk.Toplevel(root)
    dashboard.title(f"Student Dashboard - {username}")
    dashboard.geometry("600x400")
    dashboard.configure(bg=BG_HEADER)

    tk.Button(dashboard, text="Take Quiz", command=take_quiz, font=("Arial", 12), bg=BG_ACCENT, fg=TEXT_COLOR).pack(pady=10)

# Main GUI
root = tk.Tk()
root.title("Quiz System")
root.geometry("600x400")
root.configure(bg=BG_HEADER)

welcome_label = tk.Label(root, text="Welcome to the Quiz System", font=("Arial", 16, "bold"), bg=BG_HEADER, fg=TEXT_COLOR)
welcome_label.pack(pady=20)

tk.Button(root, text="Register", command=register_user, font=("Arial", 12), bg=BG_ACCENT, fg=TEXT_COLOR).pack(pady=10)

tk.Button(root, text="Login", command=login_user, font=("Arial", 12), bg=BG_ACCENT, fg=TEXT_COLOR).pack(pady=10)

root.mainloop()

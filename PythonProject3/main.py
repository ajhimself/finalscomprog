import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random
import hashlib
from PIL import Image, ImageTk

# -------- DATABASE SETUP --------
DB_FILE = "sis.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create students table with password
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_number TEXT UNIQUE,
    first_name TEXT,
    middle_name TEXT,
    last_name TEXT,
    course TEXT,
    password TEXT
)
""")

# Create grades table with semester column and units
cursor.execute("""
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject_code TEXT,
    subject_desc TEXT,
    units INTEGER,
    semester TEXT,
    prelim TEXT,
    midterm TEXT,
    final_grade TEXT,
    FOREIGN KEY(student_id) REFERENCES students(id)
)
""")
conn.commit()

# -------- GRADING SYSTEM REFERENCE --------
# Philippine 1.00-Based Grading System
# GWA Calculation: Total GWA = Σ(Grade × Units) ÷ Σ(Units)

# OFFICIAL GRADE VALUES ONLY
GRADE_VALUES = [1.00, 1.25, 1.50, 1.75, 2.00, 2.25, 2.50, 2.75]

# -------- SUBJECTS BY SEMESTER --------
semester_subjects = {
    "SY 2024-2025, 1st Semester": [
        ("HI112", "READINGS IN PHILIPPINE HISTORY", 3),
        ("HU311", "ART APPRECIATION", 3),
        ("IT115", "INTRODUCTION TO COMPUTING LEC", 2),
        ("IT115L", "INTRODUCTION TO COMPUTING LAB", 1),
        ("IT116", "FUNDAMENTALS OF PROGRAMMING LEC", 2),
        ("IT116L", "FUNDAMENTALS OF PROGRAMMING LAB", 1),
        ("IT117L", "DIGITAL AND LOGIC CIRCUITS LAB", 1),
        ("PC110", "SCIENCE, TECHNOLOGY AND SOCIETY", 3),
        ("PE111C", "PATHFIT1: MOVEMENT COMPETENCY TRAINING", 2),
        ("TH111E", "SEARCHING FOR GOD IN THE WORLD TODAY", 3)
    ],
    "SY 2024-2025, 2nd Semester": [
        ("EN110", "PURPOSIVE COMMUNICATION", 3),
        ("IT125", "COMPUTER PROGRAMMING 1 LEC", 2),
        ("IT125L", "COMPUTER PROGRAMMING 1 LAB", 1),
        ("IT126", "DATA STRUCTURE & ALGORITHM LEC", 2),
        ("IT126L", "DATA STRUCTURE & ALGORITHM LAB", 1),
        ("IT128L", "WEB DESIGN PRINCIPLES LAB", 1),
        ("MH110", "MATHEMATICS IN THE MODERN WORLD", 3),
        ("NS211", "ENVIRONMENTAL SCIENCE", 3),
        ("PE121C", "PATHFIT2: EXERCISE-BASED FITNESS ACTIVITIES", 2),
        ("PY111", "UNDERSTANDING THE SELF", 3),
        ("TH121E", "RESPONDING TO GOD`S CALL BY BECOMING FULLY HUMAN", 3)
    ],
    "SY 2025-2026, 1st Semester": [
        ("CWT111", "CIVIC WELFARE TRAINING SERVICE 1", 3),
        ("IT215", "DATABASE MANAGEMENT SYSTEM LEC", 2),
        ("IT215L", "DATABASE MANAGEMENT SYSTEM LAB", 1),
        ("IT216", "COMPUTER PROGRAMMING 2 LEC", 2),
        ("IT216L", "COMPUTER PROGRAMMING 2 LAB", 1),
        ("IT218", "MULTIMEDIA TECHNOLOGY LEC", 2),
        ("IT218L", "MULTIMEDIA TECHNOLOGY LAB", 1),
        ("MH327", "DISCRETE MATH", 3),
        ("PC217", "APPLIED PHYSICS FOR IT LEC", 2),
        ("PC217L", "APPLIED PHYSICS FOR IT LAB", 1),
        ("PE211C", "PATHFIT3:DANCE", 2),
        ("PH114", "ETHICS", 3),
        ("TH211E", "CELEBRATING GOD`S PRESENCE AS A CHRISTIAN COMM", 3)
    ]
}

# Global variables
current_student_id = None
student_info = None


# -------- GRADE GENERATION --------
def generate_realistic_grades(student_profile):
    """Generate grades ONLY from: 1.00, 1.25, 1.50, 1.75, 2.00, 2.25, 2.50, 2.75"""
    prelim = random.choice(GRADE_VALUES)
    midterm = random.choice(GRADE_VALUES)
    final = random.choice(GRADE_VALUES)
    return prelim, midterm, final


def generate_subject_grades(overall_profile):
    """Generate grades for all subjects"""

    def get_subject_profile(subject_code, base_profile):
        return base_profile

    return get_subject_profile


# -------- MODERN BUTTON CLASS --------
class ModernButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground


# -------- ADD STUDENT WINDOW (FOR ADMIN) --------
def add_student_window():
    add_win = tk.Toplevel()
    add_win.title("Add New Student")
    add_win.geometry("450x550")
    add_win.configure(bg="#f8f9fa")
    add_win.resizable(False, False)

    # Header
    header = tk.Frame(add_win, bg="#28a745", height=70)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(header, text="➕ Add New Student", font=("Segoe UI", 18, "bold"),
             bg="#28a745", fg="white").pack(pady=18)

    # Form container
    form_container = tk.Frame(add_win, bg="#f8f9fa")
    form_container.pack(fill="both", expand=True, padx=35, pady=20)

    # First Name
    tk.Label(form_container, text="First Name *", font=("Segoe UI", 9, "bold"),
             bg="#f8f9fa", fg="#495057").pack(anchor="w", pady=(0, 4))
    first_entry = tk.Entry(form_container, font=("Segoe UI", 10), relief="solid", bd=1)
    first_entry.pack(fill="x", ipady=6, pady=(0, 12))

    # Middle Name
    tk.Label(form_container, text="Middle Name", font=("Segoe UI", 9, "bold"),
             bg="#f8f9fa", fg="#495057").pack(anchor="w", pady=(0, 4))
    middle_entry = tk.Entry(form_container, font=("Segoe UI", 10), relief="solid", bd=1)
    middle_entry.pack(fill="x", ipady=6, pady=(0, 12))

    # Last Name
    tk.Label(form_container, text="Last Name *", font=("Segoe UI", 9, "bold"),
             bg="#f8f9fa", fg="#495057").pack(anchor="w", pady=(0, 4))
    last_entry = tk.Entry(form_container, font=("Segoe UI", 10), relief="solid", bd=1)
    last_entry.pack(fill="x", ipady=6, pady=(0, 12))

    # Course
    tk.Label(form_container, text="Course *", font=("Segoe UI", 9, "bold"),
             bg="#f8f9fa", fg="#495057").pack(anchor="w", pady=(0, 4))
    course_var = tk.StringVar(value="B.S. INFORMATION TECHNOLOGY")
    course_dropdown = ttk.Combobox(form_container, textvariable=course_var,
                                   values=["B.S. INFORMATION TECHNOLOGY"],
                                   font=("Segoe UI", 10), state="readonly")
    course_dropdown.pack(fill="x", ipady=6, pady=(0, 12))

    # Student Number
    tk.Label(form_container, text="Student Number *", font=("Segoe UI", 9, "bold"),
             bg="#f8f9fa", fg="#495057").pack(anchor="w", pady=(0, 4))
    student_num_entry = tk.Entry(form_container, font=("Segoe UI", 10), relief="solid", bd=1)
    student_num_entry.pack(fill="x", ipady=6, pady=(0, 12))

    # Password
    tk.Label(form_container, text="Password *", font=("Segoe UI", 9, "bold"),
             bg="#f8f9fa", fg="#495057").pack(anchor="w", pady=(0, 4))
    password_entry = tk.Entry(form_container, show="●", font=("Segoe UI", 10), relief="solid", bd=1)
    password_entry.pack(fill="x", ipady=6, pady=(0, 20))

    def save_student():
        first = first_entry.get().strip()
        middle = middle_entry.get().strip()
        last = last_entry.get().strip()
        course = course_var.get().strip()
        student_number = student_num_entry.get().strip()
        password = password_entry.get().strip()

        if not first or not last or not student_number or not password:
            messagebox.showerror("Error", "Please fill in all required fields (*)")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            cursor.execute(
                "INSERT INTO students (student_number, first_name, middle_name, last_name, course, password) VALUES (?,?,?,?,?,?)",
                (student_number, first, middle, last, course, hashed_password))
            sid = cursor.lastrowid

            # Generate grades for all semesters
            for sem, subjects in semester_subjects.items():
                for code, desc, units in subjects:
                    pre, mid, fin = generate_realistic_grades(None)
                    cursor.execute(
                        "INSERT INTO grades (student_id, subject_code, subject_desc, units, semester, prelim, midterm, final_grade) VALUES (?,?,?,?,?,?,?,?)",
                        (sid, code, desc, units, sem, pre, mid, fin))
            conn.commit()
            messagebox.showinfo("Success",
                                f"Student added successfully!\n\nStudent Number: {student_number}\nPassword: {password}")
            add_win.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Student number already exists!")

    # RECTANGULAR CONFIRM BUTTON - visually pleasing
    tk.Button(form_container, text="✓ Add Student", command=save_student,
              bg="#28a745", fg="white", font=("Segoe UI", 12, "bold"),
              relief="flat", cursor="hand2", activebackground="#218838",
              bd=0, padx=40, pady=12).pack(fill="x")


# -------- LOGIN WINDOW --------
def login():
    login_win = tk.Tk()
    login_win.title("Student Information System - Login")
    login_win.state('zoomed')
    login_win.configure(bg="#e8f0fe")

    # Main container frame
    main_container = tk.Frame(login_win, bg="#e8f0fe")
    main_container.place(relx=0.5, rely=0.5, anchor="center")

    # Logo and title section
    header_section = tk.Frame(main_container, bg="#e8f0fe")
    header_section.pack(pady=(0, 30))

    # Logo container - MOVED FURTHER DOWN
    logo_container = tk.Frame(header_section, bg="#e8f0fe")
    logo_container.pack(pady=(80, 0))

    try:
        logo_img = Image.open("adulogo.png").resize((110, 110), Image.Resampling.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(logo_container, image=logo_photo, bg="#e8f0fe")
        logo_label.image = logo_photo
        logo_label.pack()
    except:
        tk.Label(logo_container, text="🎓", font=("Segoe UI", 70), bg="#e8f0fe").pack()

    tk.Label(header_section, text="Student Information System",
             font=("Segoe UI", 36, "bold"), bg="#e8f0fe", fg="#1a237e").pack(pady=(15, 5))
    tk.Label(header_section, text="Secure Access Portal",
             font=("Segoe UI", 14), bg="#e8f0fe", fg="#5f6368").pack()

    # Cards container
    cards_frame = tk.Frame(main_container, bg="#e8f0fe")
    cards_frame.pack(pady=20)

    # ===== STUDENT LOGIN CARD =====
    student_card = tk.Frame(cards_frame, bg="white", relief="raised", bd=2)
    student_card.pack(side="left", padx=20, ipadx=25, ipady=25)

    student_icon_frame = tk.Frame(student_card, bg="white")
    student_icon_frame.pack(pady=(0, 20))

    tk.Label(student_icon_frame, text="👨‍🎓", font=("Segoe UI", 45), bg="white").pack()
    tk.Label(student_icon_frame, text="STUDENT LOGIN", font=("Segoe UI", 18, "bold"),
             bg="white", fg="#1976d2").pack(pady=(10, 5))
    tk.Label(student_icon_frame, text="Access your grades and academic records",
             font=("Segoe UI", 10), bg="white", fg="#757575").pack()

    student_form = tk.Frame(student_card, bg="white")
    student_form.pack(fill="both", padx=20, pady=20)

    tk.Label(student_form, text="Student Number", font=("Segoe UI", 10, "bold"),
             bg="white", fg="#424242").pack(anchor="w", pady=(5, 5))

    snum_frame = tk.Frame(student_form, bg="#f5f5f5", relief="solid", bd=1)
    snum_frame.pack(fill="x", pady=(0, 15))
    tk.Label(snum_frame, text=" 👤 ", font=("Segoe UI", 11), bg="#f5f5f5", fg="#757575").pack(side="left", padx=(3, 0))
    student_num_entry = tk.Entry(snum_frame, font=("Segoe UI", 11), relief="flat", bg="#f5f5f5", width=28)
    student_num_entry.pack(side="left", fill="x", expand=True, ipady=9, padx=(0, 8))

    tk.Label(student_form, text="Password", font=("Segoe UI", 10, "bold"),
             bg="white", fg="#424242").pack(anchor="w", pady=(0, 5))

    spass_frame = tk.Frame(student_form, bg="#f5f5f5", relief="solid", bd=1)
    spass_frame.pack(fill="x", pady=(0, 20))
    tk.Label(spass_frame, text=" 🔒 ", font=("Segoe UI", 11), bg="#f5f5f5", fg="#757575").pack(side="left", padx=(3, 0))
    student_pass_entry = tk.Entry(spass_frame, show="●", font=("Segoe UI", 11), relief="flat", bg="#f5f5f5", width=28)
    student_pass_entry.pack(side="left", fill="x", expand=True, ipady=9, padx=(0, 8))

    def authenticate_student():
        snum = student_num_entry.get()
        pwd = student_pass_entry.get()
        hashed_pwd = hashlib.sha256(pwd.encode()).hexdigest()
        cursor.execute(
            "SELECT id, first_name, middle_name, last_name, course FROM students WHERE student_number=? AND password=?",
            (snum, hashed_pwd))
        row = cursor.fetchone()
        if row:
            global current_student_id, student_info
            current_student_id = row[0]
            student_info = row[1:]

            # Check if grades exist, if not generate grades
            for sem in semester_subjects.keys():
                cursor.execute("SELECT COUNT(*) FROM grades WHERE student_id=? AND semester=?",
                               (current_student_id, sem))
                if cursor.fetchone()[0] == 0:
                    for code, desc, units in semester_subjects[sem]:
                        pre, mid, fin = generate_realistic_grades(None)
                        cursor.execute(
                            "INSERT INTO grades (student_id, subject_code, subject_desc, units, semester, prelim, midterm, final_grade) VALUES (?,?,?,?,?,?,?,?)",
                            (current_student_id, code, desc, units, sem, pre, mid, fin))
            conn.commit()
            login_win.destroy()
            main_app()
        else:
            messagebox.showerror("Login Failed", "Invalid student number or password.")

    student_num_entry.bind('<Return>', lambda e: authenticate_student())
    student_pass_entry.bind('<Return>', lambda e: authenticate_student())

    ModernButton(student_form, text="Sign In", command=authenticate_student,
                 bg="#1976d2", fg="white", font=("Segoe UI", 11, "bold"),
                 relief="flat", cursor="hand2", activebackground="#1565c0",
                 width=20).pack(ipady=6)

    # ===== ADMIN LOGIN CARD =====
    admin_card = tk.Frame(cards_frame, bg="white", relief="raised", bd=2)
    admin_card.pack(side="left", padx=20, ipadx=25, ipady=25)

    admin_icon_frame = tk.Frame(admin_card, bg="white")
    admin_icon_frame.pack(pady=(0, 20))

    tk.Label(admin_icon_frame, text="👨‍💼", font=("Segoe UI", 45), bg="white").pack()
    tk.Label(admin_icon_frame, text="ADMIN LOGIN", font=("Segoe UI", 18, "bold"),
             bg="white", fg="#2e7d32").pack(pady=(10, 5))
    tk.Label(admin_icon_frame, text="Manage students and academic records",
             font=("Segoe UI", 10), bg="white", fg="#757575").pack()

    admin_form = tk.Frame(admin_card, bg="white")
    admin_form.pack(fill="both", padx=20, pady=20)

    tk.Label(admin_form, text="Username", font=("Segoe UI", 10, "bold"),
             bg="white", fg="#424242").pack(anchor="w", pady=(5, 5))

    auser_frame = tk.Frame(admin_form, bg="#f5f5f5", relief="solid", bd=1)
    auser_frame.pack(fill="x", pady=(0, 15))
    tk.Label(auser_frame, text=" 👤 ", font=("Segoe UI", 11), bg="#f5f5f5", fg="#757575").pack(side="left", padx=(3, 0))
    admin_user_entry = tk.Entry(auser_frame, font=("Segoe UI", 11), relief="flat", bg="#f5f5f5", width=28)
    admin_user_entry.pack(side="left", fill="x", expand=True, ipady=9, padx=(0, 8))

    tk.Label(admin_form, text="Password", font=("Segoe UI", 10, "bold"),
             bg="white", fg="#424242").pack(anchor="w", pady=(0, 5))

    apass_frame = tk.Frame(admin_form, bg="#f5f5f5", relief="solid", bd=1)
    apass_frame.pack(fill="x", pady=(0, 20))
    tk.Label(apass_frame, text=" 🔒 ", font=("Segoe UI", 11), bg="#f5f5f5", fg="#757575").pack(side="left", padx=(3, 0))
    admin_pass_entry = tk.Entry(apass_frame, show="●", font=("Segoe UI", 11), relief="flat", bg="#f5f5f5", width=28)
    admin_pass_entry.pack(side="left", fill="x", expand=True, ipady=9, padx=(0, 8))

    def authenticate_admin():
        username = admin_user_entry.get()
        password = admin_pass_entry.get()
        if username == "admin" and password == "admin123":
            login_win.destroy()
            admin_app()
        else:
            messagebox.showerror("Login Failed", "Invalid admin credentials.")

    admin_user_entry.bind('<Return>', lambda e: authenticate_admin())
    admin_pass_entry.bind('<Return>', lambda e: authenticate_admin())

    ModernButton(admin_form, text="Sign In", command=authenticate_admin,
                 bg="#2e7d32", fg="white", font=("Segoe UI", 11, "bold"),
                 relief="flat", cursor="hand2", activebackground="#1b5e20",
                 width=20).pack(ipady=6)

    login_win.mainloop()


# -------- MAIN APPLICATION (STUDENT) --------
def main_app():
    root = tk.Tk()
    root.title("Student Information System")
    root.state('zoomed')
    root.configure(bg="#f0f2f5")

    # HEADER
    header = tk.Frame(root, bg="#1976d2", height=120)
    header.pack(fill="x")
    header.pack_propagate(False)

    try:
        logo_img = Image.open("adulogo.png").resize((80, 80), Image.Resampling.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(header, image=logo_photo, bg="#1976d2")
        logo_label.image = logo_photo
        logo_label.pack(side="left", padx=20, pady=20)
    except:
        tk.Label(header, text="🎓", font=("Segoe UI", 50), bg="#1976d2", fg="white").pack(side="left", padx=20, pady=20)

    header_text = tk.Frame(header, bg="#1976d2")
    header_text.pack(side="left", fill="y", pady=20)

    tk.Label(header_text, text="Student Grade Portal", font=("Segoe UI", 30, "bold"),
             fg="white", bg="#1976d2").pack(anchor="w")

    full_name = f"{student_info[0]} {student_info[1]} {student_info[2]}" if student_info[
        1] else f"{student_info[0]} {student_info[2]}"
    tk.Label(header_text, text=f"Welcome, {full_name}", font=("Segoe UI", 13),
             fg="#bbdefb", bg="#1976d2").pack(anchor="w")

    ModernButton(header, text="Logout", command=lambda: [root.destroy(), login()],
                 bg="#d32f2f", fg="white", font=("Segoe UI", 11, "bold"),
                 relief="flat", cursor="hand2", activebackground="#c62828",
                 padx=30, pady=12).pack(side="right", padx=20)

    # CONTENT
    content = tk.Frame(root, bg="#f0f2f5")
    content.pack(fill="both", expand=True, padx=30, pady=30)

    # Info card
    info_card = tk.Frame(content, bg="white", relief="solid", bd=1)
    info_card.pack(fill="x", pady=(0, 20))

    info_inner = tk.Frame(info_card, bg="white")
    info_inner.pack(fill="x", padx=30, pady=25)

    tk.Label(info_inner, text="📋 Student Information", font=("Segoe UI", 18, "bold"),
             bg="white", fg="#212529").pack(anchor="w", pady=(0, 15))

    info_grid = tk.Frame(info_inner, bg="white")
    info_grid.pack(fill="x")

    tk.Label(info_grid, text="Name:", font=("Segoe UI", 12, "bold"),
             bg="white", fg="#616161").grid(row=0, column=0, sticky="w", pady=8, padx=(0, 15))
    tk.Label(info_grid, text=full_name, font=("Segoe UI", 12),
             bg="white", fg="#212529").grid(row=0, column=1, sticky="w", pady=8)

    tk.Label(info_grid, text="Course:", font=("Segoe UI", 12, "bold"),
             bg="white", fg="#616161").grid(row=1, column=0, sticky="w", pady=8, padx=(0, 15))
    tk.Label(info_grid, text=student_info[3], font=("Segoe UI", 12),
             bg="white", fg="#212529").grid(row=1, column=1, sticky="w", pady=8)

    # Grades card
    grades_card = tk.Frame(content, bg="white", relief="solid", bd=1)
    grades_card.pack(fill="both", expand=True)

    grades_inner = tk.Frame(grades_card, bg="white")
    grades_inner.pack(fill="both", expand=True, padx=30, pady=25)

    # Semester selector
    selector_frame = tk.Frame(grades_inner, bg="white")
    selector_frame.pack(fill="x", pady=(0, 20))

    tk.Label(selector_frame, text="📚 Select Semester:", font=("Segoe UI", 13, "bold"),
             bg="white", fg="#212529").pack(side="left", padx=(0, 15))

    semester_var = tk.StringVar()
    semester_style = ttk.Style()
    semester_style.configure("Custom.TCombobox", padding=5)

    semester_dropdown = ttk.Combobox(selector_frame, textvariable=semester_var,
                                     values=list(semester_subjects.keys()),
                                     state="readonly", font=("Segoe UI", 11),
                                     width=40, style="Custom.TCombobox")
    semester_dropdown.pack(side="left")
    semester_dropdown.current(0)

    # Grades table
    tree_frame = tk.Frame(grades_inner, bg="white")
    tree_frame.pack(fill="both", expand=True)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="white",
                    foreground="#212529",
                    rowheight=35,
                    fieldbackground="white",
                    font=("Segoe UI", 11))
    style.configure("Treeview.Heading",
                    font=("Segoe UI", 12, "bold"),
                    background="#1976d2",
                    foreground="white",
                    relief="flat")
    style.map('Treeview', background=[('selected', '#1976d2')])

    tree = ttk.Treeview(tree_frame, columns=("Code", "Description", "Units", "Prelim", "Midterm", "Final"),
                        show="headings", height=13)
    tree.heading("Code", text="Subject Code")
    tree.heading("Description", text="Subject Description")
    tree.heading("Units", text="Units")
    tree.heading("Prelim", text="Prelim")
    tree.heading("Midterm", text="Midterm")
    tree.heading("Final", text="Final Grade")

    tree.column("Code", width=130, anchor="center")
    tree.column("Description", width=450, anchor="w")
    tree.column("Units", width=80, anchor="center")
    tree.column("Prelim", width=100, anchor="center")
    tree.column("Midterm", width=100, anchor="center")
    tree.column("Final", width=120, anchor="center")

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Configure the total_gwa tag styling
    tree.tag_configure("total_gwa", background="#FFF9C4", font=("Segoe UI", 12, "bold"))

    # GWA labels
    period_gwa_frame = tk.Frame(grades_inner, bg="#fff3e0", relief="solid", bd=1)
    period_gwa_frame.pack(fill="x", pady=(15, 0))

    period_gwa_label = tk.Label(period_gwa_frame, text="", font=("Segoe UI", 14, "bold"),
                                bg="#fff3e0", fg="#e65100")
    period_gwa_label.pack(pady=15)

    gwa_frame = tk.Frame(grades_inner, bg="#e3f2fd", relief="flat")
    gwa_frame.pack(fill="x", pady=(15, 0))

    semester_gwa_label = tk.Label(gwa_frame, text="", font=("Segoe UI", 16, "bold"),
                                  bg="#e3f2fd", fg="#1976d2")
    semester_gwa_label.pack(pady=(20, 5))

    total_gwa_label = tk.Label(gwa_frame, text="", font=("Segoe UI", 16, "bold"),
                               bg="#e3f2fd", fg="#0d47a1")
    total_gwa_label.pack(pady=(5, 20))

    def load_grades():
        for row in tree.get_children():
            tree.delete(row)

        selected_semester = semester_var.get()
        cursor.execute(
            "SELECT subject_code, subject_desc, units, prelim, midterm, final_grade FROM grades WHERE student_id=? AND semester=?",
            (current_student_id, selected_semester))
        rows = cursor.fetchall()

        prelim_weighted = 0
        midterm_weighted = 0
        final_weighted = 0
        total_units = 0

        for row in rows:
            tree.insert("", "end", values=row)

            code, desc, units, pre, mid, fin = row
            try:
                prelim_grade = float(pre)
                midterm_grade = float(mid)
                final_grade = float(fin)
                units_int = int(units)

                prelim_weighted += prelim_grade * units_int
                midterm_weighted += midterm_grade * units_int
                final_weighted += final_grade * units_int
                total_units += units_int
            except ValueError:
                pass

        if total_units > 0:
            prelim_gwa = round(prelim_weighted / total_units, 2)
            midterm_gwa = round(midterm_weighted / total_units, 2)
            final_gwa = round(final_weighted / total_units, 2)

            tree.insert("", "end",
                        values=("—", "General Weighted Average:", total_units, prelim_gwa, midterm_gwa, final_gwa),
                        tags=("total_gwa",))

            period_gwa_label.config(
                text=f"General Weighted Average:     Prelim: {prelim_gwa}     Midterm: {midterm_gwa}     Finals: {final_gwa}")
        else:
            period_gwa_label.config(text="General Weighted Average:     N/A")

        semester_weighted = 0
        semester_units = 0
        for code, desc, units, pre, mid, fin in rows:
            try:
                fin_grade = float(fin)
                units_int = int(units)
                semester_weighted += fin_grade * units_int
                semester_units += units_int
            except ValueError:
                pass

        if semester_units > 0:
            semester_gwa = round(semester_weighted / semester_units, 2)
            semester_gwa_label.config(text=f"📊 Semester GWA (Final Grades): {semester_gwa}")
        else:
            semester_gwa_label.config(text=f"📊 Semester GWA (Final Grades): N/A")

        cursor.execute("SELECT units, final_grade FROM grades WHERE student_id=?", (current_student_id,))
        all_grades = cursor.fetchall()

        total_weighted = 0
        total_units_all = 0
        for units, fin in all_grades:
            try:
                fin_grade = float(fin)
                units_int = int(units)
                total_weighted += fin_grade * units_int
                total_units_all += units_int
            except ValueError:
                pass

        if total_units_all > 0:
            total_gwa = round(total_weighted / total_units_all, 2)
            total_gwa_label.config(text=f"🎓 Total GWA (All Semesters): {total_gwa}")
        else:
            total_gwa_label.config(text=f"🎓 Total GWA (All Semesters): N/A")

    semester_dropdown.bind("<<ComboboxSelected>>", lambda e: load_grades())
    load_grades()

    root.mainloop()


# -------- ADMIN APPLICATION --------
def admin_app():
    root = tk.Tk()
    root.title("Admin Dashboard - Student Information System")
    root.state('zoomed')
    root.configure(bg="#f0f2f5")

    # HEADER
    header = tk.Frame(root, bg="#2e7d32", height=120)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(header, text="👨‍💼", font=("Segoe UI", 55), bg="#2e7d32", fg="white").pack(side="left", padx=20, pady=20)

    header_text = tk.Frame(header, bg="#2e7d32")
    header_text.pack(side="left", fill="y", pady=20)

    tk.Label(header_text, text="Admin Dashboard", font=("Segoe UI", 30, "bold"),
             fg="white", bg="#2e7d32").pack(anchor="w")
    tk.Label(header_text, text="Manage students, grades, and academic records", font=("Segoe UI", 13),
             fg="#c8e6c9", bg="#2e7d32").pack(anchor="w")

    ModernButton(header, text="Logout", command=lambda: [root.destroy(), login()],
                 bg="#d32f2f", fg="white", font=("Segoe UI", 11, "bold"),
                 relief="flat", cursor="hand2", activebackground="#c62828",
                 padx=30, pady=12).pack(side="right", padx=20)

    # CONTENT
    content = tk.Frame(root, bg="#f0f2f5")
    content.pack(fill="both", expand=True, padx=30, pady=30)

    # Action buttons
    actions_frame = tk.Frame(content, bg="#f0f2f5")
    actions_frame.pack(fill="x", pady=(0, 20))

    def view_edit_grades():
        selection = students_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a student first.")
            return

        item = students_tree.item(selection[0])
        student_id = item['values'][0]

        first_name = item['values'][2]
        middle_name = item['values'][3]
        last_name = item['values'][4]
        student_name = f"{first_name} {middle_name} {last_name}" if middle_name else f"{first_name} {last_name}"

        edit_grades_window(student_id, student_name)

    def delete_student():
        selection = students_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a student to delete.")
            return

        item = students_tree.item(selection[0])
        student_id = item['values'][0]

        first_name = item['values'][2]
        middle_name = item['values'][3]
        last_name = item['values'][4]
        student_name = f"{first_name} {middle_name} {last_name}" if middle_name else f"{first_name} {last_name}"

        if messagebox.askyesno("Confirm Delete",
                               f"Are you sure you want to delete {student_name}?\n\nThis action cannot be undone."):
            cursor.execute("DELETE FROM grades WHERE student_id=?", (student_id,))
            cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
            conn.commit()
            messagebox.showinfo("Success", "Student deleted successfully.")
            students_tree.delete(selection[0])

    ModernButton(actions_frame, text="➕ Add New Student", command=add_student_window,
                 bg="#2e7d32", fg="white", font=("Segoe UI", 12, "bold"),
                 relief="flat", cursor="hand2", activebackground="#1b5e20",
                 padx=25, pady=12).pack(side="left", padx=(0, 10))

    ModernButton(actions_frame, text="📝 View/Edit Grades", command=view_edit_grades,
                 bg="#1976d2", fg="white", font=("Segoe UI", 12, "bold"),
                 relief="flat", cursor="hand2", activebackground="#1565c0",
                 padx=25, pady=12).pack(side="left", padx=(0, 10))

    ModernButton(actions_frame, text="🗑️ Delete Student", command=delete_student,
                 bg="#d32f2f", fg="white", font=("Segoe UI", 12, "bold"),
                 relief="flat", cursor="hand2", activebackground="#c62828",
                 padx=25, pady=12).pack(side="left")

    # Students list card
    students_card = tk.Frame(content, bg="white", relief="solid", bd=1)
    students_card.pack(fill="both", expand=True)

    students_inner = tk.Frame(students_card, bg="white")
    students_inner.pack(fill="both", expand=True, padx=30, pady=25)

    tk.Label(students_inner, text="👥 All Students", font=("Segoe UI", 18, "bold"),
             bg="white", fg="#212529").pack(anchor="w", pady=(0, 20))

    # Students table
    tree_frame = tk.Frame(students_inner, bg="white")
    tree_frame.pack(fill="both", expand=True)

    students_tree = ttk.Treeview(tree_frame,
                                 columns=("ID", "Student Number", "First Name", "Middle Name", "Last Name", "Course"),
                                 show="headings", height=16)

    students_tree.heading("ID", text="ID")
    students_tree.heading("Student Number", text="Student Number")
    students_tree.heading("First Name", text="First Name")
    students_tree.heading("Middle Name", text="Middle Name")
    students_tree.heading("Last Name", text="Last Name")
    students_tree.heading("Course", text="Course")

    students_tree.column("ID", width=60, anchor="center")
    students_tree.column("Student Number", width=130, anchor="center")
    students_tree.column("First Name", width=150, anchor="w")
    students_tree.column("Middle Name", width=120, anchor="w")
    students_tree.column("Last Name", width=150, anchor="w")
    students_tree.column("Course", width=350, anchor="w")

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=students_tree.yview)
    students_tree.configure(yscrollcommand=scrollbar.set)
    students_tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Load students
    cursor.execute("SELECT id, student_number, first_name, middle_name, last_name, course FROM students")
    for row in cursor.fetchall():
        students_tree.insert("", "end", values=row)

    # Count label
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    tk.Label(students_inner, text=f"Total Students: {count}",
             font=("Segoe UI", 12, "bold"), bg="white", fg="#616161").pack(anchor="w", pady=(20, 0))

    root.mainloop()


# -------- EDIT GRADES WINDOW --------
def edit_grades_window(student_id, student_name):
    edit_win = tk.Toplevel()
    edit_win.title(f"Edit Grades - {student_name}")
    edit_win.state('zoomed')
    edit_win.configure(bg="#f0f2f5")

    # Header
    header = tk.Frame(edit_win, bg="#1976d2", height=100)
    header.pack(fill="x")
    header.pack_propagate(False)

    header_text = tk.Frame(header, bg="#1976d2")
    header_text.pack(side="left", fill="y", padx=30, pady=20)

    tk.Label(header_text, text=f"✏️ Editing Grades", font=("Segoe UI", 26, "bold"),
             fg="white", bg="#1976d2").pack(anchor="w")
    tk.Label(header_text, text=f"Student: {student_name}", font=("Segoe UI", 13),
             fg="#bbdefb", bg="#1976d2").pack(anchor="w")

    # Confirm & Close button
    ModernButton(header, text="✓ Confirm & Close", command=edit_win.destroy,
                 bg="#28a745", fg="white", font=("Segoe UI", 12, "bold"),
                 relief="flat", cursor="hand2", activebackground="#218838",
                 padx=35, pady=14).pack(side="right", padx=20)

    # Content
    content = tk.Frame(edit_win, bg="#f0f2f5")
    content.pack(fill="both", expand=True, padx=30, pady=30)

    # Semester selector
    selector_frame = tk.Frame(content, bg="#f0f2f5")
    selector_frame.pack(fill="x", pady=(0, 20))

    tk.Label(selector_frame, text="📚 Semester:", font=("Segoe UI", 13, "bold"),
             bg="#f0f2f5", fg="#212529").pack(side="left", padx=(0, 15))

    semester_var = tk.StringVar()
    semester_dropdown = ttk.Combobox(selector_frame, textvariable=semester_var,
                                     values=list(semester_subjects.keys()),
                                     state="readonly", font=("Segoe UI", 11), width=40)
    semester_dropdown.pack(side="left")
    semester_dropdown.current(0)

    # Grades card
    grades_card = tk.Frame(content, bg="white", relief="solid", bd=1)
    grades_card.pack(fill="both", expand=True)

    grades_inner = tk.Frame(grades_card, bg="white")
    grades_inner.pack(fill="both", expand=True, padx=30, pady=25)

    # Table
    tree_frame = tk.Frame(grades_inner, bg="white")
    tree_frame.pack(fill="both", expand=True)

    grades_tree = ttk.Treeview(tree_frame,
                               columns=("ID", "Code", "Description", "Units", "Prelim", "Midterm", "Final"),
                               show="headings", height=14)

    grades_tree.heading("ID", text="ID")
    grades_tree.heading("Code", text="Subject Code")
    grades_tree.heading("Description", text="Subject Description")
    grades_tree.heading("Units", text="Units")
    grades_tree.heading("Prelim", text="Prelim")
    grades_tree.heading("Midterm", text="Midterm")
    grades_tree.heading("Final", text="Final Grade")

    grades_tree.column("ID", width=50, anchor="center")
    grades_tree.column("Code", width=120, anchor="center")
    grades_tree.column("Description", width=400, anchor="w")
    grades_tree.column("Units", width=70, anchor="center")
    grades_tree.column("Prelim", width=100, anchor="center")
    grades_tree.column("Midterm", width=100, anchor="center")
    grades_tree.column("Final", width=100, anchor="center")

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=grades_tree.yview)
    grades_tree.configure(yscrollcommand=scrollbar.set)
    grades_tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def load_grades():
        for row in grades_tree.get_children():
            grades_tree.delete(row)
        cursor.execute(
            "SELECT id, subject_code, subject_desc, units, prelim, midterm, final_grade FROM grades WHERE student_id=? AND semester=?",
            (student_id, semester_var.get()))
        for row in cursor.fetchall():
            grades_tree.insert("", "end", values=row)

    def edit_selected_grade():
        selection = grades_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a grade to edit.")
            return

        item = grades_tree.item(selection[0])
        grade_id = item['values'][0]
        subject_desc = item['values'][2]
        current_prelim = item['values'][4]
        current_midterm = item['values'][5]
        current_final = item['values'][6]

        # COMPACT EDIT DIALOG
        edit_dlg = tk.Toplevel(edit_win)
        edit_dlg.title("Edit Grade")
        edit_dlg.geometry("420x420")
        edit_dlg.configure(bg="#f8f9fa")
        edit_dlg.resizable(False, False)
        edit_dlg.transient(edit_win)
        edit_dlg.grab_set()

        # Header
        dlg_header = tk.Frame(edit_dlg, bg="#1976d2", height=65)
        dlg_header.pack(fill="x")
        dlg_header.pack_propagate(False)

        tk.Label(dlg_header, text="✏️ Edit Grade", font=("Segoe UI", 16, "bold"),
                 bg="#1976d2", fg="white").pack(pady=16)

        # Form
        form = tk.Frame(edit_dlg, bg="#f8f9fa")
        form.pack(fill="both", expand=True, padx=35, pady=25)

        tk.Label(form, text=subject_desc, font=("Segoe UI", 10, "bold"),
                 bg="#f8f9fa", fg="#424242", wraplength=340).pack(pady=(0, 20))

        # Prelim
        tk.Label(form, text="Prelim Grade", font=("Segoe UI", 9, "bold"),
                 bg="#f8f9fa", fg="#616161").pack(anchor="w", pady=(0, 5))
        prelim_entry = tk.Entry(form, font=("Segoe UI", 11), relief="solid", bd=1)
        prelim_entry.insert(0, current_prelim)
        prelim_entry.pack(fill="x", ipady=8, pady=(0, 15))

        # Midterm
        tk.Label(form, text="Midterm Grade", font=("Segoe UI", 9, "bold"),
                 bg="#f8f9fa", fg="#616161").pack(anchor="w", pady=(0, 5))
        midterm_entry = tk.Entry(form, font=("Segoe UI", 11), relief="solid", bd=1)
        midterm_entry.insert(0, current_midterm)
        midterm_entry.pack(fill="x", ipady=8, pady=(0, 15))

        # Final
        tk.Label(form, text="Final Grade", font=("Segoe UI", 9, "bold"),
                 bg="#f8f9fa", fg="#616161").pack(anchor="w", pady=(0, 5))
        final_entry = tk.Entry(form, font=("Segoe UI", 11), relief="solid", bd=1)
        final_entry.insert(0, current_final)
        final_entry.pack(fill="x", ipady=8, pady=(0, 22))

        def save_changes():
            try:
                p = float(prelim_entry.get())
                m = float(midterm_entry.get())
                f = float(final_entry.get())

                cursor.execute("UPDATE grades SET prelim=?, midterm=?, final_grade=? WHERE id=?",
                               (p, m, f, grade_id))
                conn.commit()
                messagebox.showinfo("Success", "Grade updated successfully!")
                edit_dlg.destroy()
                load_grades()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers!")

        # RECTANGULAR CONFIRM BUTTON - visually pleasing
        tk.Button(form, text="✓ Confirm Changes", command=save_changes,
                  bg="#28a745", fg="white", font=("Segoe UI", 11, "bold"),
                  relief="flat", cursor="hand2", activebackground="#218838",
                  bd=0, pady=14).pack(fill="x")

    # Action buttons
    actions_frame = tk.Frame(grades_inner, bg="white")
    actions_frame.pack(fill="x", pady=(20, 0))

    ModernButton(actions_frame, text="✏️ Edit Selected Grade", command=edit_selected_grade,
                 bg="#1976d2", fg="white", font=("Segoe UI", 12, "bold"),
                 relief="flat", cursor="hand2", activebackground="#1565c0",
                 padx=25, pady=12).pack(side="left")

    semester_dropdown.bind("<<ComboboxSelected>>", lambda e: load_grades())
    load_grades()


# -------- INITIALIZE WITH SAMPLE DATA --------
cursor.execute("SELECT COUNT(*) FROM students")
if cursor.fetchone()[0] == 0:
    default_password = "password"
    hashed_default = hashlib.sha256(default_password.encode()).hexdigest()

    for i in range(5):
        first = f"Student{i + 1}"
        middle = "M"
        last = "Last"
        course = "B.S. INFORMATION TECHNOLOGY"
        student_number = str(random.randint(100000, 999999))
        cursor.execute(
            "INSERT INTO students (student_number, first_name, middle_name, last_name, course, password) VALUES (?,?,?,?,?,?)",
            (student_number, first, middle, last, course, hashed_default))
        sid = cursor.lastrowid

        for sem, subjects in semester_subjects.items():
            for code, desc, units in subjects:
                pre, mid, fin = generate_realistic_grades(None)
                cursor.execute(
                    "INSERT INTO grades (student_id, subject_code, subject_desc, units, semester, prelim, midterm, final_grade) VALUES (?,?,?,?,?,?,?,?)",
                    (sid, code, desc, units, sem, pre, mid, fin))
    conn.commit()

# Start with login
login()

import getpass
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import messagebox
import sqlite3
import subprocess
from PIL import Image, ImageTk
image = Image.open("icon.jpg")
# resize the image to fit in the window
width, height = 300, 300
image = image.resize((width, height))

# create a Tkinter-compatible photo image object from the PIL image object


class LoginRegister:
    def __init__(self, master):
        photo = ImageTk.PhotoImage(image)
        self.master = master
        master.title("Login/Register")
        master.geometry("800x500")
        master.configure(bg='black')

        # create a database connection and cursor
        self.conn = sqlite3.connect('users.db')
        self.cur = self.conn.cursor()

        # create the users table if it doesn't exist
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")

        # create labels and buttons for login and registration
        self.label_welcome = ttk.Label(
            master, text="Welcome to Exercise Rectifier!", foreground='black', font=('Helvetica', 20, 'bold'))
        self.label_welcome.pack(side='top', pady=20)

        self.label_image = ttk.Label(master, image=photo)
        # store a reference to the photo to prevent garbage collection
        self.label_image.image = photo
        self.label_image.pack(side="top", pady=20)

        self.button_login = ttk.Button(
            master, text="Login", command=self.show_login, style='Custom.TButton')
        self.button_login.pack(side='left', padx=20, pady=20)

        self.button_register = ttk.Button(
            master, text="Register", command=self.show_register, style='Custom.TButton')
        self.button_register.pack(side='right', padx=20, pady=20)

        # create custom style for the buttons
        style = ttk.Style()
        style.configure('Custom.TButton', foreground='black', background='#4CAF50', font=(
            'Helvetica', 12, 'bold'), width=25, height=9, borderwidth=0, borderradius=30)

        # create label for credits
        self.label_credits = ttk.Label(
            master, text="Created by: Tathagat, Vaidansh, Utkarsh", foreground='black', font=('Helvetica', 10))
        self.label_credits.pack(side='bottom', pady=10)
        self.label_credits = ttk.Label(
            master, text="Guided by: Mr. Ashish Patel", foreground='black', font=('Helvetica', 10))
        self.label_credits.pack(side='bottom', pady=10)

    def show_login(self):
        self.login_window = tk.Toplevel(self.master)
        self.login = Login(self.login_window, self.cur, self)

    def show_register(self):
        self.register_window = tk.Toplevel(self.master)
        self.register = Register(self.register_window, self.cur, self.conn)


class Homepage:
    def __init__(self, master, username):
        self.master = master
        master.title("Homepage")
        master.configure(background='black')
        master.bind("<Escape>", self.exit)
        self.label_welcome = ttk.Label(
            master, text=f"Welcome, {username}!", foreground='white', background='black', font=('Arial', 16))
        self.label_welcome.pack(pady=20)

        # load images for buttons
        self.bicep_curls_img = PhotoImage(
            file="bicep_curls.png").subsample(2, 2)

        self.pushups_img = PhotoImage(file="pushups.png").subsample(2, 2)

        self.rope_skipping_img = PhotoImage(
            file="rope_skipping.png").subsample(2, 2)

        self.squats_img = PhotoImage(file="squats.png").subsample(2, 2)
        self.eh = PhotoImage(file="eh.png").subsample(4, 4)
        self.exitbut = PhotoImage(file="exit.png").subsample(4, 4)
        # create buttons with images
        self.button1 = ttk.Button(master, image=self.bicep_curls_img,
                                  command=lambda: self.run_script_and_log("bicepcurl.py", "Bicep Curls"))
        self.button1.pack(pady=10)

        self.button2 = ttk.Button(master, image=self.pushups_img,
                                  command=lambda: self.run_script_and_log("pushup.py", "Pushups"))
        self.button2.pack(pady=10)

        self.button3 = ttk.Button(master, image=self.rope_skipping_img, command=lambda: self.run_script_and_log(
            "rope_skipping_counter.py", "Rope Skipping"))
        self.button3.pack(pady=10)

        self.button4 = ttk.Button(master, image=self.squats_img,
                                  command=lambda: self.run_script_and_log("squat.py", "Squats"))
        self.button4.pack(pady=10)
        self.button1.pack(side="left", padx=10)
        self.button2.pack(side="left", padx=10)
        self.button3.pack(side="left", padx=10)
        self.button4.pack(side="left", padx=10)
        style = ttk.Style()
        style.configure('Green.TButton', background='#008000', borderwidth=0, borderradius=30)
        self.history_button = ttk.Button(
            master, image=self.eh, text="Exercise History", command=self.show_history, style='Green.TButton')
        self.history_button.pack(pady=10)
        
        self.exit_button = ttk.Button(
            master, image=self.exitbut,  text="Exit", command=self.exit_program)
        self.exit_button.pack(pady=10)

        # create a database connection and cursor
        self.conn = sqlite3.connect('users.db')
        self.cur = self.conn.cursor()

        # create the exercise_logs table if it doesn't exist
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS exercise_logs (username TEXT, exercise TEXT, start_time TEXT, end_time TEXT)")

    def run_script_and_log(self, script_name, exercise_name):
        username = getpass.getuser()
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subprocess.run(["python", script_name])
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cur.execute("INSERT INTO exercise_logs VALUES (?, ?, ?, ?)",
                         (username, exercise_name, start_time, end_time))
        self.conn.commit()

    def show_history(self):
        history_window = tk.Toplevel(self.master)
        history_window.title("Exercise History")

        # create the table
        table = ttk.Treeview(history_window, columns=(
            "Start Time", "Exercise", "End Time"))
        table.heading("#0", text="ID")
        table.column("#0", width=50)
        table.heading("Start Time", text="Start Time")
        table.column("Start Time", width=150)
        table.heading("Exercise", text="Exercise")
        table.column("Exercise", width=100)
        table.heading("End Time", text="End Time")
        table.column("End Time", width=150)
        table.pack(fill="both", expand=True)

        # populate the table with data from the database
        username = getpass.getuser()
        self.cur.execute(
            "SELECT rowid, start_time, exercise, end_time FROM exercise_logs WHERE username=?", (username,))
        rows = self.cur.fetchall()
        for row in rows:
            table.insert("", "end", text=row[0],
                         values=(row[1], row[2], row[3]))

    def exit_program(self):
        self.master.destroy()

    def exit(self, event=None):
        if hasattr(self, "proc") and self.proc.poll() is None:  # check if the process is running
            self.proc.kill()  # terminate the process
        self.master.destroy()  # destroy the window


class Login:
    def __init__(self, master, cur, app):
        self.master = master
        self.cur = cur
        self.app = app
        master.title("Login")
        master.configure(bg='black')

        # create labels and entries for login form
        self.label_username = ttk.Label(
            master, text="Username:", foreground='black', font=('Helvetica', 14))
        self.label_username.grid(row=0, column=0, padx=5, pady=5)
        self.entry_username = ttk.Entry(
            master, foreground='black', font=('Helvetica', 14))
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)

        self.label_password = ttk.Label(
            master, text="Password:", foreground='black', font=('Helvetica', 14))
        self.label_password.grid(row=1, column=0, padx=5, pady=5)
        self.entry_password = ttk.Entry(
            master, show="*", foreground='black', font=('Helvetica', 14))
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        self.button_login = ttk.Button(
            master, text="Login", command=self.login, style='my.TButton')
        self.button_login.grid(row=2, column=1, padx=5, pady=10)

        # define a custom style for the login button
        style = ttk.Style()
        style.configure('my.TButton', foreground='black',
                        font=('Helvetica', 14))

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # query the database for the username and password
        self.cur.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        row = self.cur.fetchone()

        if row is not None:
            messagebox.showinfo("Login", "Login successful!")
            self.app.label_welcome.config(text=f"Welcome, {username}!")
            self.master.destroy()
            self.homepage = Homepage(tk.Toplevel(), username)
        else:
            messagebox.showerror("Login", "Username or password is incorrect.")


class Register:
    def __init__(self, master, cur, conn):
        self.master = master
        self.cur = cur
        master.title("Register")

        # create labels and entries for registration form
        self.label_username_reg = ttk.Label(master, text="New Username:")
        self.label_username_reg.grid(row=0, column=0, padx=5, pady=5)
        self.entry_username_reg = ttk.Entry(master)
        self.entry_username_reg.grid(row=0, column=1, padx=5, pady=5)

        self.label_password_reg = ttk.Label(master, text="New Password:")
        self.label_password_reg.grid(row=1, column=0, padx=5, pady=5)
        self.entry_password_reg = ttk.Entry(master, show="*")
        self.entry_password_reg.grid(row=1, column=1, padx=5, pady=5)

        self.button_register = ttk.Button(
            master, text="Register", command=self.register)
        self.button_register.grid(row=2, column=1, padx=5, pady=5)

    def register(self):
        username_reg = self.entry_username_reg.get()
        password_reg = self.entry_password_reg.get()

        # insert the new user into the database
        self.cur.execute("INSERT INTO users VALUES (?, ?)",
                         (username_reg, password_reg))
        self.cur.connection.commit()

        messagebox.showinfo("Register", "Registration successful!")
        self.master.destroy()


root = tk.Tk()
app = LoginRegister(root)
root.mainloop()

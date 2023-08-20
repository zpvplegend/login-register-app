import tkinter as tk
from tkinter import messagebox
import bcrypt

class GUI:
    def __init__(self):
        self.login_window = tk.Tk()
        self.login_window.geometry("400x400")
        self.login_window.title("Login")
        self.success=False
        self.login_gui()

    def login_gui(self):
        label_1 = tk.Label(self.login_window, text="Enter your username: ")
        label_1.place(x=140, y=100)

        text_box1 = tk.Text(self.login_window, width=35, height=1)
        text_box1.place(x=65, y=120)

        label_2 = tk.Label(self.login_window, text="Enter your password here:")
        label_2.place(x=137, y=180)

        text_box2 = tk.Text(self.login_window, width=35, height=1)
        text_box2.place(x=62, y=200)

        login_btn = tk.Button(self.login_window, text="LOGIN", font="arial,18", command=lambda: self.validation(text_box1, text_box2))
        login_btn.place(x=163, y=250)

        label_3 = tk.Label(self.login_window, text='Dont have an account? Click "REGISTER"')
        label_3.place(x=95, y=320)

        reg_btn = tk.Button(self.login_window, text="REGISTER", font="arial,18", command=self.switch_window_1)
        reg_btn.place(x=145, y=350)

    def reg_gui(self):
        self.reg_window = tk.Tk()
        self.reg_window.geometry("400x400")
        self.reg_window.title("Register")

        reg_label_1 = tk.Label(self.reg_window, text="Enter desired username: ")
        reg_label_1.place(x=133, y=100)

        self.reg_text_box1 = tk.Text(self.reg_window, width=35, height=1)
        self.reg_text_box1.place(x=65, y=120)

        reg_label_2 = tk.Label(self.reg_window, text="Enter desired password: ")
        reg_label_2.place(x=137, y=180)

        self.reg_text_box2 = tk.Text(self.reg_window, width=35, height=1)
        self.reg_text_box2.place(x=62, y=200)

        reg_btn = tk.Button(self.reg_window, text="REGISTER", font="arial,18", command=lambda: self.register())
        reg_btn.place(x=140, y=250)

    def switch_window_1(self):
        self.login_window.destroy()
        self.reg_gui()

    def switch_window_2(self):
        self.reg_window.destroy()
        self.login_window=tk.Tk()
        self.login_window.geometry("400x400")
        self.login_window.title("Login")
        self.login_gui()
        self.run()

    def validation(self, text_box1, text_box2):
        input_username = text_box1.get("1.0", "end-1c")
        input_password = text_box2.get("1.0", "end-1c")

        with open("database.txt") as database:
            for line in database:
                username, hashed_password = line.strip().split(":")
                if input_username == username and bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8')):
                    messagebox.showinfo("Success!","Login successful")
                    return
            messagebox.showinfo("Error!","Incorrect username or password")

    def user_exists(self):
        with open("database.txt", "r") as database:
            for user_exists in database:
                username, hashed_password = user_exists.strip().split(":")
                if self.input_username == username:
                    return True
        return False


    def run(self):
        self.login_window.mainloop()

    def register(self):
        self.input_username = self.reg_text_box1.get("1.0", "end-1c")
        self.input_password = self.reg_text_box2.get("1.0", "end-1c").strip()

        if self.input_password == "" or self.input_username == "":
            messagebox.showinfo("Error!", "Please choose a username and a password")

        elif self.user_exists() is True:
            messagebox.showinfo("Error!", "Username already exists")

        else:
            hashed_password = bcrypt.hashpw(self.input_password.encode('utf-8'), bcrypt.gensalt())
            with open("database.txt", "a") as database:
                database.write(f"{self.input_username}:{hashed_password.decode('utf-8')}\n")
            messagebox.showinfo("Success!", "Registration successful")
            self.switch_window_2()


gui = GUI()
gui.run()
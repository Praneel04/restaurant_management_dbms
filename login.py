from tkinter import messagebox, ttk, Tk, Label, Entry, Button, StringVar

def login_page():
    # Function to handle login
    def submit():
        username = a.get()
        password = b.get()
        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return
        try:
            cur = con.cursor()
            cur.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
            result = cur.fetchone()
            if result:
                messagebox.showinfo("Login Successful", "Welcome!")
                main_app()  # Call the main app function if login is successful
            else:
                messagebox.showwarning("Login Failed", "Invalid username or password.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    # Main window for login
    r = Tk()
    r.title("Login - Restaurant Management System")
    r.geometry("400x300")
    a = StringVar()
    b = StringVar()

    Label(r, text="RESTAURANT ADMIN LOGIN", font=("Helvetica", 16)).pack(pady=20)
    Label(r, text="Username").place(x=100, y=100)
    Entry(r, textvariable=a).place(x=170, y=100)
    Label(r, text="Password").place(x=100, y=140)
    Entry(r, textvariable=b, show="*").place(x=170, y=140)
    Button(r, text="Submit", command=submit).place(x=180, y=180)

    r.mainloop()





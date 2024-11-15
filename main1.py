from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import mysql.connector
con=mysql.connector.connect(host="localhost",user="root",password="Sepaugtf25",database="restaurant3")
check=0
print(con)
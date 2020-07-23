import tkinter as tk
#import ttk
from tkinter import *
from HealthCareApp import *
#import os
import psycopg2

def connect(): 
    try: 
        conn = psycopg2.connect(database = os.environ.get('DATABASE_NAME'),  
                            user = os.environ.get('DATABASE_USER'),  
                            password = os.environ.get('DATABASE_PASSWORD'),  
                            host = "localhost",  
                            port = "5432") 
        cur = conn.cursor() 
    except (Exception, psycopg2.DatabaseError) as error: 
        print ("Error while connecting to PostgreSQL database", error) 
    return conn, cur 



def verify_user(log_app):
    conn, cur = connect()
    usr = username_login_entry.get()
    passw = password_login_entry.get()
    try: 
        cur.execute("SELECT username,password FROM account WHERE username='"+usr+"' and password='" + passw+"';") 
    except Exception as e: 
        print('error', e)  
    #conn.commit()
    try:
        row = cur.fetchone()
    except:
        print("Loging unsuccess!")
    if row:
        login_sucess()
        log_app.destroy()
        print("Login destroyed")
        print("Loging success!")
        start_app(row[0])
    else:
        print("Loging unsuccess!")
        user_not_found()

def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    Label(login_success_screen, text="Login Success").pack()
    Button(login_success_screen, text="OK", command=delete_login_success).pack()


# Designing popup for user not found
 
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()

# Deleting popups

def delete_login_success():
    login_success_screen.destroy()


def delete_password_not_recognised():
    password_not_recog_screen.destroy()


def delete_user_not_found_screen():
    user_not_found_screen.destroy()
    
login_screen = Tk()
login_screen.geometry("400x350")
login_screen.title("Account Login")
lbl1 = tk.Label(text="Welcome to the HealthCareApp!", bg="MediumSeaGreen", width="300", height="2", font=("Calibri", 13)).pack()
lbl2= tk.Label(text="Here you can contact us get possibility to login for using our app.").pack(padx=5, pady=5)
lbl3= tk.Label(login_screen, text="Please enter details below to login").pack()
global username_verify
global password_verify

username_verify = StringVar()
password_verify = StringVar()

global username_login_entry
global password_login_entry

Label(login_screen, text="Username * ").pack()
username_login_entry = Entry(login_screen, textvariable=username_verify)
username_login_entry.pack()
Label(login_screen, text="").pack()
Label(login_screen, text="Password * ").pack()
password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
password_login_entry.pack()
btn = tk.Button(login_screen, text="Login", height="2", width="30", command = lambda : verify_user(login_screen)).pack(padx=5, pady=5)
login_screen.mainloop()

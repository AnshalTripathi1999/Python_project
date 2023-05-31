from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter import GROOVE
import base64
import mysql.connector

# Function to establish database connection
def connect_to_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Anshal@123",
        database="pythonproject"
    )
    return conn

# Function to fetch data from the database
def fetch_data():
    conn = connect_to_database()
    cursor = conn.cursor()

    # Execute the SELECT query
    cursor.execute("SELECT encryption_text FROM encryption_data")

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Close the database connection
    conn.close()

    return rows

def decrypt():
    password = code.get()

    if password == "1234":
        conn = connect_to_database()
        cursor = conn.cursor()
        
        screen2 = Toplevel(screen)
        screen2.title("decryption")
        screen2.geometry("400x200")
        screen2.configure(bg="#00bd56")

        message = text1.get(1.0, END)
        decode_message = message.encode("ascii")
        base64_bytes = base64.b64decode(decode_message)
        decrypt = base64_bytes.decode("ascii")

        Label(screen2, text="DECRYPT", font="arial", fg="white", bg="#00bd56").place(x=10, y=0)
        text2 = Text(screen2, font="Rpbote 10", bg="white", relief=GROOVE, wrap=WORD, bd=0)
        text2.place(x=10, y=40, width=380, height=150)

        text2.insert(END, decrypt)
            
        # Insert decryption data into the database
        cursor.execute("INSERT INTO decryption_data (decryption_text) VALUES (%s)", (decrypt,))
        conn.commit()
        conn.close()

    elif password == "":
        messagebox.showerror("encryption", "Input Password")

    elif password != "1234":
        messagebox.showerror("encryption", "Invalid password")

    

def encrypt():
    password = code.get()

    if password == "1234":
        conn = connect_to_database()
        cursor = conn.cursor()
        
        screen1 = Toplevel(screen)
        screen1.title("encryption")
        screen1.geometry("400x200")
        screen1.configure(bg="#ed3833")

        message = text1.get(1.0, END)
        encode_message = message.encode("ascii")
        base64_bytes = base64.b64encode(encode_message)
        encrypt = base64_bytes.decode("ascii")

        Label(screen1, text="ENCRYPT", font="arial", fg="white", bg="#ed3833").place(x=10, y=0)
        text2 = Text(screen1, font="Rpbote 10", bg="white", relief=GROOVE, wrap=WORD, bd=0)
        text2.place(x=10, y=40, width=380, height=150)

        text2.insert(END, encrypt)
        
        # Insert encryption data into the database
        cursor.execute("INSERT INTO encryption_data (encryption_text) VALUES (%s)", (encrypt,))
        conn.commit()
        conn.close()

    elif password == "":
        messagebox.showerror("encryption", "Input Password")

    elif password != "1234":
        messagebox.showerror("encryption", "Invalid password")

def reset():
    code.set("")
    text1.delete(1.0, END)


def main_screen():
    global screen
    global code
    global text1

    screen = Tk()
    screen.geometry("375x450")

    # icon
    image_icon = ImageTk.PhotoImage(Image.open("logo.png"))
    screen.iconphoto(False, image_icon)
    screen.title("PctApp")

    Label(text="Enter text for encryption and decryption", fg="black", font=("calibri", 13)).place(x=10, y=10)
    text1 = Text(font="Robote 20", bg="white", relief=GROOVE, wrap=WORD, bd=0)
    text1.place(x=10, y=50, width=355, height=100)

    Label(text="Enter secret key for encryption and decryption", fg="black", font=("calibri", 13)).place(x=10, y=170)

    code = StringVar()
    Entry(textvariable=code, width=19, bd=0, font=("arial", 25), show="*").place(x=10, y=200)

    Button(text="ENCRYPT", height="2", width=23, bg="#ed3833", fg="white", bd=0, command=encrypt).place(x=10, y=250)
    Button(text="DECRYPT", height="2", width=23, bg="#00bd56", fg="white", bd=0, command=decrypt).place(x=200, y=250)
    Button(text="RESET", height="2", width=50, bg="#1089ff", fg="white", bd=0, command=reset).place(x=10, y=300)
    Button(text="FETCH DATA", height="2", width=18, bg="#ff8000", fg="white", bd=0, command=display_data).place(x=220, y=200)

    screen.mainloop()

def display_data():
    # Fetch data from the database
    rows = fetch_data()

    # Create a new window to display the data
    display_screen = Toplevel(screen)
    display_screen.title("Data Display")
    display_screen.geometry("400x200")

    # Create a Text widget to display the data
    text = Text(display_screen, font="Rpbote 10", bg="white", relief=GROOVE, wrap=WORD, bd=0)
    text.place(x=10, y=10, width=380, height=180)

    # Insert the fetched data into the Text widget
    for row in rows:
        text.insert(END, row[0] + "\n")

    display_screen.mainloop()

main_screen()

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import re

# Initialize SQLite database connection
conn = sqlite3.connect('PlacementManagement.db')
cursor = conn.cursor()

# Google Sheets API setup using environment variable
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = os.getenv('GOOGLE_CREDENTIALS_JSON')  # Get the path to credentials.json from environment variable
creds = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scope)
client = gspread.authorize(creds)
sheet = client.open('PlacementManagement').sheet1  # Ensure this name matches your Google Sheet

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS PLACEMENT_MANAGEMENT (
    STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME TEXT,
    EMAIL TEXT,
    ROLL_NO TEXT UNIQUE,
    GENDER TEXT,
    AGG TEXT,
    PLACE TEXT,
    PACK TEXT
)
''')
conn.commit()

# The rest of your functions and GUI setup goes here...

# Helper functions
def create_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PLACEMENT_MANAGEMENT (
        STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME TEXT,
        EMAIL TEXT,
        ROLL_NO TEXT UNIQUE,
        GENDER TEXT,
        AGG TEXT,
        PLACE TEXT,
        PACK TEXT
    )
    ''')
    conn.commit()

def display_records():
    for record in tree.get_children():
        tree.delete(record)
    cursor.execute('SELECT * FROM PLACEMENT_MANAGEMENT')
    records = cursor.fetchall()
    for record in records:
        tree.insert('', 'end', values=record)

def validate_fields(name, email, roll, agg, pack):
    # Validate email
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        messagebox.showerror('Error', 'Invalid email format.')
        return False

    # Validate roll number uniqueness
    cursor.execute('SELECT * FROM PLACEMENT_MANAGEMENT WHERE ROLL_NO = ?', (roll,))
    if cursor.fetchone():
        messagebox.showerror('Error', 'Roll number must be unique.')
        return False

    # Validate aggregate (CGPA 10 or percentage 100)
    try:
        agg_value = float(agg)
        if not (0 <= agg_value <= 10 or 0 <= agg_value <= 100):
            messagebox.showerror('Error', 'Aggregate must be either CGPA (0-10) or percentage (0-100).')
            return False
    except ValueError:
        messagebox.showerror('Error', 'Aggregate must be a numeric value.')
        return False

    # Validate package (only numerics)
    try:
        float(pack)
    except ValueError:
        messagebox.showerror('Error', 'Package must be a numeric value.')
        return False

    return True

def add_record():
    name = name_strvar.get()
    email = email_strvar.get()
    roll = roll_strvar.get()
    gender = gender_strvar.get()
    agg = agg_strvar.get()
    place = place_strvar.get()
    pack = pack_strvar.get()

    if not name or not email or not roll or not gender or not agg or not place or not pack:
        messagebox.showerror('Error', 'Please fill all fields.')
        return

    if not validate_fields(name, email, roll, agg, pack):
        return

    cursor.execute('INSERT INTO PLACEMENT_MANAGEMENT (NAME, EMAIL, ROLL_NO, GENDER, AGG, PLACE, PACK) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                   (name, email, roll, gender, agg, place, pack))
    conn.commit()
    display_records()
    export_to_google_sheets()
    reset_fields()

def remove_record():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror('Error', 'Please select a record to delete.')
        return
    selected_record = tree.item(selected_item)
    student_id = selected_record['values'][0]

    cursor.execute('DELETE FROM PLACEMENT_MANAGEMENT WHERE STUDENT_ID = ?', (student_id,))
    conn.commit()
    display_records()
    export_to_google_sheets()

def update_record():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror('Error', 'Please select a record to update.')
        return

    # Get the original roll number from the selected record
    original_roll = tree.item(selected_item)['values'][3]  # Assuming 'Roll No' is the 4th column

    # Get updated values from the input fields
    name = name_strvar.get()
    email = email_strvar.get()
    new_roll = roll_strvar.get()
    gender = gender_strvar.get()
    agg = agg_strvar.get()
    place = place_strvar.get()
    pack = pack_strvar.get()

    # Check if the roll number has changed
    if new_roll != original_roll:
        # If the roll number was changed, check if the new roll number is unique
        cursor.execute('SELECT * FROM PLACEMENT_MANAGEMENT WHERE ROLL_NO = ? AND STUDENT_ID != ?', (new_roll, tree.item(selected_item)['values'][0]))
        if cursor.fetchone():
            messagebox.showerror('Error', 'Roll number must be unique.')
            return

    # Update the record in the database
    student_id = tree.item(selected_item)['values'][0]
    cursor.execute('''
        UPDATE PLACEMENT_MANAGEMENT 
        SET NAME = ?, EMAIL = ?, ROLL_NO = ?, GENDER = ?, AGG = ?, PLACE = ?, PACK = ? 
        WHERE STUDENT_ID = ?
    ''', (name, email, new_roll, gender, agg, place, pack, student_id))
    conn.commit()

    # Refresh the display
    display_records()
    export_to_google_sheets()
    messagebox.showinfo('Success', 'Record updated successfully.')

def search_records():
    roll_number = roll_search_strvar.get()
    cursor.execute('SELECT * FROM PLACEMENT_MANAGEMENT WHERE ROLL_NO = ?', (roll_number,))
    records = cursor.fetchall()
    if not records:
        messagebox.showinfo('Search Result', 'No records found.')
        display_records()  # Show all records after no match found
        return
    for record in tree.get_children():
        tree.delete(record)
    for record in records:
        tree.insert('', 'end', values=record)

def export_to_google_sheets():
    cursor.execute('SELECT * FROM PLACEMENT_MANAGEMENT')
    records = cursor.fetchall()
    sheet.clear()
    sheet.append_row(['Student ID', 'Name', 'Email', 'Roll No', 'Gender', 'Aggregate', 'Placement', 'Package'])
    for record in records:
        sheet.append_row(record)

def reset_fields():
    name_strvar.set('')
    email_strvar.set('')
    roll_strvar.set('')
    gender_strvar.set('')
    agg_strvar.set('')
    place_strvar.set('')
    pack_strvar.set('')

def populate_fields(event):
    selected_item = tree.selection()
    if selected_item:
        record = tree.item(selected_item)['values']
        name_strvar.set(record[1])
        email_strvar.set(record[2])
        roll_strvar.set(record[3])
        gender_strvar.set(record[4])
        agg_strvar.set(record[5])
        place_strvar.set(record[6])
        pack_strvar.set(record[7])

# Main GUI setup
main = tk.Tk()
main.title('Placement Management System')
main.geometry('1200x600')
main.resizable(True, True)

# Frames
input_frame = tk.Frame(main)
input_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10, expand=True)
records_frame = tk.Frame(main)
records_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10, expand=True)
button_frame = tk.Frame(input_frame)
button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
search_frame = tk.Frame(input_frame)
search_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

# Input fields
canvas = tk.Canvas(input_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(input_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

tk.Label(scrollable_frame, text="Name").pack(pady=5)
name_strvar = tk.StringVar()
tk.Entry(scrollable_frame, textvariable=name_strvar).pack(pady=5)

tk.Label(scrollable_frame, text="Email").pack(pady=5)
email_strvar = tk.StringVar()
tk.Entry(scrollable_frame, textvariable=email_strvar).pack(pady=5)

tk.Label(scrollable_frame, text="Roll Number").pack(pady=5)
roll_strvar = tk.StringVar()
tk.Entry(scrollable_frame, textvariable=roll_strvar).pack(pady=5)

tk.Label(scrollable_frame, text="Gender").pack(pady=5)
gender_strvar = tk.StringVar()
ttk.Combobox(scrollable_frame, textvariable=gender_strvar, values=['Male', 'Female']).pack(pady=5)

tk.Label(scrollable_frame, text="Aggregate").pack(pady=5)
agg_strvar = tk.StringVar()
tk.Entry(scrollable_frame, textvariable=agg_strvar).pack(pady=5)

tk.Label(scrollable_frame, text="Placement").pack(pady=5)
place_strvar = tk.StringVar()
ttk.Combobox(scrollable_frame, textvariable=place_strvar, values=['GOOGLE', 'WIPRO', 'INFOSYS', 'MICROSOFT', 'JP MORGAN']).pack(pady=5)

tk.Label(scrollable_frame, text="Package").pack(pady=5)
pack_strvar = tk.StringVar()
tk.Entry(scrollable_frame, textvariable=pack_strvar).pack(pady=5)

# Buttons 
ttk.Button(button_frame, text="Add Record", command=add_record).pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="Update Record", command=update_record).pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="Remove Record", command=remove_record).pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="Reset Fields", command=reset_fields).pack(side=tk.LEFT, padx=5)

# Search Bar
tk.Label(search_frame, text="Search by Roll Number").pack(side=tk.LEFT, padx=5)
roll_search_strvar = tk.StringVar()
tk.Entry(search_frame, textvariable=roll_search_strvar).pack(side=tk.LEFT, padx=5)
ttk.Button(search_frame, text="Search", command=search_records).pack(side=tk.LEFT, padx=5)

# Treeview (Records Display)
tree = ttk.Treeview(records_frame, columns=('ID', 'Name', 'Email', 'Roll No', 'Gender', 'Aggregate', 'Placement', 'Package'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Name', text='Name')
tree.heading('Email', text='Email')
tree.heading('Roll No', text='Roll No')
tree.heading('Gender', text='Gender')
tree.heading('Aggregate', text='Aggregate')
tree.heading('Placement', text='Placement')
tree.heading('Package', text='Package')

tree.column('ID', width=30)
tree.column('Name', width=120)
tree.column('Email', width=180)
tree.column('Roll No', width=100)
tree.column('Gender', width=80)
tree.column('Aggregate', width=80)
tree.column('Placement', width=120)
tree.column('Package', width=100)

tree.pack(fill=tk.BOTH, expand=True)
tree.bind('<<TreeviewSelect>>', populate_fields)

# Initial population of records
display_records()

main.mainloop()

# Close the database connection
conn.close()
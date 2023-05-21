import tkinter as tk
from tkinter import ttk
import pyodbc

# login information
server = 'localhost'
username = 'vmdapp'
password = 'VMD22041748'

# create connection string
conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};UID={username};PWD={password}"

# make connection
conn = pyodbc.connect(conn_str)

# get list of available databases
cursor = conn.cursor()
cursor.execute("SELECT name FROM sys.databases WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb')")
databases = [row.name for row in cursor.fetchall()]

# create window and set title
window = tk.Tk()
window.title("Consulta Rejeição")

# create label and combobox for selecting database
db_label = tk.Label(window, text='Select database:')
db_label.grid(row=0, column=0, padx=10, pady=10)

db_combobox = ttk.Combobox(window, values=databases)
db_combobox.grid(row=0, column=1, padx=10, pady=10)

# create entry field for nota number
label = tk.Label(window, text='Enter nota number:')
label.grid(row=1, column=0, padx=10, pady=10)

entry = tk.Entry(window)
entry.grid(row=1, column=1, padx=10, pady=10)

# create "Consult" button
def consultar():
    # get selected database and nota number
    database = db_combobox.get()
    num_nota = entry.get()

    # check if database and nota number are valid
    conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(f"SELECT Num_Nota, Des_Xmotivo, Des_Xjust FROM FS_NFXML WHERE Num_Nota = '{num_nota}'")
    results = cursor.fetchall()
    if len(results) == 0:
        # invalid nota number
        error_label.config(text='Enter a valid nota number.', fg='red')
        text.delete('1.0', tk.END)
    else:
        # valid nota number, display rejection information
        error_label.config(text='')
        text.delete('1.0', tk.END)
        for row in results:
            des_xjust = row.Des_Xjust if row.Des_Xjust is not None else 'No justification provided'
            text.insert(tk.END, f"Nota number: {row.Num_Nota}\nRejection reason: {row.Des_Xmotivo}\nJustification: {des_xjust}\n\n")

button = tk.Button(window, text='Consult', command=consultar)
button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# create text field to display results
text = tk.Text(window)
text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# create label to display errors
error_label = tk.Label(window)
error_label.grid(row=4, column=0, columnspan=2)

# create "Refresh" button
def atualizar():
    # clear entry and text fields
    entry.delete(0, tk.END)
    text.delete('1.0', tk.END)
    error_label.config(text='')

refresh_button = tk.Button(window, text='Refresh', command=atualizar)
refresh_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# start window
window.mainloop()

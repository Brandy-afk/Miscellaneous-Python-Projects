from tkinter import messagebox
import requests
from datetime import *
from tkinter import *
import os
from dotenv import load_dotenv

load_dotenv()

PIXELA_ENDPOINT = 'https://pixe.la/v1/users'
token = os.getenv('TOKEN')
username = os.getenv('USERNAME')

headers = {
    'X-USER-TOKEN': token
}

user_params = {
    'token': token,
    'username': username,
    'agreeTermsOfService': 'yes',
    'notMinor': 'yes'
}


graph_endpoint = f"{PIXELA_ENDPOINT}/{username}/graphs"

def check_input(callback, isDelete=False):
    selected_index = graph_ID_choices.curselection()
    if (isDelete or check_value()) and selected_index:
        callback(selected_index)
    else:
        messagebox.showerror(title='Bad Value Input!', message='Please try again!')


def check_value():
    try:
        float(value_entry.get())
        return True
    except ValueError:
        return False


def on_delete_pressed():
    check_input(delete_data, True)
    return;


def on_update_pressed():
    check_input(update_data)


def on_add_data_pressed():
    check_input(add_data)


def delete_data(index):
    the_date = datetime.now().strftime('%Y%m%d')
    endpoint = f"{graph_endpoint}/{graph_ID_choices.get(index)}/{the_date}"

    response = requests.delete(url=endpoint, headers=headers)
    response.raise_for_status()
    messagebox.showinfo(title='Success', message=f"Values deleted for {the_date}")


def update_data(index):
    params = {
        'quantity': value_entry.get()
    }

    today = datetime.today()
    the_date = today.strftime('%Y%m%d')

    endpoint = f"{graph_endpoint}/{graph_ID_choices.get(index)}/{the_date}"

    response = requests.put(url=endpoint, headers=headers, json=params)
    response.raise_for_status()
    messagebox.showinfo(title="Success", message=f"Updated a value of {params['quantity']} on {the_date}")
    value_entry.delete(0, END)
    return;


def add_data(index):
    params = {
        'date': datetime.now().strftime('%Y%m%d'),
        'quantity': value_entry.get()
    }

    endpoint = f"{PIXELA_ENDPOINT}/{username}/graphs/{graph_ID_choices.get(index)}"

    response = requests.post(url=endpoint, json=params, headers=headers)
    response.raise_for_status()
    messagebox.showinfo(title="Success", message=f"Added a value of {params['quantity']} on {params['date']}")
    value_entry.delete(0, END)


window = Tk()
window.title("Habit Tracker")
window.config(padx=20, pady=20)

title_label = Label(window, text="Habit Tracker\nAdd Data", font=("Helvetica", 20, 'bold'))
title_label.grid(row=0, column=1)

graph_label = Label(window, text="Graph ID")
graph_label.grid(row=1, column=0)

value_label = Label(window, text='Value')
value_label.grid(row=2, column=0)

graph_ID_choices = Listbox(window, height=3)
graph_ID_choices.insert(END, 'graph1')
graph_ID_choices.grid(row=1, column=1, columnspan=2)
value_entry = Entry(window)
value_entry.grid(row=2, column=1, columnspan=2)
add_button = Button(window, text='Write Data', command=on_add_data_pressed, width=16)
add_button.grid(row=3, column=1, columnspan=2)
delete_button = Button(window, text='Delete Data', command=on_delete_pressed, width=16)
delete_button.grid(row=5, column=1, columnspan=2)
update_button = Button(window, text='Update Data', command=on_update_pressed, width=16)
update_button.grid(row=4, column=1, columnspan=2)

window.mainloop()

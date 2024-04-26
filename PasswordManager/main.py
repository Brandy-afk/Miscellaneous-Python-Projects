from json import JSONDecodeError
from tkinter import *
from tkinter import messagebox
import json
import string
import random
import pyperclip

# ---------------------------- CONSTANTS ------------------------------- #
PASSWORD_LENGTH = 12


# ---------------------------- SEARCH ------------------------------- #
def on_search_pressed():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            site_dict = data[site_entry.get()]
            _create_search_popup(f"Email: {site_dict['email']} \n"
                                 f"Password: {site_dict['password']}")
    except (FileNotFoundError, KeyError):
        _create_search_popup("Website info not found!")


def _create_search_popup(message):
    messagebox.showinfo(title="Search Results", message=message)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def on_generate_pressed():
    password_entry.delete(0, END)
    new_password = _generate_password()
    pyperclip.copy(new_password)
    password_entry.insert(0, new_password)


def _generate_password(length=PASSWORD_LENGTH):
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    punctuation = string.punctuation

    all_chars = uppercase + lowercase + digits + punctuation
    return ''.join(random.choice(all_chars) for i in range(length))


# ---------------------------- SAVE PASSWORD ------------------------------- #

def on_add_password():
    if not _check_fields():
        return

    is_okay = messagebox.askyesno(title="New Password", message="Do you want to add this info? \n"
                                                                f"Website: {site_entry.get()} \n"
                                                                f"Email: {email_entry.get()} \n"
                                                                f"Password: {password_entry.get()}")
    if is_okay:
        _add_password_to_file()
        _reset_values()
    else:
        _reset_values()


def _check_fields():
    if not _check_size(1, site_entry, site_entry):
        create_input_error("Please enter valid email and website")
        return False
    elif not _check_size(PASSWORD_LENGTH, password_entry):
        create_input_error(f"Please enter valid password - {PASSWORD_LENGTH} characters long")
        return False
    else:
        return True


def create_input_error(message):
    messagebox.showerror("Input Error", message)


def _check_size(size, *args):
    for arg in args:
        if len(arg.get()) < size:
            return False
    return True


def _add_password_to_file():
    new_data = {
        site_entry.get():
            {
                'email': email_entry.get(),
                'password': password_entry.get(),
            }
    }

    try:
        with open('data.json', 'r') as data_file:
            data = json.load(data_file)
            data.update(new_data)

        with open('data.json', 'w') as data_file:
            json.dump(data, data_file, indent=4)
    except FileNotFoundError:
        with open('data.json', 'w') as data_file:
            json.dump(new_data, data_file, indent=4)

    messagebox.showinfo(title="New Password", message="Added!")


def _reset_values():
    password_entry.delete(0, END)
    email_entry.delete(0, END)
    site_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

# def center_window(tk_window):
#     tk_window.update_idletasks()
#     width = tk_window.winfo_width()
#     height = tk_window.winfo_height()
#     x_offset = (tk_window.winfo_screenwidth() - width) // 2
#     y_offset = (tk_window.winfo_screenheight() - height) // 2
#     tk_window.geometry(f"{width}x{height}+{x_offset}+{y_offset}")

window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50)

lock_image = PhotoImage(file='logo.png')
photo_canvas = Canvas(window, width=200, height=200)
photo_canvas.create_image(100, 100, image=lock_image)
photo_canvas.grid(row=0, column=1)

site_label = Label(text="Website: ")
site_label.grid(row=1, column=0)
email_label = Label(text="Username/Email: ")
email_label.grid(row=2, column=0)
password_label = Label(text="Password: ")
password_label.grid(row=3, column=0)

site_entry = Entry(width=32)
site_entry.grid(row=1, column=1, sticky='w')
email_entry = Entry(width=44)
email_entry.grid(row=2, column=1, columnspan=2, sticky='w')
password_entry = Entry(width=32)
password_entry.grid(row=3, column=1, sticky='w')

add_button = Button(text="Add", width=36, command=on_add_password)
add_button.grid(row=4, column=1, columnspan=2, sticky='w')
generate_button = Button(text="Generate", command=on_generate_pressed, width=8)
generate_button.grid(row=3, column=2, sticky='w')
search_button = Button(text="Search", command=on_search_pressed, width=8)
search_button.grid(row=1, column=2, sticky='w')

# center_window(window)

window.mainloop()

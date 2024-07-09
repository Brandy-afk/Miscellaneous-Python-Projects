from tkinter import *
from core import Core
from tkinter import ttk
from tkinter import messagebox
from player import Player


# UI class
class Application(Tk):
    def __init__(self, core: Core) -> None:
        super().__init__()
        self.core = core
        self.minsize(width=400, height=400)
        self.config(padx=30, pady=30, bg="#F0F0F0")
        self.title("Sports Statistic Tracker")

        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12), padding=5, background="#F0F0F0")
        style.configure("TEntry", font=("Arial", 12), padding=5)
        style.configure("TButton", font=("Arial", 12), padding=10, background="#4CAF50", foreground="black")
        style.map("TButton", background=[("active", "#3E8E41")])

        title_label = ttk.Label(self, text="Sports Statistic Tracker", font=("Arial", 20), justify="center",
                                foreground="#4CAF50")
        title_label.pack()
        subtitle_label = ttk.Label(self, text="Insert information to add, get, update, or delete players",
                                   font=("Arial", 8))
        subtitle_label.pack()
        subtitle_label2 = ttk.Label(self, text="First and Last name is always required.\n",
                                    font=("Arial", 8))
        subtitle_label2.pack()

        first_name_label = ttk.Label(self, text="First Name")
        first_name_label.pack(anchor="w")
        self.first_name_entry = ttk.Entry(self)
        self.first_name_entry.pack(anchor="w", fill="x")

        last_name_label = ttk.Label(self, text="Last Name")
        last_name_label.pack(anchor="w")
        self.last_name_entry = ttk.Entry(self)
        self.last_name_entry.pack(anchor="w", fill="x")

        self.entries_frame = ttk.Frame(self)
        self.entries_frame.pack(anchor="w", fill="x")

        sport_label = ttk.Label(self, text="Sport")
        sport_label.pack(anchor="w", in_=self.entries_frame)
        self.sport_var = StringVar()
        self.sport_var.set("Football")
        sport_frame = ttk.Frame(self)
        sport_frame.pack(anchor="w", in_=self.entries_frame)
        sport_radio1 = ttk.Radiobutton(sport_frame, text="Football", variable=self.sport_var, value="Football")
        sport_radio1.pack(side="left")
        sport_radio2 = ttk.Radiobutton(sport_frame, text="Basketball", variable=self.sport_var, value="Basketball")
        sport_radio2.pack(side="left")
        sport_radio3 = ttk.Radiobutton(sport_frame, text="Baseball", variable=self.sport_var, value="Baseball")
        sport_radio3.pack(side="left")

        team_label = ttk.Label(self, text="Team")
        team_label.pack(anchor="w", in_=self.entries_frame)
        self.team_entry = ttk.Entry(self)
        self.team_entry.pack(anchor="w", fill="x", in_=self.entries_frame)

        number_label = ttk.Label(self, text="Number")
        number_label.pack(anchor="w", in_=self.entries_frame)
        self.number_entry = ttk.Entry(self)
        self.number_entry.pack(anchor="w", fill="x", in_=self.entries_frame)

        position_label = ttk.Label(self, text="Position")
        position_label.pack(anchor="w", in_=self.entries_frame)
        self.position_var = StringVar()
        self.position_var.set("Defense")
        self.position_listbox = Listbox(self, height=3, bg="#E0E0E0", fg="#333333")
        self.position_listbox.pack(anchor="w", fill="x", in_=self.entries_frame)
        self.position_listbox.insert(1, "Defense")
        self.position_listbox.insert(2, "Offense")
        self.position_listbox.insert(3, "Both")

        points_label = ttk.Label(self, text="Points")
        points_label.pack(anchor="w", in_=self.entries_frame)
        self.points_var = IntVar()
        self.points_var.set(0)
        self.points_spinbox = ttk.Spinbox(self, from_=0, to=100, textvariable=self.points_var, width=5)
        self.points_spinbox.pack(anchor="w", in_=self.entries_frame)

        fouls_label = ttk.Label(self, text="Fouls")
        fouls_label.pack(anchor="w", in_=self.entries_frame)
        self.fouls_var = IntVar()
        self.fouls_var.set(0)
        self.fouls_spinbox = ttk.Spinbox(self, from_=0, to=10, textvariable=self.fouls_var, width=5)
        self.fouls_spinbox.pack(anchor="w", in_=self.entries_frame)

        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=20)

        toggle_button = ttk.Button(self.button_frame, text="Toggle Entries", command=self.toggle_entries)
        toggle_button.pack(pady=20)

        add_button = ttk.Button(self.button_frame, text="Add Player", command=self.on_add_pressed)
        add_button.pack(side="left", padx=5)

        get_button = ttk.Button(self.button_frame, text="Get Player", command=self.on_get_pressed)
        get_button.pack(side="left", padx=5)

        update_button = ttk.Button(self.button_frame, text="Update Player", command=self.on_update_pressed)
        update_button.pack(side="left", padx=5)

        delete_button = ttk.Button(self.button_frame, text="Delete Player", command=self.on_delete_pressed)
        delete_button.pack(side="left", padx=5)

        clear_button = ttk.Button(self.button_frame, text="Clear", command=self.on_clear_pressed)
        clear_button.pack(side="left", padx=5)

        self.entries_visible = True

        self.mainloop()

    def on_add_pressed(self):
        player = self.create_player()
        if player:
            if self.core.add_player(player):
                messagebox.showinfo("Success", "Player added successfully.")
                self.clear_inputs()
            else:
                messagebox.showerror("Error", "Player already exists")
        else:
            self.show_name_error()

    def on_update_pressed(self):
        player = self.create_player()
        if player:
            response = messagebox.askyesno('Update Type',
                                           'YES to override with new stats, NO to add on to existing values')
            if self.core.update_player(player, response):
                messagebox.showinfo("Success!", "Player updated successfully.")
                self.clear_inputs()
            else:
                messagebox.showerror("Error", "Player does not exist.")
        else:
            self.show_name_error()

    def on_get_pressed(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()

        if first_name and last_name:
            player = self.core.get_player(first_name, last_name)
            if player:
                stats_message = f"First Name: {player.first_name}\n"
                stats_message += f"Last Name: {player.last_name}\n"
                stats_message += f"Sport: {player.sport}\n"
                stats_message += f"Team: {player.team}\n"
                stats_message += f"Number: {player.number}\n"
                stats_message += f"Position: {player.position}\n"
                stats_message += f"Date Added: {player.date_added}\n"
                stats_message += f"Points: {player.points}\n"
                stats_message += f"Fouls: {player.fouls}"
                messagebox.showinfo("Player Stats", stats_message)
            else:
                messagebox.showerror("Error", "Player does not exist.")
        else:
            self.show_name_error()

    def on_delete_pressed(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        if first_name and last_name:
            if self.core.delete_player(first_name, last_name):
                messagebox.showinfo("Success!", "Player deleted successfully.")
                self.clear_inputs()
            else:
                messagebox.showerror("Error", "Player does not exist.")
        else:
            self.show_name_error()

    def show_name_error(self):
        messagebox.showerror("Error", "Please enter both first name and last name.")

    def on_clear_pressed(self):
        confirm = messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all inputs?")
        if confirm:
            self.clear_inputs()

    def create_player(self) -> Player:
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        sport = self.sport_var.get()
        team = self.team_entry.get()

        numberString = self.number_entry.get()
        if numberString:
            number = int(numberString)
        else:
            number = '0'

        if self.position_listbox.curselection():
            index = self.position_listbox.curselection()[0]
            position = self.position_listbox.get(index)
        else:
            position = ""  # or provide a default value
        points = self.points_var.get()
        fouls = self.fouls_var.get()

        if first_name and last_name:
            return Player(first_name, last_name, sport, team, number, position, points, fouls)
        else:
            return None

    def clear_inputs(self):
        self.first_name_entry.delete(0, END)
        self.last_name_entry.delete(0, END)
        self.sport_var.set("Football")
        self.team_entry.delete(0, END)
        self.number_entry.delete(0, END)
        self.position_listbox.selection_clear(0, END)
        self.position_listbox.selection_set(0)
        self.points_spinbox.set(0)
        self.fouls_spinbox.set(0)

    def toggle_entries(self):
        if self.entries_visible:
            self.entries_frame.pack_forget()
        else:
            self.button_frame.pack_forget()
            self.entries_frame.pack(anchor="w", fill="x")
            self.button_frame.pack(anchor='w', fill='x')

        self.entries_visible = not self.entries_visible

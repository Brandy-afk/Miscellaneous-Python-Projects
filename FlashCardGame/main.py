import csv
from tkinter import *
from tkinter import messagebox

import pandas
import random
import json
import os

# ------------------------------CONSTANTS-----------------------------------#
BACKGROUND_COLOR = "#B1DDC6"
FONT = "Helvetica"
TIME_TO_GUESS = 3


# ------------------------------VARIABLES-----------------------------------#
class GameTracker:
    def __init__(self):
        self.score = 0
        self.current_word = ""


df = pandas.read_csv("data/french_words.csv")
word_dict = {row.English: row.French for index, row in df.iterrows()}
try:
    with open("data/learned_words.json", "r") as data_file:
        learned_words = json.load(data_file)
    english_word_list = [word for word in df['English'].tolist() if word not in learned_words]
except FileNotFoundError:
    english_word_list = df['English'].tolist()

game_tracker = GameTracker()


# ------------------------------LOGIC-----------------------------------#


def get_new_word():
    cancel_action()
    if len(english_word_list) == 0:
        on_completion()
        return

    game_tracker.current_word = random.choice(english_word_list)
    set_up_french_card()
    window.action_id = window.after(TIME_TO_GUESS * 1000, set_up_english_card)


def on_completion():
    is_yes = messagebox.askyesno(title="Completed!", message=f"You completed all {len(word_dict)} words\n"
                                                             f"Would you like to play again?")
    os.remove('learned_words.txt')
    if not is_yes:
        window.quit()
    else:
        global english_word_list
        english_word_list = df['English'].tolist()
        get_new_word()


def set_up_french_card():
    flash_card.itemconfig(card_image, image=card_front)
    flash_card.itemconfig(title_text, text='French', fill='black')
    flash_card.itemconfig(word_text, text=word_dict[game_tracker.current_word], fill='black')
    return


def set_up_english_card():
    flash_card.itemconfig(card_image, image=card_back)
    flash_card.itemconfig(title_text, text='English', fill='white')
    flash_card.itemconfig(word_text, text=game_tracker.current_word, fill='white')
    return


def on_correct_pressed():
    english_word_list.remove(game_tracker.current_word)
    save_learned_word()
    get_new_word()


def save_learned_word():
    try:
        with open('learned_words.txt', 'r') as file:
            data = json.load(file)
            data.append(game_tracker.current_word)
        with open('learned_words.txt', 'w') as file:
            json.dump(data, file)
    except FileNotFoundError:
        with open('learned_words.txt', 'w') as file:
            json.dump([game_tracker.current_word], file)


def cancel_action():
    # hasattr checks to see if the object "window' has the attribute 'action_id'
    if hasattr(window, 'action_id'):
        window.after_cancel(window.action_id)


# ------------------------------UI-----------------------------------#


window = Tk()
window.title("Flash Cards")
window.config(padx=40, pady=40, bg=BACKGROUND_COLOR)

card_back = PhotoImage(file="images/card_back.png")
card_front = PhotoImage(file="images/card_front.png")
correct_image = PhotoImage(file="images/right.png")
wrong_image = PhotoImage(file="images/wrong.png")

flash_card = Canvas(width=800, height=550, highlightthickness=0, bg=BACKGROUND_COLOR)
card_image = flash_card.create_image(400, 275, image=card_front)
title_text = flash_card.create_text(400, 150, text="French", font=(FONT, 30, 'italic'), fill='black')
word_text = flash_card.create_text(400, 250, text="Word", font=(FONT, 50, 'bold'), fill='black')
flash_card.grid(row=0, column=0, columnspan=2)

correct_button = Button(image=correct_image, bg=BACKGROUND_COLOR, highlightthickness=0, command=on_correct_pressed)
correct_button.grid(row=1, column=1)
wrong_button = Button(image=wrong_image, bg=BACKGROUND_COLOR, highlightthickness=0, command=get_new_word)
wrong_button.grid(row=1, column=0)

get_new_word()
window.mainloop()

from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #

BACKGROUND_COLOR = '#FFE4E1'
CHECK_MARK = "✔"
GREEN = "#9bdeac"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# ---------------------------- TIMER RESET ------------------------------- #
reset = False


def on_reset_pressed():
    global reset
    reset = True
    update_time_text(0)
    check_box['text'] = ""
    status_label.config(text='Timer', fg='#7C1949')

# ---------------------------- TIMER MECHANISM ------------------------------- #
def on_start_pressed():
    global reset
    reset = False
    status_label.config(text='Work', fg='red')
    countdown_timer(WORK_MIN * 60, on_main_timer_end)


def on_main_timer_end():
    check_text = check_box['text']
    status_label.config(text='Break', fg=GREEN)
    if len(check_text) < 3:
        countdown_timer(SHORT_BREAK_MIN * 60, on_break_timer_end)
        check_text += CHECK_MARK
        check_box['text'] = check_text
    else:
        countdown_timer(LONG_BREAK_MIN * 60, on_break_timer_end)
        check_box['text'] = ""


def on_break_timer_end():
    on_start_pressed()


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def update_time_text(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    canvas.itemconfig(time_item, text=f"{minutes:02d}:{seconds:02d}")


def countdown_timer(seconds, callback):
    global reset
    if seconds > 0 and not reset:
        update_time_text(seconds)
        window.after(1000, countdown_timer, seconds - 60, callback)
    else:
        if reset:
            reset = False
        else:
            callback()


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Timer Applications")
window.minsize(400, 200)
window.geometry("+500+250")
window.config(bg=BACKGROUND_COLOR, padx=100, pady=50)

canvas = Canvas(width=200, height=224, bg=BACKGROUND_COLOR, highlightthickness=0)
image = PhotoImage(file='tomato.png')
canvas.create_image(100, 112, image=image)
time_item = canvas.create_text(100, 112, text="00:00", font=(FONT_NAME, 30, 'bold'), fill='white')
canvas.grid(column=1, row=1)

status_label = Label(text="Timer", font=(FONT_NAME, 36, 'bold'), bg=BACKGROUND_COLOR, fg='#7C1949')
check_box = Label(text="", font=(FONT_NAME, 24), bg=BACKGROUND_COLOR, fg=GREEN)
start_button = Button(text="Start", font=(FONT_NAME, 14), command=on_start_pressed)
reset_button = Button(text="Reset", font=(FONT_NAME, 14), command=on_reset_pressed)

status_label.grid(row=0, column=1)
start_button.grid(row=2, column=0)
reset_button.grid(row=2, column=2)
check_box.grid(row=3, column=1)

window.mainloop()

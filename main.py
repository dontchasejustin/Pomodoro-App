from tkinter import *
from tkinter import messagebox
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Helvetica"
WORK_MIN = 25  # Minutes
SHORT_BREAK_MIN = 5  # Minutes
LONG_BREAK_MIN = 20  # Minutes
PAUSE = 60  # Seconds

# # Test Values
# WORK_MIN = 2/60  # Minutes
# SHORT_BREAK_MIN = 5/60  # Minutes
# LONG_BREAK_MIN = 20/60  # Minutes
# PAUSE = 3  # Seconds

reps = 0
reset_already = True
timer = None


def reset_session():
    global reps, reset_already
    if reset_already:
        pass   
    else:
        window.after_cancel(timer)
        canvas.itemconfig(timer_text, text="00:00")
        reset_already = True
        if reps > 0:
            reps -= 1


def reset():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    status.config(text='Get started?')
    check_marks.config(text='')
    global reps
    reps = 0


def start_timer():
    global reps
    global reset_already

    reset_session()
    reset_already = False
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # print(reps)

    if reps % 8 == 0:
        countdown(long_break_sec)
        status.config(text="Take a long break!", fg="RED")
    elif reps % 2 == 0:
        countdown(short_break_sec)
        status.config(text="Take a short break!", fg="PINK")
    else:
        countdown(work_sec)
        status.config(text="Work!", fg=GREEN)


def restart_timer():
    global reps, reset_already
    reset_session()
    reset_already = False
    seconds = int(reset_amount.get())
    countdown(seconds)
    reps += 1
    # for i in range(PAUSE, 0, -1):  # "Pause" the app by putting it to sleep for a set length of time, not ideal
    #     time.sleep(1)
    #     # print(i)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def countdown(count):
    global reps, timer
    # "00:00", where count is in seconds
    mins_left = math.floor(count / 60)
    secs_left = int(count % 60)

    if secs_left < 10:
        secs_left = f'0{secs_left}'  # Format seconds to :00 instead of :9 when under 10
    time_display = f'{mins_left}:{secs_left}'

    canvas.itemconfig(timer_text, text=time_display)
    if count > 0:  # Stop counter at 0:00, when there are no seconds left
        timer = window.after(1000, countdown, count - 1)
    else:
        messagebox.showinfo(title='Session Status', message='Your session has ended!')
        start_timer()
        if reps % 2 == 0 and reps > 0:  # Add a check mark at start of each break (after first)
            checks = int(reps/2) * '✔'
            check_marks.config(text=checks)


# ---------------------------- UI SETUP ------------------------------- #
# Create application window
window = Tk()
window.config(padx=100, pady=100, bg=YELLOW)
window.minsize(width=500, height=500)
window.title('Pomodoro Timer')


# Create background image
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file='tomato.gif')
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill='white', font=('FONT_NAME', 36, 'bold'))
canvas.grid(column=1, row=1)

# Create labels and objects
status = Label(text='Get Started?', font=(FONT_NAME, 36, 'bold'), bg=YELLOW, fg=RED)
status.grid(column=1, row=0)

start_button = Button(text='(Re)Start', font=(FONT_NAME, 16, 'normal'), bg=GREEN, command=start_timer)
start_button.grid(column=0, row=2)

start_at_button = Button(text='Restart at...', font=(FONT_NAME, 16, 'normal'), bg=GREEN, command=restart_timer)
start_at_button.grid(column=1, row=2)

reset_session_button = Button(text='Reset Session', font=(FONT_NAME, 16, 'normal'), bg=RED, command=reset_session)
reset_session_button.grid(column=2, row=2)

reset_button = Button(text='Reset Progress', font=(FONT_NAME, 16, 'normal'), bg=RED, command=reset)
reset_button.grid(column=2, row=3)

reset_amount = Entry()
reset_amount.focus()
reset_amount.insert('end', '60')
reset_amount.grid(column=1, row=3)

check_marks = Label(text='', font=(FONT_NAME, 32, 'bold'), bg=YELLOW, fg=GREEN)
check_marks.grid(column=0, row=3)

window.mainloop()

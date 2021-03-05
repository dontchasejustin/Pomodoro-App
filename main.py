""" Program creates a "Pomodoro Timer" app that iterates through 4 work sessions of 25 minutes with 5 minutes breaks 
in between, with the 4th session being followed by a 20 minute long break. Monitors progress with check marks on screen. 

You can reset the timer to a specific interval, reset the current session to 00:00 without losing progress, 
or reset the app without closing it completely. Notifies user with a flashing popup box (and sound when run on a 
machine) when each session ends! """

# Todo: Disable start button while counter is not at 00:00

from tkinter import *
from tkinter import messagebox
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Helvetica"
# WORK_MIN = 25  # Minutes
# SHORT_BREAK_MIN = 5  # Minutes
# LONG_BREAK_MIN = 20  # Minutes
# PAUSE = 60  # Seconds, set for the time.sleep operation (disabled)

# Test values to replace normal usage values. Uncomment and comment out the constants above.
WORK_MIN = 2 / 60  # Minutes
SHORT_BREAK_MIN = 5 / 60  # Minutes
LONG_BREAK_MIN = 20 / 60  # Minutes
PAUSE = 3  # Seconds

reps = 0
reset_already = False
app_started = False
timer = None


def reset_session():
    """Reverts session to '00:00' while maintaining app progress (check marks). Pressing 'Start' button begins session
    over with original values."""
    global reps, reset_already
    if reset_already:  # Prevents reverting to previous task
        pass
    else:
        window.after_cancel(timer)
        canvas.itemconfig(timer_text, text="00:00")
        reset_already = True
        if reps > 0:
            reps -= 1


def reset():
    """Reverts app to original status, removing any progress (check marks) and resetting the apps details. Timer set to
    '00:00', pressing 'Start' begins the initial work session as when the app is first launched."""
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    status.config(text='Get started?')
    check_marks.config(text='')
    global reps
    reps = 0


def start_timer():
    """Prepares timer countdown by calculating session lengths & values, as well as what the current session is (work,
    short break, long break). Displays session status, then calls the 'countdown' function to begin timer operation."""
    global reps, reset_already, app_started

    # if app_started:
    #     reset_session()
    #     reset_already = False
    # else:
    #     app_started = True

    reset_already = False

    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    print(reps)

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
    """Restarts timer in the same session at on user specified length from the entry field, currently in seconds.
    Relies on 'reset_session' function to cancel timer operation and then calls 'countdown' function to begin timer
    with specified length."""
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
    """Operates timer countdown and time remaining display. Prompts user with a messagebox when each session has ended,
    not beginning next session until the messagebox is closed.

    Also responsible for tracking progress with visible check marks on screen."""
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
            checks = int(reps / 2) * '✔'
            check_marks.config(text=checks)


# ---------------------------- UI SETUP ------------------------------- #
# Create application window
window = Tk()
window.config(padx=100, pady=100, bg=YELLOW)
window.minsize(width=500, height=500)
window.title('Pomodoro Timer')

# Create background image & text object on canvas
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file='tomato.gif')
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill='white', font=('FONT_NAME', 36, 'bold'))
canvas.grid(column=1, row=1)

# Create labels and objects
status = Label(text='Get Started?', font=(FONT_NAME, 36, 'bold'), bg=YELLOW, fg=RED)
status.grid(column=1, row=0)

start_button = Button(text='Start', font=(FONT_NAME, 16, 'normal'), bg=GREEN, command=start_timer)
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

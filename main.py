from tkinter import *

# constants
TOMATO_IMG = "tomato.png"
BACKGROUND_COLOR = "#F6F7C1"
GREEN_COLOR = "#AACB73"
LIGHT_RED_COLOR = "#DD5353"
DEEP_RED_COLOR = "#B73E3E"
BLACK_COLOR = "#000000"
FONT = "Arial"

WORK_TIME = 25
SHORT_BREAK_TIME = 5
LONG_BREAK_TIME = 15
SECONDS = 0
COMPLETED = 0
completed_study = 0
running = None


def stop():
    screen.after_cancel(running)


def work_time():
    global WORK_TIME, SECONDS, COMPLETED, running, completed_study
    pomodoro_label.config(text="Work Time", fg=GREEN_COLOR)
    running = screen.after(1000, work_time)
    if running:
        if len(str(SECONDS)) < 2:
            canvas_tomato.itemconfig(text, text=f"{WORK_TIME} : 0{SECONDS}")
        else:
            canvas_tomato.itemconfig(text, text=f"{WORK_TIME} : {SECONDS}")
        if WORK_TIME > -1:
            if SECONDS == 0 and WORK_TIME != 0:
                WORK_TIME -= 1
                SECONDS = 60
            elif SECONDS == 0 and WORK_TIME == 0:
                WORK_TIME = 25
                completed_study += 1
                stop()
            else:
                SECONDS -= 1


def short_break_time():
    global SHORT_BREAK_TIME, SECONDS, COMPLETED, running
    pomodoro_label.config(text="Short Break", fg=LIGHT_RED_COLOR)
    running = screen.after(1000, short_break_time)
    if len(str(SECONDS)) < 2:
        canvas_tomato.itemconfig(text, text=f"{SHORT_BREAK_TIME} : 0{SECONDS}")
    else:
        canvas_tomato.itemconfig(text, text=f"{SHORT_BREAK_TIME} : {SECONDS}")
    if SHORT_BREAK_TIME > -1:
        if SECONDS == 0 and SHORT_BREAK_TIME != 0:
            SHORT_BREAK_TIME -= 1
            SECONDS = 60
        elif SECONDS == 0 and SHORT_BREAK_TIME == 0:
            SHORT_BREAK_TIME = 5
            stop()
        else:
            SECONDS -= 1


def long_break_time():
    global LONG_BREAK_TIME, SECONDS, COMPLETED, running, completed_study
    pomodoro_label.config(text="Long Break", fg=LIGHT_RED_COLOR)
    running = screen.after(1000, long_break_time)
    if len(str(SECONDS)) < 2:
        canvas_tomato.itemconfig(text, text=f"{LONG_BREAK_TIME} : 0{SECONDS}")
    else:
        canvas_tomato.itemconfig(text, text=f"{LONG_BREAK_TIME} : {SECONDS}")
    if LONG_BREAK_TIME > -1:
        if SECONDS == 0 and LONG_BREAK_TIME != 0:
            LONG_BREAK_TIME -= 1
            SECONDS = 60
        elif SECONDS == 0 and LONG_BREAK_TIME == 0:
            LONG_BREAK_TIME = 15
            stop()
            start_button["state"] = ACTIVE
            COMPLETED = 0
            completed_study = 0
        else:
            SECONDS -= 1


def manage_timer():
    global COMPLETED, running, completed_study
    start_button["state"] = DISABLED
    if COMPLETED % 2 == 0:
        work_time()
        running = screen.after((1 * 60) * 1000 + 5000, manage_timer)
    if COMPLETED % 2 != 0 and COMPLETED != 7:
        short_break_time()
        running = screen.after((1 * 60) * 1000 + 5000, manage_timer)
    if COMPLETED == 7:
        long_break_time()
    if COMPLETED == 8:
        stop()
    COMPLETED += 1
    completed_mark_label.config(text=f"{'✓' * completed_study}", fg=GREEN_COLOR, font=("Arial", 15, "normal"))


def restart():
    global COMPLETED, WORK_TIME, SHORT_BREAK_TIME, LONG_BREAK_TIME, SECONDS, completed_study
    try:
        stop()
    except ValueError:
        pass
    else:
        canvas_tomato.itemconfig(text, text="")
        start_button["state"] = ACTIVE
        COMPLETED = 0
        WORK_TIME = 25
        SHORT_BREAK_TIME = 5
        LONG_BREAK_TIME = 15
        completed_study = 0
        SECONDS = 0
        pomodoro_label.config(text="Pomodoro", fg="black")
        completed_mark_label.config(text="")


screen = Tk()
screen.title("Pomodoro Timer")
screen.config(bg=BACKGROUND_COLOR, pady=50, padx=50)
screen.resizable(False, False)

pomodoro_label = Label(text="Pomodoro", font=('Arial', 50, "bold"), fg=BLACK_COLOR, bg=BACKGROUND_COLOR, pady=10)
pomodoro_label.grid(row=0, column=1)

start_button = Button(text="Start", bg=BACKGROUND_COLOR, highlightthickness=0, borderwidth=0,
                      highlightbackground=BACKGROUND_COLOR, command=manage_timer)
start_button.grid(row=5, column=0)

reset_button = Button(text="Restart", bg=BACKGROUND_COLOR, highlightthickness=0, borderwidth=0,
                      highlightbackground=BACKGROUND_COLOR, command=restart)
reset_button.grid(row=5, column=2)

completed_mark_label = Label(text="", bg=BACKGROUND_COLOR)
completed_mark_label.grid(row=5, column=1)

canvas_tomato = Canvas(bg=BACKGROUND_COLOR, width=200, height=250, highlightthickness=0)
tomato_pic = PhotoImage(file=TOMATO_IMG)
canvas_tomato.create_image(100, 111, image=tomato_pic)
canvas_tomato.grid(row=1, column=1)
text = canvas_tomato.create_text(100, 130, text="", font=(FONT, 30, "normal"), fill="white")


screen.mainloop()

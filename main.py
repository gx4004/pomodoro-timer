from tkinter import *
import subprocess, os, sys

# ---------------------------- RESOURCE PATH (PyInstaller safe) ---------------- #
def resource_path(filename: str) -> str:

    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.abspath(filename)

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
fg = GREEN
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps, timer
    if timer:
        window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer", fg=GREEN)
    check_marks.config(text="")
    reps = 0

# ---------------------------- NOTIFICATION ------------------------------- #
def notify(message: str):
    icon_path = resource_path("tomato.png")  # can be .png
    # Prefer terminal-notifier; fall back to AppleScript if it fails
    try:
        subprocess.run(
            [
                "terminal-notifier",
                "-title", "Pomodoro",
                "-message", message,
                "-sound", "Glass",
                "-appIcon", icon_path,
                # you can keep -sender if you like, but it's optional:
                # "-sender", "com.apple.Terminal",
            ],
            check=False,
        )
    except FileNotFoundError:
        # Fallback: native AppleScript notification (no icon)
        subprocess.run([
            "osascript", "-e",
            f'display notification "{message}" with title "Pomodoro"'
        ])

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1
    work = WORK_MIN * 60
    short_break = SHORT_BREAK_MIN * 60
    long_break = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        title_label.config(text="Long Break", fg=RED)
        notify("Time for a long break! 🍵")
        count_down(long_break)
    elif reps % 2 == 0:
        title_label.config(text="Break", fg=PINK)
        notify("Time for a short break! ☕️")
        count_down(short_break)
    else:
        title_label.config(text="Work", fg=GREEN)
        notify("Time to focus! 💻")
        count_down(work)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global timer
    minutes = count // 60
    seconds = count % 60
    canvas.itemconfig(timer_text, text=f"{minutes:02d}:{seconds:02d}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = "✔" * (reps // 2)
        check_marks.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

title_label = Label(window, text="Timer", fg=fg, bg=YELLOW, font=(FONT_NAME, 50))
title_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
image = PhotoImage(file=resource_path("tomato.png"))
canvas.create_image(100, 112, image=image)
timer_text = canvas.create_text(103, 128, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", command=start_timer, highlightbackground=YELLOW,
                      highlightthickness=0, bg=YELLOW, fg=GREEN, relief="flat", borderwidth=0)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", command=reset_timer, highlightbackground=YELLOW,
                      highlightthickness=0, bg=YELLOW, fg=RED, relief="flat", borderwidth=0)
reset_button.grid(column=2, row=2)

check_marks = Label(text="", bg=YELLOW, fg=GREEN)
check_marks.grid(column=1, row=3)

window.mainloop()

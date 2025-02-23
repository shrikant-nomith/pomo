import tkinter as tk
import math
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import os

WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15
reps = 0
timer = None
daily_log_file = "pomodoro_log.csv"


def reset_timer():
    global reps
    window.after_cancel(timer)
    reps = 0
    canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text="TIMER", fg="cyan")
    check_marks.config(text="")


def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        timer_label.config(text="BREAK", fg="red")
    elif reps % 2 == 0:
        count_down(short_break_sec)
        timer_label.config(text="BREAK", fg="orange")
    else:
        count_down(work_sec)
        timer_label.config(text="WORK", fg="cyan")


def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        if reps % 2 != 0:  
            record_work_time(WORK_MIN)
        start_timer()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)


def record_work_time(minutes):
    today = datetime.now().strftime("%Y-%m-%d")
    file_exists = os.path.isfile(daily_log_file)
    with open(daily_log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Minutes"])
        writer.writerow([today, minutes])


def plot_graph():
    if not os.path.isfile(daily_log_file):
        return

    dates = []
    minutes = {}

    
    with open(daily_log_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date = row['Date']
            minutes_spent = int(row['Minutes'])
            if date in minutes:
                minutes[date] += minutes_spent
            else:
                minutes[date] = minutes_spent

    dates = list(minutes.keys())
    work_minutes = list(minutes.values())

    
    plt.figure(figsize=(10, 5))
    plt.bar(dates, work_minutes, color='skyblue')
    plt.xlabel('Date')
    plt.ylabel('Minutes Spent Working')
    plt.title('Daily Pomodoro Work Minutes')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


window = tk.Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg="black")


timer_label = tk.Label(text="TIMER", fg="cyan", bg="black", font=("Courier", 40, "bold"))
timer_label.grid(column=1, row=0)


canvas = tk.Canvas(width=300, height=300, bg="navy blue", highlightthickness=0)
isro_img = tk.PhotoImage(file="isro-removebg-preview.png")  # Replace with the correct ISRO logo image
canvas.create_image(30, 30, image=isro_img)
timer_text = canvas.create_text(150, 150, text="00:00", fill="white", font=("Courier", 45, "bold"))
canvas.grid(column=1, row=1)


start_button = tk.Button(text="Start", command=start_timer, highlightbackground="black", fg="black", font=("Courier", 12))
start_button.grid(column=0, row=2)

reset_button = tk.Button(text="Reset", command=reset_timer, highlightbackground="black", fg="black", font=("Courier", 12))
reset_button.grid(column=2, row=2)

graph_button = tk.Button(text="Show Graph", command=plot_graph, highlightbackground="black", fg="black", font=("Courier", 12))
graph_button.grid(column=1, row=4)


check_marks = tk.Label(fg="green", bg="black", font=("Courier", 20))
check_marks.grid(column=1, row=3)

window.mainloop()

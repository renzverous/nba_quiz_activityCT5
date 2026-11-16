import tkinter as tk
from tkinter import ttk, messagebox
import random
import os

QUESTIONS = [
    {
        "question": "Which player holds the all-time record for the most career points in NBA history?",
        "choices": ["A. Kareem Abdul-Jabbar", "B. LeBron James", "C. Michael Jordan", "D. Kobe Bryant"],
        "answer": "B"
    },
    {
        "question": "Who holds the record for scoring the most points (100) in a single NBA regular-season game?",
        "choices": ["A. Wilt Chamberlain", "B. Kobe Bryant", "C. Michael Jordan", "D. Elgin Baylor"],
        "answer": "A"
    },
    {
        "question": "Which NBA franchise achieved a historic 73-9 regular-season record in 2015-16?",
        "choices": ["A. Chicago Bulls", "B. Los Angeles Lakers", "C. Golden State Warriors", "D. Boston Celtics"],
        "answer": "C"
    },
    {
        "question": "Which legendary player famously wore jersey numbers 8 and 24 during his career with the Lakers?",
        "choices": ["A. Magic Johnson", "B. Shaquille O'Neal", "C. Jerry West", "D. Kobe Bryant"],
        "answer": "D"
    },
    {
        "question": "How many total championships did Michael Jordan win with the Chicago Bulls in the 1990s?",
        "choices": ["A. 4", "B. 5", "C. 6", "D. 7"],
        "answer": "C"
    },
    {
        "question": "Which player holds the all-time NBA record for most career assists?",
        "choices": ["A. Magic Johnson", "B. John Stockton", "C. Chris Paul", "D. Steve Nash"],
        "answer": "B"
    },
    {
        "question": "Which NBA team plays their iconic home games at Madison Square Garden?",
        "choices": ["A. Brooklyn Nets", "B. Boston Celtics", "C. New York Knicks", "D. Philadelphia 76ers"],
        "answer": "C"
    },
    {
        "question": "How many personal fouls does a player commit before fouling out of a standard NBA game?",
        "choices": ["A. 5 fouls", "B. 6 fouls", "C. 7 fouls", "D. 8 fouls"],
        "answer": "B"
    },
    {
        "question": "Which franchise originally drafted Kobe Bryant with the 13th overall pick in 1996 before trading him?",
        "choices": ["A. Charlotte Hornets", "B. Portland Trail Blazers", "C. Orlando Magic", "D. Sacramento Kings"],
        "answer": "A"
    },
    {
        "question": "What is the regulation height of an official NBA basketball hoop from the floor?",
        "choices": ["A. 9 feet", "B. 10 feet", "C. 11 feet", "D. 12 feet"],
        "answer": "B"
    }
]


TIME_LIMIT = 15
HIGH_SCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "high_score.txt")


BG_MAIN = "#121214"
BG_CARD = "#1A1A1E"
ACCENT_ORANGE = "#FF6700"
ACCENT_HOVER = "#FF8533"
TEXT_LIGHT = "#F4F4F5"
TEXT_MUTED = "#A1A1AA"
COLOR_CORRECT = "#22C55E"
COLOR_WRONG = "#EF4444"


quiz_questions = []
current_index = 0
score = 0
time_left = TIME_LIMIT
wrong_answers = []
timer_id = None
is_answered = False

root = tk.Tk()
root.title("HoopsMaster - NBA Trivia Challenge")
root.geometry("760x660")
root.configure(bg=BG_MAIN)
root.resizable(False, False)

selected_option = tk.StringVar()
choice_radios = []

timer_label = None
feedback_label = None
submit_btn = None
next_btn = None

container = tk.Frame(root, bg=BG_MAIN)
container.pack(fill="both", expand=True, padx=35, pady=25)


def read_high_score():
    """Reads the saved high score from high_score.txt."""
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as f:
                return int(f.read().strip())
        except ValueError:
            return 0
    return 0

def update_high_score(new_score):
    """Saves new_score if it beats the current record."""
    if new_score > read_high_score():
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(new_score))
        return True
    return False

def reset_container():
    for widget in container.winfo_children():
        widget.destroy()

def format_choice(question_obj, letter):
    for ch in question_obj["choices"]:
        if ch.startswith(letter + "."):
            return ch
    return "No answer"

def stop_countdown():
    global timer_id
    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None

def disable_options():
    for rb in choice_radios:
        rb.config(state="disabled")


def show_start_screen():
    reset_container()
    
    card = tk.Frame(container, bg=BG_CARD, padx=40, pady=45)
    card.pack(expand=True, fill="both")

    tk.Label(card, text="🏀 HOOPSMASTER TRIVIA", font=("Segoe UI", 12, "bold"),
             bg=BG_CARD, fg=ACCENT_ORANGE).pack(pady=(10, 5))
    
    tk.Label(card, text="Ultimate NBA Challenge", font=("Segoe UI", 24, "bold"),
             bg=BG_CARD, fg=TEXT_LIGHT).pack(pady=(0, 15))

    tk.Label(card, text=f"• {len(QUESTIONS)} Randomized NBA Questions\n"
                        f"• {TIME_LIMIT} Seconds Per Question\n"
                        f" Let's see if you have elite ball knowedlege."
                        f" OR are you just a larper?",
             font=("Segoe UI", 12), bg=BG_CARD, fg=TEXT_MUTED, justify="left").pack(pady=15)

    best_score = read_high_score()
    tk.Label(card, text=f"All-Time High Score: {best_score} / {len(QUESTIONS)}",
             font=("Segoe UI", 15, "bold"), bg=BG_CARD, fg=COLOR_CORRECT).pack(pady=20)

    tk.Button(card, text="Tip-Off (Start Quiz)", font=("Segoe UI", 14, "bold"),
              bg=ACCENT_ORANGE, fg="white", activebackground=ACCENT_HOVER,
              activeforeground="white", relief="flat", width=20, pady=8,
              cursor="hand2", command=begin_quiz).pack(pady=15)


def begin_quiz():
    global quiz_questions, current_index, score, wrong_answers
    quiz_questions = random.sample(QUESTIONS, len(QUESTIONS))
    current_index = 0
    score = 0
    wrong_answers = []
    render_question()

def render_question():
    global time_left, is_answered, timer_label, feedback_label, submit_btn, next_btn, choice_radios
    
    reset_container()
    is_answered = False
    selected_option.set("")
    time_left = TIME_LIMIT
    q_data = quiz_questions[current_index]

    header = tk.Frame(container, bg=BG_MAIN)
    header.pack(fill="x", pady=(0, 8))

    tk.Label(header, text=f"Question {current_index + 1} of {len(quiz_questions)}",
             font=("Segoe UI", 13, "bold"), bg=BG_MAIN, fg=TEXT_LIGHT).pack(side="left")

    tk.Label(header, text=f"Score: {score}",
             font=("Segoe UI", 13, "bold"), bg=BG_MAIN, fg=ACCENT_ORANGE).pack(side="left", padx=25)

    timer_label = tk.Label(header, text=f"Time Left: {time_left}s",
                           font=("Segoe UI", 13, "bold"), bg=BG_MAIN, fg=TEXT_LIGHT)
    timer_label.pack(side="right")

    progress = ttk.Progressbar(container, length=690, mode="determinate",
                               maximum=len(quiz_questions), value=current_index + 1)
    progress.pack(fill="x", pady=(0, 15))

    q_card = tk.Frame(container, bg=BG_CARD, padx=30, pady=25)
    q_card.pack(fill="both", expand=True)

    tk.Label(q_card, text=q_data["question"], font=("Segoe UI", 16, "bold"),
             bg=BG_CARD, fg=TEXT_LIGHT, wraplength=620, justify="left").pack(anchor="w", pady=(0, 20))

    choice_radios = []
    for item in q_data["choices"]:
        letter = item[0]
        rb = tk.Radiobutton(
            q_card, text=item, variable=selected_option, value=letter,
            font=("Segoe UI", 13), bg=BG_CARD, fg=TEXT_LIGHT,
            selectcolor=BG_MAIN, activebackground=BG_CARD, activeforeground=ACCENT_ORANGE,
            anchor="w", padx=10, pady=6, cursor="hand2"
        )
        rb.pack(fill="x", pady=4)
        choice_radios.append(rb)

    feedback_label = tk.Label(q_card, text="", font=("Segoe UI", 12, "bold"),
                              bg=BG_CARD, wraplength=620, justify="left")
    feedback_label.pack(anchor="w", pady=(18, 5))

    btn_row = tk.Frame(container, bg=BG_MAIN)
    btn_row.pack(pady=(15, 0))

    submit_btn = tk.Button(btn_row, text="Submit Answer", font=("Segoe UI", 12, "bold"),
                           bg=ACCENT_ORANGE, fg="white", relief="flat", width=16, pady=7,
                           cursor="hand2", command=check_answer)
    submit_btn.pack(side="left", padx=10)

    is_last = (current_index == len(quiz_questions) - 1)
    next_btn = tk.Button(btn_row, text="View Results" if is_last else "Next Question",
                         font=("Segoe UI", 12, "bold"), bg="#27272A", fg="white",
                         relief="flat", width=16, pady=7, state="disabled",
                         cursor="hand2", command=advance_question)
    next_btn.pack(side="left", padx=10)

    run_countdown()


def run_countdown():
    global time_left, timer_id
    if is_answered:
        return
    timer_label.config(
        text=f"Time Left: {time_left}s",
        fg=COLOR_WRONG if time_left <= 5 else TEXT_LIGHT
    )
    if time_left == 0:
        handle_timeout()
        return
    time_left -= 1
    timer_id = root.after(1000, run_countdown)

def check_answer():
    global score, is_answered
    if is_answered:
        return
    
    user_choice = selected_option.get()
    if user_choice == "":
        messagebox.showwarning("Selection Required", "Please select an option before submitting.")
        return

    is_answered = True
    stop_countdown()
    disable_options()
    submit_btn.config(state="disabled")

    q_data = quiz_questions[current_index]
    if user_choice == q_data["answer"]:
        score += 1
        feedback_label.config(text="Swish! Correct answer.", fg=COLOR_CORRECT)
    else:
        correct_full = format_choice(q_data, q_data["answer"])
        wrong_answers.append({
            "question": q_data["question"],
            "your_answer": format_choice(q_data, user_choice),
            "correct_answer": correct_full
        })
        feedback_label.config(text=f"Missed! Correct answer: {correct_full}", fg=COLOR_WRONG)

    next_btn.config(state="normal", bg=ACCENT_ORANGE)

def handle_timeout():
    global is_answered
    is_answered = True
    disable_options()
    submit_btn.config(state="disabled")

    q_data = quiz_questions[current_index]
    correct_full = format_choice(q_data, q_data["answer"])
    wrong_answers.append({
        "question": q_data["question"],
        "your_answer": "No answer (Time expired)",
        "correct_answer": correct_full
    })
    feedback_label.config(text=f"Clock expired! Correct answer: {correct_full}", fg=COLOR_WRONG)
    next_btn.config(state="normal", bg=ACCENT_ORANGE)

def advance_question():
    global current_index
    current_index += 1
    if current_index < len(quiz_questions):
        render_question()
    else:
        show_results_screen()

def show_results_screen():
    reset_container()
    total = len(quiz_questions)
    percent = (score / total) * 100
    is_new_best = update_high_score(score)

    if percent >= 90:
        remark = "GOAT performance! Absolute basketball knowledge."
    elif percent >= 70:
        remark = "All-Star performance! Great job."
    elif percent >= 50:
        remark = "Solid rotation player. Keep practicing!"
    else:
        remark = "Bench warmer status. Study up and try again!"

    tk.Label(container, text="Final Buzzer - Results", font=("Segoe UI", 24, "bold"),
             bg=BG_MAIN, fg=TEXT_LIGHT).pack(pady=(0, 5))

    tk.Label(container, text=f"Final Score: {score} / {total} ({percent:.0f}%)",
             font=("Segoe UI", 18, "bold"), bg=BG_MAIN, fg=ACCENT_ORANGE).pack()

    tk.Label(container, text=remark, font=("Segoe UI", 12),
             bg=BG_MAIN, fg=TEXT_MUTED).pack(pady=3)

    record_msg = "NEW HIGH SCORE RECORDED!" if is_new_best else f"Saved High Score: {read_high_score()} / {total}"
    tk.Label(container, text=record_msg, font=("Segoe UI", 12, "bold"),
             bg=BG_MAIN, fg=COLOR_CORRECT).pack(pady=(2, 12))

    tk.Label(container, text="Answer Review (Missed Questions):",
             font=("Segoe UI", 12, "bold"), bg=BG_MAIN, fg=TEXT_LIGHT).pack(anchor="w", pady=(0, 5))

    review_frame = tk.Frame(container, bg=BG_CARD)
    review_frame.pack(fill="both", expand=True)

    scrollbar = tk.Scrollbar(review_frame)
    scrollbar.pack(side="right", fill="y")

    review_text = tk.Text(review_frame, height=11, wrap="word", font=("Segoe UI", 11),
                          bg=BG_CARD, fg=TEXT_LIGHT, relief="flat", padx=12, pady=10,
                          yscrollcommand=scrollbar.set)
    review_text.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=review_text.yview)

    if not wrong_answers:
        review_text.insert("end", "Perfect game! You answered every NBA question correctly.")
    else:
        for idx, item in enumerate(wrong_answers, start=1):
            review_text.insert("end", f"{idx}. {item['question']}\n")
            review_text.insert("end", f"   • Your Answer: {item['your_answer']}\n")
            review_text.insert("end", f"   • Correct Answer: {item['correct_answer']}\n\n")

    review_text.config(state="disabled")

    btn_row = tk.Frame(container, bg=BG_MAIN)
    btn_row.pack(pady=(15, 0))

    tk.Button(btn_row, text="Restart Quiz", font=("Segoe UI", 12, "bold"),
              bg=ACCENT_ORANGE, fg="white", relief="flat", width=16, pady=7,
              cursor="hand2", command=begin_quiz).pack(side="left", padx=10)

    tk.Button(btn_row, text="Exit", font=("Segoe UI", 12, "bold"),
              bg="#27272A", fg="white", relief="flat", width=16, pady=7,
              cursor="hand2", command=on_app_close).pack(side="left", padx=10)

def on_app_close():
    stop_countdown()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_app_close)
show_start_screen()
root.mainloop()

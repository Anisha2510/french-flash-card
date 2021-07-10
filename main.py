from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(lang_title, text="French")
    canvas.itemconfig(word, text=current_card["French"])
    canvas.itemconfig(card_bg, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(lang_title, text="English")
    canvas.itemconfig(word, text=current_card["English"])
    canvas.itemconfig(card_bg, image=card_back)


def is_known():
    to_learn.remove(current_card)
    data_to_learn = pandas.DataFrame(to_learn)
    data_to_learn.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_bg = canvas.create_image(400, 263, image=card_front)
lang_title = canvas.create_text(400, 150, text="", fill="black", font=("Arial", 40, "italic"))
word = canvas.create_text(400, 263, text="", fill="black", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
wrong_btn = Button(image=cross_image, highlightthickness=0, command=next_card)
wrong_btn.grid(column=0, row=1)

right_image = PhotoImage(file="images/right.png")
right_btn = Button(image=right_image, highlightthickness=0, command=is_known)
right_btn.grid(column=1, row=1)

next_card()

window.mainloop()

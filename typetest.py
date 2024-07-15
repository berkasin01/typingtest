from tkinter import *
from datetime import datetime
import time
from bs4 import BeautifulSoup
import requests


class TypeTest:
    def __init__(self):
        self.main = Tk()
        self.main.title("Typing Speed Test")
        self.main.geometry("1000x1000")

        self.title = Label(text="TYPING SPEED TEST", font=("Arial", "30", "bold"))
        self.title.grid(column=0, row=0)
        self.subtitle = Label(text="How fast are your fingers? Do the one-minute typing test to find out! Press the "
                                   "space bar after each word. At the end, you'll get your typing speed in CPM and "
                                   "WPM. "
                                   "Good luck!")
        self.subtitle.grid(column=0, row=1, pady=25, padx=25)

        self.most_recent_score = Label(text="The Most Recent Score:", font=("Arial", "15", "bold"))
        self.most_recent_score.grid(column=0, row=2, pady=50)

        self.display_score = Label(text="Score:0", font=("Arial", "15", "bold"))
        self.display_score.grid(column=0, row=3, pady=10)

        self.text = Label(text="Text goes here")
        self.text.grid(column=0, row=4, pady=50)

        self.user_entry = Entry(width=50)
        self.user_entry.grid(column=0, row=5, pady=10)

        self.restart = Button(text="Start", command=self.restart)
        self.restart.grid(column=0, row=7)

        self.timer = Label(text="Press Start to start the Timer and get your first text")
        self.timer.grid(column=0, row=6)

        self.all_scores = []
        self.timer_id = None
        self.text_insert = ""
        self.indices = []
        self.score = 0
        self.clean_list = []

        self.update_text()
        self.count_down(count=60)
        self.update_score()

        self.main.mainloop()

    def restart(self):
        if self.timer_id is not None:
            self.main.after_cancel(self.timer_id)
        self.count_down(count=60)
        self.score = 0
        self.display_score.config(text=f"Score:{self.score}")
        self.user_entry.delete(0, END)
        self.update_text()

    def update_text(self):
        url = "https://randomtextgenerator.com/"
        list = []
        response = requests.get(url=url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.find(id="randomtext_box").text
        text_to_clean = text.split(" ")
        del text_to_clean[0]
        self.indices = text_to_clean[0:200]
        self.text_insert = " ".join(self.indices)
        self.text.config(text=self.text_insert, font=("Arial", "10", "italic"), wraplength=750)

    def update_score(self):
        with open(file="recentscores.txt") as f:
            scores_data = f.readlines()
            self.all_scores = [score.strip("\n") for score in scores_data]
            self.most_recent_score.config(text=f"The Most Recent Score: {self.all_scores[len(self.all_scores)-1]}")

    def count_down(self, count):
        self.timer.config(text=count, font=("Arial", "15", "bold"))
        if count > 0:
            user_entry_list = self.user_entry.get().split(" ")
            if self.user_entry.get():
                for word in user_entry_list:
                    try:
                        find_index = self.indices.index(word)
                        if word == self.indices[find_index]:
                            get_index = self.indices.index(word)
                            self.clean_list.append(word)
                            self.display_score.config(text=f"Score:{self.score}")
                            self.indices.pop(get_index)
                            for x in self.clean_list:
                                if x in user_entry_list:
                                    index = user_entry_list.index(x)
                                    user_entry_list.pop(index)
                            self.score = len(self.clean_list)-1
                            print(user_entry_list)
                            print(self.score)
                    except ValueError:
                        pass
            self.timer_id = self.main.after(1000, self.count_down, count - 1)
        else:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            with open("recentscores.txt","a") as f:
                f.write(f"\n{current_time}-Score:{self.score-1}")


demo = TypeTest()

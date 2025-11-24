# ui/result_screen.py
from tkinter import Frame, Label, Button
from utils.constants import BG_COLOR, BORDER_COLOR


class ResultScreen(Frame):
    def __init__(self, parent, manager):
        super().__init__(parent, bg=BG_COLOR,
                         highlightbackground=BORDER_COLOR,
                         highlightthickness=6)
        self.manager = manager

        self.result_label = Label(
            self,
            text="YOU WIN",
            font=("Comic Sans MS", 52, "bold"),
            fg="white",
            bg=BG_COLOR
        )
        self.result_label.pack(pady=100)

        Button(
            self,
            text="PLAY AGAIN",
            font=("Comic Sans MS", 22),
            width=15,
            command=lambda: manager.show_screen("ModeSelect")
        ).pack(pady=20)

        Button(
            self,
            text="BACK TO MENU",
            font=("Comic Sans MS", 18),
            width=15,
            command=lambda: manager.show_screen("MainMenu")
        ).pack()

    def load(self, result_text="", p1_score=None, p2_score=None):
        # show and update result text
        self.place(relwidth=1, relheight=1)
        if result_text:
            self.result_label.config(text=result_text)

    def unload(self):
        self.place_forget()

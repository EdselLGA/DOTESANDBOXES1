# ui/difficulty_select.py
from tkinter import Frame, Label, Button
from utils.constants import BG_COLOR, BORDER_COLOR


class DifficultySelect(Frame):
    def __init__(self, parent, manager):
        super().__init__(parent, bg=BG_COLOR,
                         highlightbackground=BORDER_COLOR,
                         highlightthickness=6)
        self.manager = manager

        Label(
            self,
            text="SELECT DIFFICULTY",
            font=("Comic Sans MS", 38),
            fg="white",
            bg=BG_COLOR
        ).pack(pady=60)

        Button(
            self,
            text="EASY",
            font=("Comic Sans MS", 22),
            width=15,
            command=lambda: manager.show_screen("GameScreen", mode="AI", difficulty="easy")
        ).pack(pady=10)

        Button(
            self,
            text="MEDIUM",
            font=("Comic Sans MS", 22),
            width=15,
            command=lambda: manager.show_screen("GameScreen", mode="AI", difficulty="medium")
        ).pack(pady=10)

        Button(
            self,
            text="HARD",
            font=("Comic Sans MS", 22),
            width=15,
            command=lambda: manager.show_screen("GameScreen", mode="AI", difficulty="hard")
        ).pack(pady=10)

        Button(
            self,
            text="BACK",
            font=("Comic Sans MS", 18),
            width=12,
            command=lambda: manager.show_screen("ModeSelect")
        ).pack(side="bottom", pady=30)

    def load(self):
        self.place(relwidth=1, relheight=1)

    def unload(self):
        self.place_forget()

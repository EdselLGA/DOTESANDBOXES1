from tkinter import Frame, Label, Button
from utils.constants import BG_COLOR, BORDER_COLOR


class ModeSelect(Frame):
    def __init__(self, parent, manager):
        super().__init__(parent, bg=BG_COLOR,
                         highlightbackground=BORDER_COLOR,
                         highlightthickness=6)
        self.manager = manager

        Label(
            self,
            text="SELECT MODE",
            font=("Comic Sans MS", 40),
            fg="white",
            bg=BG_COLOR
        ).pack(pady=80)

        Button(
            self,
            text="VS AI",
            font=("Comic Sans MS", 22),
            width=15,
            command=lambda: manager.show_screen("DifficultySelect")
        ).pack(pady=15)

        Button(
            self,
            text="VS PLAYER",
            font=("Comic Sans MS", 22),
            width=15,
            command=lambda: manager.show_screen("GameScreen", mode="PVP")
        ).pack(pady=15)

        Button(
            self,
            text="BACK",
            font=("Comic Sans MS", 18),
            width=12,
            command=lambda: manager.show_screen("MainMenu")
        ).pack(side="bottom", pady=50)

    def load(self, **kwargs):
        self.place(relwidth=1, relheight=1)

    def unload(self):
        self.place_forget()

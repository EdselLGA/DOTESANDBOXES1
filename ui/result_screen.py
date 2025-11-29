# ui/result_screen.py
from tkinter import Frame, Label, Button, PhotoImage
from utils.constants import BG_COLOR, BORDER_COLOR

class ResultScreen(Frame):
    def __init__(self, parent, manager):
        super().__init__(parent, bg=BG_COLOR, highlightbackground=BORDER_COLOR, highlightthickness=0)
        self.manager = manager

        try:
            self.img_p1 = PhotoImage(file="assets/player_blue.png").subsample(2, 2)
        except: self.img_p1 = None
        try:
            self.img_p2 = PhotoImage(file="assets/player_red.png").subsample(2, 2)
        except: self.img_p2 = None
        try:
            self.img_back = PhotoImage(file="assets/back_button.png").subsample(2, 2)
        except: self.img_back = None

        container = Frame(self, bg=BG_COLOR)
        container.pack(pady=(50, 20))

        self.lbl_winner_name = Label(container, text="PLAYER",
                                     font=("Comic Sans MS", 48, "bold"),
                                     fg="white", bg=BG_COLOR)
        self.lbl_winner_name.pack()

        self.lbl_wins_text = Label(container, text="WINS",
                                   font=("Comic Sans MS", 48, "bold"),
                                   fg="white", bg=BG_COLOR)
        self.lbl_wins_text.pack()

        score_frame = Frame(self, bg=BG_COLOR)
        score_frame.pack(pady=30)

        # P1
        p1_panel = Frame(score_frame, bg=BG_COLOR)
        p1_panel.pack(side="left", padx=30)
        if self.img_p1:
            Label(p1_panel, image=self.img_p1, bg=BG_COLOR).pack(side="left", padx=5)
        self.lbl_p1_score = Label(p1_panel, text="", font=("Arial", 20, "bold"),
                                  fg="white", bg="#2B2A2A", width=5)
        self.lbl_p1_score.pack(side="left")

        # P2
        p2_panel = Frame(score_frame, bg=BG_COLOR)
        p2_panel.pack(side="left", padx=30)
        if self.img_p2:
            Label(p2_panel, image=self.img_p2, bg=BG_COLOR).pack(side="left", padx=5)
        self.lbl_p2_score = Label(p2_panel, text="", font=("Arial", 20, "bold"),
                                  fg="white", bg="#2B2A2A", width=5)
        self.lbl_p2_score.pack(side="left")

        self.btn_play_again = Button(self, text="PLAY AGAIN",
                                     font=("Comic Sans MS", 24),
                                     fg="white", bg="black",
                                     bd=2, cursor="hand2",
                                     command=lambda: manager.show_screen("ModeSelect"))
        self.btn_play_again.pack(pady=50, ipadx=20, ipady=5)

        self.btn_back = Button(self, image=self.img_back if self.img_back else None,
                               bg=BG_COLOR, bd=0,
                               cursor="hand2",
                               command=lambda: manager.show_screen("MainMenu"))

    def load(self, result_text="", p1_score=0, p2_score=0, **kwargs):
        self.place(relwidth=1, relheight=1)
        self.btn_back.place(x=20, y=630)

        raw = str(result_text).upper()

        if "PLAYER 1" in raw:
            self.lbl_winner_name.config(text="PLAYER 1")
            self.lbl_wins_text.config(text="WINS")
        elif "PLAYER 2" in raw:
            self.lbl_winner_name.config(text="PLAYER 2")
            self.lbl_wins_text.config(text="WINS")
        else:
            self.lbl_winner_name.config(text="IT'S A")
            self.lbl_wins_text.config(text="TIE")

        self.lbl_p1_score.config(text=str(int(p1_score)))
        self.lbl_p2_score.config(text=str(int(p2_score)))

    def unload(self):
        self.place_forget()
        try: self.btn_back.place_forget()
        except: pass

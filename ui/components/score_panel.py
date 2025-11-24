from tkinter import Frame, Label

class ScorePanel(Frame):
    def __init__(self, parent, p1_name="P1", p2_name="P2", **kwargs):
        super().__init__(parent, **kwargs)
        self.p1_label = Label(self, text=f"{p1_name}: 0", font=("Comic Sans MS", 16))
        self.p2_label = Label(self, text=f"{p2_name}: 0", font=("Comic Sans MS", 16))
        self.p1_label.pack(pady=2)
        self.p2_label.pack(pady=2)

    def update_scores(self, p1_score, p2_score):
        self.p1_label.config(text=f"P1: {p1_score}")
        self.p2_label.config(text=f"P2: {p2_score}")

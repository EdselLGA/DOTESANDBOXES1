# core/game_engine.py
from tkinter import *
from core.hint_engine import HintEngine
import numpy as np

size_of_board = 600
number_of_dots = 6

dot_color = '#7BC043'
player1_color = '#0492CF'
player1_color_light = '#67B0CF'
player2_color = '#EE4035'
player2_color_light = '#EE7E77'

dot_width = 0.25 * size_of_board / number_of_dots
edge_width = 0.1 * size_of_board / number_of_dots
distance_between_dots = size_of_board / number_of_dots

class GameEngine:
    def __init__(self, canvas):
        self.canvas = canvas

        self.hints = HintEngine(self)

        # Logical matrices
        self.row_status = np.zeros((number_of_dots - 1, number_of_dots))   # 5x6
        self.col_status = np.zeros((number_of_dots, number_of_dots - 1))   # 6x5
        self.box_owner = np.zeros((number_of_dots - 1, number_of_dots - 1))  # 5x5

        self.player1_turn = True
        self.turntext_handle = None

        self.refresh_board()
        self.display_turn_text()

    # RESET GAME
    def reset_game_state(self):
        self.canvas.delete("edge")
        self.canvas.delete("box")
        self.canvas.delete("turn")
        self.canvas.delete("hint")

        self.row_status.fill(0)
        self.col_status.fill(0)
        self.box_owner.fill(0)

        self.player1_turn = True

        self.refresh_board()
        self.display_turn_text()

    # GRID LOGIC
    def convert_grid_to_logical_position(self, grid_pos):
        gp = np.array(grid_pos)
        pos = (gp - distance_between_dots / 4) // (distance_between_dots / 2)

        # horizontal edge
        if pos[1] % 2 == 0 and (pos[0] - 1) % 2 == 0:
            r = int((pos[0] - 1) // 2)
            c = int(pos[1] // 2)
            return [r, c], "row"

        # vertical edge
        if pos[0] % 2 == 0 and (pos[1] - 1) % 2 == 0:
            r = int(pos[0] // 2)
            c = int((pos[1] - 1) // 2)
            return [r, c], "col"

        return [], False

    def is_grid_occupied(self, pos, t):
        r, c = pos
        return (self.row_status[r][c] == 1) if t == "row" else (self.col_status[r][c] == 1)

    # GRID DRAWING
    def refresh_board(self):
        self.canvas.delete("grid")
        self.canvas.delete("dot")

        for i in range(number_of_dots):
            x = i * distance_between_dots + distance_between_dots / 2

            self.canvas.create_line(x, distance_between_dots / 2,
                                    x, size_of_board - distance_between_dots / 2,
                                    fill="gray", dash=(2, 2), tags="grid")

            self.canvas.create_line(distance_between_dots / 2, x,
                                    size_of_board - distance_between_dots / 2, x,
                                    fill="gray", dash=(2, 2), tags="grid")

        # dots
        for i in range(number_of_dots):
            for j in range(number_of_dots):
                cx = i * distance_between_dots + distance_between_dots / 2
                cy = j * distance_between_dots + distance_between_dots / 2
                self.canvas.create_oval(cx - dot_width / 2, cy - dot_width / 2,
                                        cx + dot_width / 2, cy + dot_width / 2,
                                        fill=dot_color, outline=dot_color, tags="dot")

    # DRAW EDGE
    def make_edge(self, t, pos):
        r, c = pos

        if t == "row":
            sx = distance_between_dots/2 + r*distance_between_dots
            sy = distance_between_dots/2 + c*distance_between_dots
            ex = sx + distance_between_dots
            ey = sy
        else:
            sx = distance_between_dots/2 + r*distance_between_dots
            sy = distance_between_dots/2 + c*distance_between_dots
            ex = sx
            ey = sy + distance_between_dots

        color = player1_color if self.player1_turn else player2_color

        self.canvas.create_line(sx, sy, ex, ey, fill=color,
                                width=edge_width, tags="edge")
        self.canvas.tag_lower("edge", "dot")

    # SHADE BOX
    def shade_box(self, r, c, owner):
        color = player1_color_light if owner == 1 else player2_color_light

        sx = distance_between_dots/2 + r*distance_between_dots + edge_width/2
        sy = distance_between_dots/2 + c*distance_between_dots + edge_width/2
        ex = sx + distance_between_dots - edge_width
        ey = sy + distance_between_dots - edge_width

        self.canvas.create_rectangle(sx, sy, ex, ey, fill=color,
                                     outline="", tags="box")
        self.canvas.tag_lower("box", "dot")

    # BOX DETECTION
    def update_boxes(self):
        completed = False

        for r in range(number_of_dots - 1):
            for c in range(number_of_dots - 1):

                if self.box_owner[r][c] != 0:
                    continue

                top = self.row_status[r][c] == 1
                bottom = self.row_status[r][c+1] == 1
                left = self.col_status[r][c] == 1
                right = self.col_status[r+1][c] == 1

                if top and bottom and left and right:
                    owner = 1 if self.player1_turn else 2
                    self.box_owner[r][c] = owner
                    self.shade_box(r, c, owner)
                    completed = True

        return completed

    # TURN TEXT
    def display_turn_text(self):
        if self.turntext_handle:
            self.canvas.delete(self.turntext_handle)

        text = f"Next turn: Player {'1' if self.player1_turn else '2'}"
        color = player1_color if self.player1_turn else player2_color

        self.turntext_handle = self.canvas.create_text(
            size_of_board - 120, size_of_board - 20,
            text=text, fill=color, font="cmr 15 bold", tags="turn"
        )

    # HINT SUPPORT
    def get_hint(self):
        return self.hints.get_best_move()

    def highlight_edge(self, t, pos):
        self.canvas.delete("hint")
        r, c = pos

        if t == "row":
            sx = distance_between_dots/2 + r*distance_between_dots
            sy = distance_between_dots/2 + c*distance_between_dots
            ex = sx + distance_between_dots
            ey = sy
        else:
            sx = distance_between_dots/2 + r*distance_between_dots
            sy = distance_between_dots/2 + c*distance_between_dots
            ex = sx
            ey = sy + distance_between_dots

        self.canvas.create_line(sx, sy, ex, ey,
                                fill="yellow", width=edge_width+2,
                                dash=(4,2), tags="hint")

        self.canvas.tag_raise("hint")
        self.canvas.tag_lower("hint", "dot")

    # CLICK HANDLER
    def click(self, event):
        self.canvas.delete("hint")

        pos, t = self.convert_grid_to_logical_position([event.x, event.y])
        if not t:
            return None

        if self.is_grid_occupied(pos, t):
            return None

        r, c = pos

        if t == "row":
            self.row_status[r][c] = 1
        else:
            self.col_status[r][c] = 1

        self.make_edge(t, pos)

        scored = self.update_boxes()

        if not scored:
            self.player1_turn = not self.player1_turn

        self.display_turn_text()

        if self.is_gameover():
            p1 = int(np.count_nonzero(self.box_owner == 1))
            p2 = int(np.count_nonzero(self.box_owner == 2))

            winner = "Winner: Player 1" if p1 > p2 else (
                     "Winner: Player 2" if p2 > p1 else "It's a tie")

            return {
                "result_text": winner,
                "player1_score": p1,
                "player2_score": p2
            }

        return None

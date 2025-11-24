from tkinter import *
import numpy as np

size_of_board = 600
number_of_dots = 6
dot_color = '#7BC043'
player1_color = '#0492CF'
player1_color_light = '#67B0CF'
player2_color = '#EE4035'
player2_color_light = '#EE7E77'
Green_color = '#7BC043'

dot_width = 0.25 * size_of_board / number_of_dots
edge_width = 0.1 * size_of_board / number_of_dots
distance_between_dots = size_of_board / number_of_dots

class GameEngine:
    def __init__(self, canvas):
        self.canvas = canvas

        self.player1_starts = True
        self.pointsScored = False
        self.player1_turn = not self.player1_starts

        self.board_status = np.zeros((number_of_dots - 1, number_of_dots - 1))
        self.row_status = np.zeros((number_of_dots, number_of_dots - 1))
        self.col_status = np.zeros((number_of_dots - 1, number_of_dots))

        self.turntext_handle = None
        self.already_marked_boxes = []

        self.refresh_board()

    def reset_game_state(self):
        self.canvas.delete("all")
        self.refresh_board()

        self.board_status.fill(0)
        self.row_status.fill(0)
        self.col_status.fill(0)

        self.pointsScored = False
        self.player1_starts = not self.player1_starts
        self.player1_turn = not self.player1_starts
        self.already_marked_boxes = []

        self.display_turn_text()

    def is_grid_occupied(self, pos, t):
        r, c = pos
        if t == "row":
            return self.row_status[c][r] == 1
        if t == "col":
            return self.col_status[c][r] == 1
        return True

    def convert_grid_to_logical_position(self, grid_pos):
        grid_pos = np.array(grid_pos)
        pos = (grid_pos - distance_between_dots / 4) // (distance_between_dots / 2)

        if pos[1] % 2 == 0 and (pos[0] - 1) % 2 == 0:
            return [int((pos[0] - 1)//2), int(pos[1]//2)], "row"

        if pos[0] % 2 == 0 and (pos[1] - 1) % 2 == 0:
            return [int(pos[0]//2), int((pos[1]-1)//2)], "col"

        return [], False

    def pointScored(self):
        self.pointsScored = True

    def mark_box(self):
        for box in np.argwhere(self.board_status == -4):
            box = list(box)
            if box not in self.already_marked_boxes:
                self.already_marked_boxes.append(box)
                self.shade_box(box, player1_color_light)

        for box in np.argwhere(self.board_status == 4):
            box = list(box)
            if box not in self.already_marked_boxes:
                self.already_marked_boxes.append(box)
                self.shade_box(box, player2_color_light)

    def update_board(self, t, pos):
        r, c = pos
        mod = -1 if self.player1_turn else 1

        if c < number_of_dots - 1 and r < number_of_dots - 1:
            self.board_status[c][r] = (abs(self.board_status[c][r])+1)*mod
            if abs(self.board_status[c][r]) == 4:
                self.pointScored()

        if t == "row":
            self.row_status[c][r] = 1
            if c >= 1:
                self.board_status[c-1][r] = (abs(self.board_status[c-1][r])+1)*mod
                if abs(self.board_status[c-1][r]) == 4:
                    self.pointScored()

        if t == "col":
            self.col_status[c][r] = 1
            if r >= 1:
                self.board_status[c][r-1] = (abs(self.board_status[c][r-1])+1)*mod
                if abs(self.board_status[c][r-1]) == 4:
                    self.pointScored()

    def is_gameover(self):
        print("DEBUG board_status:")
        print(self.board_status)
        return (self.row_status == 1).all() and (self.col_status == 1).all()

    def refresh_board(self):
        self.canvas.delete("grid")
        self.canvas.delete("dot")

        for i in range(number_of_dots):
            x = i * distance_between_dots + distance_between_dots/2
            self.canvas.create_line(x, distance_between_dots/2,
                                    x, size_of_board-distance_between_dots/2,
                                    fill="gray", dash=(2,2), tags="grid")
            self.canvas.create_line(distance_between_dots/2, x,
                                    size_of_board-distance_between_dots/2, x,
                                    fill="gray", dash=(2,2), tags="grid")

        for i in range(number_of_dots):
            for j in range(number_of_dots):
                cx = i * distance_between_dots + distance_between_dots/2
                cy = j * distance_between_dots + distance_between_dots/2
                self.canvas.create_oval(cx-dot_width/2, cy-dot_width/2,
                                        cx+dot_width/2, cy+dot_width/2,
                                        fill=dot_color, outline=dot_color, tags="dot")

    def make_edge(self, t, pos):
        r, c = pos
        if t == "row":
            sx = distance_between_dots/2 + r*distance_between_dots
            sy = distance_between_dots/2 + c*distance_between_dots
            ex = sx + distance_between_dots
            ey = sy
        else:
            sy = distance_between_dots/2 + c*distance_between_dots
            ey = sy + distance_between_dots
            sx = distance_between_dots/2 + r*distance_between_dots
            ex = sx

        color = player1_color if self.player1_turn else player2_color
        self.canvas.create_line(sx, sy, ex, ey,
                                fill=color, width=edge_width, tags="edge")

    def shade_box(self, box, color):
        r, c = box
        sx = distance_between_dots/2 + c*distance_between_dots + edge_width/2
        sy = distance_between_dots/2 + r*distance_between_dots + edge_width/2
        ex = sx + distance_between_dots - edge_width
        ey = sy + distance_between_dots - edge_width

        self.canvas.create_rectangle(sx, sy, ex, ey,
                                     fill=color, outline="", tags="box")

    def display_turn_text(self):
        if self.turntext_handle:
            self.canvas.delete(self.turntext_handle)

        text = "Next turn: Player1" if self.player1_turn else "Next turn: Player2"
        color = player1_color if self.player1_turn else player2_color

        self.turntext_handle = self.canvas.create_text(
            size_of_board - 120, size_of_board - 20,
            text=text, fill=color, font="cmr 15 bold", tags="turn"
        )

    def click(self, event):
        grid = [event.x, event.y]
        pos, t = self.convert_grid_to_logical_position(grid)

        if t and not self.is_grid_occupied(pos, t):

            self.update_board(t, pos)
            self.make_edge(t, pos)
            self.mark_box()
            self.refresh_board()

            if self.pointsScored:
                self.pointsScored = False
            else:
                self.player1_turn = not self.player1_turn

            if self.is_gameover():
                p1 = len(np.argwhere(self.board_status == -4))
                p2 = len(np.argwhere(self.board_status == 4))

                print(f"GAME OVER! Scores calculated -> P1: {p1}, P2: {p2}")

                if p1 > p2:
                    return "Winner: Player 1", p1, p2
                if p2 > p1:
                    return "Winner: Player 2", p1, p2
                return "It's a tie", p1, p2

            self.display_turn_text()

        return None

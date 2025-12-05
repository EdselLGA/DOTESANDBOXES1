import numpy as np

class AIEngine:
    def __init__(self, engine):
        self.engine = engine



    def easy_move(self):
        moves = []

        for r in range(self.engine.row_status.shape[0]):
            for c in range(self.engine.row_status.shape[1]):
                if self.engine.row_status[r][c] == 0:
                    moves.append(("row", (r, c)))

        for r in range(self.engine.col_status.shape[0]):
            for c in range(self.engine.col_status.shape[1]):
                if self.engine.col_status[r][c] == 0:
                    moves.append(("col", (r, c)))

        if not moves:
            return None

        return moves[np.random.randint(0, len(moves))]

    def medium_move(self):
        for br in range(5):
            for bc in range(5):

                box_edges = [
                    ("row", (br, bc)),
                    ("row", (br, bc+1)),
                    ("col", (br, bc)),
                    ("col", (br+1, bc))
                ]

                filled_edges = 0
                empty_edge = None

                for t, (r, c) in box_edges:
                    if t == "row":
                        if self.engine.row_status[r][c] == 1:
                            filled_edges += 1
                        else:
                            empty_edge = ("row", (r, c))

                    else:
                        if self.engine.col_status[r][c] == 1:
                            filled_edges += 1
                        else:
                            empty_edge = ("col", (r, c))

                if filled_edges == 3 and empty_edge is not None:
                    return empty_edge

        return self.easy_move()

    def hard_move(self):
        return self.engine.hints.get_best_move()

    def get_ai_move(self, difficulty):
        if difficulty == "easy":
            return self.easy_move()
        if difficulty == "medium":
            return self.medium_move()
        if difficulty == "hard":
            return self.hard_move()
        return None

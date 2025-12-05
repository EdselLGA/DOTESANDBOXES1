import numpy as np

class HintEngine:
    def __init__(self, engine):
        self.engine = engine
        self.N = 6

    # =====================================================
    # PUBLIC: returns ("row"/"col", (r,c)) of best move
    # =====================================================
    def get_best_move(self):
        moves = self._get_all_moves()
        if not moves:
            return None

        best_score = -999999
        best_move = None

        for move in moves:
            score = self._evaluate(move)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _get_all_moves(self):
        moves = []

        for r in range(self.N - 1):
            for c in range(self.N):
                if self.engine.row_status[r][c] == 0:
                    moves.append(("row", (r, c)))

        for r in range(self.N):
            for c in range(self.N - 1):
                if self.engine.col_status[r][c] == 0:
                    moves.append(("col", (r, c)))

        return moves

    # =====================================================
    # Heuristic evaluation function (core)
    # =====================================================
    def _evaluate(self, move):
        t, (r, c) = move
        score = 0

        self._apply(t, r, c)

        if self._would_complete_box():
            score += 100

        if self._creates_three_sided_box():
            score -= 50

        chain_gain = self._estimate_chain_gain()
        score += chain_gain * 20

        touching = self._count_touching_sides(move)
        if touching == 0:
            score += 2
        elif touching == 1:
            score += 5
        elif touching == 2:
            score += 3

        self._undo(t, r, c)

        return score

    def _apply(self, t, r, c):
        if t == "row":
            self.engine.row_status[r][c] = 1
        else:
            self.engine.col_status[r][c] = 1

    def _undo(self, t, r, c):
        if t == "row":
            self.engine.row_status[r][c] = 0
        else:
            self.engine.col_status[r][c] = 0

    def _would_complete_box(self):
        for r in range(self.N - 1):
            for c in range(self.N - 1):

                if self.engine.box_owner[r][c] != 0:
                    continue

                top    = self.engine.row_status[r][c] == 1
                bottom = self.engine.row_status[r][c + 1] == 1
                left   = self.engine.col_status[r][c] == 1
                right  = self.engine.col_status[r + 1][c] == 1

                if top and bottom and left and right:
                    return True

        return False

    # =====================================================
    # 3-sided trap check
    # =====================================================
    def _creates_three_sided_box(self):
        for r in range(self.N - 1):
            for c in range(self.N - 1):

                if self.engine.box_owner[r][c] != 0:
                    continue

                sides = (
                    self.engine.row_status[r][c] +
                    self.engine.row_status[r][c + 1] +
                    self.engine.col_status[r][c] +
                    self.engine.col_status[r + 1][c]
                )

                if sides == 3:
                    return True

        return False

    # =====================================================
    # Chain estimation: count boxes with 2 sides
    # =====================================================
    def _estimate_chain_gain(self):
        chain = 0

        for r in range(self.N - 1):
            for c in range(self.N - 1):

                if self.engine.box_owner[r][c] != 0:
                    continue

                sides = (
                    self.engine.row_status[r][c] +
                    self.engine.row_status[r][c + 1] +
                    self.engine.col_status[r][c] +
                    self.engine.col_status[r + 1][c]
                )

                if sides == 2:
                    chain += 1

        return chain

    # =====================================================
    # Count how many sides of nearby boxes touch the move
    # Helps rank "safe" edges
    # =====================================================
    def _count_touching_sides(self, move):
        t, (r, c) = move

        def count_box_sides(br, bc):
            if br < 0 or bc < 0 or br >= self.N-1 or bc >= self.N-1:
                return 0

            top    = self.engine.row_status[br][bc]
            bottom = self.engine.row_status[br][bc+1]
            left   = self.engine.col_status[br][bc]
            right  = self.engine.col_status[br+1][bc]

            return top + bottom + left + right

        total = 0

        if t == "row":
            # affects box above and below the row
            if c - 1 >= 0:
                total += count_box_sides(r, c - 1)
            if c < self.N - 1:
                total += count_box_sides(r, c)

        else:
            # affects box left and right of a vertical line
            if r - 1 >= 0:
                total += count_box_sides(r - 1, c)
            if r < self.N - 1:
                total += count_box_sides(r, c)

        return total

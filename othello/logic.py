class Rule:
    def __init__(self, board, cell, turn):
        self.board = board
        self.cell = cell
        self.turn = turn
        # cellのインデックスを二次元のインデックスに変換
        # 行、列のインデックス
        self.cell_row = cell // 8
        self.cell_column = cell % 8
        # オセロの駒の処理のために、拡張した盤面を用いることにする
        # 拡張した盤面
        extended_board = []
        for _ in range(10):
            extended_board.append(["empty"] * 10)
        for i in range(8):
            for j in range(8):
                extended_board[i + 1][j + 1] = board[i][j]
        self.extended_board = extended_board
        self.extended_cell_row = self.cell_row + 1
        self.extended_cell_column = self.cell_column + 1

    def can_place_piece(self):
        can_place_piece = False
        # 黒の手番。当該cellの周囲の８方向に駒を置けるかを確認する。
        if (
            self.turn == "black's turn"
            and self.board[self.cell_row][self.cell_column] == "empty"
        ):
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if not (dy == 0 and dx == 0):
                        y = self.extended_cell_row + dy
                        x = self.extended_cell_column + dx
                        if not (1 <= y < 9 and 1 <= x < 9):
                            continue
                        if self.extended_board[y][x] == "white":
                            y += dy
                            x += dx
                            while 1 <= y < 9 and 1 <= x < 9:
                                if self.extended_board[y][x] == "white":
                                    y += dy
                                    x += dx
                                if self.extended_board[y][x] == "empty":
                                    break
                                if self.extended_board[y][x] == "black":
                                    can_place_piece = True
                                    break
            return can_place_piece

        # 白の手番。当該cellの周囲の８方向に駒を置けるかを確認する。
        if (
            self.turn == "white's turn"
            and self.board[self.cell_row][self.cell_column] == "empty"
        ):
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if not (dy == 0 and dx == 0):
                        y = self.extended_cell_row + dy
                        x = self.extended_cell_column + dx
                        if not (1 <= y < 9 and 1 <= x < 9):
                            continue
                        if self.extended_board[y][x] == "black":
                            y += dy
                            x += dx
                            while 1 <= y < 9 and 1 <= x < 9:
                                if self.extended_board[y][x] == "black":
                                    y += dy
                                    x += dx
                                if self.extended_board[y][x] == "empty":
                                    break
                                if self.extended_board[y][x] == "white":
                                    can_place_piece = True
                                    break
            return can_place_piece

    def place_piece(self):
        # 黒の手番
        if self.turn == "black's turn":
            # 打ったセルを黒にする
            self.board[self.cell_row][self.cell_column] = "black"
            # 以下、黒にひっくり返す処理
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if not (dy == 0 and dx == 0):
                        y = self.extended_cell_row + dy
                        x = self.extended_cell_column + dx
                        n = 0  # ひっくり返す駒枚数を各方向ごとに数える
                        if not (1 <= y < 9 and 1 <= x < 9):
                            continue
                        if self.extended_board[y][x] == "white":
                            y += dy
                            x += dx
                            n += 1
                            while 1 <= y < 9 and 1 <= x < 9:
                                if self.extended_board[y][x] == "white":
                                    y += dy
                                    x += dx
                                    n += 1
                                if self.extended_board[y][x] == "empty":
                                    break
                                if self.extended_board[y][x] == "black":
                                    # 駒(n枚)をひっくり返す
                                    for r in range(1, n + 1):
                                        self.board[self.cell_row + r * dy][
                                            self.cell_column + r * dx
                                        ] = "black"
                                    break

        # 白の手番。
        if self.turn == "white's turn":
            # 打ったセルを白にする
            self.board[self.cell_row][self.cell_column] = "white"
            # 以下、白にひっくり返す処理
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if not (dy == 0 and dx == 0):
                        y = self.extended_cell_row + dy
                        x = self.extended_cell_column + dx
                        n = 0  # ひっくり返す駒枚数を各方向ごとに数える
                        if not (1 <= y < 9 and 1 <= x < 9):
                            continue
                        if self.extended_board[y][x] == "black":
                            y += dy
                            x += dx
                            n += 1
                            while 1 <= y < 9 and 1 <= x < 9:
                                if self.extended_board[y][x] == "black":
                                    y += dy
                                    x += dx
                                    n += 1
                                if self.extended_board[y][x] == "empty":
                                    break
                                if self.extended_board[y][x] == "white":
                                    # 駒(n枚)をひっくり返す
                                    for r in range(1, n + 1):
                                        self.board[self.cell_row + r * dy][
                                            self.cell_column + r * dx
                                        ] = "white"
                                    break

    def change_turn(self):
        # 黒の手番の時は、白の手番に変更する
        if self.turn == "black's turn":
            self.turn = "white's turn"
        # 白の手番の時は、黒の手番に変更する
        else:
            self.turn = "black's turn"


def end_game(board):
    black_count = 0
    white_count = 0

    for row in board:
        for cell in row:
            if cell == "black":
                black_count += 1
            elif cell == "white":
                white_count += 1

    if black_count > white_count:
        winner = "black"
    elif black_count < white_count:
        winner = "white"
    else:
        winner = "draw"
    return {
        "blackCount": black_count,
        "whiteCount": white_count,
        "winner": winner,
    }

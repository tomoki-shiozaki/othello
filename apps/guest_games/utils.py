from itertools import product


def default_board():
    board = [["empty" for _ in range(8)] for _ in range(8)]
    board[3][3] = "black"
    board[4][4] = "black"
    board[3][4] = "white"
    board[4][3] = "white"
    return board


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

    # 周囲の８つの方向に対して、駒を置くことができるか確認する
    # dx, dyは1, -1 ,0のいずれか（(x, y)=(0, 0)を除く）
    def find_reversable_pieces_in_each_direction(self, dy, dx):
        can_place_piece = False
        reversable_pieces = []
        reversed_pieces = 0  # ひっくり返す（可能性のある）駒の枚数を数える
        # 結果を返すための変数（初期状態）
        result = {
            "can_place_piece": can_place_piece,
            "reversable_pieces": reversable_pieces,
        }

        # ターンに応じた色の設定
        if self.turn == "black's turn":
            placed_piece_color = "black"
            reversed_piece_color = "white"
        elif self.turn == "white's turn":
            placed_piece_color = "white"
            reversed_piece_color = "black"

        # 駒を置いた場所に既に駒がおかれている場合は処理を終了する。
        if self.board[self.cell_row][self.cell_column] != "empty":
            return result

        # 以下、dy, dxの方向に駒がおけるかを確認する
        y = self.extended_cell_row + dy
        x = self.extended_cell_column + dx

        # 盤面の範囲外の場合は処理を終了する
        if not (1 <= y < 9 and 1 <= x < 9):
            return result

        # ひっくり返せる駒がある場合
        if self.extended_board[y][x] == reversed_piece_color:
            y += dy
            x += dx
            reversed_pieces += 1

            # はさめる駒を探す
            while 1 <= y < 9 and 1 <= x < 9:
                # はさめる駒をさらに探す
                if self.extended_board[y][x] == reversed_piece_color:
                    y += dy
                    x += dx
                    reversed_pieces += 1
                # 駒がなく、はさむことができない。処理を終了する
                if self.extended_board[y][x] == "empty":
                    return result
                # はさむことのできる駒を発見
                if self.extended_board[y][x] == placed_piece_color:
                    # 駒を置くことができる
                    result["can_place_piece"] = True
                    # ひっくり返せる駒の位置を追加
                    for r in range(1, reversed_pieces + 1):
                        result["reversable_pieces"].append(
                            {
                                "y": self.cell_row + r * dy,
                                "x": self.cell_column + r * dx,
                            }
                        )
                    return result
        return result

    def find_reversable_pieces(self):
        can_place_piece = False
        reversable_pieces = []
        # 結果を返すための変数（初期化してある）
        result = {
            "can_place_piece": can_place_piece,
            "reversable_pieces": reversable_pieces,
        }
        for dy, dx in product([-1, 0, 1], repeat=2):
            if not (dy == 0 and dx == 0):
                result_in_each_direction = (
                    self.find_reversable_pieces_in_each_direction(dy, dx)
                )
                if result_in_each_direction["can_place_piece"]:
                    result["can_place_piece"] = True
                    result["reversable_pieces"] += result_in_each_direction[
                        "reversable_pieces"
                    ]
        return result

    def place_and_reverse_pieces(self, reversable_pieces):
        # ターンに応じた色の設定
        if self.turn == "black's turn":
            placed_piece_color = "black"
        elif self.turn == "white's turn":
            placed_piece_color = "white"

        # 駒を置く
        self.board[self.cell_row][self.cell_column] = placed_piece_color
        # 駒を裏返す
        for cell_position in reversable_pieces:
            self.board[cell_position["y"]][cell_position["x"]] = placed_piece_color

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

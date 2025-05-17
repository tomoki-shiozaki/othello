from ..logic import Rule, end_game
from django.test import TestCase


class TestOthelloGameLogic(TestCase):
    def setUp(self):
        self.board = [["empty"] * 8 for _ in range(8)]
        self.board[3][3] = "black"
        self.board[3][4] = "white"
        self.board[4][3] = "white"
        self.board[4][4] = "black"

    def test_find_reversable_pieces(self):
        # 黒のターンで、(2, 4)に駒を置けるか
        rule = Rule(self.board, 20, "black's turn")
        result = rule.find_reversable_pieces()

        self.assertTrue(result["can_place_piece"])
        self.assertEqual(len(result["reversable_pieces"]), 1)
        self.assertTrue(
            any(item == {"y": 3, "x": 4} for item in result["reversable_pieces"])
        )

    def test_find_reversable_pieces_invalid(self):
        # (0, 0)に駒を置けるか。周囲に逆転できる駒がなく、無効な手であることを確認
        rule = Rule(self.board, 0, "black's turn")
        result = rule.find_reversable_pieces()

        self.assertFalse(result["can_place_piece"])
        self.assertEqual(len(result["reversable_pieces"]), 0)

    def test_place_and_reverse_pieces_black_turn(self):
        # 黒のターンで、(2, 4)に駒を置く
        rule = Rule(self.board, 20, "black's turn")
        result = rule.find_reversable_pieces()
        reversable_pieces = result["reversable_pieces"]

        # (2, 4)は黒、(3, 3)は黒、(3, 4)は黒、(4, 3)は白、(4, 4)は黒
        rule.place_and_reverse_pieces(reversable_pieces)
        self.assertEqual(rule.board[2][4], "black")
        self.assertEqual(rule.board[3][4], "black")

    def test_place_and_reverse_pieces_white_turn(self):
        # 白のターンで、(2, 3)に駒を置く
        rule = Rule(self.board, 19, "white's turn")
        reversable_pieces = [{"y": 3, "x": 3}]
        rule.place_and_reverse_pieces(reversable_pieces)

        self.assertEqual(rule.board[2][3], "white")
        self.assertEqual(rule.board[3][3], "white")

    def test_place_and_reverse_pieces_no_reversal(self):
        # 駒を置く場所にひっくり返す駒がない場合
        reversable_pieces = []
        rule = Rule(self.board, 0, "black's turn")
        rule.place_and_reverse_pieces(reversable_pieces)

        # (0, 0)に黒の駒を置く場合、その周辺の駒が影響を受けないことを確認
        self.assertEqual(self.board[0][0], "black")
        self.assertEqual(self.board[0][1], "empty")
        self.assertEqual(self.board[1][0], "empty")
        self.assertEqual(self.board[1][1], "empty")

    def test_change_turn_black_turn(self):
        rule = Rule(self.board, 0, "black's turn")
        rule.change_turn()

        self.assertEqual(rule.turn, "white's turn")
        # 他のボード状態が変わっていないことを確認
        self.assertEqual(self.board[3][3], "black")
        self.assertEqual(self.board[4][4], "black")

    def test_change_turn_white_turn(self):
        rule = Rule(self.board, 0, "white's turn")
        rule.change_turn()

        self.assertEqual(rule.turn, "black's turn")
        # 他のボード状態が変わっていないことを確認
        self.assertEqual(self.board[3][3], "black")
        self.assertEqual(self.board[4][4], "black")

    def test_end_game_winner_is_black(self):
        self.board[2][4] = "black"
        self.board[3][4] = "black"
        result = end_game(self.board)
        self.assertEqual(result["blackCount"], 4)
        self.assertEqual(result["whiteCount"], 1)
        self.assertEqual(result["winner"], "black")

    def test_end_game_winner_is_white(self):
        self.board[2][3] = "white"
        self.board[3][3] = "white"
        result = end_game(self.board)
        self.assertEqual(result["blackCount"], 1)
        self.assertEqual(result["whiteCount"], 4)
        self.assertEqual(result["winner"], "white")

    def test_end_game_draw(self):
        result = end_game(self.board)
        self.assertEqual(result["blackCount"], 2)
        self.assertEqual(result["whiteCount"], 2)
        self.assertEqual(result["winner"], "draw")

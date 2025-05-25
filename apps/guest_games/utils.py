def default_board():
    board = [["empty" for _ in range(8)] for _ in range(8)]
    board[3][3] = "black"
    board[4][4] = "black"
    board[3][4] = "white"
    board[4][3] = "white"
    return board

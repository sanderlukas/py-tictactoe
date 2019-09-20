def print_board(board):
    i = 0
    for row in board:
        print(" " + row[0] + " | " + row[1] + " | " + row[2])
        i += 1
        if i != 3:
            print(11 * "-")
        else:
            print()


def is_gameboard_filled(board):
    for row in board:
        s = set(row)
        if "." in s:
            return False
    return True


def evaluate(board):
    for i in range(3):
        if board[i][0] == board[i][1] and board[i][1] == board[i][2]:
            if board[i][0] == player:
                return 10
            elif board[i][0] == opponent:
                return -10

    for i in range(3):
        if board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            if board[0][i] == player:
                return 10
            elif board[0][i] == opponent:
                return -10

    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        if board[0][0] == player:
            return 10
        elif board[0][0] == opponent:
            return -10

    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        if board[0][2] == player:
            return 10
        elif board[0][2] == opponent:
            return -10
    return 0


def minimax(board, depth, isMax):
    score = evaluate(board)

    if score == 10:
        return score - depth

    if score == -10:
        return score - depth

    if is_gameboard_filled(board):
        return 0

    if isMax:
        best = -1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == ".":
                    board[i][j] = player
                    best = max(best, minimax(board, depth + 1, not isMax))
                    board[i][j] = "."
        return best
    else:
        best = 1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == ".":
                    board[i][j] = opponent
                    best = min(best, minimax(board, depth + 1, not isMax))
                    board[i][j] = "."
        return best


def find_best_move(board):
    best_value = -1000
    best_move = [-1, -1]

    for i in range(3):
        for j in range(3):
            if board[i][j] == ".":
                board[i][j] = player
                move_value = minimax(board, 0, False)
                board[i][j] = "."

                if move_value > best_value:
                    best_move = [i, j]
                    best_value = move_value
    return best_move


def check_correct_coords(move):
    if len(move) != 3 and move[1] != " " and (int(move[0]) not in range(3) or int(move[2]) not in range(3)):
        return False
    return True


def make_move(turn, move, board):
    global game_finished
    if isinstance(move, list):
        x, y = move
    else:
        x, y = list(map(int, move.split()))

    if board[x][y] == ".":
        board[x][y] = turn
    else:
        if not is_gameboard_filled(board):
            print("Cell is filled! Choose another move!\n")
            return False
    print_board(board)
    return True


markers = ["X", "O"]
game_board = [
    [".", ".", "."],
    [".", ".", "."],
    [".", ".", "."]
]

player = input("[X / O]? ")
while player not in markers:
    print("Choose either X or O!")
    player = input("[X / O]? ")

opponent = "O" if player == "X" else "X"

print("\nPlayer -", player)
print("Opponent -", opponent)
print()
print_board(game_board)
print("Valid moves are between 0 and 2.\nSeparate the indexes " +
      "with a space e.g. '1 1' which fills the second cell of the second row.")

game_finished = False
while not game_finished:
    player_move = input("Your move?: ")
    while not check_correct_coords(player_move):
        player_move = input("Your move?: ")

    players_valid_move = make_move(player, player_move, game_board)
    while not players_valid_move:
        player_move = input("Your move?: ")
        players_valid_move = make_move(player, player_move, game_board)

    status = evaluate(game_board)
    game_draw = is_gameboard_filled(game_board)
    if status != 0:
        print("Winner -> Player({})".format(player))
        break
    if game_draw:
        print("Draw game!")
        break

    ai_move = find_best_move(game_board)
    make_move(opponent, ai_move, game_board)

    status = evaluate(game_board)
    game_draw = is_gameboard_filled(game_board)
    if status != 0:
        print("Winner -> Computer({})".format(opponent))
        break
    if game_draw:
        print("Draw game!")
        break

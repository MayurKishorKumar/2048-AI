import numpy as np

NUMBER_OF_MOVES = 4
SAMPLE_COUNT = 50

SPM_SCALE_PARAM = 10
SL_SCALE_PARAM = 4
SEARCH_PARAM = 200

from game_functions import add_new_tile, random_move, \
    move_down, move_left, \
    move_right, move_up


def get_search_params(noofmoves):
    searches_per_move = SPM_SCALE_PARAM * (1 + (noofmoves // SEARCH_PARAM))
    search_length = SL_SCALE_PARAM * (1 + (noofmoves // SEARCH_PARAM))
    return searches_per_move, search_length


def ai_move(board, searches_per_move, search_length):
    dic = {0: 0, 2: 0, 4: 4, 8: 16, 16: 48, 32: 128, 64: 320, 128: 768, 256: 1792, 512: 4096, 1024: 9216, 2048: 20480}
    fmove = [move_left, move_up, move_down, move_right]
    fscores = np.zeros(NUMBER_OF_MOVES)
    for findex in range(NUMBER_OF_MOVES):
        fmovefun = fmove[findex]
        fboard, fmove_valid, fscore = fmovefun(board)
        if fmove_valid:
            fboard = add_new_tile(fboard)
            fscores[findex] += fscore
        else:
            continue
        for _ in range(searches_per_move):
            noofmoves = 1
            final_board = np.copy(fboard)
            game_valid = True
            while game_valid and noofmoves < search_length:
                final_board, game_valid, score = random_move(final_board)
                if game_valid:
                    final_board = add_new_tile(final_board)
                    fscores[findex] += score
                    noofmoves += 1
    best_move_index = np.argmax(fscores)
    best_move = fmove[best_move_index]
    final_board, game_valid, score = best_move(board)
    for elem in final_board:
        for ele in elem:
            score += dic[ele]
    print(score)
    return final_board, game_valid, score


def ai_move3(board, searches_per_move, search_length):
    dic = {0: 0, 2: 0, 4: 4, 8: 16, 16: 48, 32: 128, 64: 320, 128: 768, 256: 1792, 512: 4096, 1024: 9216, 2048: 20480}
    len = 0
    fmove = [move_left, move_up, move_down, move_right]
    available = []
    for ele in fmove:
        x, y, z = ele(board)
        if y:
            available.append(ele)

    if (available) == None:
        return board, False
    max_score = float('-inf')
    alpha = float('-inf')
    beta = float('-inf')
    depth = 1
    max_depth = 8
    for ele in available:
        board1, y, z = ele(board)
        score = search2(board1, alpha, beta, depth, max_depth)
        if score > max_score:
            score = max_score
            max_move = ele
    x, y, z = max_move(board)
    score = 0
    for elem in x:
        for ele in elem:
            score += dic[ele]
    print(score)
    return x, True, score


def ai_move2(board, searches_per_move, search_length):
    len = 0
    dic = {0: 0, 2: 0, 4: 4, 8: 16, 16: 48, 32: 128, 64: 320, 128: 768, 256: 1792, 512: 4096, 1024: 9216, 2048: 20480}
    fmove = [move_left, move_up, move_down, move_right]
    available = []
    for ele in fmove:
        x, y, z = ele(board)
        if y:
            available.append(ele)

    if (available) == None:
        return board, False
    max_score = float('-inf')
    alpha = float('-inf')
    beta = float('-inf')
    depth = 1
    max_depth = 5
    for ele in available:
        board1, y, z = ele(board)
        score = search2(board1, alpha, beta, depth, max_depth)
        if score > max_score:
            score = max_score
            max_move = ele
    x, y, z = max_move(board)
    score = 0
    for elem in x:
        for ele in elem:
            score += dic[ele]
    print(score)
    return x, True, score
    return x, True


def search(board, alpha, beta, depth, max_depth):
    if depth > max_depth:
        return evaluate(board)
    v = float('-inf')
    fmove = [move_left, move_up, move_down, move_right]
    available = []
    tot = 0
    lenth = 0
    for ele in fmove:
        x, y, z = ele(board)
        if y:
            available.append(ele)
    if len(available) == 0:
        return evaluate(board)
    for i in range(len(available)):
        board1, y, z = available[i](board)

        tot += search(board1, alpha, beta, depth + 1, max_depth)
        lenth += 1
        i = i + 1

    return tot / lenth


def search2(board, alpha, beta, depth, max_depth):
    if depth > max_depth:
        return evaluate(board)
    v = float('-inf')
    fmove = [move_left, move_up, move_down, move_right]
    available = []
    for ele in fmove:
        x, y, z = ele(board)
        if y:
            available.append(ele)
    if len(available) == 0:
        return evaluate(board)
    for i in range(len(available)):
        board1, y, z = available[i](board)
        prev_v = v
        v = max(v, search(board1, alpha, beta, depth + 1, max_depth))
        if v >= beta:
            return v
        alpha = max(alpha, v)
        i = i + 1
    return v


def evaluate(board):
    empty = 0
    max_score = 0
    result = 0
    WEIGHT_MATRIX = [
        [2048, 1024, 64, 32],
        [512, 128, 16, 2],
        [256, 8, 2, 1],
        [4, 2, 1, 1]
    ]
    mono = 0

    row, col = len(board), len(board[0]) if len(board) > 0 else 0
    for r in board:
        diff = r[0] - r[1]
        for i in range(col - 1):
            if (r[i] - r[i + 1]) * diff <= 0:
                mono += 1
            diff = r[i] - r[i + 1]

    for j in range(row):
        diff = board[0][j] - board[1][j]
        for k in range(col - 1):
            if (board[k][j] - board[k + 1][j]) * diff <= 0:
                mono += 1
            diff = board[k][j] - board[k + 1][j]
    smoothness = 0

    row, col = len(board), len(board[0]) if len(board) > 0 else 0
    for r in board:
        for i in range(col - 1):
            smoothness += abs(r[i] - r[i + 1])
            pass
    for j in range(row):
        for k in range(col - 1):
            smoothness += abs(board[k][j] - board[k + 1][j])
    for i in range(len(board)):
        for j in range(len(board)):
            result += board[i][j] * WEIGHT_MATRIX[i][j]
    for ele in board:
        for elem in ele:
            if elem == 0:
                empty += 1
    return smoothness + mono + result + empty
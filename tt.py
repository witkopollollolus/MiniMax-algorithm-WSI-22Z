import copy
import math
import random

def check_full(board):
    full = True
    for row in range(heigth):
        for column in range(width):
            if board[row][column] == 0:
                full = False
    return full

def check_state(board):
    for row in range(heigth):
        for column in range(width-3):
            if board[row][column]+board[row][column+1]+board[row][column+2]+board[row][column+3] == 4:
                return heigth*width
            elif board[row][column]+board[row][column+1]+board[row][column+2]+board[row][column+3] == -4:
                return -heigth*width
    for row in range(heigth-3):
        for column in range(width):
            if board[row][column]+board[row+1][column]+board[row+2][column]+board[row+3][column] == 4:
                return heigth*width
            elif board[row][column]+board[row+1][column]+board[row+2][column]+board[row+3][column] == -4:
                return -heigth*width
    for row in range(heigth-3):
        for column in range(width-3):
            if board[row][column]+board[row+1][column+1]+board[row+2][column+2]+board[row+3][column+3] == 4:
                return heigth*width
            elif board[row][column]+board[row+1][column+1]+board[row+2][column+2]+board[row+3][column+3] == -4:
                return -heigth*width
    for row in range(heigth-3):
        for column in range(width-3):
            if board[row][width-column-1]+board[row+1][width-column-2]+board[row+2][width-column-3]+board[row+3][width-column-4] == 4:
                return heigth*width
            elif board[row][width-column-1]+board[row+1][width-column-2]+board[row+2][width-column-3]+board[row+3][width-column-4] == -4:
                return -heigth*width
    return 0

def board_print(board):
    for n in range(heigth):
        row = []
        for m in range(width):
            if board[n][m] == 1:
                row.append('x')
            elif board[n][m] == -1:
                row.append('o')
            elif board[n][m] == 0:
                row.append(' ')
        print(row)
    return 0


def successors(board, turn):
    board_successors = []
    successor_tile = []
    for column in range(width):
        temp = copy.deepcopy(board)
        if temp[heigth-1][column] == 0:
            if turn == 1:
                temp[heigth-1][column] = 1
            else:
                temp[heigth-1][column] = -1
            board_successors.append(temp)
            successor_tile.append((heigth-1, column))
        else:
            for row in range(heigth):
                if temp[heigth-row-2][column] == 0:
                    if turn == 1:
                        temp[heigth-row-2][column] = 1
                    else:
                        temp[heigth-row-2][column] = -1
                    board_successors.append(temp)
                    successor_tile.append((heigth-row-2, column))
                    break
    return board_successors, successor_tile


def heuristic(tile, turn):
    n = tile[0]
    m = tile[1]
    return turn*(-math.floor(abs(n-(heigth-1)/2))-math.floor(abs(m-(width-1)/2))+math.floor(abs((heigth-1)/2))+math.floor(abs((width-1)/2))+1)


def minimax(board, turn, d):
    if check_state(board) != 0:
        return check_state(board)
    if check_full(board):
        return 0
    if d == 0:
        if turn == 1:
            return 1
        else:
            return -1
    w = []     
    for board_state in successors(board, turn)[0]:
        w.append(minimax(board_state, -turn, d-1))
    if turn == 1:
        return max(w)
    else:
        return min(w)


def main():
    board = []
    global heigth
    global width
    heigth = 4
    width = 5
    depth = 3
    for m in range(heigth):
        row = []
        for n in range(width):
            row.append(0)
        board.append(row)
    turn = 1
    board_print(board)
    print('-----'*width)
    while check_state(board) == 0 and not check_full(board):
        estimations = []
        for k, i in enumerate(successors(board, turn)[0]):
            if minimax(i, -turn, depth) == 1 or minimax(i, -turn, depth) == -1:
                estimations.append(heuristic(successors(board, turn)[1][k], turn))
            else:
                estimations.append(minimax(i, -turn, depth))
        moves = []
        print(estimations)
        for l, j in enumerate(successors(board, turn)[0]):
            if minimax(j, -turn, depth) == 1 or minimax(j, -turn, depth) == -1:
                if turn == 1:
                    if heuristic(successors(board, turn)[1][l], turn) == max(estimations):
                        moves.append(j)
                else:
                    if heuristic(successors(board, turn)[1][l], turn) == min(estimations):
                        moves.append(j)
            else:
                if turn == 1:
                    if minimax(j, -turn, depth) == max(estimations):
                        moves.append(j)
                else:
                    if minimax(j, -turn, depth) == min(estimations):
                        moves.append(j)
        move = random.randint(0, len(moves)-1)
        board = moves[move]
        turn = -turn
        board_print(board)
        print('-----'*width)
    if check_state(board) == width*heigth:
        print('MAX won!')
    elif check_state(board) == -width*heigth:
        print('MIN won!')
    else:
        print('DRAW!')


if __name__ == "__main__":
    main()
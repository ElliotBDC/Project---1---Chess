from bboard import BBoard
from copy import deepcopy
#from main import Board

# Evaluation Function
classic_board = [
    ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
    ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
    ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
    ]

piece_scores = {'wp': 100, 'wn': 310, 'wb': 320, 'wr':510, 'wq': 900, 'wk':10000,
                'bp': -100, 'bn': -310, 'bb': -320, 'br':-510, 'bq': -900, 'bk':-10000}

# Piece-square tables for each white piece
piece_squares = {
'wp' : [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0]
],

'wn' : [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
],

'wb' : [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
],

'wr' : [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [0, 0, 0, 5, 5, 0, 0, 0]
],

'wq' : [
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [0, 0, 5, 5, 5, 5, 0, -5],
    [-10, 5, 5, 5, 5, 5, 0, -10],
    [-10, 0, 5, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20]
],

'wk' : [
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [20, 30, 10, 0, 0, 10, 30, 20]
],

'bp' : [
    [0, 0, 0, 0, 0, 0, 0, 0], 
    [5, 10, 10, -20, -20, 10, 10, 5], 
    [5, -5, -10, 0, 0, -10, -5, 5], 
    [0, 0, 0, 20, 20, 0, 0, 0], 
    [5, 5, 10, 25, 25, 10, 5, 5],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [50, 50, 50, 50, 50, 50, 50, 50], 
    [0, 0, 0, 0, 0, 0, 0, 0]],

'bn' : [
    [-50, -40, -30, -30, -30, -30, -40, -50], [-40, -20, 0, 5, 5, 0, -20, -40], [-30, 5, 10, 15, 15, 10, 5, -30], [-30, 0, 15, 20, 20, 15, 0, -30], [-30, 5, 15, 20, 20, 15, 5, -30], [-30, 0, 10, 15, 15, 10, 0, -30], [-40, -20, 0, 0, 0, 0, -20, -40], [-50, -40, -30, -30, -30, -30, -40, -50]],
'bb' : [
    [-20, -10, -10, -10, -10, -10, -10, -20], [-10, 5, 0, 0, 0, 0, 5, -10], [-10, 10, 10, 10, 10, 10, 10, -10], [-10, 0, 10, 10, 10, 10, 0, -10], [-10, 5, 5, 10, 10, 5, 5, -10], [-10, 0, 5, 10, 10, 5, 0, -10], [-10, 0, 0, 0, 0, 0, 0, -10], [-20, -10, -10, -10, -10, -10, -10, -20]],
'br' : [
    [0, 0, 0, 5, 5, 0, 0, 0], [-5, 0, 0, 0, 0, 0, 0, -5], [-5, 0, 0, 0, 0, 0, 0, -5], [-5, 0, 0, 0, 0, 0, 0, -5], [-5, 0, 0, 0, 0, 0, 0, -5], [-5, 0, 0, 0, 0, 0, 0, -5], [5, 10, 10, 10, 10, 10, 10, 5], [0, 0, 0, 0, 0, 0, 0, 0]],
'bq' : [
    [-20, -10, -10, -5, -5, -10, -10, -20], [-10, 0, 5, 0, 0, 0, 0, -10], [-10, 5, 5, 5, 5, 5, 0, -10], [0, 0, 5, 5, 5, 5, 0, -5], [-5, 0, 5, 5, 5, 5, 0, -5], [-10, 0, 5, 5, 5, 5, 0, -10], [-10, 0, 0, 0, 0, 0, 0, -10], [-20, -10, -10, -5, -5, -10, -10, -20]],
'bk' : [
    [20, 30, 10, 0, 0, 10, 30, 20], [20, 20, 0, 0, 0, 0, 20, 20], [-10, -20, -20, -20, -20, -20, -20, -10], [-20, -30, -30, -40, -40, -30, -30, -20], [-30, -40, -40, -50, -50, -40, -40, -30], [-30, -40, -40, -50, -50, -40, -40, -30], [-30, -40, -40, -50, -50, -40, -40, -30], [-30, -40, -40, -50, -50, -40, -40, -30]]
}

def evaluate(board):
    score = 0
    white_material = 0
    black_material = 0
    for index_x, row in enumerate(board):
        for index_y, piece in enumerate(row):
            if piece != "":
                score = score + (piece_scores[piece])
                if piece[0] == "w":
                    white_material = white_material + piece_squares[piece][index_x][index_y]
                else:
                    black_material = black_material + piece_squares[piece][index_x][index_y]
                #print(f"{piece} : {piece_squares[piece][index_x][index_y]}")
    score = score + (white_material - black_material)
    return score


def minimax(depth, state):
        best_move = ""
        if depth == 0:
                return evaluate(state.board), ""
        if state.move % 2 == 0:
            moves = actions(state)
            max = float("-inf")
            if moves == 0:
                if state.isCheckmate("WHITE", state.isInCheck()[1]):
                    return float("inf"), ""
                return 0, ""
            for move in moves:
                new_state = BBoard(result(deepcopy(state), move), state.move+1)
                score = minimax(depth-1, new_state)[0]
                if score > max:
                    max = score
                    best_move = move
            return max, best_move
        else:
            moves = actions(state)
            min = float("inf")
            if moves == 0:
                if state.isCheckmate("BLACK", state.isInCheck()[1]):
                    return float("-inf"), " "
                return 0, " "
            for move in moves:
                new_state = BBoard(result(deepcopy(state), move), state.move+1)
                score = minimax(depth-1, new_state)[0]
                if score < min:
                    min = score
                    best_move = move
            return min, best_move



# [(6, 0, 'wp'), (4, 0)]
    

def actions(state):
    if state.move % 2 == 0:
        #print(state.getAllMoves("WHITE"))
        return state.getAllMoves("WHITE")
    #print("H")
    return state.getAllMoves("BLACK")

# Returns the reuslting board after an action has been made
def result(state, action):
    state.makeMove(action[0], action[1][0], action[1][1])
    #print("     ")
    #for row in state.board:
    #    print(row)
    #print("         ")
    return state.board

def startMiniMax(depth, board):
    b = BBoard(board)
    return minimax(depth, b)
    

#Returns ### if the game is over
#def terminal(state):
#    ...


if __name__ == "__main__":
    b = BBoard(classic_board)

    #print(b.getAllMoves("WHITE"))
    #print(evaluate(classic_board))
    print(minimax(2, b)[1][1])


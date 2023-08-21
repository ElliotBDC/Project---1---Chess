import numpy as np

# Generating array of 64 bit numbers
arr = np.random.randint(0, (2**63)-1, size=(6, 2, 64), dtype=np.int64)

# Generating constant 64 bit numbers to XOR when turn = BLACK
constant_key = np.random.randint(0, (2**63)-1, dtype=np.int64)
print("Zobrist keys loaded")

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

piece_values = {'p' : 0, 'n' : 1, 'b' : 2, 'r' : 3, 'q' : 4, 'k': 5}
colour_values = {'w' : 0, 'b' : 1}

def calculateZobristKey(board, move, all_pieces):
    key = 0
    ### TODO: Change looping through board to looping through piece list (I have to
    # create one first). - Will increase efficiency of program
    #all_pieces = board.white_pieces + board.black_pieces
    for piece in all_pieces:    
        position = (piece[1][0]*8)+piece[1][1]
        key = key ^ arr[piece_values[piece[0][1]], colour_values[piece[0][0]], position]
    if move % 2 == 1:
        key = key ^ constant_key
    return key

keys = {}

def addKey(key, evaluation_score):
    keys[key] = (evaluation_score)


#calculateZobristKey(classic_board, 5)
print(arr)
#print(arr[5, 1, 63])
import numpy as np

RANK_1 = 0b11111111
RANK_4 = RANK_1 << 8*3
RANK_5 = RANK_1 << 8*4
RANK_8 = RANK_1 << 8*7
FILE_H = 0b100000001000000010000000100000001000000010000000100000001
FILE_G = FILE_H << 1
FILE_A = 0b1000000010000000100000001000000010000000100000001000000010000000
FILE_B = FILE_A >> 1

class Board:

    #Declaring the bitboards for each piece
    BP = 0b11111111000000000000000000000000000000000000000000000000
    BN = 0b100001000000000000000000000000000000000000000000000000000000000
    BB = 0b10010000000000000000000000000000000000000000000000000000000000
    BR = 0b1000000100000000000000000000000000000000000000000000000000000000
    BQ = 0b100000000000000000000000000000000000000000000000000000000000
    BK = 0b1000000000000000000000000000000000000000000000000000000000000
    WP = 0b1111111100000000
    WN = 0b1000010
    WB = 0b100100
    WR = 0b10000001
    WQ = 0b1000
    WK = 0b10000
    OCCUPIED = WP|WN|WB|WR|WQ|WK|BP|BN|BB|BR|BQ|BK
    EMPTY = ~OCCUPIED
    WhitePlayerMove = True

    mailboard = [
    ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
    ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
    ['', ' ', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
    ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
    ]

    def __init__(self) -> None:
        pass

    def getAllMoves(self):
        moves = ""
        if self.WhitePlayerMove:
            File_1 = FILE_A
            File_2 = FILE_H
            Rank_1 = 2

num = 5
print(num.bit_count())
print(bin(RANK_8))



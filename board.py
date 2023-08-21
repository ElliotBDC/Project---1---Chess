#import numpy as np
import precomputed

RANK_1 = 0b11111111
RANK_4 = RANK_1 << 8*3
RANK_5 = RANK_1 << 8*4
RANK_8 = RANK_1 << 8*7
FILE_H = 0b100000001000000010000000100000001000000010000000100000001
FILE_G = FILE_H << 1
FILE_A = 0b1000000010000000100000001000000010000000100000001000000010000000
FILE_B = FILE_A >> 1
KNIGHT_MOVES = 0b101000010001000000000001000100001010

LSB_LOOKUP = {
  1: 0,
  2: 1,
  4: 2,
  8: 3,
  16: 4,
  32: 5,
  64: 6,
  128: 7,
  256: 8,
  512: 9,
  1024: 10,
  2048: 11,
  4096: 12,
  8192: 13,
  16384: 14,
  32768: 15,
  65536: 16,
  131072: 17,
  262144: 18,
  524288: 19,
  1048576: 20,
  2097152: 21,
  4194304: 22,
  8388608: 23,
  16777216: 24,
  33554432: 25,
  67108864: 26,
  134217728: 27,
  268435456: 28,
  536870912: 29,
  1073741824: 30,
  2147483648: 31,
  4294967296: 32,
  8589934592: 33,
  17179869184: 34,
  34359738368: 35,
  68719476736: 36,
  137438953472: 37,
  274877906944: 38,
  549755813888: 39,
  1099511627776: 40,
  2199023255552: 41,
  4398046511104: 42,
  8796093022208: 43,
  17592186044416: 44,
  35184372088832: 45,
  70368744177664: 46,
  140737488355328: 47,
  281474976710656: 48,
  562949953421312: 49,
  1125899906842624: 50,
  2251799813685248: 51,
  4503599627370496: 52,
  9007199254740992: 53,
  18014398509481984: 54,
  36028797018963968: 55,
  72057594037927936: 56,
  144115188075855872: 57,
  288230376151711744: 58,
  576460752303423488: 59,
  1152921504606846976: 60,
  2305843009213693952: 61,
  4611686018427387904: 62,
  9223372036854775808: 63
}

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
    PlayerToMovePieces = WP|WN|WB|WR|WQ|WK

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
        self.OCCUPIED = self.WP|self.WN|self.WB|self.WR|self.WQ|self.WK|self.BP|self.BN|self.BB|self.BR|self.BQ|self.BK
        self.EMPTY = ~self.OCCUPIED
        if self.WhitePlayerMove:
            PLAYER_PIECES = self.WP
            ENEMY_PIECES = self.BP|self.BN|self.BB|self.BR|self.BQ|self.BK
            self.PlayerToMovePieces = self.WP|self.WN|self.WB|self.WR|self.WQ|self.WK

            #------------Pawn Moves--------------#

            # Pawn moving 1 square forward

            ForwardOne = PLAYER_PIECES << 8 & EMPTY
            LSB = ForwardOne & -ForwardOne 
            while LSB != 0:
                position = LSB_LOOKUP[LSB]

                if LSB & RANK_8 == 0:
                    pos_1 = position//8
                    pos_2 = str(position%8)
                    moves+= ""+ str(pos_1+1) + pos_2 + str(pos_1) + pos_2
                else:
                    pos_1 = position%8
                    pos_2 = position%8
                    moves += "" + pos_1 + pos_2 + "QP" + pos_1 + pos_2 + "NP" + pos_1 + pos_2 + "RP" + pos_1 + pos_2 + "BP"

                ForwardOne = ForwardOne & ~LSB
                LSB = ForwardOne & -ForwardOne

            # Pawn moving 2 squares forward - Only possible from the starting pawn position

            ForwardTwo = PLAYER_PIECES << 16 & EMPTY & EMPTY << 8 & RANK_4
            LSB = ForwardTwo & -ForwardTwo
            while LSB != 0:
                position = LSB_LOOKUP[LSB]
                pos_1 = position//8
                pos_2 = str(position%8)
                moves+= ""+ str(pos_1+2) + pos_2 + str(pos_1) + pos_2
                ForwardTwo = ForwardTwo & ~LSB
                LSB = ForwardTwo & -ForwardTwo

            # Pawn captures to the right

            CapturesRight = PLAYER_PIECES << 7 & ENEMY_PIECES & ~FILE_A
            LSB = CapturesRight & -CapturesRight
            while LSB != 0:
                position = LSB_LOOKUP[LSB]

                if LSB & RANK_8 == 0:
                    pos_1 = position/8
                    pos_2 = str(position%8)
                    moves+= ""+ str(pos_1+1) + pos_2-1 + str(pos_1) + pos_2
                else:
                    pos_1 = str(position%8-1)
                    pos_2 = str(position%8)
                    moves += "" + pos_1 + pos_2 + "QP" + pos_1 + pos_2 + "NP" + pos_1 + pos_2 + "RP" + pos_1 + pos_2 + "BP"

            CapturesRight = CapturesRight & ~LSB
            LSB = CapturesRight & -CapturesRight

            # Pawn captures to the left

            CapturesLeft = PLAYER_PIECES << 9 & ENEMY_PIECES & ~FILE_H
            LSB = CapturesLeft & -CapturesLeft
            while LSB != 0:
                position = LSB_LOOKUP[LSB]

                if LSB & RANK_8 == 0:
                    pos_1 = position/8
                    pos_2 = str(position%8+1)
                    moves+= ""+ str(pos_1+1) + pos_2 + str(pos_1) + pos_2
                else:
                    pos_1 = str(position%8+1)
                    pos_2 = str(position%8)
                    moves += "" + pos_1 + pos_2 + "QP" + pos_1 + pos_2 + "NP" + pos_1 + pos_2 + "RP" + pos_1 + pos_2 + "BP"

            CapturesLeft = CapturesLeft & ~LSB
            LSB = CapturesLeft & -CapturesLeft

            # En passant to the right

            LSB = PLAYER_PIECES >> 1 & self.BP & RANK_5 & ~FILE_A
            if LSB != 0:
                position = LSB_LOOKUP[LSB]
                moves+= position%8-1 + position%8 + "WE"
            
            # En passant to the left

            LSB = PLAYER_PIECES << 1 & self.BP & RANK_5 & ~FILE_H
            if LSB != 0:
                position = LSB_LOOKUP[LSB]
                moves += position%8+1 + position%8 + "WE"

            #------------Knight Moves--------------#

            moves += self.getKnightMoves(self.WN)

            #------------Bishop Moves--------------#

            moves+= self.getBishopMoves(self.WB)

            #------------Rook Moves--------------#

            moves+= self.getRookMoves(self.WR)

            #------------Queen Moves--------------#

            moves+= self.getBishopMoves(self.WQ)
            moves+= self.getRookMoves(self.WQ)

            #------------King Moves--------------#


        else:
        

            
            PLAYER_PIECES = self.BP
            ENEMY_PIECES = self.WP|self.WN|self.WB|self.WR|self.WQ|self.WK
            self.PlayerToMovePieces = self.BP|self.BN|self.BB|self.BR|self.BQ|self.BK

            # Pawn moving 1 square forward

            ForwardOne = PLAYER_PIECES >> 8 & EMPTY
            LSB = ForwardOne & -ForwardOne 
            while LSB != 0:
                position = LSB_LOOKUP[LSB]

                if LSB & RANK_1 == 0:
                    pos_1 = position//8
                    pos_2 = str(position%8)
                    moves+= ""+ str(pos_1-1) + pos_2 + str(pos_1) + pos_2
                else:
                    pos_1 = position%8
                    pos_2 = position%8
                    moves += "" + pos_1 + pos_2 + "QP" + pos_1 + pos_2 + "NP" + pos_1 + pos_2 + "RP" + pos_1 + pos_2 + "BP"

                ForwardOne = ForwardOne & ~LSB
                LSB = ForwardOne & -ForwardOne

            # Pawn moving 2 squares forward - Only possible from the starting pawn position

            ForwardTwo = PLAYER_PIECES >> 16 & EMPTY & EMPTY >> 8 & RANK_5
            LSB = ForwardTwo & -ForwardTwo
            while LSB != 0:
                position = LSB_LOOKUP[LSB]
                pos_1 = position//8
                pos_2 = str(position%8)
                moves+= ""+ str(pos_1-2) + pos_2 + str(pos_1) + pos_2
                ForwardTwo = ForwardTwo & ~LSB
                LSB = ForwardTwo & -ForwardTwo

            # Pawn captures to the right

            CapturesRight = PLAYER_PIECES >> 7 & ENEMY_PIECES & ~FILE_H
            LSB = CapturesRight & -CapturesRight
            while LSB != 0:
                position = LSB_LOOKUP[LSB]

                if LSB & RANK_1 == 0:
                    pos_1 = position/8
                    pos_2 = str(position%8)
                    moves+= ""+ str(pos_1-1) + pos_2+1 + str(pos_1) + pos_2
                else:
                    pos_1 = str(position%8+1)
                    pos_2 = str(position%8)
                    moves += "" + pos_1 + pos_2 + "QP" + pos_1 + pos_2 + "NP" + pos_1 + pos_2 + "RP" + pos_1 + pos_2 + "BP"

            CapturesRight = CapturesRight & ~LSB
            LSB = CapturesRight & -CapturesRight

            # Pawn captures to the left

            CapturesLeft = PLAYER_PIECES >> 9 & ENEMY_PIECES & ~FILE_A
            LSB = CapturesLeft & -CapturesLeft
            while LSB != 0:
                position = LSB_LOOKUP[LSB]

                if LSB & RANK_1 == 0:
                    pos_1 = position/8
                    pos_2 = str(position%8+1)
                    moves+= ""+ str(pos_1-1) + pos_2 + str(pos_1) + pos_2
                else:
                    pos_1 = str(position%8-1)
                    pos_2 = str(position%8)
                    moves += "" + pos_1 + pos_2 + "QP" + pos_1 + pos_2 + "NP" + pos_1 + pos_2 + "RP" + pos_1 + pos_2 + "BP"

            CapturesLeft = CapturesLeft & ~LSB
            LSB = CapturesLeft & -CapturesLeft

            # En passant to the right

            LSB = PLAYER_PIECES << 1 & self.BP & RANK_5 & ~FILE_A
            if LSB != 0:
                position = LSB_LOOKUP[LSB]
                moves+= position%8+1 + position%8 + "BE"
            
            # En passant to the left

            LSB = PLAYER_PIECES >> 1 & self.BP & RANK_5 & ~FILE_H
            if LSB != 0:
                position = LSB_LOOKUP[LSB]
                moves += position%8-1 + position%8 + "BE"

            #------------Knight Moves--------------#

            moves += self.getKnightMoves(self.BN)

        
        



        return moves
    
    def getKnightMoves(self, KNIGHTS):
        LSB = KNIGHTS & -KNIGHTS
        moves = ""
        print(f"KNIGHTS: {KNIGHTS} + LSB {LSB}")
        while LSB != 0:
            pos = LSB_LOOKUP[LSB]
            Possible_Moves = precomputed.KNIGHT_MOVES[pos] & ~(self.PlayerToMovePieces)
            print(f"LSB {LSB} + Moves {bin(Possible_Moves)}")
            LSB_2 = Possible_Moves & -Possible_Moves
            print(f"LSB 2 V {bin(LSB_2)}")
            while LSB_2 != 0:
                print(LSB_2)
                position = LSB_LOOKUP[LSB_2]
                moves+=""+str(pos//8)+str(pos%8)+str(position//8)+str(position%8)
                Possible_Moves = Possible_Moves & ~LSB_2
                LSB_2 = Possible_Moves & -Possible_Moves
            KNIGHTS = KNIGHTS &~ LSB
            print(f"KNIGHTS 2 {KNIGHTS}")
            LSB = KNIGHTS & -KNIGHTS
            print(f"LSB 2 {LSB}")
        print(moves)
        return moves

    def getRookMoves(self):
        

    def getBishopMoves(self):
        ...

    def getKingMoves(self, king):
        pos = LSB_LOOKUP[king]
        Possible_Moves = precomputed.KING_MOVES[pos] & ~(self.PlayerToMovePieces)
        LSB = Possible_Moves & -Possible_Moves
        while LSB != 0:
            position = LSB_LOOKUP[LSB]
            moves +=pos//8+pos%8+position//8+position%8
            Possible_Moves = Possible_Moves & ~LSB
            LSB = Possible_Moves & -Possible_Moves
        return moves
            


newBoard = Board()
print(newBoard.getAllMoves())
print(f"{int(len(newBoard.getAllMoves())/4)} possible moves")



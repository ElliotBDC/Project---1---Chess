import precomputed
from precomputed import LSB_LOOKUP

RANK_1 = 0b11111111
RANK_4 = RANK_1 << 8*3
RANK_5 = RANK_1 << 8*4
RANK_8 = RANK_1 << 8*7
FILE_H = 0b100000001000000010000000100000001000000010000000100000001
FILE_G = FILE_H << 1
FILE_A = 0b1000000010000000100000001000000010000000100000001000000010000000
FILE_B = FILE_A >> 1
KNIGHT_MOVES = 0b101000010001000000000001000100001010

FILE_MASKS = [72340172838076673, 144680345676153346, 289360691352306692, 
              578721382704613384, 1157442765409226768, 2314885530818453536, 
              4629771061636907072, 9259542123273814144]

RANK_MASKS = [255, 65280, 16711680, 4278190080, 1095216660480, 280375465082880,
            71776119061217280, 18374686479671623680]

POSITIVE_DIAGONAL_MASKS = [1, 258, 66052, 16909320, 4328785936, 1108169199648, 283691315109952,
                72624976668147840, 145249953336295424, 290499906672525312,
                580999813328273408, 1161999622361579520, 2323998145211531264,
                4647714815446351872, 9223372036854775808]

NEGATIVE__DIAGONAL_MASKS = [128, 32832, 8405024, 2151686160, 550831656968, 141012904183812, 
                       36099303471055874, 9241421688590303745, 4620710844295151872, 
                       2310355422147575808, 1155177711073755136, 577588855528488960, 
                       288794425616760832, 144396663052566528, 72057594037927936]


def reverse_bits(bits):
    if bits >= 0:
        return int(bin(bits)[:1:-1], 2)
    else:
        return int(bin(bits)[:2:-1], 2)

class Board:

    #Declaring the bitboards for each piece
    VALID_BOARD = 0b1111111111111111111111111111111111111111111111111111111111111111
    bitboards = {
    'BP' : 0b11111111000000000000000000000000000000000000000000000000,
    'BN' : 0b100001000000000000000000000000000000000000000000000000000000000,
    'BB' : 0b10010000000000000000000000000000000000000000000000000000000000,
    'BR' : 0b1000000100000000000000000000000000000000000000000000000000000000,
    'BQ' : 0b100000000000000000000000000000000000000000000000000000000000,
    'BK' : 0b1000000000000000000000000000000000000000000000000000000000000,
    'WP' : 0b1111111100000000,
    'WN' : 0b1000010,
    'WB' : 0b100100,
    'WR' : 0b10000001,
    'WQ' : 0b1000,
    'WK' : 0b10000,
    'OCCUPIED' : 18446462598732906495

    }            

    EMPTY = ~bitboards['OCCUPIED']
    WhitePlayerMove = True

    mailboard = [
    ['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR'],
    ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP'],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP'],
    ['WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR']
    ]

    def __init__(self) -> None:
        pass

    def getAllMoves(self):
        moves = ""
        #self.bitboards['OCCUPIED'] = self.bitboards['WP']|self.bitboards['WN']|self.bitboards['WB']|self.bitboards['WR']|self.bitboards['WR']|self.bitboards['WK']|self.bitboards['BP']|self.bitboards['BN']|self.bitboards['BB']|self.bitboards['BR']|self.bitboards['BQ']|self.bitboards['BK']
        #self.EMPTY = ~self.bitboards['OCCUPIED']
        if self.WhitePlayerMove:
            self.ENEMY_PIECES = self.bitboards['BP']|self.bitboards['BN']|self.bitboards['BB']|self.bitboards['BR']|self.bitboards['BQ']|self.bitboards['BK']
            self.PlayerToMovePieces = self.bitboards['WP']|self.bitboards['WN']|self.bitboards['WB']|self.bitboards['WR']|self.bitboards['WQ']|self.bitboards['WK']

            #------------Pawn Moves--------------#

            # Pawn moving 1 square forward

            ForwardOne = self.bitboards['WP'] << 8 & self.EMPTY
            LSB = ForwardOne & -ForwardOne 
            while LSB != 0:
                position = LSB_LOOKUP[LSB]

                if LSB & RANK_8 == 0:
                    pos_1 = position//8
                    pos_2 = str(position%8)
                    moves+= str(pos_1-1) + pos_2 + str(pos_1) + pos_2 + "P"
                else:
                    pos_1 = position%8
                    pos_2 = position%8
                    moves += pos_1 + pos_2 + "QPP" + pos_1 + pos_2 + "NPP" + pos_1 + pos_2 + "RPP" + pos_1 + pos_2 + "BPP"

                ForwardOne = ForwardOne & ~LSB
                LSB = ForwardOne & -ForwardOne

            # Pawn moving 2 squares forward - Only possible from the starting pawn position

            ForwardTwo = self.bitboards['WP'] << 16 & self.EMPTY & (self.EMPTY << 8) & RANK_4
            LSB = ForwardTwo & -ForwardTwo
            while LSB != 0:
                position = LSB_LOOKUP[LSB]
                pos_1 = position//8
                pos_2 = str(position%8)
                moves+= str(pos_1-2) + pos_2 + str(pos_1) + pos_2 + "P"
                ForwardTwo = ForwardTwo & ~LSB
                LSB = ForwardTwo & -ForwardTwo

            # Pawn captures to the right

            CapturesRight = self.bitboards['WP'] << 7 & self.ENEMY_PIECES & ~FILE_A
            LSB = CapturesRight & -CapturesRight
            while LSB != 0:
                position = LSB_LOOKUP[LSB]

                if LSB & RANK_8 == 0:
                    pos_1 = position//8
                    pos_2 = position%8
                    moves+= str(pos_1-1) + str(pos_2+1) + str(pos_1) + str(pos_2) + "P"
                else:
                    pos_1 = str(position%8-1)
                    pos_2 = str(position%8)
                    moves += pos_1 + pos_2 + "QPP" + pos_1 + pos_2 + "NPP" + pos_1 + pos_2 + "RPP" + pos_1 + pos_2 + "BPP"

                CapturesRight = CapturesRight & ~LSB
                LSB = CapturesRight & -CapturesRight

            # Pawn captures to the left

            CapturesLeft = self.bitboards['WP'] << 9 & self.ENEMY_PIECES & ~FILE_H
            LSB = CapturesLeft & -CapturesLeft
            while LSB != 0:
                position = LSB_LOOKUP[LSB]

                if LSB & RANK_8 == 0:
                    pos_1 = position//8
                    pos_2 = position%8
                    moves+= str(pos_1-1) + str(pos_2-1) + str(pos_1) + str(pos_2) + "P"
                else:
                    pos_1 = str(position%8+1)
                    pos_2 = str(position%8)
                    moves += pos_1 + pos_2 + "QPP" + pos_1 + pos_2 + "NPP" + pos_1 + pos_2 + "RPP" + pos_1 + pos_2 + "BPP"

                CapturesLeft = CapturesLeft & ~LSB
                LSB = CapturesLeft & -CapturesLeft

            # En passant to the right

            LSB = self.bitboards['WP'] >> 1 & self.bitboards['BP'] & RANK_5 & ~FILE_A
            if LSB != 0:
                position = LSB_LOOKUP[LSB]
                moves+= str(position%8-1) + str(position%8) + "WE"
            
            # En passant to the left

            LSB = self.bitboards['WP'] << 1 & self.bitboards['BP'] & RANK_5 & ~FILE_H
            if LSB != 0:
                position = LSB_LOOKUP[LSB]
                moves += str(position%8+1) + str(position%8) + "WE"

            #------------Knight Moves--------------#

            moves += self.getKnightMoves(self.bitboards['WN'])

            #------------Bishop Moves--------------#

            moves+= self.getBishopMoves(self.bitboards['WB'])

            #------------Rook Moves--------------#

            moves+= self.getRookMoves(self.bitboards['WR'])

            #------------Queen Moves--------------#

            moves+= self.getBishopMoves(self.bitboards['WQ'], True)
            moves+= self.getRookMoves(self.bitboards['WQ'], True)

            #------------King Moves--------------#

            moves+= self.getKingMoves(self.bitboards['WK'])


        else:

            self.ENEMY_PIECES = self.bitboards['WP']|self.bitboards['WN']|self.bitboards['WB']|self.bitboards['WR']|self.bitboards['WQ']|self.bitboards['WK']
            self.PlayerToMovePieces = self.bitboards['BP']|self.bitboards['BN']|self.bitboards['BB']|self.bitboards['BR']|self.bitboards['BQ']|self.bitboards['BK']

            # Pawn moving 1 square forward

            ForwardOne = self.bitboards['BP'] >> 8 & self.EMPTY
            LSB = ForwardOne & -ForwardOne 
            while LSB != 0:
                position = LSB_LOOKUP[LSB]

                if LSB & RANK_1 == 0:
                    pos_1 = position//8
                    pos_2 = str(position%8)
                    moves+=str(pos_1+1) + pos_2 + str(pos_1) + pos_2 + "P"
                else:
                    pos_1 = str(position%8)
                    pos_2 = str(position%8)
                    moves += pos_1 + pos_2 + "QPP" + pos_1 + pos_2 + "NPP" + pos_1 + pos_2 + "RPP" + pos_1 + pos_2 + "BPP"

                ForwardOne = ForwardOne & ~LSB
                LSB = ForwardOne & -ForwardOne

            # Pawn moving 2 squares forward - Only possible from the starting pawn position

            ForwardTwo = self.bitboards['BP'] >> 16 & self.EMPTY & (self.EMPTY >> 8) & RANK_5
            LSB = ForwardTwo & -ForwardTwo
            while LSB != 0:
                position = LSB_LOOKUP[LSB]
                pos_1 = position//8
                pos_2 = str(position%8)
                moves+=str(pos_1+2) + pos_2 + str(pos_1) + pos_2 + "P"
                ForwardTwo = ForwardTwo & ~LSB
                LSB = ForwardTwo & -ForwardTwo

            # Pawn captures to the right

            CapturesRight = self.bitboards['BP'] >> 7 & self.ENEMY_PIECES & ~FILE_H
            LSB = CapturesRight & -CapturesRight
            while LSB != 0:
                position = LSB_LOOKUP[LSB]

                if LSB & RANK_1 == 0:
                    pos_1 = position//8
                    pos_2 = position%8
                    moves+= str(pos_1+1) + str(pos_2-1) + str(pos_1) + str(pos_2) + "P"
                else:
                    pos_1 = str(position%8+1)
                    pos_2 = str(position%8)
                    moves += pos_1 + pos_2 + "QPP" + pos_1 + pos_2 + "NPP" + pos_1 + pos_2 + "RPP" + pos_1 + pos_2 + "BPP"

                CapturesRight = CapturesRight & ~LSB
                LSB = CapturesRight & -CapturesRight

            # Pawn captures to the left

            CapturesLeft = self.bitboards['BP'] >> 9 & self.ENEMY_PIECES & ~FILE_A
            LSB = CapturesLeft & -CapturesLeft
            while LSB != 0:
                position = LSB_LOOKUP[LSB]

                if LSB & RANK_1 == 0:
                    pos_1 = position//8
                    pos_2 = position%8
                    moves+= str(pos_1+1) + str(pos_2+1) + str(pos_1) + str(pos_2) + "P"
                else:
                    pos_1 = str(position%8-1)
                    pos_2 = str(position%8)
                    moves += pos_1 + pos_2 + "QPP" + pos_1 + pos_2 + "NPP" + pos_1 + pos_2 + "RPP" + pos_1 + pos_2 + "BPP"

                CapturesLeft = CapturesLeft & ~LSB
                LSB = CapturesLeft & -CapturesLeft

            # En passant to the right

            LSB = self.bitboards['BP'] << 1 & self.bitboards['BP'] & RANK_5 & ~FILE_H
            if LSB != 0:
                position = LSB_LOOKUP[LSB]
                moves+= str(position%8+1) + str(position%8) + "BEP"
            
            # En passant to the left

            LSB = self.bitboards['BP'] >> 1 & self.bitboards['BP'] & RANK_5 & ~FILE_A
            if LSB != 0:
                position = LSB_LOOKUP[LSB]
                moves += str(position%8-1) + str(position%8) + "BEP"

            #------------Knight Moves--------------#

            moves += self.getKnightMoves(self.bitboards['BN'])

            #------------Bishop Moves--------------#

            moves+= self.getBishopMoves(self.bitboards['BB'])

            #------------Rook Moves--------------#

            moves+= self.getRookMoves(self.bitboards['BR'])

            #------------Queen Moves--------------#

            moves+= self.getBishopMoves(self.bitboards['BQ'], True)
            moves+= self.getRookMoves(self.bitboards['BQ'], True)

            #------------King Moves--------------#

            moves+= self.getKingMoves(self.bitboards['BK'])
        
        return moves

    def getKnightMoves(self, KNIGHTS):
        LSB = KNIGHTS & -KNIGHTS
        moves = ""
        while LSB != 0:
            pos = LSB_LOOKUP[LSB]
            Possible_Moves = precomputed.KNIGHT_MOVES[pos] & ~(self.PlayerToMovePieces) & self.VALID_BOARD
            LSB_2 = Possible_Moves & -Possible_Moves
            while LSB_2 != 0:
                position = LSB_LOOKUP[LSB_2]
                moves += str(pos//8)+str(pos%8)+str(position//8)+str(position%8)+"N"
                Possible_Moves = Possible_Moves & ~LSB_2
                LSB_2 = Possible_Moves & -Possible_Moves
            KNIGHTS = KNIGHTS &~ LSB
            LSB = KNIGHTS & -KNIGHTS
        return moves

    # Using Hyperbola Quintessence to calcdulate Rook and Bishop Moves

    def getRookMoves(self, ROOKS, queen=False):
        piece_type = "R" if queen == False else "Q"
        moves=""
        LSB = ROOKS & -ROOKS
        while LSB !=0:
            position = LSB_LOOKUP[LSB]
            Possible_Horizontal = (self.bitboards['OCCUPIED']-2*position)^reverse_bits(reverse_bits(self.bitboards['OCCUPIED'])-2*reverse_bits(position)) & self.VALID_BOARD
            Possible_Vertical = ((self.bitboards['OCCUPIED']&FILE_MASKS[position%8])-(2*position))^reverse_bits(reverse_bits(self.bitboards['OCCUPIED']&FILE_MASKS[position%8])-(2*reverse_bits(position))) & self.VALID_BOARD
            Possible_Moves = (Possible_Horizontal&RANK_MASKS[position//8]|Possible_Vertical&FILE_MASKS[position%8]) & self.VALID_BOARD & ~self.PlayerToMovePieces
            LSB_2 = Possible_Moves & -Possible_Moves
            while LSB_2 != 0:
                pos_2 = LSB_LOOKUP[LSB_2]
                moves += str(position//8)+str(position%8)+str(pos_2//8)+str(pos_2%8)+piece_type
                Possible_Moves = Possible_Moves & ~LSB_2
                LSB_2 = Possible_Moves & -Possible_Moves
            ROOKS = ROOKS & ~LSB
            LSB = ROOKS & -ROOKS
        return moves

    def getBishopMoves(self, BISHOPS, queen=False):
        piece_type = "B" if queen == False else "Q"
        moves=""
        LSB = BISHOPS & -BISHOPS
        while LSB != 0:
            position = LSB_LOOKUP[LSB]
            Possible_Pos_Diagonal = ((self.bitboards['OCCUPIED']&POSITIVE_DIAGONAL_MASKS[position//8+position%8])-(2*position))^reverse_bits(reverse_bits(self.bitboards['OCCUPIED']&POSITIVE_DIAGONAL_MASKS[position//8+position%8])-(2*reverse_bits(position))) & self.VALID_BOARD
            Possible_Neg_Diagonal = ((self.bitboards['OCCUPIED']&NEGATIVE__DIAGONAL_MASKS[position//8+7-(position%8)])-(2*position))^reverse_bits(reverse_bits(self.bitboards['OCCUPIED']&NEGATIVE__DIAGONAL_MASKS[position//8+7-(position%8)])-(2*reverse_bits(position))) & self.VALID_BOARD
            Possible_Moves = (Possible_Pos_Diagonal&POSITIVE_DIAGONAL_MASKS[position//8+position%8]|Possible_Neg_Diagonal&NEGATIVE__DIAGONAL_MASKS[position//8+7-(position%8)]) & self.VALID_BOARD & ~self.PlayerToMovePieces
            LSB_2 = Possible_Moves & -Possible_Moves
            while LSB_2 != 0:
                pos_2 = LSB_LOOKUP[LSB_2]
                moves += str(position//8)+str(position%8)+str(pos_2//8)+str(pos_2%8)+piece_type
                Possible_Moves = Possible_Moves & ~LSB_2
                LSB_2 = Possible_Moves & -Possible_Moves
            BISHOPS = BISHOPS & ~LSB
            LSB = BISHOPS & -BISHOPS
        return moves

    def getKingMoves(self, king):
        moves=""
        pos = LSB_LOOKUP[king]
        Possible_Moves = precomputed.KING_MOVES[pos] & ~(self.PlayerToMovePieces) & self.VALID_BOARD
        LSB = Possible_Moves & -Possible_Moves
        while LSB != 0:
            position = LSB_LOOKUP[LSB]
            moves += str(pos//8)+str(pos%8)+str(position//8)+str(position%8)+"K"
            Possible_Moves = Possible_Moves & ~LSB
            LSB = Possible_Moves & -Possible_Moves
        return moves
            
    def moveToAlgebra(self, move):
        str_move = chr(ord(move[1])+49)+str(int(move[0]))+chr(ord(move[3])+49)+str(int(move[2]))
        return str_move
    
    def printMailBoard(self):
        for row in self.mailboard:
            print(row)

    
    def makeMove(self, move):
        if move[2].isnumeric(): # General moves (capturing and moving pieces). Doesn't include enpassant, promotions or castling.
            x1 = int(move[0])
            y1 = int(move[1])
            x2 = int(move[2])
            y2 = int(move[3])
            print(f"{x1}{y1}{x2}{y2}")
            print(move)
            COLOUR = "W" if self.WhitePlayerMove == True else "B"
            captured_piece = self.mailboard[7-x2][7-y2]
            if captured_piece != '':
                self.bitboards[captured_piece] &= ~(0b1<<(x2*8+y2))
            self.mailboard[7-x2][7-y2] = self.mailboard[7-x1][7-y1]
            new_pos = ((0b1<<(x2*8 + y2)) | (0b1<<(x1*8 + y1)))

            # Incremental updates to bitboards

            self.bitboards[COLOUR+move[4]] = self.bitboards[COLOUR+move[4]] ^ new_pos
            self.bitboards['OCCUPIED'] ^= new_pos
            self.EMPTY ^= new_pos

            self.mailboard[7-x1][7-y1] = ""

            """
            if self.bitboards[COLOUR+move[4]] & (0b1 << (x1*8 + y1)) != 0:
                self.mailboard[7-x2][7-y2] = self.mailboard[7-x1][y1-1]
                self.bitboards[COLOUR+move[4]] = self.bitboards[COLOUR+move[4]] ^ ((0b1<<(x2*8 + y2)) | (0b1<<(x1*8 + y1)))
            self.mailboard[7-x1][y1-1] = ""
            """
        elif move[3] == "P": # Handling Promotions
            y1 = int(move[0])
            y2 = int(move[1])
            info = 7, 'W', 6 if self.WhitePlayerMove else 0, 'B', 1
            x2 = info[0]
            COLOUR = info[1]
            x1 = info[2]
            captured_piece = self.mailboard[7-x2][y2]
            if captured_piece != '':
                self.bitboards[captured_piece] &= ~(0b1<<(x2*8+y2))
            self.mailboard[7-x2][7-y2] = COLOUR + move[2] 
            self.bitboards[COLOUR+move[2]] = self.bitboards[COLOUR+move[2]] | 0b1<<(x2*8 + y2)
            print(self.bitboards[COLOUR+move[2]])
            print(f"{7-x1}x + {7-y1}y")
            self.mailboard[7-x1][y1] = ""


            
            """
            match move[4]:
                case "P":
                    print("Y")
                    print(x1*8 + y1)
                    if self.bitboards['WP'] & (0b1 << (x1*8 + y1)) != 0:
                        self.mailboard[7-x2][7-y2] = self.mailboard[7-x1][7-y1]
                        self.bitboards['WP'] = self.bitboards['WP'] ^ ((0b1<<(x2*8 + y2)) | (0b1<<(x1*8 + y1)))
                    else:
                        self.mailboard[x2][y2] = self.mailboard[x1][y1]
                        self.bitboards['BP'] = self.bitboards['BP'] ^ ((0b1<<(x2*8 + y2)) | (0b1<<(x1*8 + y1)))
                    self.mailboard[7-x1][7-y1] = ""
                case "N": 
                    if self.bitboards['WN'] & (0b1 << x1*8 + y1) != 0:
                        self.mailboard[7-x2][7-y2] = self.mailboard[7-x1][7-y1]
                        self.bitboards['WN'] = self.bitboards['WN'] ^ ((0b1<<(x2*8 + y2)) | (0b1<<(x1*8 + y1)))
                    else:
                        self.mailboard[7-x2][7-y2] = self.mailboard[7-x1][7-y1]
                        self.bitboards['BN'] = self.bitboards['BN'] ^ ((0b1<<(x2*8 + y2)) | (0b1<<(x1*8 + y1)))
                    self.mailboard[7-x1][7-y1] = ""
                case "B":
                    if self.bitboards['WB'] & (0b1 << x1*8 + y1) != 0:
                        self.mailboard[7-x2][7-y2] = self.mailboard[7-x1][7-y1]
                        self.bitboards['WB'] = self.bitboards['WB'] ^ ((0b1<<(x2*8 + y2)) | (0b1<<(x1*8 + y1)))
                    else:
                        self.mailboard[7-x2][7-y2] = self.mailboard[7-x1][7-y1]
                        self.bitboards['BB'] = self.bitboards['BB'] ^ ((0b1<<(x2*8 + y2)) | (0b1<<(x1*8 + y1)))
                    self.mailboard[7-x1][7-y1] = ""
                case "R":
                    if self.bitboards['WR'] & (0b1 << x1*8 + y1) != 0:
                        self.mailboard[7-x2][7-y2] = self.mailboard[7-x1][7-y1]
                        self.bitboards['WR'] = self.bitboards['WR'] ^ ((0b1<<(x2*8 + y2)) | (0b1<<(x1*8 + y1)))
                    else:
                        self.mailboard[7-x2][7-y2] = self.mailboard[7-x1][7-y1]
                        self.bitboards['BR'] = self.bitboards['BR'] ^ ((0b1<<(x2*8 + y2)) | (0b1<<(x1*8 + y1)))
                    self.mailboard[7-x1][7-y1] = ""
                case "Q":
                    if self.bitboards['WQ'] & (0b1 << x1*8 + y1) != 0:
                        self.mailboard[7-x2][7-y2] = self.mailboard[7-x1][7-y1]
                        self.bitboards['WQ'] = self.bitboards['WQ'] ^ ((0b1<<(x2*8 + y2)) | (0b1<<(x1*8 + y1)))
                    else:
                        self.mailboard[7-x2][7-y2] = self.mailboard[7-x1][7-y1]
                        self.bitboards['BQ'] = self.bitboards['BQ'] ^ ((0b1<<(x2*8 + y2)) | (0b1<<(x1*8 + y1)))
                    self.mailboard[7-x1][7-y1] = ""
                case "K":
                    if self.bitboards['WK'] & (0b1 << x1*8 + y1) != 0:
                        self.mailboard[7-x2][7-y2] = self.mailboard[7-x1][7-y1]
                        self.bitboards['WK'] = self.bitboards['WK'] ^ ((0b1<<(x2*8 + y2)) | (0b1<<(x1*8 + y1)))
                    else:
                        self.mailboard[7-x2][7-y2] = self.mailboard[7-x1][7-y1]
                        self.bitboards['BK'] = self.bitboards['BK'] ^ ((0b1<<(x2*8 + y2)) | (0b1<<(x1*8 + y1)))
                    self.mailboard[7-x1][7-y1] = ""
                    """
        self.WhitePlayerMove = not self.WhitePlayerMove
        
            
if __name__ == "__main__":
    newBoard = Board()
    print(newBoard.getAllMoves())
    print(f"{int(len(newBoard.getAllMoves())/5)} possible moves")
    newBoard.makeMove(newBoard.getAllMoves()[:5])
    print(f"{int(len(newBoard.getAllMoves())/5)} possible moves")
    print(newBoard.getAllMoves())
    print(newBoard.printMailBoard())




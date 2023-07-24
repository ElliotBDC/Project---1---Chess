from copy import deepcopy

class BBoard():

    #Board 
    move = 0
    white_king = [7, 4]
    black_king = [0, 4]
    board = [
    ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
    ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
    ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
    ]
    moves = []
    promotion_list = ['q', 'r', 'n', 'b']
    onscreen_promotion_list = ['bq', 'br', 'bn', 'bb']
    white_king_moved = False
    black_king_moved = False
    rooks_moved = [False, False, False, False]
    sizeOfPiece = ""
    pawn_promotion_position = []
    pieces = [
    [0, 4, 'bk'], [0, 0, 'br'], [0, 1, 'bn'], [0, 2, 'bb'], [0, 3, 'bq'], [0, 5, 'bb'], [0, 6, 'bn'], [0, 7, 'br'],
    [1, 0, 'bp'], [1, 1, 'bp'], [1, 2, 'bp'], [1, 3, 'bp'], [1, 4, 'bp'], [1, 5, 'bp'], [1, 6, 'bp'], [1, 7, 'bp'],
    [7, 4, 'wk'], [7, 0, 'wr'], [7, 1, 'wn'], [7, 2, 'wb'], [7, 3, 'wq'], [7, 5, 'wb'], [7, 6, 'wn'], [7, 7, 'wr'],
    [6, 0, 'wp'], [6, 1, 'wp'], [6, 2, 'wp'], [6, 3, 'wp'], [6, 4, 'wp'], [6, 5, 'wp'], [6, 6, 'wp'], [6, 7, 'wp']
    ]
    pieces_midpoint = 16

    def __init__(self, board="", pieces=[] ,move=0):
        if board != "":
            self.board = deepcopy(board)
        else:
            self.board = [
                        ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
                        ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
                        ['', '', '', '', '', '', '', ''],
                        ['', '', '', '', '', '', '', ''],
                        ['', '', '', '', '', '', '', ''],
                        ['', '', '', '', '', '', '', ''],
                        ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
                        ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
                        ]
        self.move = move
        self.pieces = pieces
    def isValidMove(self, piece, piece_pos, end_pos, optional_enpassant=False):
        #Checking to make sure program doesnt accidentally count the user placing the piece back on the same square as a move
        if (piece_pos[0], piece_pos[1]) == (end_pos[0], end_pos[1]):
            return False
        if self.board[end_pos[0]][end_pos[1]] != "":
            if piece[0] == self.board[end_pos[0]][end_pos[1]][0]:
                return False
        if piece[1] == "p":
            if piece[0] == "w":
                if end_pos[1] == piece_pos[1]:
                    if abs(piece_pos[0] - end_pos[0]) == 2 and piece_pos[0] == 6:
                        if self.board[end_pos[0]][end_pos[1]] != "" or self.board[end_pos[0]+1][end_pos[1]] != "":
                            return False
                        return True
                    elif piece_pos[0] - end_pos[0] == 1:
                        if self.board[end_pos[0]][end_pos[1]] != "":
                            return False
                        return True
                elif end_pos[1] == piece_pos[1]+1 or end_pos[1] == piece_pos[1]-1:
                    if abs(piece_pos[0] - end_pos[0]) == 1:
                        if self.board[end_pos[0]][end_pos[1]] != "":
                            return True
                        if end_pos[0] == 2 and self.moves[-1][1] == "bp" and self.moves[-1][2][0] == 3 and (self.moves[-1][2][1] == piece_pos[1]+1 or self.moves[-1][2][1] == piece_pos[1]-1):
                            if optional_enpassant == True:
                                return None
                            return True
                    return False
                return False
            else:
                if end_pos[1] == piece_pos[1]:
                    if abs(piece_pos[0] - end_pos[0]) == 2 and piece_pos[0]==1:
                        if self.board[end_pos[0]][end_pos[1]] != "" or self.board[end_pos[0]-1][end_pos[1]] != "":
                            return False
                        return True
                    elif piece_pos[0] - end_pos[0] == -1:
                        if self.board[end_pos[0]][end_pos[1]] != "":
                            return False
                        return True
                elif end_pos[1] == piece_pos[1]+1 or end_pos[1] == piece_pos[1]-1:
                    if piece_pos[0] - end_pos[0] == -1:
                        if self.board[end_pos[0]][end_pos[1]] != "":
                            return True
                        if end_pos[0] == 5 and self.moves[-1][1] == "wp" and self.moves[-1][2][0] == 4 and (self.moves[-1][2][1] == piece_pos[1]+1 or self.moves[-1][2][1] == piece_pos[1]-1):
                            if optional_enpassant == True:
                                return None
                            return True
                    return False
                return False
        if piece[1] == "b":
            #Check for diagonal
            if abs(end_pos[0]-piece_pos[0]) == abs(end_pos[1]-piece_pos[1]):
                return self.isValidDiagRow(piece_pos[0], piece_pos[1], end_pos[0], end_pos[1])
            return False
        if piece[1] == "n":
            if abs(end_pos[0]-piece_pos[0]) == 2 and abs(end_pos[1]-piece_pos[1]) == 1:
                return True
            elif  abs(end_pos[0]-piece_pos[0]) == 1 and abs(end_pos[1]-piece_pos[1]) == 2:
                return True
            return False
        if piece[1] == "r":
            if piece_pos[0] == end_pos[0] and piece_pos[1] != end_pos[1]:
                return self.isValidDiagRow(piece_pos[0], piece_pos[1], end_pos[0], end_pos[1])
            elif piece_pos[0] != end_pos[0] and piece_pos[1] == end_pos[1]:
                return self.isValidDiagRow(piece_pos[0], piece_pos[1], end_pos[0], end_pos[1])
            return False
        if piece[1] == "k":
            if abs(end_pos[0]-piece_pos[0]) == abs(end_pos[1]-piece_pos[1]):
                if (abs(end_pos[0]-piece_pos[0]) == 1 and abs(end_pos[1]-piece_pos[1]) == 1):
                    return True
            elif (end_pos[0]==piece_pos[0]+1 or end_pos[0]==piece_pos[0]-1) and end_pos[1]==piece_pos[1]:
                return True 
            elif (end_pos[1]==piece_pos[1]+1 or end_pos[1]==piece_pos[1]-1) and end_pos[0]==piece_pos[0]:
                return True
            if piece[0] == "w":
                if self.white_king_moved == False:
                    if (end_pos[1] == 2 and self.rooks_moved[0] == False) or (end_pos[1] == 6 and self.rooks_moved[1] == False):
                        if self.isCheckWhileMoving(self.white_king, end_pos, 1 if end_pos[1] - piece_pos[1] > 0 else -1, "WHITE"):
                            return None
            else:
                if self.black_king_moved == False:
                    if (end_pos[1] == 2 and self.rooks_moved[2] == False) or (end_pos[1] == 6 and self.rooks_moved[3] == False):
                        if self.isCheckWhileMoving(self.black_king, end_pos, 1 if end_pos[1] - piece_pos[1] > 0 else -1, "BLACK"):
                            return None
            return False
        if piece[1] == "q":
            if piece_pos[0] == end_pos[0] and piece_pos[1] != end_pos[1]:
                return self.isValidDiagRow(piece_pos[0], piece_pos[1], end_pos[0], end_pos[1])
            elif piece_pos[0] != end_pos[0] and piece_pos[1] == end_pos[1]:
                return self.isValidDiagRow(piece_pos[0], piece_pos[1], end_pos[0], end_pos[1])
            elif abs(end_pos[0]-piece_pos[0]) == abs(end_pos[1]-piece_pos[1]):
                return self.isValidDiagRow(piece_pos[0], piece_pos[1], end_pos[0], end_pos[1])
            return False
        return False
        
    def isCheckWhileMoving(self, start_pos, end_pos, direction, COLOUR):
        choice = "wk" if COLOUR == "WHITE" else "bk"
        for i in range(0, abs(end_pos[1]-start_pos[1])):
            if i > 0:
                if self.board[start_pos[0]][start_pos[1]+i*direction] != '':
                    return False
            if self.makeMove((start_pos[0], start_pos[1], choice), start_pos[0], start_pos[1]+(i*direction), True) == False:
                return False
        return True

    def isInCheck(self, optional_return_both=False):
        #white_pieces = [(index_x, index_y, y) for index_x, x in enumerate(self.board) for index_y, y in enumerate(x) if y != "" and y[0] == "w" and (abs(self.black_king[0]-index_x) == abs(self.black_king[1]-index_y) or (self.black_king[0]==index_x and self.black_king[1] != index_x) or (self.black_king[1]==index_y and self.black_king[0] != index_x) or (abs(self.black_king[0]-index_x) == 2 and abs(self.black_king[1]-index_y) == 1) or (abs(self.black_king[0]-index_x) == 1 and abs(self.black_king[1]-index_y) == 2))]
        #black_pieces = [(index_x, index_y, y) for index_x, x in enumerate(self.board) for index_y, y in enumerate(x) if y != "" and y[0] == "b" and (abs(self.white_king[0]-index_x) == abs(self.white_king[1]-index_y) or (self.white_king[0]==index_x and self.white_king[1] != index_x) or (self.white_king[1]==index_y and self.white_king[0] != index_x) or (abs(self.white_king[0]-index_x) == 2 and abs(self.white_king[1]-index_y) == 1) or (abs(self.white_king[0]-index_x) == 1 and abs(self.white_king[1]-index_y) == 2))]
        white_pieces = self.pieces[self.pieces_midpoint:]
        black_pieces = self.pieces[0:self.pieces_midpoint]
        white_pieces_list = []
        black_check = False
        white_check = False
        for x in range(0, len(white_pieces)):
            if self.isValidMove(white_pieces[x][2], (white_pieces[x][0], white_pieces[x][1]), (self.black_king[0], self.black_king[1])) == True:
                white_pieces_list.append((white_pieces[x][0], white_pieces[x][1]))
        if len(white_pieces_list) > 0:
            if optional_return_both == False:
                return ("BLACK", white_pieces_list)
            black_check = True
        black_pieces_list = []
        for x in black_pieces:
            if self.isValidMove(x[2], (x[0], x[1]), (self.white_king[0], self.white_king[1])) == True:
                black_pieces_list.append((x[0], x[1]))
        if len(black_pieces_list) > 0:
            if optional_return_both == False:
                return ("WHITE", black_pieces_list)
            white_check = True
        if optional_return_both == False:
            return (False, "")
        if white_check and black_check:
            return (2, "")
        elif white_check:
            return ("WHITE", black_pieces_list)
        elif black_check:
            return ("BLACK", white_pieces_list)
        return (False, "")
    
    # canKingMove() can be used in both checking for CheckMates and StaleMates.

    def canKingMove(self, COLOUR):
        king = (deepcopy(self.white_king), 'wk') if COLOUR == "WHITE" else (deepcopy(self.black_king), 'bk')
        condition = False
        for row in range(-1, 2):
            for column in range(-1, 2):
                if (0 > row+king[0][0] or row+king[0][0] > 7 or 0 > column+king[0][1] or column+king[0][1] > 7) == False:
                    if self.isValidMove(king[1], king[0], [king[0][0]+row, king[0][1]+column]):
                            if COLOUR == "WHITE":
                                self.white_king = [king[0][0]+row, king[0][1]+column]
                            else:
                                self.black_king = [king[0][0]+row, king[0][1]+column]
                            tmp = self.board[king[0][0]+row][king[0][1]+column]
                            self.board[king[0][0]][king[0][1]] = ""
                            self.board[king[0][0]+row][king[0][1]+column]= king[1]
                            if self.isInCheck()[0] != COLOUR:
                                condition = True
                            if COLOUR == "WHITE":
                                self.white_king = [king[0][0]+row, king[0][1]+column]
                            else:
                                self.black_king = [king[0][0], king[0][1]]
                            self.board[king[0][0]][king[0][1]] = king[1]
                            self.board[king[0][0]+row][king[0][1]+column]= tmp
        if condition == True:
            return True
        return False

    def isCheckmate(self, COLOUR, checking_pieces):
        king = (deepcopy(self.white_king), 'wk') if COLOUR == "WHITE" else (deepcopy(self.black_king), 'bk')
        condition_1, condition_2, condition_3 = False, False, False

        # Condition 1 - Can the king escape check by moving to an adjacent square.
        condition_1 = self.canKingMove(COLOUR)
                            
        # Condition 2 - Can the checking piece be captured?
        if len(checking_pieces) == 1:
            if COLOUR == "WHITE":
                white_pieces = [(index_x, index_y, y) for index_x, x in enumerate(self.board) for index_y, y in enumerate(x) if y != "" and y[0] == "w"]
                for x in white_pieces:
                    #if self.isValidMove(x[0], [x[1], x[2]], [checking_pieces[0][0], checking_pieces[0][1]]):
                    if self.makeMove(x, checking_pieces[0][0], checking_pieces[0][1], True):
                        condition_2 = True   
                        
            elif COLOUR == "BLACK":
                black_pieces = [(index_x, index_y, y) for index_x, x in enumerate(self.board) for index_y, y in enumerate(x) if y != "" and y[0] == "b"]
                for x in black_pieces:
                    if self.makeMove(x, checking_pieces[0][0], checking_pieces[0][1], True):
                        condition_2 = True

        # Condition 3 - Can the check be blocked by another piece
        if len(checking_pieces) == 1:
            positions = self.isValidDiagRow(king[0][0], king[0][1], checking_pieces[0][0], checking_pieces[0][1], optional_return_positions=True)
            black_pieces = [(index_x, index_y, y) for index_x, x in enumerate(self.board) for index_y, y in enumerate(x) if y != "" and y[0] == "b" and y[1] != "k"]
            white_pieces = [(index_x, index_y, y) for index_x, x in enumerate(self.board) for index_y, y in enumerate(x) if y != "" and y[0] == "w" and y[1] != "k"]
            if COLOUR == "WHITE":
                for x in white_pieces:
                    for j in positions:
                        if self.isValidMove(x[2], (x[0], x[1]), (j[0], j[1])):
                            condition_3 = True
            elif COLOUR == "BLACK":
                for x in black_pieces:
                    for j in positions:
                        if self.isValidMove(x[2], (x[0], x[1]), (j[0], j[1])):
                            condition_3 = True
        
        if condition_1 or condition_2 or condition_3:
            return False
        return True
        
    
    def isValidDiagRow(self, piece_row, piece_column, end_row, end_column, optional_return_positions=False):
        #Checking for the type of validation we will have to perform. rr/c stands for the step in the corresponding column/row
        rr = -1 if (piece_row - end_row) > 0 else 1
        rc = -1 if (piece_column - end_column) > 0 else 1
        iterAmount = piece_row-end_row
        optional_positions = []
        if end_column == piece_column:
            rc = 0
        elif end_row == piece_row:
            rr = 0
            iterAmount = piece_column-end_column
        for i in range(0, abs(iterAmount)-1):
            piece_row = piece_row + rr
            piece_column = piece_column + rc
            optional_positions.append((piece_row, piece_column))
            if self.board[piece_row][piece_column] != "":
                if optional_return_positions != True:
                    return False
        if optional_return_positions == True:
            return optional_positions
        return True
    
    def isStalemate(self):
        COLOUR = "WHITE" if self.move % 2 == 0 else "BLACK"
        if self.getAllMoves(COLOUR) == 0:
            print("IS STALEMATE")
            return True
        return False
    
    def getAllMoves(self, COLOUR):
        moves_list = []
        if COLOUR == "WHITE":
            white_pieces = [(index_x, index_y, y) for index_x, x in enumerate(self.board) for index_y, y in enumerate(x) if y != "" and y[0] == "w"]
            for piece in white_pieces:
                for row in range(0, 8):
                    for column in range(0, 8):
                        if self.makeMove(piece, row, column, optional_return=True) == True:
                            moves_list.append([piece, (row,column)])
        elif COLOUR == "BLACK":
            black_pieces = [(index_x, index_y, y) for index_x, x in enumerate(self.board) for index_y, y in enumerate(x) if y != "" and y[0] == "b"]
            for piece in black_pieces:
                for row in range(0, 8):
                    for column in range(0, 8):
                        if self.makeMove(piece, row, column, optional_return=True) == True:
                            moves_list.append([piece, (row,column)])
        if len(moves_list) == 0:
            return 0
        return moves_list
                    
    #Optional return means no change is made 
    def makeMove(self, piece_held, row_clicked, column_clicked, optional_return=False, choice="", AI=False):
        boolean_validMove = self.isValidMove(piece_held[2], [piece_held[0], piece_held[1]], [row_clicked, column_clicked], optional_enpassant=True)
        attpiece_index = 0
        defpiece_index = 0
        if boolean_validMove == True:
            print(f"{self.pieces}")
            attpiece_index = self.pieces.index([piece_held[0], piece_held[1], piece_held[2]])
            tmp = self.board[row_clicked][column_clicked]
            self.board[piece_held[0]][piece_held[1]] = ""
            self.board[row_clicked][column_clicked] = piece_held[2]
            if piece_held[2][1] == "k":
                if piece_held[2][0] == "w":
                    self.white_king =  [row_clicked, column_clicked]
                else:
                    self.black_king = [row_clicked, column_clicked]
            self.pieces[attpiece_index] = [row_clicked, column_clicked, piece_held[2]]
            if tmp != "":
                defpiece = [row_clicked, column_clicked, self.board[row_clicked][column_clicked]]
                defpiece_index = self.pieces.index(defpiece)
                print(f"tmp: {tmp}, piece_held: {piece_held}")
                self.pieces.remove(defpiece)
                if piece_held[2][0] == "b":
                    self.pieces_midpoint -= 1
            currentCheck = self.isInCheck(optional_return_both=True)[0]
            if ((currentCheck == "BLACK" and self.move % 2 != 0) or (currentCheck == "WHITE" and self.move % 2 == 0)) or currentCheck == 2:
                self.board[piece_held[0]][piece_held[1]] = piece_held[2]
                self.board[row_clicked][column_clicked] = tmp
                if piece_held[2][1] == "k":
                    if piece_held[2][0] == "w":
                        self.white_king = [piece_held[0], piece_held[1]]
                    else:
                        self.black_king = [piece_held[0], piece_held[1]]
                if optional_return == True:
                    if tmp != "":
                        self.pieces.insert(defpiece, defpiece_index)
                    if piece_held[2][0] == "b":
                        self.pieces_midpoint += 1
                    return False
                self.pieces[attpiece_index] = [piece_held[0], piece_held[1], piece_held[2]]
                if tmp != "":
                    self.pieces.insert(defpiece, defpiece_index)
                if piece_held[2][0] == "b":
                    self.pieces_midpoint += 1
            else: #elif ((self.isInCheck()[0] == "BLACK" and self.move % 2 != 0) or (self.isInCheck()[0] == "WHITE" and self.move % 2 == 0)) == False:
                if optional_return == True:
                    self.board[piece_held[0]][piece_held[1]] = piece_held[2]
                    self.board[row_clicked][column_clicked] = tmp
                    if piece_held[2][1] == "k":
                        if piece_held[2][0] == "w":
                            self.white_king = [piece_held[0], piece_held[1]]
                        else:
                            self.black_king = [piece_held[0], piece_held[1]]
                    self.pieces[attpiece_index] = [piece_held[0], piece_held[1], piece_held[2]]
                    if tmp != "":
                        defpiece = [row_clicked, column_clicked, self.board[row_clicked][column_clicked]]
                        defpiece_index = self.pieces.index(defpiece)
                        self.pieces.insert(defpiece, defpiece_index)
                    if piece_held[2][0] == "b":
                        self.pieces_midpoint += 1
                    return True
                if (piece_held[2] == "wp" and row_clicked == 0) or (piece_held[2] == "bp" and row_clicked == 7):
                    if AI == False:
                        global choice_making
                        choice_making = True
                        self.pawn_promotion_position = [row_clicked,column_clicked]
                    else:
                        self.board[row_clicked][column_clicked] = str(piece_held[2][0] + choice)
                if piece_held[2] == "wk":
                    self.white_king = [row_clicked, column_clicked]
                    self.white_king_moved = True
                elif piece_held[2] == "bk":
                    self.black_king = [row_clicked, column_clicked]
                    self.black_king_moved = True
                elif piece_held[2] == "wr":
                    if piece_held[1] == 0:
                        self.rooks_moved[0] = True
                    else:
                        self.rooks_moved[1] = True
                elif piece_held[2] == "br":
                    if piece_held[1] == 0:
                        self.rooks_moved[2] = True
                    else:
                        self.rooks_moved[3] = True
                self.moves.append([self.move, piece_held[2], [row_clicked, column_clicked]])
                self.move = self.move + 1
            if optional_return == True:
                return False
        elif boolean_validMove == None:
            if piece_held[2][1] == "p":
                tmp = self.board[row_clicked][column_clicked]
                self.board[piece_held[0]][piece_held[1]] = ""
                self.board[row_clicked][column_clicked] = piece_held[2]
                tmp2 = self.board[row_clicked-(1 if piece_held[2][0] == "w" else -1)][column_clicked]
                self.board[row_clicked-(-1 if piece_held[2][0] == "w" else 1)][column_clicked] = ""
                if (self.isInCheck()[0] == "BLACK" and self.move % 2 != 0) or (self.isInCheck()[0] == "WHITE" and self.move % 2 == 0):
                    self.board[piece_held[0]][piece_held[1]] = piece_held[2]
                    self.board[row_clicked][column_clicked] = tmp
                    self.board[row_clicked-(1 if piece_held[2][0] == "w" else -1)][column_clicked] = tmp2
                    if optional_return == True:
                        return False
                else: #elif ((self.isInCheck()[0] == "BLACK" and self.move % 2 != 0) or (self.isInCheck()[0] == "WHITE" and self.move % 2 == 0)) == False:
                    if optional_return == True:
                        self.board[piece_held[0]][piece_held[1]] = piece_held[2]
                        self.board[row_clicked][column_clicked] = tmp
                        return True
                    self.moves.append([self.move, piece_held[2], [row_clicked, column_clicked]])
                    self.move = self.move + 1
            elif piece_held[2][1] == "k":
                tmp = self.board[row_clicked][column_clicked]
                self.board[piece_held[0]][piece_held[1]] = ""
                self.board[row_clicked][column_clicked] = piece_held[2]
                if piece_held[2][1] == "k":
                    if piece_held[2][0] == "w":
                        self.white_king =  [row_clicked, column_clicked]
                    else:
                        self.black_king = [row_clicked, column_clicked]
                if (self.isInCheck()[0] == "BLACK" and self.move % 2 != 0) or (self.isInCheck()[0] == "WHITE" and self.move % 2 == 0):
                    self.board[piece_held[0]][piece_held[1]] = piece_held[2]
                    self.board[row_clicked][column_clicked] = tmp
                    if piece_held[2][1] == "k":
                        if piece_held[2][0] == "w":
                            self.white_king = [piece_held[0], piece_held[1]]
                        else:
                            self.black_king = [piece_held[0], piece_held[1]]
                    if optional_return == True:
                        return False
                else: #elif ((self.isInCheck()[0] == "BLACK" and self.move % 2 != 0) or (self.isInCheck()[0] == "WHITE" and self.move % 2 == 0)) == False:
                    if optional_return == True:
                        self.board[piece_held[0]][piece_held[1]] = piece_held[2]
                        self.board[row_clicked][column_clicked] = tmp
                        if piece_held[2][1] == "k":
                            if piece_held[2][0] == "w":
                                self.white_king = [piece_held[0], piece_held[1]]
                            else:
                                self.black_king = [piece_held[0], piece_held[1]]
                        return True
                    if piece_held[2] == "wk":
                        self.white_king = [row_clicked, column_clicked]
                        if column_clicked == 2:
                            self.board[7][0] = ""
                            self.board[7][3] = "wr"
                        else:
                            self.board[7][7] = ""
                            self.board[7][5] = "wr"
                    elif piece_held[2] == "bk":
                        self.black_king = [row_clicked, column_clicked]
                        if column_clicked == 2:
                            self.board[0][0] = ""
                            self.board[0][3] = "br"
                        else:
                            self.board[0][7] = ""
                            self.board[0][5] = "br"
                    self.moves.append([self.move, piece_held[2], [row_clicked, column_clicked]])
                    self.move = self.move + 1
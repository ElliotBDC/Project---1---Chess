public class Moves {

    static long BLACK_PIECES;
    static long WHITE_PIECES;
    static long NOT_WHITE_PIECES;
    static long NOT_BLACK_PIECES;
    static long PAWN_MOVES;
    static long Mleft;
    static int index;

    static long FILE_A=72340172838076673L;
    static long FILE_H=-9187201950435737472L;
    static long FILE_AB=217020518514230019L;
    static long FILE_GH=-4557430888798830400L;
    static long RANK_1=-72057594037927936L;
    static long RANK_4=1095216660480L;
    static long RANK_5=4278190080L;
    static long RANK_8=255L;
    static long CENTRE=103481868288L;
    static long EXTENDED_CENTRE=66229406269440L;
    static long KING_SIDE=-1085102592571150096L;
    static long QUEEN_SIDE=1085102592571150095L;
    static long KING_B7=460039L;
    static long KNIGHT_C6=43234889994L;
    static long EMPTY;
    
    public static String getAllPossibleMoves(long WP, long BP, long WN, long BN, long WB, long BB,
     long WR, long BR, long WQ, long BQ, long WK, long BK) {
        String moves = "";
        BLACK_PIECES = BP | BN | BB | BR | BQ;
        WHITE_PIECES = WP | WN | WB | WR | WQ;
        // The following indicates the squares (0) where there are no pieces of the corresponding colour / opp king
        NOT_WHITE_PIECES = WP | WN | WB | WR | WQ | WK;
        NOT_BLACK_PIECES = BP | BN | BB | BR | BQ | BK;
        
        EMPTY =~(WP|WN|WB|WR|WQ|WK|BP|BN|BB|BR|BQ|BK);
        moves+=getWPawnMoves(Board.WP);
        return moves;
    }

    public static String getWPawnMoves(long WP) {
        String moves = "";

        // Captures right
        PAWN_MOVES = (WP>>7)&BLACK_PIECES&~RANK_8&~FILE_A;
        Mleft = PAWN_MOVES&~(PAWN_MOVES-1);
        while (Mleft != 0) {
            index = Long.numberOfTrailingZeros(Mleft);
            moves+=""+(index/8+1)+(index%8-1)+(index/8)+index%8;
            PAWN_MOVES = PAWN_MOVES&~Mleft;
            Mleft = PAWN_MOVES&~(PAWN_MOVES-1);
        }

        // Captures left
        PAWN_MOVES = (WP>>9)&BLACK_PIECES&~RANK_8&~FILE_H;
        Mleft = PAWN_MOVES&~(PAWN_MOVES-1);
        while (Mleft != 0) {
            index = Long.numberOfTrailingZeros(Mleft);
            moves+=""+(index/8+1)+(index%8+1)+(index/8)+index%8;
            PAWN_MOVES = PAWN_MOVES&~Mleft;
            Mleft = PAWN_MOVES&~(PAWN_MOVES-1);
        }

        // Move forward 1
        PAWN_MOVES = (WP>>8)&EMPTY&~RANK_8;
        Mleft = PAWN_MOVES&~(PAWN_MOVES-1);
        while (Mleft != 0) {
            index = Long.numberOfTrailingZeros(Mleft);
            moves+="("+(index/8+1)+(index%8)+(index/8)+index%8+")";
            PAWN_MOVES = PAWN_MOVES&~Mleft;
            Mleft = PAWN_MOVES&~(PAWN_MOVES-1);
        }

        // Move forward 2
        PAWN_MOVES = (WP>>16)&EMPTY&(EMPTY>>8)&RANK_4; 
        Mleft = PAWN_MOVES&~(PAWN_MOVES-1);
        while (Mleft != 0) {
            index = Long.numberOfTrailingZeros(Mleft);
            moves+="("+(index/8+2)+(index%8)+(index/8)+index%8+")";
            PAWN_MOVES = PAWN_MOVES&~Mleft;
            Mleft = PAWN_MOVES&~(PAWN_MOVES-1);
        }

        // Promotion by capturing right
        PAWN_MOVES = (WP>>7)&BLACK_PIECES&RANK_8&~FILE_A;
        Mleft = PAWN_MOVES&~(PAWN_MOVES-1);
        while (Mleft != 0) {
            index = Long.numberOfTrailingZeros(Mleft);
            moves+=""+(index/8+1)+(index%8-1)+(index/8)+index%8+"WQ"+(index/8+1)+(index%8-1)+(index/8)+index%8+"WN"
            +(index/8+1)+(index%8-1)+(index/8)+index%8+"WR"+(index/8+1)+(index%8-1)+(index/8)+index%8+"WB";
            PAWN_MOVES = PAWN_MOVES&~Mleft;
            Mleft = PAWN_MOVES&~(PAWN_MOVES-1);
        }

        // Promotion by capturing left
        PAWN_MOVES = (WP>>9)&BLACK_PIECES&RANK_8&~FILE_H;
        Mleft = PAWN_MOVES&~(PAWN_MOVES-1);
        while (Mleft != 0) {
            index = Long.numberOfTrailingZeros(Mleft);
            moves+=""+(index/8+1)+(index%8+1)+(index/8)+index%8+"WQ"+(index/8+1)+(index%8+1)+(index/8)+index%8+"WN"
            +(index/8+1)+(index%8+1)+(index/8)+index%8+"WR"+(index/8+1)+(index%8+1)+(index/8)+index%8+"WB";
            PAWN_MOVES = PAWN_MOVES&~Mleft;
            Mleft = PAWN_MOVES&~(PAWN_MOVES-1);
        }

        //Promotion by moving forward 1
        PAWN_MOVES = (WP>>8)&EMPTY&RANK_8;
        Mleft = PAWN_MOVES&~(PAWN_MOVES-1);
        while (Mleft != 0) {
            index = Long.numberOfTrailingZeros(Mleft);
            moves+=""+(index/8+1)+(index%8)+(index/8)+index%8+"WQ"+(index/8+1)+(index%8)+(index/8)+index%8+"WN"
            +(index/8+1)+(index%8)+(index/8)+index%8+"WR"+(index/8+1)+(index%8)+(index/8)+index%8+"WB";
            PAWN_MOVES = PAWN_MOVES&~Mleft;
            Mleft = PAWN_MOVES&~(PAWN_MOVES-1);
        }
        return moves;
    }

    public static void getBPawnMoves(long BP) {

    }

    
}

import java.util.Arrays;

public class Board {
    static long WP=0L, WN=0L, WB=0L, WR=0L, WQ=0L, WK=0L, BP=0L, BB=0L, BN=0L, BR=0L, BQ=0L,BK=0L;
    public static void loadBoard() {
        String chessBoard[][] = {
            {"r", "n", "b", "q", "k", "b", "n", "r"},
            {"p", "p", "p", "p", "p", "p", "p", "p"},
            {" ", " ", " ", " ", " ", " ", " ", " "},
            {" ", " ", " ", " ", " ", " ", " ", " "},
            {" ", " ", " ", " ", " ", " ", " ", " "},
            {" ", " ", " ", " ", " ", " ", " ", " "},
            {"P", "P", "P", "P", "P", "P", "P", "P"},
            {"R", "N", "B", "Q", "K", "B", "N", "R"}
        };
        String Binary;
        for (int i = 0; i < 64; i++) {
            Binary="0000000000000000000000000000000000000000000000000000000000000000";
            Binary = Binary.substring(i+1) + "1" + Binary.substring(0, i);
            int row = i / 8;
            int col = i % 8;
            switch (chessBoard[row][col]) {
                case "P": WP+=convertStringToBitboard(Binary);
                    break;
                case "N": WN+=convertStringToBitboard(Binary);
                    break;
                case "B": WB+=convertStringToBitboard(Binary);
                    break;
                case "R": WR+=convertStringToBitboard(Binary);
                    break;
                case "Q": WQ+=convertStringToBitboard(Binary);
                    break;
                case "K": WK+=convertStringToBitboard(Binary);
                    break;
                case "p": BP+=convertStringToBitboard(Binary);
                    break;
                case "n": BN+=convertStringToBitboard(Binary);
                    break;
                case "b": BB+=convertStringToBitboard(Binary);
                    break;
                case "r": BR+=convertStringToBitboard(Binary);
                    break;
                case "q": BQ+=convertStringToBitboard(Binary);
                    break;
                case "k": BK+=convertStringToBitboard(Binary);
                    break;
            }
        }
        printBoard(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
    }
            
        public static long convertStringToBitboard(String Binary) {
                if (Binary.charAt(0) == '0') {
                    return Long.parseLong(Binary, 2);
                } else {
                    return Long.parseLong("1" + Binary.substring(2), 2)*2;
                }
            }

        public static void printBoard(long WP,long WN,long WB,long WR,long WQ,
            long WK,long BP,long BN,long BB,long BR,long BQ,long BK) {
                String chessBoard[][]=new String[8][8];
            for (int i=0;i<64;i++) {
                chessBoard[i/8][i%8]=" ";
            }
            for (int i=0;i<64;i++) {
                if (((WP>>i)&1)==1) {chessBoard[i/8][i%8]="P";}
                if (((WN>>i)&1)==1) {chessBoard[i/8][i%8]="N";}
                if (((WB>>i)&1)==1) {chessBoard[i/8][i%8]="B";}
                if (((WR>>i)&1)==1) {chessBoard[i/8][i%8]="R";}
                if (((WQ>>i)&1)==1) {chessBoard[i/8][i%8]="Q";}
                if (((WK>>i)&1)==1) {chessBoard[i/8][i%8]="K";}
                if (((BP>>i)&1)==1) {chessBoard[i/8][i%8]="p";}
                if (((BN>>i)&1)==1) {chessBoard[i/8][i%8]="n";}
                if (((BB>>i)&1)==1) {chessBoard[i/8][i%8]="b";}
                if (((BR>>i)&1)==1) {chessBoard[i/8][i%8]="r";}
                if (((BQ>>i)&1)==1) {chessBoard[i/8][i%8]="q";}
                if (((BK>>i)&1)==1) {chessBoard[i/8][i%8]="k";}
            }
            for (int i=0;i<8;i++) {
                System.out.println(Arrays.toString(chessBoard[i]));
            }
    }
    public static String getAllPossibleMoves() {
        return Moves.getAllPossibleMoves(WP, BP, WN, BN, WB, BB, WR, BR, WQ, BQ, WK, BK);
    }
}
    


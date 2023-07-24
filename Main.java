public class Main {
    public static void main(String[] args) {
        //Client.connectToServer("localhost", 12345);
        Board.loadBoard();
        String moves = Board.getAllPossibleMoves();
        System.out.println(moves);
    }
}
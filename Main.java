public class Main {
    public static void main(String[] args) {
        Client client = new Client();
        client.connectToServer("localhost", 12345);
    }
}
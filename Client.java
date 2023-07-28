import java.io.*;
import java.net.*;
import java.util.Scanner;

public class Client {
    public static void connectToServer(String address, int port) {
        try {
            Socket socket = new Socket(address, port);
            System.out.println("Connected!");
            
            OutputStream outputStream = socket.getOutputStream();
            PrintWriter output = new PrintWriter(outputStream, true);
            
            InputStream inputStream = socket.getInputStream();
            BufferedReader input = new BufferedReader(new InputStreamReader(inputStream));
        
            //DataInputStream input = new DataInputStream(System.in);
            //DataOutputStream out = new DataOutputStream(socket.getOutputStream());
            

            Scanner scanner = new Scanner(System.in);
            while (true) {
                String message = scanner.nextLine();
                if (message.equalsIgnoreCase("exit")) {
                    break;
                } 
                
                output.println(message);

                String response = input.readLine();
                System.out.println(response);
                if (response.equalsIgnoreCase("++".toString())) {
                    String bestMove = Board.runSearch(6);
                    output.println(bestMove);
                    if (Board.WhiteToMove == true) {
                        Search.doMove('w', bestMove,Board.WP,Board.WN,Board.WB,Board.WR,Board.WQ,Board.WK,Board.BP,Board.BN,Board.BB,Board.BR,Board.BQ,Board.BK,Board.EP, Board.CWK, Board.CWQ, Board.CBK, Board.CBQ, true);
                    } else {
                        Search.doMove('b', bestMove,Board.WP,Board.WN,Board.WB,Board.WR,Board.WQ,Board.WK,Board.BP,Board.BN,Board.BB,Board.BR,Board.BQ,Board.BK,Board.EP, Board.CWK, Board.CWQ, Board.CBK, Board.CBQ, false);
                    }
                }
            
            }

            output.close();
            input.close();
            socket.close();
            scanner.close();

        } catch (UnknownHostException u) {
            System.out.println(u.toString());
        } catch(IOException i) {
            System.out.println(i.toString());
        }
        }
    }

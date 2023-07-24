import java.io.*;
import java.net.*;
import java.util.Scanner;

public class Client {
    public void connectToServer(String address, int port) {
        try {
            Socket socket = new Socket(address, port);
            System.out.println("Connected");
            
            OutputStream outputStream = socket.getOutputStream();
            PrintWriter output = new PrintWriter(outputStream, true);
            
            InputStream inputStream = socket.getInputStream();
            BufferedReader input = new BufferedReader(new InputStreamReader(inputStream));
        
            Scanner scanner = new Scanner(System.in);
            while (true) {
                String message = scanner.nextLine();
                if (message.equalsIgnoreCase("exit")) {
                    break;
                }
                output.println(message);

                String response = input.readLine();
                System.out.println(response);
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

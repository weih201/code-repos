/*
 * Wei Han's New File
 *  Created on 23/08/2011
 *  wei han 523979
 */

import java.awt.*;
import javax.swing.*;
import java.util.Scanner;
import java.util.ArrayList;

import java.io.*;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;

/**
 * DictServer.java: the main class of the dictionary server
 *
 */
public class DictServer extends JFrame {
	/**
	 * 	Below are the class level variables used in the application
	 */
	static int serverPort = 5000;   //the class variable to store the server listening port
	static String dictFileName = ""; // the dictionary file name
	static private ServerSocket svrSocket;   // the remote dictionary server Server Socket
	static int[] wordsNumber = new int[26]; // Accelerating array contains the word number start from a given letter,  
								// there are 26 letter in English, so the array length is 26
	/**
	 *  below are the GUI components used in this application	
	 */
	JLabel jlblStart = new JLabel("Server Started");  //a JLabel component used to indicate server status
	JLabel jlblListen = new JLabel("Server Listening at Port:"); 
	JLabel jlblPort = new JLabel(""); //JLabel component used to indicate server listening port
	JLabel  jlblLog = new JLabel("System Log:"); 
	JTextArea jtaLog = new JTextArea(); //JTextAera component used to display server log information
	
	public static void main(String[] args) {
		if(args.length!=2){  // check input paramateres length
			System.out.println("Usage: java DictServer port Dictfile");
			System.exit(0);
		}
		
		serverPort = Integer.parseInt(args[0]);  // store the server port
		dictFileName = args[1];   //store the dictionary file name
		
/**
 * 		Creating the DictServer and make it visible
 */
		DictServer frame = new DictServer();   
		frame.setTitle("Remote Dictionary Server Control Panel");
		frame.setSize(720,480);
		frame.setLocationRelativeTo(null);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setVisible(true);

		frame.jlblPort.setText(serverPort+"");
		
		if(!frame.startService()){    //Starting Dictionary Service
			frame.jlblStart.setText("Server Start Failed");   //service starting failed, change the server status info
			frame.jlblListen.setText("");
			frame.jlblPort.setText("");
		}
	}
	
	public JTextArea getJtaLog() {
		return jtaLog;
	}
	
/**
 *  public DictServer():
 *  	Constructor method of the Dictserver,
 *  	Initializing the Server application GUI interface	
 */
	public DictServer(){
		JPanel p1 = new JPanel();
		p1.add(jlblListen);
		p1.add(jlblPort);
		
		JPanel p2 = new JPanel();
		BoxLayout box = new BoxLayout(p2,BoxLayout.X_AXIS);
		p2.setLayout(box);
		p2.add(jlblStart);
		p2.add(p1);
		
		JScrollPane jscPane = new JScrollPane(jtaLog);
		jtaLog.setLineWrap(true);
		jtaLog.setWrapStyleWord(true);
		jtaLog.setEditable(false);
		JPanel p3 = new JPanel();
		p3.setLayout(new BorderLayout());
		p3.add(jlblLog,BorderLayout.NORTH);
		p3.add(jscPane,BorderLayout.CENTER);
		
		setLayout(new BorderLayout());
		add(p2,BorderLayout.NORTH);
		add(p3,BorderLayout.CENTER);
		
		dictionaryInit();   //Init the accelerating array wordNumber
	}

/**
 * 	void dictionaryInit():
 * 	Initializing the accelerating array wordNumber
 *  after the initlization, the wordNumber array will contain the word number 
 *  in the dictionary start from different letter
 */
	void dictionaryInit(){
		File file = new File(dictFileName);  //create File object from the given Dictfile name
		try{
			Scanner input = new Scanner(file);   //creating the Scanner object for the File

			for(int i=0;i<26;i++) wordsNumber[i] = 0; //init the wordNumber as 0
			
			while(input.hasNext()){
				String line;
				line = input.nextLine(); //read a line from file
				if(line.length()<=0)continue; //skip the blank line
				char ch = line.charAt(0);   //if not the blank line, read the first letter of the line
				
				if(Character.isLetter(ch)){   // update the array element for the corresponding starting letter
					if((ch-'A')<26)wordsNumber[ch-'A']++;  
					else if((ch-'a')<26)wordsNumber[ch-'a']++;
				}
			}
		}
		catch(FileNotFoundException e){
			System.out.println("Dictionary file name wrong: please check the dictioanry file name and restarting as following:");
			System.out.println("Usage: java DictServer port Dictfile");
			System.exit(0);
		}
	}
	
	boolean startService(){
		try{
			svrSocket = new ServerSocket(serverPort); //creating the serverSocket from the given port
			
			int clientNo=1;
			
			while(true){
				Socket sock = svrSocket.accept();  //Listening at the port

				InetAddress cliNetAddress = sock.getInetAddress();  //a client accessed, get the client info
				/* Updating the client info in the jtaLog */
				jtaLog.append("The "+clientNo+"th clients just connected.\r\n");
				jtaLog.append("The "+clientNo+"th clients' host name is "+cliNetAddress.getHostName()+"\r\n");
				jtaLog.append("The "+clientNo+"th clients' IP address is "+cliNetAddress.getHostAddress()+"\r\n");
				
				ClientThread task = new ClientThread(sock,clientNo); //creating a new task for the socket connection
				new Thread(task).start();  //creat a new Thread for the task and starting it
				clientNo++;  //increase client Number
			}
		}
		catch(IOException e){
			System.out.println("Server Socket Creation Failed. Please Restart");
			return false;
		}
	}

/**
 *   public Result search (String word)
 *   		Searching the input in the dictionary file	
 */
	public Result search(String word){
		String lowWord = word.toLowerCase();  //convert the word  to lower case
		String meaningStr;
		String[] meanings;
		Result result = new Result();
		char ch = lowWord.charAt(0);
		
		if(!Character.isLetter(ch)){ //not valid word, return error
			result.errorCode = -2;   //error
			return result;
		}
		
		int index = ch-'a';  //get the input word's index in the wordsNumber array
		int skipLine = 0;    // init the skipLine
		
		for(int i=0;i<index;i++)skipLine += wordsNumber[i]; //get this word's skipLine number, 
												// which is the sum of the wordsNumber before the word's index 
		
		File file = new File(dictFileName);
		try{
			Scanner input = new Scanner(file);
			
			for(int i=0;i<skipLine;i++) input.nextLine();  //skip the skipLine lines in the dictionary file

			for(int i =0; i<wordsNumber[index];i++){  //searching the word in its index range
				String key = lowWord+":";      //create the input word match pattern
				meaningStr = input.nextLine();
				
				if(meaningStr.indexOf(key)==0){  //the read line starts with input word match pattern, the word found
					meanings = parseMeanings(meaningStr); //change the word means into the String[] form
					result.errorCode = 0;   // success code
					result.meanings =meanings;
					return result;
				}
			}
		}
		catch(FileNotFoundException e){
			System.out.println("Dictionary file name wrong: please check the dictioanry file name and restarting as following:");
			System.out.println("Usage: java DictServer port Dictfile");
			System.exit(0);
		}
		result.errorCode = -1; //Not Found
		return result;
	}

/**
 *  public String[] parseMeanings(String meanStr)
 *  	Parsing the dictionary item into the String[] form
 */
	public String[] parseMeanings(String meanStr){
		ArrayList<String> meansList = new ArrayList<String>();// a arrayList help variable
		StringBuilder stringBuilder = new StringBuilder();  // a StringBuilder help variable
		String aMean;
		
		int i=0;
		while(!(meanStr.charAt(i)==':'))i++;   //search the first ':' in the word item
		
		i++;
		stringBuilder.append(meanStr.charAt(i));  //after the ':', the item string come to the means section
									// append the char into helper stringBuilder variable
		i++;
		
		for(;i<meanStr.length();i++){   // searching the dictionary item
			char ch = meanStr.charAt(i);  //get a new char
			if(Character.isDigit(ch)){   //if the char is a digit, this means a new word means item starting
				aMean = stringBuilder.toString();  //store the current mean into a String variable aMean
				meansList.add(aMean);  //add this current mean into the arrayList variable
				
				stringBuilder.setLength(0);  //set the StringBuilder variable as the zero length
			}
			stringBuilder.append(ch);  // append the new char to the stringBuilder help variable
		}
		aMean = stringBuilder.toString();  //storing the last mean into a String variable
		meansList.add(aMean);   //add the last mean into the ArrayList helper variable
		
		int meanNum = meansList.size();  
		String[] means = new String[meanNum]; // create the String[] variable
		for(i=0;i<meanNum;i++){
			means[i] = new String(meansList.get(i)); //storing the word means into this String[] variable
		}
		
		return means;   //return word means
	}
	
/**
 * The inner class ClientThread used for communication to the client side
 * the task is based on the connection, i.e. per thread per connection
 */
	class ClientThread implements Runnable {
		private Socket socket;
		private int clientNo;
		
		public ClientThread(Socket sock,int cliNo){   // constructor method, initializing the task socket
			this.socket = sock;
			this.clientNo = cliNo;
		}
		
		public void run(){
			try{
				ObjectOutputStream out;
				DataInputStream in;
				String inputWord;
				Result result;
				
				out = new ObjectOutputStream(socket.getOutputStream()); //creating the output stream
				in = new DataInputStream(socket.getInputStream()); //creating the input stream
				
				while(true){ // the task always running
						inputWord = in.readUTF();  //read input word
						jtaLog.append("New search word:: "+inputWord+"\r\n"); //append the input to system log 

						result = search(inputWord); //search the word
						
						out.writeObject(result);  //output the result
				}
			}
			catch(IOException e){
				System.out.println("Socket Connection Lost, Exiting the "+ clientNo+"th thread.");
				jtaLog.append("The "+clientNo+"th clients' thread exited.\r\n");
			}
		}
	}
}

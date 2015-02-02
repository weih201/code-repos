/*
 *  Wei Han's New File
 *  Created on 23/08/2011
 *  Wei han 523979
 */
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

/**
 * DictClient.java: the main class of the dictionary client
 *		The GUI interface and the user control in this class
 */
public class DictClient extends JFrame {
/**
 * 	Below are the class level variables used in the application
 */
	static String serverIP = "";   
	static int serverPort = 5000;
	static String word = "word";
	static RemoteDictionary dictionary;  
	
/**
 *  below are the GUI components used in this application	
 */
	private JLabel jlRemoteServer = new JLabel("RemoteDictionary Server IP address:");
	private JLabel jlServerIP = new JLabel("");
	private JLabel jlPort = new JLabel("Server Port:");
	private JLabel jlPortVal = new JLabel("");
	
	private JLabel jlStatus = new JLabel("Status:");
	private JLabel jlStatusInfo = new JLabel("");
	
	private JLabel jlWordInput = new JLabel("Please Input a Word");
	private JTextField jtfWord = new JTextField("word",18);
	private JButton jbtSearch = new JButton("Search");
	
	private JLabel jlResult = new JLabel();
	private JTextArea jtaResult = new JTextArea(10,25);   // a JTextAera component used to store the search result
	
	public static void main(String[] args) {
		if(args.length!=3){     //checking input parameters number
			System.out.println("Usage: java DictClient addrss  port  word-to-look-for");
			System.exit(0);
		}
		
		serverIP = args[0];
		serverPort = Integer.parseInt(args[1]);
		word = args[2];

		/**
		 * 		Creating the DictServer and make it visible
		 */
		DictClient frame = new DictClient();
		frame.setTitle("Remote Dictionary Client");
		frame.setSize(800,480);
		frame.setLocationRelativeTo(null);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setVisible(true);
		
		/**
		 *  connect to server 
		 */
		if(frame.start(word)){
			frame.jlStatusInfo.setText("Connected");
		}
		else{
			frame.jlStatusInfo.setText("DisConnected");
		}
	}

/**
 * public boolean start(String word)
 * 		Connecting to server
 */
	public boolean start(String word){
		int connStatus;
		dictionary = new RemoteDictionary(serverIP,serverPort); //creating RemoteDictionary class
		connStatus = dictionary.connect(); 
		if(connStatus==0){   //Success to connect to the server
			Result sResult;
			word = word.trim();
			sResult = dictionary.search(word);   //search the command line input word in the remote dictionary
			
			resultUpdate(sResult);          //display the searching result
			jlServerIP.setText(serverIP);   //updating the connection info
			jlPortVal.setText(serverPort+"");
			return true;
		}
		else if(connStatus==-1) {
			System.out.println("The input server address wrong, pleas checking and restart program as:");
			System.out.println("Usage: java DictClient addrss  port  word-to-look-for");
			System.exit(0);
		}
		else {
			System.out.println("Socket IO creation failed, pleas checking and restart program as:");
			System.out.println("Usage: java DictClient addrss  port  word-to-look-for");
			System.exit(0);
		}
		return false;
	}

/**
 * 	public DictClient();
 * 		The DictClient class constructor
 * 		The client GUI panel created in this method
 */
	public DictClient() {
		JPanel p1 = new JPanel();
		BoxLayout box = new BoxLayout(p1,BoxLayout.X_AXIS);
		p1.setLayout(box);
		p1.add(jlRemoteServer);
		p1.add(Box.createHorizontalStrut(5));
		p1.add(jlServerIP);
		
		p1.add(Box.createHorizontalStrut(100));
		p1.add(jlPort);
		p1.add(Box.createHorizontalStrut(5));
		p1.add(jlPortVal);

		JPanel p2 = new JPanel();
		p2.add(jlStatus);
		p2.add(jlStatusInfo);
		
		JPanel pConn = new JPanel();
		BoxLayout box2 = new BoxLayout(pConn,BoxLayout.Y_AXIS);
		pConn.setLayout(box2);
		pConn.add(p1);
		pConn.add(p2);
		pConn.setBorder(BorderFactory.createTitledBorder("Dictionary Connection"));
		
		JPanel p3= new JPanel(new FlowLayout());
		p3.add(jlWordInput);
		p3.add(jtfWord);
		p3.add(jbtSearch);
		
		JScrollPane ptaResult = new JScrollPane();
		ptaResult.add(jtaResult);
		
		JPanel p4 =new JPanel(new BorderLayout());
		p4.add(jlResult,BorderLayout.NORTH);
		jtaResult.setLineWrap(true);
		jtaResult.setWrapStyleWord(true);
		JScrollPane jscrPane = new JScrollPane(jtaResult);
		p4.add(jscrPane,BorderLayout.CENTER);
		
		JPanel pSearch = new JPanel(new BorderLayout());
		pSearch.add(p3,BorderLayout.NORTH);
		pSearch.add(p4,BorderLayout.CENTER);
		pSearch.setBorder(BorderFactory.createTitledBorder("Dictionary Search"));
		
		add(pConn,BorderLayout.NORTH);
		add(pSearch,BorderLayout.CENTER);
		
		jbtSearch.addActionListener(new ActionListener(){  //new search
			public void actionPerformed(ActionEvent e){
				if(!dictionary.isConnect())return;  
				
				Result sResult;
				word = jtfWord.getText().trim();
				sResult = dictionary.search(word);   //searching
				
				resultUpdate(sResult);
			}
		});
	}

/**
 * 	public void resultUpdate(Result result)
 * 		The method used to update the search result in the JTextArea component:jtaResult
 */
	public void resultUpdate(Result result){
		String resultHint,resultStr;
		StringBuilder resultBuilder = new StringBuilder(); // a StringBuilder helper variable
		
		if(result.errorCode == 0){  //found
			resultHint="Hi, the means of the word: \""+ word+"\" are:";  //the hint str
			jlResult.setForeground(Color.BLUE);
			jlResult.setText(resultHint);
			jlResult.setFont(new Font("Serif",Font.BOLD,24)); //display hint str in the jlResult 
			
			for(int i=0;i<result.meanings.length;i++){    //retrive the result.means info into the stringbuilder helper
				resultBuilder.append(result.meanings[i]);
				resultBuilder.append("\r\n");
			}
			resultStr = resultBuilder.toString();   //change the stringbuiler into a String
			jtaResult.setFont(new Font("Serif",Font.BOLD,18));
			jtaResult.setText(resultStr);   //displaying the result
		}
		else if(result.errorCode == -1){  //not found
			resultHint="I'm sorry. I cannot find \""+word+"\" in remote dictionary.";
			jlResult.setForeground(Color.RED);
			jlResult.setText(resultHint);
			jlResult.setFont(new Font("SansSerif",Font.BOLD+Font.ITALIC,24));
			jtaResult.setText("");
		}
		else if(result.errorCode == -2) {   //error
			resultHint="Sorry. \""+word+"\" is not a valid word, please try another word.";
			jlResult.setForeground(Color.RED);
			jlResult.setText(resultHint);
			jlResult.setFont(new Font("SansSerif",Font.BOLD+Font.ITALIC,24));
			jtaResult.setText("");
		}
		else if(result.errorCode == -3) {   //error
			resultHint="Sorry. The socket connection has lost. Please restart program";
			jlResult.setForeground(Color.RED);
			jlResult.setText(resultHint);
			jlResult.setFont(new Font("SansSerif",Font.BOLD+Font.ITALIC,24));
			jtaResult.setText("");
			jlStatusInfo.setText("DisConnected");
		}
		else if(result.errorCode == -4) {   //error
			resultHint="Sorry. Bad data received, please try another word.";
			jlResult.setForeground(Color.RED);
			jlResult.setText(resultHint);
			jlResult.setFont(new Font("SansSerif",Font.BOLD+Font.ITALIC,24));
			jtaResult.setText("");
		}
	}
}

/*
 * Wei Han's New File
 *  Created on 23/08/2011
 *  Wei Han  523979
 */

import java.net.*;
import java.io.*;

/**
 * RemoteDictionary.java: the communication class to the remote dictionary server
 *		
 */
public class RemoteDictionary {

	private String address;   // server IP address
	private int port;         // server port

	private boolean connect = false;  //the variable to indicate whether the client success connet to the server
	
	private Socket  cliSocket;   //the client socket
	private DataOutputStream out;  // output object
	private ObjectInputStream in;  // input object
	
	public RemoteDictionary() {
	}
	
	public RemoteDictionary(String address,int port){
		this.address = address;
		this.port = port;
	}

	public String getAddress() {
		return address;
	}

	public void setAddress(String address) {
		this.address = address;
	}

	public int getPort() {
		return port;
	}

	public void setPort(int port) {
	
		this.port = port;
	}

	public boolean isConnect() {
		return connect;
	}

	public void setConnect(boolean connet) {
		this.connect = connect;
	}
	
/**
 * 	  	public boolean connect()
 * 			The method used to connect to the remote dictionary server
 * 			connect success : return true
 * 			connect failed : return false
 */
	public int connect(){
		try{
			cliSocket = new Socket(address,port);
			out = new DataOutputStream(cliSocket.getOutputStream());
			in = new ObjectInputStream(cliSocket.getInputStream());
		}
		catch(UnknownHostException e){   //server address wrong
			return -1;       //
		}
		catch(IOException ex){   //IO object creating failed
			return -2;
		}
		
		connect = true;
		return 0;
	}
	
/**
 * 	  	public Result search(String word)
 * 			The method used to send the search word to remote server and get the search result form server
 * 			return the search result
 */
	public Result search(String word){
		Result result=new Result();
		
		try{
			out.writeUTF(word);  //sending the search word to server
		}
		catch(IOException e){
			System.out.println("Socket Connection Lost, Please Restart");
			result.errorCode =-3;
			return result;
		}
		
		try{
			result = (Result)in.readObject();  //read the return from server
			return result;
		}
		catch(ClassNotFoundException e){
			result.errorCode = -4;
			return result;
		}
		catch(IOException ex){
			System.out.println("Socket Connection Lost, Please Restart");
			result.errorCode =-3;
			return result;
		}
	}
}

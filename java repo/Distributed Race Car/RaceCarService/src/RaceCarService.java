/*
 * Wei Han's New File
 *  Created on 30/09/2011
 */

import java.rmi.*;
import java.rmi.server.*;
import java.rmi.registry.*;

public class RaceCarService extends UnicastRemoteObject implements RaceCarServiceInterface{
	private CallBack car1 = null;  //will be created as 'Y' car
	private CallBack car2 = null;  // will be created as 'G' car
	
	private boolean starting = false;
	
	public RaceCarService() throws RemoteException {
		super();
	}
	
	public char connect(CallBack car) throws RemoteException {
		if (car1 == null) {
		// car1 registered
			car1 = car;
			car1.notify("Wait for a second car to join");
			System.out.println("Car1 Connecting");
			return 'Y';   //yellow car
			}
		else if (car2 == null) {
		// car2 registered
			car2 = car;
			car2.notify("Wait to start");
			car1.notify("Wait to start");
			System.out.println("Car2 Connecting");
			return 'G';   //Green Car
			}
		else {
		// Already two cars
			car.notify("Two cars are already in the game");
			System.out.println("Another Car Connecting");
			return ' ';  
			}
		}
	
	public void myPos(int x_pos, int y_pos,int index, char color) throws RemoteException{
		if(color == 'Y'){
			car2.rivalPos(x_pos, y_pos, index);
		}
		else {
			car1.rivalPos(x_pos, y_pos,index);
		}
	}
	
	public void start(char color) throws RemoteException {
		if(starting){
			car1.starting();
			car2.starting();
		}
		else starting = true;
	}
	
	public void reStart(char color) throws RemoteException {
		car1.reStart();
		car2.reStart();
		starting = false;
	}

	public void notifyWin(char color)throws RemoteException{
		car1.win(color);
		car2.win(color);
	}
	
	public void notifyCollision(char color) throws RemoteException{
		;
	}

	public static void main(String[] args) {
		try {
			RaceCarServiceInterface server = new RaceCarService();
			Registry registry = LocateRegistry.createRegistry(1099); //.getRegistry(); is not work here ?
			
			if (registry == null) {
				System.out.println("server is null");
			    throw new NullPointerException("cannot bind to null");   
			}

			registry.rebind("RaceCarService", server);
			System.out.println("Server " + server + " registered");
		}
		catch (Exception ex) {
			ex.printStackTrace();
		}
	}
}

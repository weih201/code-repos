/*
 * Wei Han's New File
 *  Created on 30/09/2011
 */

import java.rmi.*;

public interface RaceCarServiceInterface extends Remote{
	public char connect(CallBack car) throws RemoteException;
	public void myPos(int x_pos, int y_pos, int index, char color) throws RemoteException;
	public void start(char color) throws RemoteException;
	public void reStart(char color) throws RemoteException;
	public void notifyWin(char color)throws RemoteException;
	public void notifyCollision(char color) throws RemoteException;
}

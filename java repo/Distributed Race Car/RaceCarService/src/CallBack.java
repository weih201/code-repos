/*
 * Wei Han's New File
 *  Created on 30/09/2011
 */

import java.rmi.*;

public interface CallBack extends Remote {
	public void starting() throws RemoteException;
	public void rivalPos(int x, int y, int index)throws RemoteException;
	public void crashed(boolean crashed) throws RemoteException;
	public void win(char color) throws RemoteException;
	public void notify(String msg) throws RemoteException;
	public void reStart() throws RemoteException;
}

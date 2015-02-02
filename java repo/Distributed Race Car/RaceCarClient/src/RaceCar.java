/*
 * Wei Han's New File
 *  Created on 30/09/2011
 */

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class RaceCar extends UnicastRemoteObject implements CallBack{
	final int MaxCarNum = 16;
	private RaceCarFrame frame;
	
	private int x_pos;
	private int y_pos;
	
	private int rival_X;
	private int rival_Y;
	
	private int speed = 5;
	private String cur_Car;
	private char color;

	private int index;
	private int rival_index;
	
	private boolean crashed = false;
	private boolean win = false;
	private boolean top = false;
	
	public RaceCar() throws RemoteException{
		
	}
	
	public RaceCar(RaceCarFrame frm) throws RemoteException{
		this.frame = frm;
	}

	public RaceCar(String carStr) throws RemoteException{
		this.cur_Car = carStr;
	}

	public RaceCar(String carStr,RaceCarFrame frm) throws RemoteException{
		this.cur_Car = carStr;
		this.frame = frm;
	}
	
	public RaceCar(String carStr,int x, int y) throws RemoteException{
		this.cur_Car = carStr;
		this.x_pos = x;
		this.y_pos = y;
	}

	public void starting() throws RemoteException{
		RaceCarFrame.spinTimer.start();
	}
	
	public void rivalPos(int x, int y, int index)throws RemoteException{
		this.rival_X = x;
		this.rival_Y = y;
		this.rival_index = index;
	}
	
	public void crashed(boolean crashed) throws RemoteException{
		setCrashed(crashed);
	}
	
	public void win(char color) throws RemoteException{
		if(color == this.color){
			frame.jlblStatus.setText("Status: Game Finished");
			frame.jlblNotify.setText("Notify: Win");
		}
		else{
			frame.jlblStatus.setText("Status: Game Finished");
			frame.jlblNotify.setText("Notify: Lost");
		}
		RaceCarFrame.spinTimer.stop();
	}
	
	public void notify(String msg)throws RemoteException{
		frame.jlblNotify.setText("Notify: "+msg);
	}
	
	
	public void reStart() throws RemoteException{
		this.frame.initPane(this.frame.jpTrack);
	}
	
	public void setColor(char color) {
		this.color = color;
	}

	public char getColor() {
		return color;
	}

	public boolean isCrashed() {
		return crashed;
	}

	public void setCrashed(boolean crashed) {
		this.crashed = crashed;
	}

	public boolean isWin() {
		if(top){
			if(this.x_pos<=425&&this.y_pos>=450&&this.y_pos<=510){
				this.win=true;
				return win;
			}
			else {
				return win;
			}
		}
		else {
			if(this.x_pos>=425&&this.y_pos>=50&&this.y_pos<=110){
				this.top=true;
			}
			return win;
		}
	}

	public void setWin(boolean win) {
		this.win = win;
	}

	public void setTop(boolean top) {
		this.top = top;
	}

	public int getIndex() {
		index  = getCarIndex(cur_Car);
		return index;
	}

	public void setIndex(int index) {
		this.index = index;
	}

	public int getRival_index() {
		return rival_index;
	}

	public void setRival_index(int rival_index) {
		this.rival_index = rival_index;
	}

	public int getX_pos() {
		return x_pos;
	}

	public void setX_pos(int x_pos) {
		this.x_pos = x_pos;
	}

	public int getY_pos() {
		return y_pos;
	}

	public void setY_pos(int y_pos) {
		this.y_pos = y_pos;
	}

	public int getRival_X() {
		return rival_X;
	}

	public void setRival_X(int rival_X) {
		this.rival_X = rival_X;
	}

	public int getRival_Y() {
		return rival_Y;
	}

	public void setRival_Y(int rival_Y) {
		this.rival_Y = rival_Y;
	}

	public int getSpeed() {
		return speed;
	}

	public void setSpeed(int speed) {
		this.speed = speed;
	}

	public String getCur_Car() {
		return cur_Car;
	}

	public void setCur_Car(String cur_Car) {
		this.cur_Car = cur_Car;
	}
	
	void speedUp(){
		speed +=1;
		if(speed>10)speed =10;
	}
	
	void slowDown(){
		speed -=1;
		if(speed<0) speed = 0;
	}
	
	void turnLeft(){
		cur_Car = getLeftCar(cur_Car);
	}
	
	void turnRight(){
		cur_Car = getRightCar(cur_Car);
	}

	public String getLeftCar(String car){
		index = getCarIndex(car);
		if(index >= 0){
			index--;
			if(index<0) index=MaxCarNum-1;
			car = getCar(car,index);
		}
		return car;
	}
	
	public String getRightCar(String car){
		index = getCarIndex(car);
		if(index >= 0){
			index++;
			if(index >= MaxCarNum) index= 0;
			car = getCar(car,index);
		}
		return car;
	}
	
	String getCar(String car,int index){
		int idx = car.lastIndexOf('.');
		idx--;
		while(Character.isDigit(car.charAt(idx)))idx--;
		return (car.substring(0,idx+1)+index+".gif");
	}
	
	int getCarIndex(String car){
		int carIndex;
		int index = car.lastIndexOf('.');
		index-=2;
		if(Character.isDigit(car.charAt(index))){
			carIndex = Integer.parseInt(Character.toString(car.charAt(index)))*10;
			index++;
			carIndex += Integer.parseInt(Character.toString(car.charAt(index)));
			return carIndex;
		}
		else{
			index++;
			if(Character.isDigit(car.charAt(index))){
				carIndex = Integer.parseInt(Character.toString(car.charAt(index)));
				return carIndex;
			}
		}
		return -1;
	}
}

/*
 * Wei Han's New File
 *  Created on 30/09/2011
 */

import javax.swing.*;

import java.awt.*;
import java.awt.event.*;
import javax.swing.border.*;

import java.rmi.*;
import java.rmi.registry.*;

public class RaceCarFrame extends JFrame {
	JButton jbtConnect = new JButton("Connect");
	JButton jbtStart = new JButton("Start");
	JButton jbtStop  = new JButton("Stop");
	JButton jbtAcc   = new JButton("Speed Up");
	JButton jbtDec   = new JButton("Slow Down");
	JButton jbtLeft  = new JButton("<=Left");
	JButton jbtRight = new JButton("Right=>");
	
	JLabel jlblStatus = new JLabel("Status: Not Connected");
	JLabel jlblNotify = new JLabel("Notify: Wait to connect");
	JLabel jlblCar = new JLabel("");
	
	TrackPane jpTrack = new TrackPane();
	
	private JMenuItem jmiRestart,jmiAbout;

	private String yCarStr = "image/car1/car0.gif";
	private String gCarStr = "image/car2/car0.gif";
	
	private String hostName="";
	private RaceCarServiceInterface raceCarService;
	private char color;

	RaceCar myCar; 
	RaceCar rivalCar; 
	
	static final double PI = 3.14159;
	
	static Timer spinTimer;

	public RaceCarFrame(){
		JPanel jpStart = new JPanel();
		jpStart.setLayout(new GridLayout(1,3));
		jpStart.add(jbtConnect);
		jpStart.add(jbtStart);
		jpStart.add(jbtStop);
		
		JPanel jpControl = new JPanel();
		jpControl.setLayout(new BorderLayout());
		jpControl.add(jbtLeft,BorderLayout.WEST);
		jpControl.add(jbtRight,BorderLayout.EAST);
		jpControl.add(jbtAcc,BorderLayout.NORTH);
		jpControl.add(jbtDec,BorderLayout.CENTER);
		
		JPanel jpStatus = new JPanel();
		JPanel jpNotify = new JPanel();
		jpNotify.setLayout(new GridLayout(2,1));
		jpNotify.add(jlblStatus);
		jpNotify.add(jlblNotify);
		jpStatus.add(jpNotify,BorderLayout.CENTER);
		jpStatus.add(jlblCar,BorderLayout.WEST);
		
		JPanel jpButton = new JPanel();
		jpButton.setLayout(new BorderLayout());
		jpButton.add(jpStart,BorderLayout.WEST);
		jpButton.add(jpStatus,BorderLayout.CENTER);
		jpButton.add(jpControl,BorderLayout.EAST);
		jpButton.setBorder(new LineBorder(Color.BLACK));
		
		add(jpTrack,BorderLayout.CENTER);
		add(jpButton,BorderLayout.NORTH);
		
		JMenuBar jmb = new JMenuBar();
		setJMenuBar(jmb);
		
		JMenu operationMenu = new JMenu("Operation");
		operationMenu.add(jmiRestart = new JMenuItem("Restart",'R'));
		
		JMenu helpMenu = new JMenu("Help");
		helpMenu.add(jmiAbout = new JMenuItem("About",'A'));
		
		jmb.add(operationMenu);
		jmb.add(helpMenu);

		spinTimer = new Timer(50,new TimerListener());
		
		addKeyListener(new keyListener());

		jbtConnect.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e){
				
			while(hostName.length()<1){
				hostName = JOptionPane.showInputDialog("Please input the Race Server Address:");
			}
			
			if(initRMI()){
				jpTrack.setConnected(true);
				initPane(jpTrack);
			}
		}
		});
		jbtConnect.addKeyListener(new keyListener());

		jbtStart.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e){
				try{
					raceCarService.start(myCar.getColor());
				}
				catch(RemoteException ex){
					
				}
			}
		});
		jbtStart.addKeyListener(new keyListener());
		
		jbtStop.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e){
				spinTimer.stop();
			}
		});
		jbtStop.addKeyListener(new keyListener());

		jbtLeft.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e){
				myCar.turnLeft();
			}
		});
		jbtLeft.addKeyListener(new keyListener());
	
		jbtRight.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e){
				myCar.turnRight();
			}
		});
		jbtRight.addKeyListener(new keyListener());

		jbtAcc.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e){
				myCar.speedUp();
			}
		});
		jbtAcc.addKeyListener(new keyListener());

		jbtDec.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e){
				myCar.slowDown();
			}
		});
		jbtDec.addKeyListener(new keyListener());

		jmiRestart.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e){
				try{
					raceCarService.reStart(myCar.getColor());
				}
				catch(RemoteException ex){
					
				}
				initPane(jpTrack);
			}
		});
		jmiRestart.addKeyListener(new keyListener());

		jmiAbout.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e){
				JOptionPane.showMessageDialog(null, "Race Car Game");
			}
		});
		jmiAbout.addKeyListener(new keyListener());
	}
	
	public void initPane(TrackPane panel){
		System.out.println("System.getProperty(\"user.dir\") is:"+System.getProperty("user.dir"));

		if(color == 'Y'){
			panel.setCar1(myCar);
			panel.setCar2(rivalCar);
			
			myCar.setCrashed(false);
			myCar.setCur_Car(yCarStr);
			rivalCar.setCur_Car(gCarStr);

			myCar.setWin(false);
			myCar.setTop(false);
		}
		else {
			panel.setCar2(myCar);
			panel.setCar1(rivalCar);
			
			myCar.setCrashed(false);
			myCar.setCur_Car(gCarStr);
			rivalCar.setCur_Car(yCarStr);

			myCar.setWin(false);
			myCar.setTop(false);
		}
		
		spinTimer.stop();
		panel.repaint();
	}
	
	public boolean initRMI() {
		try {
			Registry registry = LocateRegistry.getRegistry(hostName);
			raceCarService = (RaceCarServiceInterface)registry.lookup("RaceCarService");
			
			try{
				myCar = new RaceCar(this);
				rivalCar = new RaceCar();
				
				color = raceCarService.connect(myCar);
				myCar.setColor(color);
				
				if(color == 'Y'){
					myCar.setCur_Car(yCarStr);
					myCar.setColor('Y');
					
					rivalCar.setCur_Car(gCarStr);
					rivalCar.setColor('G');
					jlblStatus.setText("Connect to "+hostName);

					ImageIcon yCarIcon = new ImageIcon(yCarStr);
					jlblCar.setIcon(yCarIcon);
				}
				else if(color == 'G'){
					myCar.setCur_Car(gCarStr);
					myCar.setColor('G');
					
					rivalCar.setCur_Car(yCarStr);
					rivalCar.setColor('Y');
					jlblStatus.setText("Connect to "+hostName);

					ImageIcon gCarIcon = new ImageIcon(gCarStr);
					jlblCar.setIcon(gCarIcon);
				}
				else return false;
			}
			catch(RemoteException e){
				e.printStackTrace();
				return false;
			}
			
			return true;
		}
		catch (Exception e){
			System.out.println(e);
			return false;
		}
	}
	
	class keyListener implements KeyListener{
		public void keyPressed(KeyEvent e){
			switch(e.getKeyCode()){
				case KeyEvent.VK_DOWN:  myCar.slowDown();break;
				case KeyEvent.VK_UP:    myCar.speedUp();break;
				case KeyEvent.VK_LEFT:  myCar.turnLeft();break;
				case KeyEvent.VK_RIGHT: myCar.turnRight();break;
			}
		}
		
		public void keyReleased(KeyEvent e){
			
		}

		public void keyTyped(KeyEvent e){
			
		}
	}
	
	class TimerListener implements ActionListener{
		public void actionPerformed(ActionEvent e){
			
			int car1Index = myCar.getIndex();
			int speed1 = myCar.getSpeed();
			int x_pos,y_pos;
			
			int car1DeltaX = 0-(int)(speed1*Math.cos(car1Index*22.5/360.0*2*PI));
			int car1DeltaY = 0-(int)(speed1*Math.sin(car1Index*22.5/360.0*2*PI));
			
			x_pos = myCar.getX_pos()+car1DeltaX;
			y_pos = myCar.getY_pos()+car1DeltaY;
			
			if(collision(myCar)) myCar.setCrashed(true);
			if(collision(rivalCar)) rivalCar.setCrashed(true);

			if(collision(myCar,rivalCar)){
				myCar.setCrashed(true);
				rivalCar.setCrashed(true);
			}
			
			if(!myCar.isCrashed()){
				myCar.setX_pos(x_pos);
				myCar.setY_pos(y_pos);
				
				try{
					raceCarService.myPos(x_pos, y_pos, myCar.getIndex(), myCar.getColor());
				}
				catch(RemoteException ex){
					
				}
			}
			
			rivalCar.setX_pos(myCar.getRival_X());
			rivalCar.setY_pos(myCar.getRival_Y());
			rivalCar.setCur_Car(myCar.getCar(rivalCar.getCur_Car(), myCar.getRival_index()));
			
			if(myCar.isWin()){
				try{
					raceCarService.myPos(x_pos, y_pos,myCar.getIndex(), myCar.getColor());
					raceCarService.notifyWin(myCar.getColor());
				}
				catch(RemoteException ex){
				}
			}
			
			if(rivalCar.isWin()){
				
			}
			
			ImageIcon carIcon = new ImageIcon(myCar.getCur_Car());
			jlblCar.setIcon(carIcon);

			jpTrack.repaint();
		}
	}
		
		public boolean collision(RaceCar car1,RaceCar car2){  //two car collision
			if((Math.abs(car1.getX_pos()-car2.getX_pos())<40)&&(Math.abs(car1.getY_pos()-car2.getY_pos())<40))return true;
			else return false;
		}

		public boolean collision(RaceCar car){  //collision with track
			int x_pos  = car.getX_pos();
			int y_pos  = car.getY_pos();
			
			if((x_pos<50)||(y_pos<50)||(x_pos>760)||(y_pos>510)) return true;
			else if((x_pos>110)&&(y_pos>110)&&(x_pos<700)&&(y_pos<450)) return true;
			else return false;
		}

		
	public static void main(String[] args) {
		RaceCarFrame frame = new RaceCarFrame();
		frame.setTitle("Race Car");
		frame.setSize(870,700);
		frame.setLocationRelativeTo(null);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setVisible(true);
	}
}

class TrackPane extends JPanel {
	
	private RaceCar car1;
	private RaceCar car2;
	
	int x1_base;
	int y1_base;
	
	int x2_base;
	int y2_base;
	
	boolean connected = false;
	
	public TrackPane(){
		
	}

	public boolean isConnected() {
		return connected;
	}

	public void setConnected(boolean connected) {
		this.connected = connected;
	}

	public void setCar1(RaceCar car1) {
		x1_base = 425;
		y1_base = 450;
		
		car1.setX_pos(x1_base);
		car1.setY_pos(y1_base);
		this.car1 = car1;
	}

	public void setCar2(RaceCar car2) {
		x2_base = 200;
		y2_base = 500;

		car2.setX_pos(x2_base);
		car2.setY_pos(y2_base);
		this.car2 = car2;
	}

	protected void paintComponent(Graphics g){
		super.paintComponent(g);
		
		Color c1 = Color.green;
		g.setColor(c1);
		g.fillRect(150, 150, 550, 300);  //inner side
		
		Color c2 = Color.black;
		g.setColor(c2);
		g.drawRect(50, 50, 750, 500);    //outer side
		g.drawRect(150, 150, 550, 300);

		Color c3 = Color.yellow;
		g.setColor(c3);
		g.drawRect(100, 100, 650, 400);

		Color c4 = Color.RED;
		g.setColor(c4);
		g.drawLine(425, 450, 425, 550);
		
		if(connected){
			ImageIcon car1Icon = new ImageIcon(this.car1.getCur_Car());
			ImageIcon car2Icon = new ImageIcon(this.car2.getCur_Car());

			Image car1 = car1Icon.getImage();
			Image car2 = car2Icon.getImage();

			g.drawImage(car1,this.car1.getX_pos(),this.car1.getY_pos(),40,40,this);
			g.drawImage(car2,this.car2.getX_pos(),this.car2.getY_pos(),40,40,this);
		}
	}
}


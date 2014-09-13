import java.awt.*;
import java.awt.event.*;
import java.math.*;

public class DTrans extends Frame
{
	private double pi=3.141592;
	int A=45,cs=0;
	double xx,yy,zz;
    double ad=(pi/180)*A;

	public DTrans()
	{
		addMouseListener(new MyMouseAdapter(this));
		addWindowListener(new MyWindowAdapter());
	}


//	public void set_camera(int a ,int b ,int y)
//	{
//		double rad=pi/180;
//		cosa=Math.cos(rad*a);
//		cosb=Math.cos(rad*b);
//		cosy=Math.cos(rad*y);
//	}

	
	public void rotate()
	{
		double xxx=xx,yyy=yy,zzz=zz;
		ad=(pi/180)*A;
		switch(cs)
		{
			case 0:
				break;
			case 1:
				yy=yyy*Math.cos(ad)-zzz*Math.sin(ad);
				zz=yyy*Math.sin(ad)+zzz*Math.cos(ad);
				break;
			case 2:
				xx=zzz*Math.sin(ad)+xxx*Math.cos(ad);
				zz=zzz*Math.cos(ad)-xxx*Math.sin(ad);
				break;
			case 3:
				yy=yyy*Math.cos(ad)+xxx*Math.sin(ad);
				xx=-yyy*Math.sin(ad)+xxx*Math.cos(ad);
				break;

		}
	}

	public void paint(Graphics g)
	{
		g.setColor(Color.yellow); 

		int nx,ny;
		int[] x={1110 , 600 , 900, 1000,700 , 800, 3000, 1100, 1000, 900 ,700 , 600 , 400 , 900 , 150 , 3110};
		int[] y={3000 , 950 , 680, 810 ,150 , 280, 800, 700 , 2000, 400 ,208 , 150 , 110 , 680 , 550 , 3000};
		int[] z={1110 , 715 , 100, 660 ,60  , 80 , 800  , 600, 900 , 800 ,60  , 400, 300 , 100 , 715 , -3110};
		//int oldxx=(int)(x[i]*b3(0)+x[(i+1)]*b2(0)+x[(i+2)]*b1(0)+x[(i+3)]*b0(0));
		//int oldyy=(int)(y[i]*b3(0)+y[(i+1)]*b2(0)+y[(i+2)]*b1(0)+y[(i+3)]*b0(0));

		int i=0;
		for (double v=0;v<=1;v+=0.005)
			for (double u=0;u<=1;u+=0.005)
			{
				xx=(x[i]*b3(u)*b3(v)+x[i+1]*b2(u)*b3(v)+x[i+2]*b1(u)*b3(v)+x[i+3]*b0(u)*b3(v)+x[i+4]*b3(u)*b2(v)+x[i+5]*b2(u)*b2(v)+x[i+6]*b1(u)*b2(v)+x[i+7]*b0(u)*b2(v)+x[i+8]*b3(u)*b1(v)+x[i+9]*b2(u)*b1(v)+x[i+10]*b1(u)*b1(v)+x[i+11]*b0(u)*b1(v)+x[i+12]*b3(u)*b0(v)+x[i+13]*b2(u)*b0(v)+x[i+14]*b1(u)*b0(v)+x[i+15]*b0(u)*b0(v));
				yy=(y[i]*b3(u)*b3(v)+y[i+1]*b2(u)*b3(v)+y[i+2]*b1(u)*b3(v)+y[i+3]*b0(u)*b3(v)+y[i+4]*b3(u)*b2(v)+y[i+5]*b2(u)*b2(v)+y[i+6]*b1(u)*b2(v)+y[i+7]*b0(u)*b2(v)+y[i+8]*b3(u)*b1(v)+y[i+9]*b2(u)*b1(v)+y[i+10]*b1(u)*b1(v)+y[i+11]*b0(u)*b1(v)+y[i+12]*b3(u)*b0(v)+y[i+13]*b2(u)*b0(v)+y[i+14]*b1(u)*b0(v)+y[i+15]*b0(u)*b0(v));
				zz=(z[i]*b3(u)*b3(v)+z[i+1]*b2(u)*b3(v)+z[i+2]*b1(u)*b3(v)+z[i+3]*b0(u)*b3(v)+z[i+4]*b3(u)*b2(v)+z[i+5]*b2(u)*b2(v)+z[i+6]*b1(u)*b2(v)+z[i+7]*b0(u)*b2(v)+z[i+8]*b3(u)*b1(v)+z[i+9]*b2(u)*b1(v)+z[i+10]*b1(u)*b1(v)+z[i+11]*b0(u)*b1(v)+z[i+12]*b3(u)*b0(v)+z[i+13]*b2(u)*b0(v)+z[i+14]*b1(u)*b0(v)+z[i+15]*b0(u)*b0(v));
				
				rotate();
				
				nx=(int)((xx-zz));
				ny=(int)((yy-zz));
				g.drawOval(nx-300,ny+300,1,1);
			}
	}
/*
//		for (double v=-pi/2;v<=pi/2;v+=0.05)
//			for (double u=-pi;u<=pi;u+=0.05)
//			{
//				xx=4*Math.cos(v)*Math.cos(u);
//				yy=4*Math.cos(v)*Math.sin(u);
//				zz=4*Math.sin(v);
//
////				nx = (int)(102400 * ((double)xx / (zz + 1024)) + 512);
////				ny = (int)(76800 * ((double)yy / (zz + 768)) + 384);
//				nx=(int)(100*(xx-(cosa/cosy)*zz));
//				ny=(int)(100*(yy-(cosb/cosy)*zz));
//				g.drawOval(nx+300,ny+300,1,1);
//				//g.drawLine(oldxx,oldyy,xx,yy);
//				//oldxx=xx;oldyy=yy;
//			}

		//g.drawString("Finished!!!",600,400);
	}//end of update
*/

	
	public static void main(String args[])  
	{
		DTrans appwin = new DTrans();

		appwin.setSize(new Dimension(1024, 768));
		appwin.setTitle("B-SPline Project");
		appwin.setBackground(Color.black);
		appwin.setVisible(true);
		//appwin.set_camera(appwin.aa,appwin.bb,appwin.cc);
		appwin.repaint();
	}
	private double b0(double u)
	{
		return ((u*u*u)/6.0);
	}
	private double b1(double u)
	{
		double temp;
		temp=1.0/6.0*(-3*u*u*u+3*u*u+3*u+1);
		return (temp);
	}
	private double b2(double u)
	{
		double temp;
		temp=1.0/6.0*(3*u*u*u-6*u*u+4);
		return (temp);
	}
	private double b3(double u)
	{
		double temp;
		temp=(1.0/6.0)*((1-u)*(1-u)*(1-u));
		return (temp);
	}
}//end of class DTrans

class MyMouseAdapter extends MouseAdapter  
{
	DTrans appWindow;
	public MyMouseAdapter(DTrans appWindow)  
	{
		this.appWindow = appWindow;
	}
	public void mousePressed(MouseEvent me)  
	{
		//appWindow.mouseX = me.getX();
		//appWindow.mouseY = me.getY();
		appWindow.A+=5;
		if (me.getX()<=341)
			appWindow.cs=1;
		else if (me.getX()<=680 && me.getX()>341)
			appWindow.cs=2;
		else
			appWindow.cs=3;

			appWindow.repaint();
	}
}
class MyWindowAdapter extends WindowAdapter  
{
	public void windowClosing(WindowEvent we) 
	{
		System.exit(0);
	}
}

import java.awt.*;
import java.awt.event.*;

public class eleven5 extends Frame {
    int mouseX, mouseY;
    private int k= 0;int rep=0;private int os=0;
	private int [] x= new int [4];
	private int [] y=new int [4];

   public eleven5()  {
      addMouseListener(new MyMouseAdapter(this));
      addWindowListener(new MyWindowAdapter());
   }

	public void update(Graphics g)
	{
		g.setColor(Color.pink);  

		if (rep==1)
		{
			x[k]=mouseX;
			y[k]=mouseY;
			g.drawOval(mouseX,mouseY,4,4);g.drawString(String.valueOf(os),mouseX,mouseY);
			rep=0;os++;
			if (k==3)
				k=0;
			else
				k++;
		}

		if (os>=4)
		{
			int xx,yy,i=os%4;
			int oldxx=(int)(x[i]*b3(0)+x[(i+1)%4]*b2(0)+x[(i+2)%4]*b1(0)+x[(i+3)%4]*b0(0));
			int oldyy=(int)(y[i]*b3(0)+y[(i+1)%4]*b2(0)+y[(i+2)%4]*b1(0)+y[(i+3)%4]*b0(0));

			//for (i=0;i<num-3;i++)
			//{
			g.setColor(Color.yellow);
			for (double u=0;u<=1;u+=0.001)
			{
				xx=(int)(x[i]*b3(u)+x[(i+1)%4]*b2(u)+x[(i+2)%4]*b1(u)+x[(i+3)%4]*b0(u));
				yy=(int)(y[i]*b3(u)+y[(i+1)%4]*b2(u)+y[(i+2)%4]*b1(u)+y[(i+3)%4]*b0(u));
				g.drawLine(oldxx,oldyy,xx,yy);
				oldxx=xx;oldyy=yy;
			}
			//}
		}
	}

   // Creat the window.
   public static void main(String args[])  {
		eleven5 appwin = new eleven5();

		appwin.setSize(new Dimension(1024, 768));
		appwin.setTitle("B-SPline Project");
	    appwin.setBackground(Color.black);
		appwin.setVisible(true);
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
}

class MyMouseAdapter extends MouseAdapter  
{
   eleven5 appWindow;
   public MyMouseAdapter(eleven5 appWindow)  {
      this.appWindow = appWindow;
   }
   public void mousePressed(MouseEvent me)  {
      appWindow.mouseX = me.getX();
      appWindow.mouseY = me.getY();
	  appWindow.rep=1;
      appWindow.repaint();
      //appWindow.update();
   }
}
class MyWindowAdapter extends WindowAdapter  {
   public void windowClosing(WindowEvent we) {
      System.exit(0);
   }
}

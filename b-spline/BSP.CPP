#include <graphics.h>
#include <iostream.h>
#include <stdlib.h>
#include <stdio.h>
#include <conio.h>
#define max_num 20;
struct Point
{
	float x,y;
};
float b0(float u)
{
	return ((u*u*u)/6.0);
}
float b1(float u)
{
	float temp;
	temp=1.0/6.0*(-3*u*u*u+3*u*u+3*u+1);
	return (temp);
}
float b2(float u)
{
	float temp;
	temp=1.0/6.0*(3*u*u*u-6*u*u+4);
	return (temp);
}
float b3(float u)
{
	float temp;
	temp=(1.0/6.0)*((1-u)*(1-u)*(1-u));
	return (temp);
}
int main(void)
{
   int gdriver = DETECT, gmode, errorcode;
   initgraph(&gdriver, &gmode, "");
   int num;
   cout << "enter number of vertices: MAX = 20" << endl;
   cin >> num ;
   cout << endl;
   Point a[20];
   cout << "Enter 4 verteces:" << endl ;
   for (int i=0;i<num;i++)
   {
   cin >> a[i].x >> a[i].y;
   cout << endl;
   }

   float xx,yy;
   for (i=0;i<num-3;i++)
   {
   for (float u=0;u<=1;u+=0.005)
   {
	xx=a[i].x*b3(u)+a[i+1].x*b2(u)+a[i+2].x*b1(u)+a[i+3].x*b0(u);
	yy=a[i].y*b3(u)+a[i+1].y*b2(u)+a[i+2].y*b1(u)+a[i+3].y*b0(u);
	putpixel(xx,yy,RED);
   }
   }
   getch();
   closegraph();
   return 0;
}



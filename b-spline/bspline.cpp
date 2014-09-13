/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

		B-spline subdivision for 2D polygons

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/


#include <gl/glu.h>

#include <math.h>

#include <stdlib.h>

#include <time.h>
#include <stdio.h>


#define num_control_vertices		3					//the number of control vertices

#define number_iterations			3					//the numbere of iterations to be done


struct point{											//point structure to help organize data
	double	x,y;
};

typedef point *pointpointer;							//point typedef to aid in forming 2D
														//dynamic array of point structure.

point	*control;										//the array that my control points are in

point	*original;										//an array that holds the original control array
														//which can be used to reset control points.

point	**controlSurface;								//the array that holds the conrol points for my surface

point	**originalSurface;								//an array that holds the original control points of
														//my surface which can be used to reset control points.

int		Vx_min=0;										//the screen's maximum and minimum width and height.
int		Vx_max=500;
int		Vy_min=0;
int		Vy_max=550;

int		algorithm=0;									//a variable that keeps up with which
														//algorithm to display

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//	uses the original array to set the control array
void setControl(point* control){
   for (int i=0;i<num_control_vertices;i++)
		control[i]=original[i];
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//	uses the original array to set the control array
void setControlSurface(point **control){
   for (int i=0;i<num_control_vertices;i++)
		for (int j=0;j<num_control_vertices;j++)
			controlSurface[i][j]=originalSurface[i][j];
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// allocates necessary memory and intialized original arrays with the control points
void init(void){
	glClearColor(0.0, 0.0, 0.0, 0.0);

	original=new point[num_control_vertices];
	control=new point[num_control_vertices*pow(2,number_iterations)];		//num_control_vertices*pow(2,number_iterations) is
	for (int i=0;i<num_control_vertices*pow(2,number_iterations);i++){		//is used to allocate enough memory for all the
		control[i].x=0;														//possible points that the system can add, given
		control[i].y=0;														//that the number of control vertices will be
	}																		//num_control_vertices and the number of subdivision
																			//iterations will be number_iterations.
	originalSurface=new pointpointer[num_control_vertices];
	for (i=0;i<num_control_vertices;i++)
		originalSurface[i]=new point[num_control_vertices];

	controlSurface=new pointpointer[num_control_vertices*pow(2,number_iterations)];
	for (i=0;i<num_control_vertices*pow(2,number_iterations);i++)
		controlSurface[i]=new point[num_control_vertices*pow(2,number_iterations)];

	for (i=0;i<num_control_vertices*pow(2,number_iterations);i++)
		for (int j=0;j<num_control_vertices*pow(2,number_iterations);j++){
			controlSurface[i][j].x=0;
			controlSurface[i][j].y=0;
		}

	original[0].x=75.0;											//the original triangle
	original[0].y=425.0;
	original[1].x=400.0;
	original[1].y=150.0;
	original[2].x=100.0;
	original[2].y=100.0;

	originalSurface[0][0].x=(rand()%50)+0.0;					//the original triangles used
	originalSurface[0][0].y=(rand()%50)+300.0;					//in creating the surface.
	originalSurface[0][1].x=(rand()%50)+50.0;
	originalSurface[0][1].y=(rand()%50)+265.0;
	originalSurface[0][2].x=(rand()%50)+30.0;
	originalSurface[0][2].y=(rand()%50)+170.0;


	originalSurface[1][0].x=-(rand()%50)+365.0;
	originalSurface[1][0].y=(rand()%50)+165.0;
	originalSurface[1][1].x=-(rand()%50)+450.0;
	originalSurface[1][1].y=(rand()%50)+200.0;
	originalSurface[1][2].x=-(rand()%50)+450.0;
	originalSurface[1][2].y=(rand()%50)+80.0;


	originalSurface[2][0].x=-(rand()%50)+375.0;
	originalSurface[2][0].y=(rand()%50)+365.0;
	originalSurface[2][1].x=-(rand()%50)+450.0;
	originalSurface[2][1].y=(rand()%50)+400.0;
	originalSurface[2][2].x=-(rand()%50)+450.0;
	originalSurface[2][2].y=(rand()%50)+315.0;
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// adds two point variables together. helps to clear up congested code.
point operator+(point p1,point p2){
point temp;
	temp.x=p1.x+p2.x;
	temp.y=p1.y+p2.y;
return temp;
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// subtract two point variables. helps to clear up congested code.
point operator-(point p1,point p2){
point temp;
	temp.x=p1.x-p2.x;
	temp.y=p1.y-p2.y;
return temp;
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//	calculates the midpoint between to points. helps to clear up congested code.
point MidPoint(point p1, point p2){
point temp=p1+p2;
	temp.x/=2.0;
	temp.y/=2.0;
return temp;
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//	transposes a square 2D array 
void transpose(point **result){
int		total=num_control_vertices*(int)pow(2,number_iterations);
point	temp;
	for (int i=0;i<total;i++)
		for (int j=i;j<total;j++)
			if (i!=j){
				temp=result[j][i];
				result[j][i]=result[i][j];
				result[i][j]=temp;
			}
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//	this function actually performs the B-Spline Split & Tweak polygon
//	smoothing algorithm. The first parameter is the current polygon and
//	the second parameter is the current iteration which is used to calculate
//	how many points will need to be manipulated.
point* bspline(point* result,int iteration){
int		total=num_control_vertices*(int)pow(2,iteration-1);
point	*midpoints=new point[total];						//array which will hold all the midpoints
point	*newVertices=new point[total];						//array which will hold the new vertices
															//which have been pulled towards the average
															//of their neighboring midpoints.
	for (int i=0;i<total;i++)									//calculating midpoints
		midpoints[i]=MidPoint(result[i],result[(i+1)%total]);
	for (i=0;i<total;i++)										//calculating average of neighboring midpoints
		newVertices[(i+1)%total]=MidPoint(MidPoint(midpoints[i],midpoints[(i+1)%total]),result[(i+1)%total]);
	for (i=0;i<total;i++){
		result[2*i]=newVertices[i];								//combining the two arrays to form a new set
		result[2*i+1]=midpoints[i];								//of control points.
	}

	delete midpoints;
	delete newVertices;
return result;
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//	this function actually performs the B-Spline 4-Point Subdivide polygon
//	smoothing algorithm. The first parameter is the current polygon and
//	the second parameter is the current iteration which is used to calculate
//	how many points will need to be manipulated.
point* fourPts(point* result,int iteration){
int		total=num_control_vertices*(int)pow(2,iteration-1);
point	m;													//variable which will be used to store the midpoint 
															//of the current edge.
point	*oldVertices=new point[total];						//array which hold all the old vertices
point	*newMidpoints=new point[total];						//array which will hold the new vertices which
															//are midpoints that have been pushed 1/8 the distance
															//from the current edges midpoint to the midpoint of
															//the vertices which neighbor it on the left and right
	for (int i=0;i<total;i++){								//which will now be refered to as m'.
		oldVertices[i]=result[i];
		m=MidPoint(result[(i+1)%total],result[(i+2)%total]);		//calculating midpoint
		newMidpoints[(i+1)%total]=MidPoint(MidPoint(MidPoint(m,m+(m-MidPoint(result[i],result[(i+3)%total]))),m),m);
	}																//to simplify the task of adding a distance to
																	//a point I moved m' outside of the polygonto a point
																	//that is colinear to the line formed between m and m'
																	//but at the same distance that m' was from m. By
																	//doing this I can then obtain the desired point by
																	//taking successive midpoints until a distance of 1/8
																	//from m is obtained.
	for (i=0;i<total;i++){
		result[2*i]=oldVertices[i];									//combining the two arrays to form a new set
		result[2*i+1]=newMidpoints[i];								//of control points
	}

	delete oldVertices;
	delete newMidpoints;
return result;
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
void display(void){
  int total;
	glClear(GL_COLOR_BUFFER_BIT);

	glBegin(GL_POLYGON);			//green square
		glColor3ub(0,128,0);
		glVertex2d(134,545);
		glVertex2d(174,545);
		glVertex2d(174,505);
		glVertex2d(134,505);
	glEnd();

	glBegin(GL_POLYGON);			//yellow square
		glColor3ub(255,255,0);
		glVertex2d(198,545);
		glVertex2d(238,545);
		glVertex2d(238,505);
		glVertex2d(198,505);
	glEnd();

	glBegin(GL_POLYGON);			//white square
		glColor3ub(255,255,255);
		glVertex2d(262,545);
		glVertex2d(302,545);
		glVertex2d(302,505);
		glVertex2d(262,505);
	glEnd();

	glBegin(GL_POLYGON);			//red square
		glColor3ub(128,0,0);
		glVertex2d(326,545);
		glVertex2d(366,545);
		glVertex2d(366,505);
		glVertex2d(326,505);

	glEnd();

	glBegin(GL_LINES);

		if (algorithm==0||algorithm==1)
			for (int i=0;i<=number_iterations;i++){					//changes colors of iterations
				glColor3ub(255/number_iterations*(number_iterations-i),255/number_iterations*(number_iterations-i),255/number_iterations*i);

				setControl(control);								//initializes the control polygon
				for (int j=1;j<=i;j++)
					if (algorithm==0)
						bspline(control,j);							//applies the Split & Tweak algorithm
					else											//an appropriate number of times.
						fourPts(control,j);							//applies the 4-Point algorithm an
																	//an appropriate number of times.
				total=num_control_vertices*pow(2,i);				//calculates number of vertices to display
				for (j=0;j<total;j++){
					glVertex2d(control[j].x, control[j].y);			//use vertices to form polygon
					glVertex2d(control[(j+1)%total].x, control[(j+1)%total].y);
				}
			}
		else{
			glColor3ub(255,255,255);
			total=num_control_vertices*pow(2,number_iterations);		//calculates number of vertices to display
			setControlSurface(controlSurface);							//initializes the control polygon

			for (int i=0;i<num_control_vertices;i++)
				if (algorithm==2)
					bspline(bspline(bspline(controlSurface[i],1),2),3);	//applies Split & Tweak algorithm to form
				else													//the first set of polygons in the surface.
					fourPts(fourPts(fourPts(controlSurface[i],1),2),3);	//applies 4-Point algorithm to form
																		//the first set of polygons in the surface.

			transpose(controlSurface);									//transposes set of arrays.

			for (i=0;i<total;i++)
				if (algorithm==2)
					bspline(bspline(bspline(controlSurface[i],1),2),3);	//applies Split & Tweak algorithm to form
				else													//the second set of polygons in the surface.
					fourPts(fourPts(fourPts(controlSurface[i],1),2),3);	//applies 4-Point algorithm to form
																		//the second set of polygons in the surface.
			for (i=0;i<total;i++)
				for (int j=0;j<total;j++){
					glVertex2d(controlSurface[j][i].x, controlSurface[j][i].y);	//use vertices to form surface
					glVertex2d(controlSurface[(j+1)%total][i].x, controlSurface[(j+1)%total][i].y);

					glVertex2d(controlSurface[i][j].x, controlSurface[i][j].y);
					glVertex2d(controlSurface[i][(j+1)%total].x, controlSurface[i][(j+1)%total].y);
				}
		}

	glEnd();
	glFlush();
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//	determines where the mouse is when it is clicked and tests to see if 
//	the user has chosen to change the algorithm that is being diaplayed.
void mouse(int button, int state, int x, int y){
	if (x>134&&x<174&&y<Vy_max-505&&y>Vy_max-545)		//the green square
		algorithm=0;
	else if (x>198&&x<238&&y<Vy_max-505&&y>Vy_max-545)	//the yellow square
		algorithm=1;
	else if (x>262&&x<302&&y<Vy_max-505&&y>Vy_max-545)	//the white square
		algorithm=2;
	else if (x>326&&x<366&&y<Vy_max-505&&y>Vy_max-545)	//the red square
		algorithm=3;
	glutPostRedisplay();
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
void reshape(int w, int h){
   glViewport(0, 0, (GLsizei) w, (GLsizei) h); 
   glMatrixMode (GL_PROJECTION);
   glLoadIdentity ();
   gluOrtho2D(Vx_min, Vx_max, Vy_min, Vy_max);
   glMatrixMode (GL_MODELVIEW);
}

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
int main(int argc, char** argv){
	srand((unsigned)time( NULL ));
	printf("click:\nthe green square for the \"Split & Tweak\" algorithm\n");
	printf("the yellow square for the 4-Point Subdivision algorithm\n");
	printf("the white square for the surface adaptation of the \"Split & Tweak\" algorithm\n");
	printf("the red square for the surface adaptation of the 4-Point Subdivision algorithm\n\n");
	printf("push enter to render the graphics objects");
	char c;
	scanf("%c",&c);

	glutInit(&argc, argv);
	glutInitDisplayMode (GLUT_DEPTH | GLUT_SINGLE | GLUT_RGB);
	glutInitWindowSize (Vx_max-Vx_min, Vy_max-Vy_min); 
	glutInitWindowPosition (100, 100);
	glutCreateWindow (argv[0]);

	init();

	glutDisplayFunc(display); 
	glutReshapeFunc(reshape);
	glutMouseFunc(mouse);
	glutMainLoop();

	delete control;
	delete original;
	for (int i=0;i<num_control_vertices;i++)
		delete originalSurface[i];
	delete originalSurface;
	for (i=0;i<num_control_vertices*pow(2,number_iterations);i++)
		delete controlSurface[i];
	delete controlSurface;

	return 0;
}

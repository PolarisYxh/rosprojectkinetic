#include <stdlib.h>
#include <iostream>
#include <math.h>
using namespace std;
const double PI=3.141592653;
int main(int argc, char** argv)
{
double r[3][3];
for(int i=0;i<3;i++)
{
    for(int j=0;j<3;j++)
{
    if(i*3+j+1<argc)
    {
        r[i][j]=strtod(argv[i*3+j+1],NULL);
    }
   
    else r[i][j]=0;
    cout<<r[i][j]<<" "<<endl;
}
}

double thetaz = atan2(r[2][1], r[1][1]);
double thetay = atan2(-1 * r[3][1], sqrt(r[3][2]*r[3][2] + r[3][3]*r[3][3]));
double thetax = atan2(r[3][2], r[3][3]);
cout<<"thetax:"<<thetax<<" "<<"thetay:"<<thetay<<" "<<"thetaz:"<<thetaz<<endl;
}
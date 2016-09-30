#include "nexper1.h"

/*
//use the following to test nexper()
#include <iostream.h>
#include "my_notation.h"

VOID	nexper(USHORT n, USHORT * a, BOOLEAN & more, USHORT & x, USHORT & y);
//******************************************
VOID	main(VOID)
{
	USHORT		n=3;
	USHORT		a[50];
	BOOLEAN		more=false;
	USHORT		x=0, y=0;
	USHORT		counter=1;
	
	do{
		nexper(n, a, more, x, y);
		cout<< '(' << counter << ')';
		for(USHORT	i=1; i<=n; i++){
			cout<< '\t' <<a[i-1]; //cout<< '\t' <<a[i];
		}
		cout<< '\n';
		counter++;
	}while(more);
}
*/
//******************************************
void	nexper(
unsigned short			n,		//in
unsigned short *		a,		//io
BOOLEAN	&		more,	//io
unsigned short	&		x,		//out
unsigned short	&		y)		//out	
{
	//nexper = next permutation
	//from pg 59 of the book by Nijenhuis and Wilf
	
	//n=number of elements being permuted
	//a[] =elements of {0, 1, 2, ...n-1} in a particular order 
	//more= whether there are more permutations coming
	//even = whether permutation is even
	//(x,y)= the single transposition (of a[] elements) executed by this method
	
	//must set "more" to false before FIRST call to nexper()
	
	//Original version is 1 based in its array indices 
	//and array entries. I changed it to zero based.
	
	static LONG 	nlast=0;
	static LONG		m, nf;
	static BOOLEAN	even; // static LONG v;
	LONG			j;
	
	if(n!=nlast){
		line30:
		nlast = n;
		nf=1;
		for(j=1; j<=n; j++){
			nf *= j;
			a[j-1] = j-1; //a[j]=j;
		}
		x=0; y=0;//I added this
		even = true; //v=1; //moved this for consistency
		m=1;//moved this for consistency
		more = (m!=nf);
		return;
	}
	
	if(!more) goto line30;
		
	LONG	t, h, m1, b, h1, m2, j1;
	if(even){ //v=1
		t=a[1];//t=a[2];
		a[1]=a[0];//a[2]=a[1];
		a[0]=t;//a[1]=t;
		x=a[0]; y=a[1];//I added this
		even = false; //v=2;
		m++;
		more = (m!=nf);
	}else{	//v=2
		h=3;
		m1=m/2;
		b=m1%h;
		while(b==0){
			m1=m1/h;
			h++;
			b=m1%h;
		}
		m1=n;
		h1=h-1;
		for(j=1;j<=h1;j++){
			m2=a[j-1]-a[h-1];//m2=a[j]-a[h];
			if(m2<0) m2 += n;
			if(m2<m1){
				m1=m2;
				j1=j;
		 	}
		}
		h--; j1--;//I added this
		t=a[h];
		a[h]=a[j1];
		a[j1]=t;
		x=a[h]; y=a[j1];//I added this
		even = true; //v=1;
		m++;
	}
}

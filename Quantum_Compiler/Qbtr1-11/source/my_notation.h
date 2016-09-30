# pragma once


#define VOID      void
//I won't use int
//#define INT       int 
#define SHORT     short		//16bits
#define LONG      long		//32bits
//#define USHORT    unsigned short
typedef	unsigned short	USHORT;
//#define ULONG     unsigned long
typedef	unsigned long	ULONG;
#define CHAR      char		//8bits
#define FLOAT     float		//32bits
//******************************************
//according to Universal Headers/Types.h
//double				64bits
//double_t=extended, fastest
//68K: 					80 bits
//68K with 68881: 		96 bits
//PowerPC:				64 bits
//#define DOUBLE	  double_t
#define DOUBLE	  double
//******************************************
/*
clapack, in f2c.h, defines
typedef double doublereal;
typedef struct { doublereal r, i; } doublecomplex;
*/
#define CLA_COMPLEX __CLPK_doublecomplex

//double_complex is defined in <complex> of the Plauger libarry
//#define COMPLEX  double_complex
//#define  COMPLEX   std::complex<double>
#define  COMPLEX   __CLPK_doublecomplex
#define  real()		r
#define  imag()		i
//******************************************
//according to Universal Headers/Types.h
//Boolean = unsigned char (8 bits)
//#define	BOOLEAN	  Boolean
#define	BOOLEAN	  bool

#define STREAMBUF streambuf
#define IOS       ios
#define OSTREAM   ostream
#define ISTREAM   istream
#define IOSTREAM  iostream
#define IFSTREAM  ifstream
#define OFSTREAM  ofstream



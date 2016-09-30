#include "clapack_needs.h"
//******************************************
CLA_COMPLEX  operator * (
const CLA_COMPLEX  &  	z1,			//in
const CLA_COMPLEX  &   	z2)			//in
{
	CLA_COMPLEX		z;
	z.real()= (z1.real())*(z2.real()) - (z1.imag())*(z2.imag());
	z.imag()= (z1.real())*(z2.imag()) + (z1.imag())*(z2.real());
	return z;
}
//******************************************
CLA_COMPLEX  operator + (
const CLA_COMPLEX  &  	z1,			//in
const CLA_COMPLEX  & 	z2)			//in
{
	CLA_COMPLEX		z;
	z.real()= z1.real()+ z2.real();
	z.imag()= z1.imag()+ z2.imag();
	return z;
}
//******************************************
CLA_COMPLEX  operator - (
const CLA_COMPLEX  &  	 z1,		//in
const CLA_COMPLEX  &     z2)		//in
{
	CLA_COMPLEX		z;
	z.real()= z1.real()- z2.real();
	z.imag()= z1.imag()- z2.imag();
	return z;
}
	

#include "Qbtr_global_funs.h"

#pragma mark --about angles--
//I always express angles
//in radians if hidden from the user,
//in degrees if visible to user.
//******************************************
VOID 	limited_degrees(
DOUBLE  &  ang)		//io
{
	//nan = not a number. See fp.h. isnan(x) is a global method.
	//if(isnan(ang))return;
	while(ang<0){ang +=360;}
	while(ang>360){ang -=360;}
	if(is_zero(ang-360)){ang = 0;}	
}
//******************************************
VOID 	limited_radians(
DOUBLE  &  ang)		//io
{
	//nan = not a number. See fp.h. isnan(x) is a global method.
	//if(isnan(ang))return;
	while(ang<0){ang += my_two_pi;}
	while(ang>my_two_pi){ang -= my_two_pi;}
	if(is_zero(ang - my_two_pi)){ang = 0;}
}
//******************************************
VOID 	limited_radians(
VECTOR<DOUBLE>  &  angles)	//io
{
	USHORT	len = angles.get_len();
	for(USHORT i=0; i<len; i++){
		limited_radians(angles[i]);
	}
}
//******************************************
VOID 	cs_to_radians(
const DOUBLE  &		c,	//in
const DOUBLE  & 	s,	//in
DOUBLE  &  	ang)		//out
{
/*
	if(s*s>1){
		cout << "supposed sine exceeded 1 in magnitude by " << sqrt(s*s-1) <<k_endline;
	}
	if(c*c>1){
		cout << "supposed cosine exceeded 1 in magnitude by " << sqrt(c*c-1) <<k_endline;
	}
*/
	ang = atan2(s, c);
	limited_radians(ang);
}
#pragma mark --pidgin i/o--
//******************************************
VOID	my_get(
IFSTREAM &	strm,	//io
CHAR  & 	ch)		//out
{		
	//With exceptions(failbit),
	//peek() will throw if eof()=true already
	
	//eof() first so peek() doesn't get a chance to throw
	if(strm.eof()||(strm.peek() == EOF)){
		throw END_OF_FILE();
	}else{
		strm.get(ch);
	}		
}
#pragma mark	--other--
//******************************************
VOID	change_sign(
DOUBLE	&	x)	//io
{
	x = -x;
}
//******************************************
BOOLEAN		is_zero(
const DOUBLE &		x,						//in
const DOUBLE & epsilon /*k_norm_delta*/) 	//in
{
	return (x > -epsilon  && x < epsilon);
}
//******************************************
USHORT	get_min(
const VECTOR<USHORT> &	vec)	//in		
{
	USHORT		min = max_ushort;
	USHORT		len = vec.get_len();
	for(USHORT	j=0; j<len; j++){		
		if(vec[j]<min) min=vec[j];
	}
	return min;
}
//******************************************
DOUBLE  my_factorial(
USHORT n)	//in
{
	DOUBLE	x;
	switch(n){
		case 0: x= 1; break;
		case 1: x= 1; break;
		case 2: x= 2; break;
		case 3: x= 6; break;
		case 4: x= 2.4e1; break;
		case 5: x= 1.2e2; break;
		case 6: x= 7.2e2; break;
		case 7: x= 5.04e3; break;
		case 8: x= 4.032e4; break;
		case 9: x= 3.6288e5; break;
		case 10: x= 3.6288e6; break;
		case 11: x= 3.99168e7; break;
		case 12: x= 4.790016e8; break;
		default:
			x= 4.790016e8;
			for(USHORT i=13; i<=n; i++){
				x *=i;
			}			
		break;
	}
	return x;
}
//******************************************
USHORT 		find_num_of_distinct_entries(
const VECTOR<DOUBLE> &		entries,			//in
VECTOR<USHORT> *			degens_p /*=0*/)	//io
{
	//We assume that entries are ordered monotonically.
	//If not, equal entries may be counted as different.
	USHORT	num_of_distincts = 0;
	USHORT	len = entries.get_len();
	DOUBLE	prev = entries[0];
	if(degens_p != 0) degens_p->set_to_default_vec(1/*default*/, len/*len*/);
	for(USHORT	i=1; i<len; i++){//start at 1		
		if(is_zero(prev - entries[i])){
			if(degens_p != 0){
				(*degens_p)[num_of_distincts]++;
			}
		}else{
			num_of_distincts++;
			prev = entries[i];
		}
	}
	num_of_distincts++;
	if(degens_p !=0)degens_p->resize(0, num_of_distincts);
	return	num_of_distincts;
}

#pragma mark --functions of complex numbers--
//******************************************
VOID	change_sign(
COMPLEX  &  z)	//io
{
	z.real()= -z.real();
	z.imag()= -z.imag();
}
//******************************************
DOUBLE		zmag(
const COMPLEX & 	z)	//in
{
	//mag = magnitude
	return sqrt(pow(z.real(), 2) + pow(z.imag(), 2));
}
//******************************************
BOOLEAN		is_zero(
const COMPLEX & 	z,						//in
const DOUBLE & epsilon /*k_norm_delta*/) 	//in
{
	return is_zero(zmag(z), epsilon);
}	

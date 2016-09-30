#include "STRINGY.h"
//#include <fp.h>

#pragma mark--creation/destruction--
//******************************************
VOID	STRINGY::clear()
{
	delete [] its_cstr;
	its_cstr = 0;
	its_len = 0;	
}
//******************************************
VOID	STRINGY::copy(
const STRINGY  &	s)		//in
{
	//s = source
	if(s.its_cstr == 0){
		its_len=0;
		its_cstr = 0;
	}else{
		its_len = s.its_len;
		its_cstr = new CHAR [its_len+1];//new[]
		ThrowIfNil_(its_cstr);	
		strcpy(its_cstr, s.its_cstr);
	}
}
//******************************************
STRINGY::STRINGY()
	:its_len(0)
{
	its_cstr = new  CHAR [1];//new[]
	ThrowIfNil_(its_cstr);
	its_cstr[0] = '\0';
}
//******************************************
STRINGY::STRINGY(
CHAR ch,			//in
USHORT len)			//in
	:its_len(len)
{
	//Creates a ch-filled stringy of length len.
	//See below, where this constructor is
	//used to define && for stringies.
	its_cstr = new  CHAR [len+1];//new[]
	ThrowIfNil_(its_cstr);
	for( USHORT i=0; i< len; i++){
		its_cstr[i] = ch;
	}
	its_cstr[len]='\0';
}
//******************************************
STRINGY::STRINGY(
const CHAR  *	cstr)	//in
{
	if(cstr==0){
		its_len=0;
		its_cstr=0;
	}else{
		its_len = strlen(cstr);
		its_cstr = new CHAR [its_len +1];//new[]
		ThrowIfNil_(its_cstr);
		strcpy(its_cstr, cstr);
	}
}
//******************************************
STRINGY::STRINGY(
SHORT i)		//in
{
	CHAR 	cstr[80];
	sprintf(cstr, "%i", i);
	its_len = strlen(cstr);
	its_cstr = new CHAR [its_len +1];//new[]
	ThrowIfNil_(its_cstr);
	strcpy(its_cstr, cstr);
}
//******************************************
STRINGY::STRINGY(
USHORT i)		//in
{
	CHAR 	cstr[80];
	sprintf(cstr, "%i", i);
	its_len = strlen(cstr);
	its_cstr = new CHAR [its_len +1];//new[]
	ThrowIfNil_(its_cstr);
	strcpy(its_cstr, cstr);
}
//******************************************
STRINGY::STRINGY(
LONG i)		//in
{
	CHAR 	cstr[80];
	sprintf(cstr, "%i", i);
	its_len = strlen(cstr);
	its_cstr = new CHAR [its_len +1];//new[]
	ThrowIfNil_(its_cstr);
	strcpy(its_cstr, cstr);
}
//******************************************
STRINGY::STRINGY(
DOUBLE x)		//in
{
	CHAR 	cstr[80];
	sprintf(cstr, "%f", x);
	its_len = strlen(cstr);
	its_cstr = new CHAR [its_len +1];//new[]
	ThrowIfNil_(its_cstr);
	strcpy(its_cstr, cstr);
}
//******************************************
STRINGY::STRINGY(
const STRINGY  &	s) 		//in
{
	copy(s);
}
//******************************************
STRINGY  & 	STRINGY::operator= (
const STRINGY  &	rhs)	//in
{
	if(this != &rhs){
		if(its_len == rhs.its_len){
			if(rhs.its_len==0){
				clear();
			}else{
				strcpy(its_cstr, rhs.its_cstr);
			}
		}else{
			clear();
			copy(rhs);
		}
	}
	return *this;
}
//******************************************
STRINGY::~STRINGY() 
{
	clear();
}
#pragma mark --cstr, len--
//******************************************
#ifndef		_do_inline
USHORT	STRINGY::get_len() const
{
	return its_len;
}
#endif
//******************************************
#ifndef		_do_inline
const CHAR  *  STRINGY::get_string() const
{
	return its_cstr;
}
#endif
//******************************************
STRINGY		STRINGY::get_sub_stringy(
USHORT	starting_pos,	//in
USHORT	sub_str_len)	//in
const 
{
	//starting_pos is zero based
	ThrowIf_(starting_pos + sub_str_len > its_len);
	STRINGY  sub_sgy('x', sub_str_len);
	for (USHORT i =0; i<sub_str_len; i++){
		sub_sgy[i] = its_cstr[i + starting_pos]; 
	}
	return sub_sgy;
}
#pragma mark--comparison--
//******************************************
BOOLEAN		operator==(
const STRINGY  &	s1,		//in	
const STRINGY  & 	s2)		//in
{
	if(s1.its_cstr == s2.its_cstr){
		 return true;
	}else{ //if they are not equal:
		if( (s1.its_cstr==0)||(s2.its_cstr==0) ){
			return false;
		}else{
			return ( strcmp(s1.its_cstr, s2.its_cstr)==0 );
		}
	}
}
//******************************************
#ifndef		_do_inline
BOOLEAN		operator!=(
const STRINGY  &	s1,		//in
const STRINGY  &	s2)		//in
{
	return !(s1==s2);
}
#endif
//******************************************
BOOLEAN		operator==(
const STRINGY  &	s,	//in
const CHAR  *	cstr)	//in
{
	if(s.its_cstr == cstr){
		 return true;
	}else{ //if they are not equal:
		if( (s.its_cstr==0)||(cstr==0) ){
			return false;
		}else{
			return ( strcmp(s.its_cstr, cstr)==0 );
		}
	}
}
//******************************************
#ifndef		_do_inline
BOOLEAN		operator!=(
const STRINGY  &	s,		//in
const CHAR  *		cstr)	//in
{
	return !(s==cstr);
}
#endif
//******************************************
BOOLEAN		operator==(
const CHAR  *	cstr,		//in		
const STRINGY  &	s)		//in
{
	if(cstr == s.its_cstr){
		 return true;
	}else{ //if they are not equal:
		if( (cstr==0)||(s.its_cstr==0) ){
			return false;
		}else{
			return ( strcmp(cstr, s.its_cstr)==0 );
		}
	}
}
//******************************************
#ifndef		_do_inline
BOOLEAN		operator!=(
const CHAR  *		cstr,	//in
const STRINGY  & 	s)		//in
{
	return !(cstr==s);
}
#endif
//******************************************
BOOLEAN		operator<(
const STRINGY  &	s1,		//in
const STRINGY  &	s2)		//in
{
	if(s1.its_cstr == s2.its_cstr){
		return false;
	}else if(s1.its_cstr == 0){
		return true;
	}else if(s2.its_cstr == 0){
		return false;
	}else{
		return ( strcmp(s1.its_cstr , s2.its_cstr) < 0 );
	}
}
#pragma mark	--subscripting--
//******************************************
#ifndef		_do_inline
CHAR  &		STRINGY::operator[](
USHORT i)		//in
{
	//Returns alias to the ith character of a stringy so that 
	//the ith character can be changed.
	ThrowIf_(i >= its_len);
	return its_cstr[i];
}
#endif
//******************************************
#ifndef		_do_inline
const CHAR  & STRINGY::operator[](
USHORT 	i)		//in
const 
{
	//Constant function that returns a constant alias to 
	//the ith character of a stringy.
	//For use on constant objects. See, for example, the copy constructor.
	ThrowIf_(i >= its_len);
	return its_cstr[i];
}
#endif
#pragma mark--concatenation--
//******************************************
STRINGY		STRINGY::operator &&(
const STRINGY  &	rhs)		//in
{
	//concatenates two stringies.
	if(its_cstr==0){
		return rhs;
	}else{ //if its_cstr!=0:
		if(rhs==0){
			return *this;
		}else{//if its_cstr and rhs are both non-zero:
			USHORT tot_len = its_len + rhs.its_len;
			STRINGY temp('a', tot_len);	//temp = temporary
			strcpy(temp.its_cstr, its_cstr);
			strcat(temp.its_cstr, rhs.its_cstr);
			return temp;
		}
	}
}
#pragma mark--i/o--
//******************************************
OSTREAM  &		operator<<(
OSTREAM  &		out_bd,		//io
const STRINGY  &	s)		//in
{
	//Stream output. This also works for a file, 
	//since an fstream is an ostream. 
	out_bd << s.its_cstr;
	return out_bd;
}
//******************************************
ISTREAM  &		operator>> (
ISTREAM  &	in_bd,		//io
STRINGY  &	s) 			//in
{ 
	//Stream input. This works also for a file, 
	//since an fstream is an istream. 
	CHAR 	cstr[STRINGY::stringy_max_len + 1];
	in_bd >> cstr; 
	delete []  s.its_cstr;
	s.its_len= strlen(cstr);
	s.its_cstr = new CHAR [s.its_len +1];//new[]
	ThrowIfNil_(s.its_cstr);

	strcpy(s.its_cstr, cstr);
	return in_bd;
}
//******************************************
ISTREAM  &		STRINGY::copy_line(
ISTREAM  &	in_bd,		//io
USHORT	max_len,		//in
CHAR	stop_char)		//in
{
	//usually stop_char = endline

	//This member function for STRINGY acts like 
	//the "getline" member function for ISTREAM.
	//Both transfer a string from an istream object to something else
	//(a stringy and a character array, respectively).
	//This also works for a file, as an fstream is an istream.
	CHAR 	cstr[stringy_max_len + 1];
	in_bd.getline(
		cstr,
		(stringy_max_len < max_len)? stringy_max_len : max_len,
		stop_char
	);
	delete [] its_cstr;
	its_len=strlen(cstr);
	its_cstr = new CHAR [its_len +1];//new[]
	ThrowIfNil_(its_cstr);

	strcpy(its_cstr, cstr);
	return in_bd;
}
//******************************************




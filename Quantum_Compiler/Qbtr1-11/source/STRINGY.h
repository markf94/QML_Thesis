#pragma once
#include "prefix2.h"

#include <string.h>
#include <iostream>
#include <fstream>

class STRINGY
{
private:
	CHAR  *  	its_cstr;
	USHORT 		its_len;   
	//len = length. 
	//"its_len"  does NOT include the \0 termination character.

public:
	enum {stringy_max_len = 255};//256 once include termination char
	
	VOID clear();
	VOID copy(const STRINGY  & s);	
    STRINGY();
	STRINGY(CHAR ch, USHORT len);
	STRINGY(const CHAR  * cstr);
	STRINGY(SHORT i);
	STRINGY(USHORT i);
	STRINGY(LONG i);
	STRINGY(DOUBLE x);
	STRINGY(const STRINGY  & s);
	STRINGY  & operator= (const STRINGY  & rhs);
	virtual ~STRINGY();
	
	USHORT 			get_len() const;
	const CHAR  *  	get_string() const;
	STRINGY			get_sub_stringy(USHORT	starting_pos, USHORT sub_str_len) const;

	friend BOOLEAN operator==(const STRINGY  & s1, const STRINGY  & s2);
	friend BOOLEAN operator!=(const STRINGY  & s1, const STRINGY  & s2);
	
	friend BOOLEAN operator==(const STRINGY  & s, const CHAR  * cstr);
	friend BOOLEAN operator!=(const STRINGY  & s, const CHAR  * cstr);
	
	friend BOOLEAN operator==(const CHAR  * cstr, const STRINGY  & s);	
	friend BOOLEAN operator!=(const CHAR  * cstr, const STRINGY  & s);
			
	friend BOOLEAN operator<(const STRINGY  & s1, const STRINGY  & s2);	
		
	CHAR  & operator[] (USHORT i);  
	const CHAR  &  operator[] (USHORT i) const;
	
 	STRINGY operator &&(const STRINGY  & rhs);
 	 
	friend OSTREAM  & operator<<( OSTREAM  & out_bd, const STRINGY  & s);		
	friend ISTREAM  & operator>>( ISTREAM  & in_bd, STRINGY  &  s);
	ISTREAM  & copy_line(ISTREAM  & in_bd, USHORT max_len, CHAR stop_char);
		
};
#ifdef	_do_inline
//******************************************
inline
USHORT	STRINGY::get_len() const
{
	return its_len;
}
//******************************************
inline
const CHAR  *  STRINGY::get_string() const
{
	return its_cstr;
}
//******************************************
inline
BOOLEAN		operator!=(
const STRINGY  &	s1,		//in
const STRINGY  &	s2)		//in
{
	return !(s1==s2);
}
//******************************************
inline
BOOLEAN		operator!=(
const STRINGY  &	s,		//in
const CHAR  *		cstr)	//in
{
	return !(s==cstr);
}
//******************************************
inline
BOOLEAN		operator!=(
const CHAR  *		cstr,	//in
const STRINGY  & 	s)		//in
{
	return !(cstr==s);
}
//******************************************
inline
CHAR  &		STRINGY::operator[](
USHORT i)		//in
{
	//Returns alias to the ith character of a stringy so that 
	//the ith character can be changed.
	ThrowIf_(i >= its_len);
	return its_cstr[i];
}
//******************************************
inline
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

#endif	//inlines

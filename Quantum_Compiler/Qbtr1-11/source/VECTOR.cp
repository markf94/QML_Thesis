#include "VECTOR.h"
#pragma mark	--creation/destruction--
//******************************************
template<class TYPE>
VOID   VECTOR<TYPE>::clear( )
{
	delete [] its_array_p;
	its_array_p=0;
	its_len=0;
}
//******************************************
template<class TYPE>
VOID   VECTOR<TYPE>::copy(
const VECTOR<TYPE>  &  s)		//in
{
	 //s = source
	its_len = s.its_len;
	if(its_len==0){
		its_array_p = 0;
	}else{
		its_array_p = new TYPE [its_len];//new[]
		ThrowIfNil_(its_array_p);
		//delete:	I delete its_array_p in ~VECTOR().		
		for(USHORT i=0; i<its_len; i++){
			its_array_p[i] = s[i];
		}
	}
}
//******************************************
template<class TYPE>
VOID   VECTOR<TYPE>::set_to_default_vec(
const TYPE  & default_value,		//in
USHORT len )						//in
{
	if(its_len == len){
		for(USHORT i=0; i<len; i++){
			its_array_p[i] = default_value;
		}
	}else{		
		delete [] its_array_p;
		if(len==0){
			its_array_p = 0;
		}else{
			its_array_p= new TYPE [len];//new[]
			ThrowIfNil_(its_array_p);
		
			for(USHORT i=0; i<len; i++){
				its_array_p[i] = default_value;
			}
		}		
		its_len = len;
	}
}
//******************************************
template<class TYPE>
VOID   VECTOR<TYPE>::resize(
const TYPE  & default_value,	//in
USHORT new_len )				//in
{
	if(new_len == its_len)return;
	if(new_len==0){
		clear();
		return;
	}
	TYPE  * new_array_p= new TYPE [new_len];//new[]
	ThrowIfNil_(new_array_p);

	USHORT i;
	if(its_len < new_len){
		for(i=0; i<its_len; i++){
			new_array_p[i] = its_array_p[i];
		}
		for(i=its_len; i < new_len; i++){
			new_array_p[i] = default_value;
		}
	}else{
		for(i=0; i<new_len; i++){
			new_array_p[i] = its_array_p[i];
		}
	}
	delete [] its_array_p;
	its_array_p = new_array_p;
	its_len = new_len;
}
//******************************************
template<class TYPE>
VECTOR<TYPE>::VECTOR()
	:its_array_p(0),
	its_len(0)
{}
//******************************************
template<class TYPE>
VECTOR<TYPE>::VECTOR(
const TYPE  &	default_value,	//in
USHORT		len)				//in
	:its_array_p(0),
	its_len(0)
{
	set_to_default_vec(default_value, len);
}
//******************************************
template<class TYPE>
VECTOR<TYPE>::VECTOR(
const  VECTOR<TYPE>  &	 s)		//in	
{
	copy(s);
}
//******************************************
template<class TYPE>
VECTOR<TYPE>  & 	VECTOR<TYPE>::operator=(
const VECTOR<TYPE>  &	rhs)	//in 
{
	//rhs = right hand side 
	if(this != &rhs){
		if(its_len == rhs.its_len){
			for(USHORT i= 0; i<its_len; i++){
				its_array_p[i] = rhs[i];
			}		
		}else{	
			clear();
			copy(rhs);
		}
	}
	return *this;
}
//******************************************
template<class TYPE>
VECTOR<TYPE>::~VECTOR()
{
	clear();
}
#pragma mark	--simple accessors--
//******************************************
#ifndef		_do_inline
template<class TYPE>
USHORT  VECTOR<TYPE>::get_len() const
{
	return  its_len;
}		
#endif
//******************************************
template<class TYPE>
USHORT   VECTOR<TYPE>::loc_of_target(
const TYPE  &  tar)		//in
const 
{
	if(its_len == 0) return max_ushort;
	USHORT loc = max_ushort; 
	for(USHORT i=0; i< its_len; i++){
		if( its_array_p[i] == tar){
			loc=i;
			break;
		}
	}
	return loc;
}
//******************************************
template<class TYPE>
TYPE  &  VECTOR<TYPE>::operator[](
USHORT i)		//in
const
{
	ThrowIf_(i>=its_len);
	return its_array_p[i];
}

#pragma mark --vector friends--
#pragma mark --comparison--
//******************************************
template<class TYPE>
BOOLEAN		operator==(
const  VECTOR<TYPE>  & 	s1,		//in	
const  VECTOR<TYPE>  &  s2)		//in
{

	if(s1.its_len != s2.its_len)return false;
	USHORT len = s1.its_len;
	for(USHORT i=0; i<len; i++){
		if(s1.its_array_p[i] != s2.its_array_p[i])return false;
	}
	return true;
}
//******************************************
template<class TYPE>
BOOLEAN		operator!=(
const  	VECTOR<TYPE>  &		s1,		//in
const	VECTOR<TYPE>  &		s2)		//in
{
	return !(s1==s2);
}		
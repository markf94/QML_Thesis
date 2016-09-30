#include "L_LIST.h"
#pragma mark	--DIR_DATA<TYPE>--
//******************************************
template<class TYPE>
DIR_DATA<TYPE>::DIR_DATA()
	:its_next_p(0)
{}
//******************************************
template<class TYPE>
DIR_DATA<TYPE>::DIR_DATA(
const TYPE  &		data,		//in
DIR_DATA<TYPE>  *	next_p)		//in
 	:its_data(data),
 	its_next_p(next_p)
{}
//******************************************
template<class TYPE>
DIR_DATA<TYPE>::DIR_DATA(
const DIR_DATA<TYPE>  &		source)		//in
	:its_data(source.its_data),
	its_next_p(0)
{}
#pragma mark	--L_LIST<TYPE>--

#pragma mark 	--creation/destruction--		
//******************************************
template<class TYPE>
VOID   L_LIST<TYPE>::clear( )
{
	DIR_DATA<TYPE>  *  x_p = its_first_p;
	while(x_p) {
		x_p =   its_first_p->its_next_p;
		delete  its_first_p;
		its_first_p = x_p;
	}
	its_first_p = 0;
	its_last_p = 0;
	its_len = 0;
}
//******************************************
template<class TYPE>
VOID   L_LIST<TYPE>::copy(
const L_LIST<TYPE>  &  prev_list)		//in
{
	its_len = prev_list.its_len;
	if(its_len==0){
		its_first_p = 0;
		its_last_p = 0;
		return;
	}
	DIR_DATA<TYPE>  *  x_p  =  prev_list.its_first_p;
	
	DIR_DATA<TYPE>  *  new_x_p = new DIR_DATA<TYPE>(x_p->its_data, 0);
	ThrowIfNil_(new_x_p);
	//delete:	I delete new_x_p via ~L_LIST()->L_LIST()::clear(). 
	//			See also L_LIST()::extract_xxx() methods.	
	its_first_p = new_x_p;    
	its_last_p= new_x_p;
	x_p  =  x_p->its_next_p;	
	while(x_p) {
		new_x_p = new DIR_DATA<TYPE>(x_p->its_data, 0);
		ThrowIfNil_(new_x_p);
		//delete:	I delete new_x_p via ~L_LIST()->L_LIST()::clear().
		//			See also L_LIST()::extract_xxx() methods.		  
		its_last_p->its_next_p  = new_x_p;
		its_last_p  = new_x_p;			
		x_p  =  x_p->its_next_p;
	}
}
//******************************************
template<class TYPE>
L_LIST<TYPE>::L_LIST()
	:its_first_p(0),
	its_last_p(0),
	its_len(0)
{}
//******************************************
template<class TYPE>
L_LIST<TYPE>::L_LIST(
const  L_LIST<TYPE>  &	s ) //in
{
	//s = source
	copy(s);
}
//******************************************
template<class TYPE>
L_LIST<TYPE>  &		L_LIST<TYPE>::operator=(
const L_LIST<TYPE>  &	rhs)	//in
{
	//rhs = right hand side
	if(this != &rhs) {
		clear();
		copy(rhs);
	}
	return *this;
}
//******************************************
template<class TYPE>
L_LIST<TYPE>::~L_LIST()
{
	clear();
}
#pragma mark	--simple accessors--
//******************************************
#ifndef		_do_inline
template<class TYPE>
DIR_DATA<TYPE>  *   L_LIST<TYPE>::get_first_p() const
{
	return  its_first_p;
}
#endif
//******************************************
#ifndef		_do_inline
template<class TYPE>
DIR_DATA<TYPE>  *   L_LIST<TYPE>::get_last_p() const
{
	return  its_last_p;
}
#endif
//******************************************
#ifndef		_do_inline
template<class TYPE>
const USHORT  L_LIST<TYPE>::get_len() const
{
	return  its_len;
}		
#endif

//******************************************
template<class TYPE> 
BOOLEAN		L_LIST<TYPE>::has_this(
const TYPE  & target)		//in
const
{
	DIR_DATA<TYPE>  *  x_p = its_first_p;
	if(x_p==0)return false;
	while(x_p->its_data != target){
		x_p = x_p->its_next_p;
		if(x_p==0)return false;
	}
	return true;
}
//******************************************
template<class TYPE>
TYPE  &    L_LIST<TYPE>::operator[] (
USHORT loc)		//in
const
{
	//0 based indexing
	//assume that its_len>0
	if(loc >= its_len)loc=its_len-1;
	DIR_DATA<TYPE>  *  x_p = its_first_p;
	for(USHORT i=0; i < loc; i++){
		x_p = x_p->its_next_p;
	}
	return x_p->its_data;
}

#pragma mark--insert an element--
//******************************************
template<class TYPE>
VOID	L_LIST<TYPE>::insert_first(
const TYPE  & data)		//in
{
	DIR_DATA<TYPE>  *  x_p = new DIR_DATA<TYPE>(data, its_first_p);
	ThrowIfNil_(x_p);
	//delete:	I delete x_p via ~L_LIST()->L_LIST()::clear().
	//			See also L_LIST()::extract_xxx() methods.		 
	its_len++;
	if(its_first_p == 0){ 
		its_first_p = x_p;
		its_last_p = x_p;
	}else{
		its_first_p = x_p;
	}
}
//******************************************
template<class TYPE>
VOID	L_LIST<TYPE>::insert_last(
const TYPE  & data)		//in
{
	DIR_DATA<TYPE>  *  x_p = new DIR_DATA<TYPE>(data, 0);
	ThrowIfNil_(x_p);
	//delete:	I delete x_p via ~L_LIST()->L_LIST()::clear().
	//			See also L_LIST()::extract_xxx() methods.	  
	its_len++;
	if(its_first_p == 0){ 
		its_first_p = x_p;
		its_last_p = x_p;
	}else{
		its_last_p->its_next_p = x_p;
		its_last_p = x_p;
	}
}
#pragma mark	--extract an element--
//******************************************
template<class TYPE>
BOOLEAN		L_LIST<TYPE>::extract_first(
TYPE  & 	data)		//out
{
	if(its_first_p == 0) return false;
	its_len--;
	data = its_first_p->its_data;
	DIR_DATA<TYPE>  *  x_p  = its_first_p->its_next_p;
	delete  its_first_p;
	its_first_p = x_p;
	if(its_first_p == 0) its_last_p = 0;
	return true;
}
//******************************************
template<class TYPE>
BOOLEAN		L_LIST<TYPE>::extract_first()
{
	if(its_first_p == 0) return false;
	its_len--;
	DIR_DATA<TYPE>  *  x_p  = its_first_p->its_next_p;
	delete  its_first_p;
	its_first_p = x_p;
	if(its_first_p == 0) its_last_p = 0;
	return true;
}
//******************************************
template<class TYPE> 
BOOLEAN		L_LIST<TYPE>::extract_last()
{
	if(its_len == 0) return false;
	if(its_len==1){
		delete its_last_p;	
		its_last_p=0;
		its_first_p=0;
		its_len=0;
		return true;
	}	
	DIR_DATA<TYPE>  *  x_p = its_first_p;
	DIR_DATA<TYPE>  *  pre_x_p = its_first_p;
	while(x_p != its_last_p){
		pre_x_p = x_p;
		x_p = x_p->its_next_p;
	}
	pre_x_p->its_next_p =0;
	delete its_last_p;
	its_last_p = pre_x_p;
	its_len--;
	return true;
}
//******************************************
template<class TYPE> 
BOOLEAN		L_LIST<TYPE>::extract_target(
const TYPE  & target)	//in
{
	DIR_DATA<TYPE>  *  x_p = its_first_p;
	DIR_DATA<TYPE>  *  pre_x_p = its_first_p;
	while(x_p->its_data != target){
		pre_x_p = x_p;
		x_p = x_p->its_next_p;
		if(x_p==0)return false;
	}
	if(x_p==its_first_p) return extract_first();
	if(x_p==its_last_p) return extract_last();
	pre_x_p->its_next_p = x_p->its_next_p;
	delete x_p;
	x_p = 0;
	its_len--;
	return true;
}
//******************************************
template<class TYPE> 
BOOLEAN		L_LIST<TYPE>::extract_target(
DIR_DATA<TYPE>  * target_p)		//in
{
	if(target_p==its_first_p){
		target_p=0;
		return extract_first();
	}
	if(target_p==its_last_p){
		target_p=0;
		return extract_last();
	}

	DIR_DATA<TYPE>  *  x_p = its_first_p;
	DIR_DATA<TYPE>  *  pre_x_p = its_first_p;
	while(x_p != target_p){
		pre_x_p = x_p;
		x_p = x_p->its_next_p;
		if(x_p==0)return false;
	}
	pre_x_p->its_next_p = x_p->its_next_p;
	delete x_p;
	x_p = 0;
	target_p=0;
	its_len--;
	return true;
}

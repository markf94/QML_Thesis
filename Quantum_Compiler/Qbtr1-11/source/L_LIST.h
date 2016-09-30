#pragma once
#include "prefix2.h"

//******************************************
template<class TYPE>
class DIR_DATA  //dir_data = directed data
{
public:
	TYPE				its_data;
	DIR_DATA<TYPE>  * 	its_next_p;
	
	DIR_DATA();
 	DIR_DATA(const TYPE  & data, DIR_DATA<TYPE>  * next_p);
	DIR_DATA(const DIR_DATA<TYPE>  & source);		
};
//******************************************
template<class TYPE>
class L_LIST
{   
private:
	DIR_DATA<TYPE>  * 	its_first_p;
  	DIR_DATA<TYPE>  * 	its_last_p;
  	USHORT 				its_len;  //len = length
public:
	VOID clear();
	VOID copy(const L_LIST<TYPE>  &  prev_list);	
	L_LIST();
	L_LIST(  const  L_LIST<TYPE>  &  s );
	L_LIST<TYPE>  &  operator=( const L_LIST<TYPE>  & rhs);
	virtual ~L_LIST();

	DIR_DATA<TYPE>  *   get_first_p() const;
	DIR_DATA<TYPE>  *   get_last_p() const;
	const USHORT		get_len() const;	
	BOOLEAN  has_this( const TYPE  & target) const;
	TYPE  &   operator[] (USHORT loc) const;

	VOID	insert_first(const TYPE  & data);
	VOID	insert_last(const TYPE  & data);
	
	BOOLEAN		extract_first(TYPE  & data);
	BOOLEAN		extract_first();	
	BOOLEAN		extract_last();
	BOOLEAN		extract_target( const TYPE  & target);
	BOOLEAN		extract_target( DIR_DATA<TYPE>  * target_p);	
};	
#ifdef	_do_inline
//******************************************
template<class TYPE>
inline
DIR_DATA<TYPE>  *   L_LIST<TYPE>::get_first_p() const
{
	return  its_first_p;
}
//******************************************
template<class TYPE>
inline
DIR_DATA<TYPE>  *   L_LIST<TYPE>::get_last_p() const
{
	return  its_last_p;
}
//******************************************
template<class TYPE>
inline
const USHORT  L_LIST<TYPE>::get_len() const
{
	return  its_len;
}		
#endif	//inlines
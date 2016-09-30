#pragma once
#include "prefix2.h"

#include "Qbtr_globals.h"

//forward class declaration of template
template<class TYPE> class VECTOR; 
//forward function declaration of friend  to be
template<class TYPE> BOOLEAN	operator!=(const  VECTOR<TYPE>  & s1, const VECTOR<TYPE>  &  s2);
template<class TYPE> BOOLEAN	operator==(const  VECTOR<TYPE>  & s1, const VECTOR<TYPE>  &  s2);

//******************************************
template<class TYPE>
class VECTOR
{   
protected:
	TYPE  *		its_array_p;
  	USHORT		its_len;  //len = length
public:
	VOID	clear();
	VOID	copy(const VECTOR<TYPE>  &  s);
	VOID	set_to_default_vec(const TYPE  & default_value, USHORT len);
	VOID	resize(const TYPE  & default_value, USHORT new_len);	
	VECTOR();
	VECTOR(const TYPE  & default_value, USHORT len);
	VECTOR(const  VECTOR<TYPE>  &  s);
	VECTOR<TYPE>  &		operator=(const VECTOR<TYPE>  & rhs);
	virtual ~VECTOR();
	
	USHORT  get_len() const;			
	USHORT  loc_of_target(const TYPE  &  tar) const; 
	TYPE  & operator[](USHORT i) const;
	
	friend BOOLEAN	operator==<TYPE>(const  VECTOR<TYPE>  & s1, const VECTOR<TYPE>  &  s2);
	friend BOOLEAN	operator!=<TYPE>(const  VECTOR<TYPE>  & s1, const VECTOR<TYPE>  &  s2);
};

#ifdef	_do_inline
//******************************************
template<class TYPE>
inline
USHORT  VECTOR<TYPE>::get_len() const
{
	return  its_len;
}		
#endif	//inlines


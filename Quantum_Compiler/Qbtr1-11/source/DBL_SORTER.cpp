#include "DBL_SORTER.h"
#include "Qbtr_global_funs.h"

#pragma mark --creation/destruction
//******************************************
DBL_SORTER::DBL_SORTER(
VECTOR<DOUBLE> * vec_p,
BOOLEAN		want_increasing /*= true*/)
: its_vec_p(vec_p),
its_want_increasing(want_increasing)
{
}
#pragma mark --sorting--
//******************************************
BOOLEAN		DBL_SORTER::a_is_less_than_b(
USHORT		i,	//in
USHORT		j)	//in
const
{
	DOUBLE		diff = (*its_vec_p)[j] - (*its_vec_p)[i];
	BOOLEAN		answer;
	
	if(is_zero(diff)){
		//using is_zero() should avoid a lot of unnecessary reorderings
		answer = false;
	}else if( (diff<0 && its_want_increasing) || (diff>0 && !its_want_increasing)){
		answer = false;
	}else{
		answer = true;
	}
	
	return 	answer;		 
}
//******************************************
VOID	DBL_SORTER::sort(
PERMUTATION  & 	pmut)	//out
{
	USHORT	len = its_vec_p->get_len();
	ThrowIf_(len != pmut.get_len());
	USHORT		k;

	USHORT * 	ids_p = 	new USHORT [len];
	DOUBLE * 	arr_p = 	new DOUBLE [len];
	
	for(k = 0; k<len; k++){
		ids_p[k] = k;
		arr_p[k] = (*its_vec_p)[k];	
	}

	//------------------------------------------
	//Ascending indirect shell sort.
	//Comes from page 235 of Practical Algorithms in C++ by Flamig.

  	USHORT 	temp_id;
  	USHORT  i, j, h;

	for (h = len; h > 1;) { 
   		if(h<5){
   			h= 1;
   		}else{
   			h = (5*h-1)/11;
   		}
    	// Perform insertion sort with increment h
    	for(i = h; i < len; i++) {
     	 	temp_id = ids_p[i];
      		j = i;
      		while(j >= h && a_is_less_than_b(temp_id, ids_p[j-h])) {
        		ids_p[j] = ids_p[j-h];
        		j = j-h;
      		}
      		ids_p[j] = temp_id;
    	}
  	}
	//------------------------------------------

	for(k = 0; k<len; k++){
		pmut[k] = ids_p[k];
		(*its_vec_p)[ids_p[k]] = arr_p[k];
	}
	
	delete [] ids_p;
	delete [] arr_p;
} 





#pragma	once
#include "prefix2.h"

#include "PERMUTATION.h"

class DBL_SORTER
{
private: 
	VECTOR<DOUBLE> *	its_vec_p;
	BOOLEAN				its_want_increasing;
public:
	DBL_SORTER(VECTOR<DOUBLE> * vec_p, BOOLEAN  want_increasing = true );
	BOOLEAN		a_is_less_than_b(USHORT  i, USHORT j)const;
	VOID		sort(PERMUTATION  & pmut); 
};

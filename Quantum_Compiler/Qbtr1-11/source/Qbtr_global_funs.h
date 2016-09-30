#pragma once
#include "prefix2.h"

#include "VECTOR.h"
#include "Qbtr_globals.h"

class END_OF_FILE {};

//global functions(their prototypes):
VOID		limited_degrees(DOUBLE  & ang);
VOID		limited_radians(DOUBLE  & ang);
VOID		limited_radians(VECTOR<DOUBLE>  & ang);
VOID 		cs_to_radians(const DOUBLE  &  c, const DOUBLE  &  s, DOUBLE  &  ang);

VOID		my_get(IFSTREAM & strm, CHAR  & ch);

VOID		change_sign(DOUBLE	&	x);
BOOLEAN		is_zero(const DOUBLE &	x, const DOUBLE & epsilon = k_norm_delta);
USHORT		get_min(const VECTOR<USHORT> &	vec);
DOUBLE  	my_factorial(USHORT n);
USHORT 		find_num_of_distinct_entries(const VECTOR<DOUBLE> & entries,
				VECTOR<USHORT> * degens_p = 0);


VOID		change_sign(COMPLEX  &  z);
DOUBLE		zmag(const COMPLEX &  z);
BOOLEAN		is_zero(const COMPLEX &  z, const DOUBLE & epsilon = k_norm_delta);
	



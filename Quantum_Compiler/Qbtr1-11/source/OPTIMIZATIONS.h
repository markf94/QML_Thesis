#pragma once
#include "prefix2.h"

class OPTIMIZATIONS
{
public:
	static BOOLEAN  its_lighten_right_mats;
	static BOOLEAN  its_extract_d_mat_phases;	
	static USHORT	its_pmut_opt_level;
};

#define		_do_lazy_if_central_mat_not_diagonal		1
#define		_do_lazy_if_central_mat_diagonal			1
#pragma once
#include "prefix2.h"

class PERMUTATION;
//w_spec = write specifications
//strm = stream
//engl = english
//pict = picture
//pmut = permutation
struct W_SPEC{
	OFSTREAM  *		its_engl_strm_p;
	OFSTREAM  *		its_pict_strm_p;
	PERMUTATION	 *  its_pmut_p;
};

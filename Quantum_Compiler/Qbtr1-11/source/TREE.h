#pragma once
#include "prefix2.h"

//rt_nd = root node
//cum = cummulative
//cum_num_of_elem_ops = cummulative number of elementary operations

#include "W_SPEC.h"
class	NODE;
class	UNITARY_MAT;

//******************************************
class TREE
{
private:
	static USHORT	its_full_num_of_bits;
	static DOUBLE	its_cum_phase; //in radians
	NODE  *			its_rt_nd_p;
	
public:
	TREE(UNITARY_MAT * init_unitary_mat_p, BOOLEAN destroy_init_unitary_mat);
	~TREE();
	
	static USHORT  				get_full_num_of_bits();
	static VOID  				add_to_cum_phase(const DOUBLE  &  delta);

	VOID	write(W_SPEC &  w_spec);
	VOID	write_num_of_bits(W_SPEC &  w_spec);		
	VOID	write_cum_phase(W_SPEC &  w_spec);
	VOID	write_cum_num_of_elem_ops(W_SPEC &  w_spec);	
};

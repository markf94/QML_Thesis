#pragma once
#include "prefix2.h"

//mat = matrix
//nd = node
//pa = parent

class CENTRAL_MAT;
class UNITARY_MAT;
#include "PERMUTATION.h"
#include "Qbtr_globals.h"
#include "W_SPEC.h"

//******************************************
class NODE
{
private:

//	NODE  *					its_left_nd_p;
//	NODE  * 				its_right_nd_p;

	//level = 1 for root node
	//level = full_num_of_bits + 1 for node whose central_mat is diagonal unitary.
	USHORT					its_level;
	
	//cum_pmut = cummulative permutation
	PERMUTATION  			its_pmut;
	PERMUTATION				its_cum_pmut;
	
	CENTRAL_MAT  *	  		its_central_mat_p;	
	USHORT					its_num_of_left_mats;
	UNITARY_MAT  *  *		its_left_mats_p_p;
	UNITARY_MAT  *  *		its_right_mats_p_p;	


	VOID	allocate_side_mats();
	VOID	delete_side_mats();
	BOOLEAN	fill_side_mat(USHORT pj, UNITARY_MAT * *  pa_side_mats_p_p);
	VOID	private_init(UNITARY_MAT * *  pa_side_mats_p_p);

public:	
	NODE  *					its_left_nd_p;
	NODE  * 				its_right_nd_p;

//	VOID	allocate_side_mats();
//	VOID	delete_side_mats();
//	BOOLEAN	fill_side_mat(USHORT pj, UNITARY_MAT * *  pa_side_mats_p_p);
//	VOID	private_init(UNITARY_MAT * *  pa_side_mats_p_p);
	NODE(UNITARY_MAT  *	 init_unitary_mat_p, BOOLEAN destroy_init_unitary_mat);
	NODE(NODE  &  pa_nd, SIDE  pa_side);
	~NODE();
	
	BOOLEAN		is_a_final_node_of_the_tree();
	
	VOID		write(W_SPEC &  w_spec);		
};	

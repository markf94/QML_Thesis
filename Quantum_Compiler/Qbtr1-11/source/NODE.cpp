#include "NODE.h"
#include "CENTRAL_MAT.h"
#include "UNITARY_MAT.h"
#include "TREE.h"
#include "OPTIMIZATIONS.h"
#include "Qbtr_global_funs.h"
#include "D_MAT.h"

#pragma mark	--creation/destruction--
//******************************************
VOID	NODE::allocate_side_mats()
{
	USHORT	num_of_bits_in_a_left_mat = TREE::get_full_num_of_bits() - its_level;	
	its_left_mats_p_p	= new UNITARY_MAT  * [its_num_of_left_mats];
	its_right_mats_p_p	= new UNITARY_MAT  * [its_num_of_left_mats];
	for(USHORT j=0; j<its_num_of_left_mats; j++){
		its_left_mats_p_p[j] = new UNITARY_MAT(num_of_bits_in_a_left_mat);
		its_right_mats_p_p[j] = new UNITARY_MAT(num_of_bits_in_a_left_mat);
	}
}
//******************************************
VOID	NODE::delete_side_mats()
{
	USHORT	j;
	if(its_left_mats_p_p!=0){
		for(j=0; j<its_num_of_left_mats; j++){
			delete its_left_mats_p_p[j];
			its_left_mats_p_p[j]=0;
		}
		delete [] its_left_mats_p_p;
		its_left_mats_p_p=0;
	}
	if(its_right_mats_p_p!=0){
		for(j=0; j<its_num_of_left_mats; j++){
			delete its_right_mats_p_p[j];
			its_right_mats_p_p[j]=0;
		}
		delete [] its_right_mats_p_p;
		its_right_mats_p_p=0;
	}
}
//******************************************
BOOLEAN		NODE::fill_side_mat(
USHORT				pj,						//in
UNITARY_MAT * *  	pa_side_mats_p_p)		//in
{
	//pa_side_mats = parent side matrices
	//pj will be used as the index for pa_side_mats
	USHORT		j = 2*pj;
	D_MAT * 	d_mat_p = &its_central_mat_p->get_d_mat(pj);
	if(OPTIMIZATIONS::its_extract_d_mat_phases){
		if(pa_side_mats_p_p[pj]->is_d_mat(d_mat_p)){
			its_left_mats_p_p[j]->set_to_identity();
			its_left_mats_p_p[j+1]->set_to_identity();
			its_right_mats_p_p[j]->set_to_identity();
			its_right_mats_p_p[j+1]->set_to_identity();
			return true;//cs decompo is ideal
		}
	}
	pa_side_mats_p_p[pj]->do_cs_decompo( 
		*its_left_mats_p_p[j],  *its_left_mats_p_p[j+1],
		*its_right_mats_p_p[j], *its_right_mats_p_p[j+1],
		*d_mat_p);
	return false;//cs decompo is not ideal
}
//******************************************
VOID	NODE::private_init(
UNITARY_MAT * *  	pa_side_mats_p_p)		//in
{
	if(OPTIMIZATIONS::its_pmut_opt_level==2){
		its_pmut.set_to_identity(TREE::get_full_num_of_bits());
		//In the future, this method  will set
		//its_pmut to something more interesting
		//than the identity permutation
	}

	its_central_mat_p = new CENTRAL_MAT(its_level);

	//level=1, 	num_of_pa_left_mats=1
	//level=2, 	num_of_pa_left_mats=2
	//level= full_num_of_bits + 1, num_of_pa_left_mats=2^full_num_of_bits
	USHORT	num_of_pa_left_mats= 1<<(its_level-1);

	//pj will be used as the index for pa_side_mats	
	USHORT		pj;
	BOOLEAN	 	all_pa_side_mats_are_identity=true;
	for(pj=0; pj<num_of_pa_left_mats; pj++){
		if(!pa_side_mats_p_p[pj]->is_identity()){
			all_pa_side_mats_are_identity=false;
			break;
		}
	}
	
	if(all_pa_side_mats_are_identity){
		its_central_mat_p->set_identity_flag(true);
		its_num_of_left_mats = 0;		
		its_left_mats_p_p=0;
		its_right_mats_p_p=0;
		//Central mat has been created already.
		//Its d_mats are initially identity matrices.
	}else if(its_level==(TREE::get_full_num_of_bits() + 1)){
		its_num_of_left_mats = 0;
		its_left_mats_p_p = 0;
		its_right_mats_p_p = 0;		
		for(pj=0; pj<num_of_pa_left_mats; pj++){
			pa_side_mats_p_p[pj]->fill_one_dim_d_mat(its_central_mat_p->get_d_mat(pj));
		}
	}else{//its_level< (full_num_of_bits + 1)
		its_num_of_left_mats = (1 << its_level);//=2 for level 1; 	
		allocate_side_mats();
		for(pj=0; pj<num_of_pa_left_mats; pj++){
			fill_side_mat(pj, pa_side_mats_p_p);
		} 
	}	
}
//******************************************
NODE::NODE(
UNITARY_MAT  *	init_unitary_mat_p, 			//in
BOOLEAN			destroy_init_unitary_mat)		//in
:its_left_nd_p(0),
its_right_nd_p(0)
{
	its_level = 1;
	UNITARY_MAT	 *  *	pa_side_mats_p_p = new UNITARY_MAT * [1];
	pa_side_mats_p_p[0] = init_unitary_mat_p;
	
	private_init(pa_side_mats_p_p);//this method does no destruction
	if(OPTIMIZATIONS::its_pmut_opt_level==2){
		its_cum_pmut = its_pmut;
	}	
	
	if(destroy_init_unitary_mat){
		delete init_unitary_mat_p;
		init_unitary_mat_p = 0;
	}
	delete [] pa_side_mats_p_p;
}	
//******************************************
NODE::NODE(
NODE  & 	pa_nd,		//in
SIDE		pa_side)	//in
:its_left_nd_p(0),
its_right_nd_p(0)
{
	//pa_nd = parent node	
	its_level = pa_nd.its_level + 1;
	UNITARY_MAT	 *  *	pa_side_mats_p_p = 
		(pa_side==left_sd?pa_nd.its_left_mats_p_p:pa_nd.its_right_mats_p_p);

	private_init(pa_side_mats_p_p);//this method does no destruction		
	if(OPTIMIZATIONS::its_pmut_opt_level==2){
		its_cum_pmut = its_pmut*(pa_nd.its_cum_pmut);
	}	

	//level=1, 	num_of_pa_left_mats=1
	//level=2, 	num_of_pa_left_mats=2
	//level= full_num_of_bits + 1, num_of_pa_left_mats=2^full_num_of_bits
	USHORT	num_of_pa_left_mats= 1<<(its_level-1);
	for(USHORT pj=0; pj<num_of_pa_left_mats; pj++){
		delete pa_side_mats_p_p[pj];
	}

	if(pa_side==left_sd){
		delete [] pa_nd.its_left_mats_p_p;
		pa_nd.its_left_mats_p_p=0;
		pa_nd.its_left_nd_p = this;
	}else{
		delete [] pa_nd.its_right_mats_p_p;
		pa_nd.its_right_mats_p_p=0;
		pa_nd.its_right_nd_p = this;
	}	
}
//******************************************
NODE::~NODE()
{
	delete its_central_mat_p;
	its_central_mat_p=0;
	
	delete_side_mats();
	
	delete	its_left_nd_p;
	its_left_nd_p=0;
	delete	its_right_nd_p;
	its_right_nd_p=0;
}
#pragma mark  --simple accessors--
//******************************************
BOOLEAN		NODE::is_a_final_node_of_the_tree()
{
	return 	(   its_level==(TREE::get_full_num_of_bits() + 1)  )||
			(	its_central_mat_p->is_identity() 
				&& its_left_mats_p_p == 0 
				&& its_right_mats_p_p == 0  );
}

#pragma mark	--writers--
#ifdef _do_recursive_write
//******************************************
VOID	NODE::write(
W_SPEC & 	w_spec)	//io
{
//IMP: will read tree from right to left (this way: <--)
	if (its_right_nd_p != 0){
  		its_right_nd_p->write(w_spec);
  	}

	PERMUTATION	 inv;
	if(OPTIMIZATIONS::its_pmut_opt_level==2){
		inv.resize(0, TREE::get_full_num_of_bits());
		its_cum_pmut.get_inverse(inv);
		w_spec.its_pmut_p = &inv;
	}    
	its_central_mat_p->write(w_spec);

	if (its_left_nd_p != 0){
   		its_left_nd_p->write(w_spec);
   	}
}
#else
//******************************************
VOID	NODE::write(
W_SPEC & 	w_spec)	//io
{
	PERMUTATION	 inv;
	if(OPTIMIZATIONS::its_pmut_opt_level==2){
		inv.resize(0, TREE::get_full_num_of_bits());
		its_cum_pmut.get_inverse(inv);
		w_spec.its_pmut_p = &inv;
	}    

	its_central_mat_p->write(w_spec);
}
#endif

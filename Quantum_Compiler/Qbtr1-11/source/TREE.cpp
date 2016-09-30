#include "TREE.h"
#include "L_LIST.h"
#include "NODE.h"
#include "UNITARY_MAT.h"
#include "CENTRAL_MAT.h"
#include "Qbtr_global_funs.h"
#include "OPTIMIZATIONS.h"

USHORT	TREE::its_full_num_of_bits;
DOUBLE	TREE::its_cum_phase;
//******************************************
TREE::TREE(
UNITARY_MAT  *	init_unitary_mat_p, 			//in
BOOLEAN			destroy_init_unitary_mat)		//in
{
	//If its_full_num_of_bits==0,
	//then init_unitary matrix is just exp(i*angle).
	its_full_num_of_bits = init_unitary_mat_p->get_num_of_bits();	
	its_cum_phase = 0;
	its_rt_nd_p = new NODE(init_unitary_mat_p, destroy_init_unitary_mat);
	L_LIST<NODE  *>		nd_path;//a continuous path
	nd_path.insert_first(its_rt_nd_p);
	//root node has level 1
	//level= level of tree splitting = number of elements in nd_path
	USHORT	level=1; 
	
	NODE   * 	cur_nd_p; //cur = current
	NODE   * 	next_nd_p;
	while(level!=0){
		cur_nd_p = nd_path.get_first_p()->its_data;
		//since level!=0, cur_nd_p!=0 here
		if(cur_nd_p->is_a_final_node_of_the_tree()){
			nd_path.extract_first();
			level--;
		}else{
			if(cur_nd_p->its_left_nd_p == 0){
				next_nd_p = new NODE(*cur_nd_p, left_sd);
				nd_path.insert_first(next_nd_p);
				level++;
			}else if(cur_nd_p->its_right_nd_p == 0){
				next_nd_p = new NODE(*cur_nd_p, right_sd);
				nd_path.insert_first(next_nd_p);
				level++;
			}else{
				nd_path.extract_first();
				level--;				
			}
		}
	}
} 
//******************************************
TREE::~TREE()
{
 	delete	its_rt_nd_p;          
    its_rt_nd_p = 0;                   
}
#pragma mark --simple accessors--
//******************************************
USHORT	TREE::get_full_num_of_bits()
{
 	return its_full_num_of_bits;                 
}
//******************************************
VOID	TREE::add_to_cum_phase(
const DOUBLE  &  delta)		//in
{
 	its_cum_phase += delta;
 	limited_radians(its_cum_phase);                 
}
#pragma mark   --writers--
#ifdef _do_recursive_write 
//write using recursion
//******************************************
VOID	TREE::write(
W_SPEC & 	w_spec)	//io
{
	if (its_rt_nd_p != 0){
      	its_rt_nd_p->write(w_spec);
  	}
  	write_cum_phase(w_spec);
  				
	#ifdef	_write_verbose_engl_file
		write_cum_num_of_elem_ops(w_spec);
	#endif
}
#else
//write without using recursion (preferred)
//******************************************
VOID	TREE::write(
W_SPEC & 	w_spec)	//io
{
	//IMP: will read tree from right to left (this way: <--)
	write_num_of_bits(w_spec);
	
	L_LIST<NODE  *>		postponed_nds;//not a continuous path
	//Postponed nodes are nodes that have been visited
	//but whose writing has been postponed.

	NODE   * 	nd_p = its_rt_nd_p;
	while(true){
		if(nd_p != 0){			
			postponed_nds.insert_first(nd_p);
			nd_p = nd_p->its_right_nd_p;
		}else{
			//Extract first of the list and put it in nd_p.
			//Exit while() loop if postponed_nds is empty.
			if(!postponed_nds.extract_first(nd_p))break;
			nd_p->write(w_spec);
			nd_p = nd_p->its_left_nd_p;
		}
	}
  	write_cum_phase(w_spec);
  	 			
	#ifdef	_write_verbose_engl_file
		write_cum_num_of_elem_ops(w_spec);
	#endif
}
#endif
//******************************************
VOID	TREE::write_num_of_bits(
W_SPEC & 	w_spec)	//io
{
	if(w_spec.its_engl_strm_p!=0){
		*w_spec.its_engl_strm_p
			<< its_full_num_of_bits
			<<k_endline;
	}
	if(w_spec.its_pict_strm_p!=0){
		*w_spec.its_pict_strm_p
			<< its_full_num_of_bits
			<<k_endline;
	}
}
//******************************************
VOID	TREE::write_cum_phase(
W_SPEC & 	w_spec)	//io
{
	if(is_zero(its_cum_phase))return;
	if(w_spec.its_engl_strm_p!=0){
		*w_spec.its_engl_strm_p
			<< "PHAS"
			<<'\t'
			<<its_cum_phase*180/my_pi
			<<k_endline;
	}
	if(w_spec.its_pict_strm_p!=0){
		for(USHORT i=0 ; i<its_full_num_of_bits ; i++){
			*w_spec.its_pict_strm_p<<'~';
		}
		*w_spec.its_pict_strm_p << k_endline;
	}
}
//******************************************
VOID	TREE::write_cum_num_of_elem_ops(
W_SPEC & 	w_spec)	//io
{
  	if(w_spec.its_engl_strm_p !=0){
		*w_spec.its_engl_strm_p
			<< '{'
			<< " number of steps = "
			<< CENTRAL_MAT::get_cum_num_of_elem_ops()
			<< k_endline
			<< '}'
			<< k_endline;
	}
	if(w_spec.its_pict_strm_p!=0){
		*w_spec.its_pict_strm_p
			<< '{'
			<< k_endline
			<< '}'
			<< k_endline;
	}
}
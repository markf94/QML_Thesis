#include "UNITARY_MAT.h"
#include "TREE.h"
#include "STRINGY.h"
#include "OPTIMIZATIONS.h"
#include "PERMUTATION.h"
#include "CENTRAL_MAT.h"
#include "W_SPEC.h"


//This global is a string that denotes the
//matrix being decomposed. The global will
//be used as a prefix in file names.
STRINGY		g_mat_name;

VOID	pmut_opt1_grow_one_tree(
UNITARY_MAT *  u_p, W_SPEC & w_spec,
BOOLEAN keep_identity_pmut, const PERMUTATION & desired_pmut);

VOID	pmut_opt1_grow_many_trees(
UNITARY_MAT *  u_p, W_SPEC & w_spec,
BOOLEAN keep_identity_pmut, const PERMUTATION & desired_pmut);

	
//******************************************
//VOID  main(VOID)
int  main(VOID)
{
	SetDebugThrow_(debugAction_Alert);
	SetDebugSignal_(debugAction_Alert);

	//params = parameters
	//comp = components
	//engl = english
	//pict = picture
	//i(o)strm = in(out) stream
	//opt = optimization
	//pmut = permutation
	IFSTREAM		param_strm;
	USHORT			do_compilation, do_decompilation;
	USHORT			do_light_right_opt;
	USHORT			do_complex_d_mat_opt;
	USHORT			pmut_opt_level;
	USHORT			do_all_bit_pmuts, keep_identity_pmut;
	PERMUTATION		desired_pmut;
	USHORT			pmut_len, i;
	
	param_strm.open("qbtr-params.in");
	if(!param_strm.is_open()) { 
		cerr<<"'qbtr-params.in' file is missing.";
		exit(-1);
	}
	
	param_strm.exceptions(ios::badbit | ios::failbit);
	try{
			param_strm.ignore(500, k_endline);
		param_strm>>g_mat_name;
			param_strm.ignore(500, k_endline);
			param_strm.ignore(500, k_endline);
		param_strm>>do_compilation;
			param_strm.ignore(500, k_endline);
			param_strm.ignore(500, k_endline);
		param_strm>>do_decompilation;
			param_strm.ignore(500, k_endline);
			param_strm.ignore(500, k_endline);
		param_strm>>do_light_right_opt;
			param_strm.ignore(500, k_endline);
			param_strm.ignore(500, k_endline);
		param_strm>>do_complex_d_mat_opt;
			param_strm.ignore(500, k_endline);
			param_strm.ignore(500, k_endline);
		param_strm>>pmut_opt_level;
			param_strm.ignore(500, k_endline);
			param_strm.ignore(500, k_endline);
		if(pmut_opt_level==1){
			param_strm>>do_all_bit_pmuts;
			param_strm.ignore(500, k_endline);
		}else{
			param_strm.ignore(500, k_endline);
		}
			param_strm.ignore(500, k_endline);
		if(pmut_opt_level==1){
			param_strm>>keep_identity_pmut;
			param_strm.ignore(500, k_endline);
		}else{
			param_strm.ignore(500, k_endline);
		}
			param_strm.ignore(500, k_endline);
			param_strm.ignore(500, k_endline);
		if(pmut_opt_level==1 && !keep_identity_pmut){
			param_strm>>pmut_len;
			desired_pmut.resize(0, pmut_len);
			for(i=0; i<pmut_len; i++){
				param_strm>>desired_pmut[i];
			}
			param_strm.ignore(500, k_endline);
		}else{
			param_strm.ignore(500, k_endline);
			param_strm.ignore(500, k_endline);
		}	
	}
	catch(const ios::failure  &  io_exc){
		cerr<<"'qbtr-params.in' file is illegal.";
		exit(-1);
	}
	param_strm.close();

	OPTIMIZATIONS::its_lighten_right_mats = do_light_right_opt;
	OPTIMIZATIONS::its_extract_d_mat_phases = do_complex_d_mat_opt;
	OPTIMIZATIONS::its_pmut_opt_level = pmut_opt_level;
	//pmut_opt_level>1 not yet implemented
	ThrowIf_(pmut_opt_level>1);
	
	if(do_compilation){		
		IFSTREAM	comp_strm;

	 	comp_strm.open((g_mat_name && ".in").get_string());
	 	if( !comp_strm.is_open() ) { 
	 		cerr<<"'mat_name.in' file is missing.";
	 		exit(-1);
	 	}
	 	UNITARY_MAT  *  u_p = new UNITARY_MAT();
		//u_p is destroyed by TREE()->NODE()
		//if choose destroy option in TREE().
		u_p->read_components_file(&comp_strm);
		comp_strm.close();
		
		if(u_p->get_num_of_bits()==0){
			OPTIMIZATIONS::its_pmut_opt_level = pmut_opt_level = 0;
		}
	
		if(pmut_opt_level==1){	
			if(!keep_identity_pmut){
				ThrowIf_(u_p->get_num_of_bits()!=pmut_len);
			}else{
				pmut_len = u_p->get_num_of_bits();
				desired_pmut.set_to_identity(pmut_len);
			}
		}

		OFSTREAM  		engl_strm;
		OFSTREAM  		pict_strm;
		W_SPEC			w_spec;
	 	engl_strm.open((g_mat_name && "-engl.out").get_string());
	 	pict_strm.open((g_mat_name && "-pict.out").get_string());
		engl_strm<<fixed<<showpoint<<setprecision(9);
		w_spec.its_engl_strm_p = &engl_strm;
		w_spec.its_pict_strm_p = &pict_strm;
		if(pmut_opt_level!=1){
			TREE	tree(u_p, true);//destroys u_p
			w_spec.its_pmut_p = 0;
		 	tree.write(w_spec);
		}else{//pmut_opt_level==1
			if(!do_all_bit_pmuts){
				//destroys u_p
				pmut_opt1_grow_one_tree(u_p, w_spec, keep_identity_pmut, desired_pmut);
			}else{//do all bit permutations
				//destroys u_p
				pmut_opt1_grow_many_trees(u_p, w_spec, keep_identity_pmut, desired_pmut);
			}
		}//pmut_opt_level
	 	engl_strm.close();
	 	pict_strm.close();
 	}//do compilation
 	
 	if(do_decompilation){

	 	UNITARY_MAT 	v;

 		IFSTREAM	engl_strm;
	 	engl_strm.open((g_mat_name && "-engl.out").get_string());
	 	if(!engl_strm.is_open()) {
	 		cerr<<"'mat_name-engl.out' file is missing.";
	 		exit(-1);
	 	}	 	
		v.read_english_file(&engl_strm);
		engl_strm.close();
	 
	 	OFSTREAM	comp_strm;
	 	comp_strm.open((g_mat_name && "-chk.out").get_string());//chk = check
	 	comp_strm<<fixed<<showpoint;
		v.write_components_file(&comp_strm);
		comp_strm.close();

		if(do_compilation){
	 		IFSTREAM	decr_strm;//decr = decrement
		 	decr_strm.open((g_mat_name && ".in").get_string());
		 	if( !decr_strm.is_open() ) { 
		 		cerr<<"'mat_name.in' file is missing.";
		 		exit(-1);
		 	}		
			v.read_decrements_file(&decr_strm);
			decr_strm.close();
			
		 	OFSTREAM	err_strm;//err = error
		 	err_strm.open((g_mat_name && "-err.out").get_string());
		 	err_strm<<fixed<<showpoint;
			v.write_components_file(&err_strm);
			err_strm.close();
		}
	}	
}
//******************************************
VOID	pmut_opt1_grow_one_tree(
UNITARY_MAT * 			u_p,						//io
W_SPEC & 				w_spec,						//io
BOOLEAN					keep_identity_pmut,			//in
const PERMUTATION & 	desired_pmut)				//in
{
	if(!keep_identity_pmut){
		u_p->permute_bits(desired_pmut);
	}				
	TREE	tree(u_p, true);
	PERMUTATION		inv_pmut(desired_pmut.get_len());
	if(!keep_identity_pmut){
		desired_pmut.get_inverse(inv_pmut);
		w_spec.its_pmut_p = &inv_pmut;
	}else{
		w_spec.its_pmut_p = 0;
	}			
 	tree.write(w_spec);
}
//******************************************
VOID	pmut_opt1_grow_many_trees(
UNITARY_MAT * 			u_p,						//io
W_SPEC & 				w_spec,						//io
BOOLEAN					keep_identity_pmut,			//in
const PERMUTATION & 	desired_pmut)				//in
{
	//save the ostream pointers
	OFSTREAM * 		engl_strm_p = w_spec.its_engl_strm_p;
	OFSTREAM * 		pict_strm_p = w_spec.its_pict_strm_p;

	OFSTREAM		pmut_strm;//permutation log
	pmut_strm.open((g_mat_name && "-pmut.out").get_string());
	TRANSPOSITION	transp;//identity by default
	USHORT			p_counter=1;
	BOOLEAN			more_pmuts;
	USHORT			pmut_len = desired_pmut.get_len();
	PERMUTATION		pmut(pmut_len);
	PERMUTATION		inv_pmut(pmut_len);
	pmut.prepare_for_lazy_advance();
	do{	
		more_pmuts = pmut.lazy_advance(transp);
		u_p->transpose_bits(transp);
		TREE	tree(u_p, false);//destroy u_p at the end of this method
	  	//In write:
	  	//If engl_strm_p = 0, then no actual 
	  	//writing is done in english file.
	 	//Same for pict_strm_p.
	 	//If pmut_p = 0, no permutation is done when writing english file.				 
		if(pmut!=desired_pmut){
			w_spec.its_engl_strm_p = 0;
			w_spec.its_pict_strm_p = 0;
			w_spec.its_pmut_p = 0;
		}else{
			w_spec.its_engl_strm_p = engl_strm_p;
			w_spec.its_pict_strm_p = pict_strm_p;
			if(!keep_identity_pmut){
				desired_pmut.get_inverse(inv_pmut);
				w_spec.its_pmut_p = &inv_pmut;
			}else{
				w_spec.its_pmut_p = 0;
			}
		}
		CENTRAL_MAT::set_cum_num_of_elem_ops(0);
		tree.write(w_spec);
		pmut_strm<< '(' << p_counter << ')';
		for(USHORT	i=0; i<pmut_len; i++){
			pmut_strm<<'\t'<<pmut[i];
		}
		pmut_strm<< k_endline <<'\t'<<"number of steps = ";
		pmut_strm<<CENTRAL_MAT::get_cum_num_of_elem_ops()<<k_endline;
		p_counter++;
	}while(more_pmuts);
	delete	u_p;
	pmut_strm.close();
}

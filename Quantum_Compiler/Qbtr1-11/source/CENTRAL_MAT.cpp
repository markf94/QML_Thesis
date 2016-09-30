#include "CENTRAL_MAT.h"
#include "D_MAT.h"
#include "TREE.h"
#include "had_transforms.h"
#include "L_LIST.h"
#include "BIT_VECTOR.h"
#include "Qbtr_global_funs.h"
#include "OPTIMIZATIONS.h"
#include "PERMUTATION.h"
#include "nu_n1_transforms.h"

LONG	CENTRAL_MAT::its_cum_num_of_elem_ops=0;

#pragma mark	--creation/destruction--
//******************************************
CENTRAL_MAT::CENTRAL_MAT(
USHORT	level)			//in
:its_is_identity(false),
its_is_croty90(false)
{

	USHORT	num_of_bits = TREE::get_full_num_of_bits();
	ThrowIf_(level < 1 || level > (num_of_bits + 1)  );

	if(level <= num_of_bits){
		its_is_diagonal = false;
		//For single d  matrix: level = 1, bpos_of_rot = num_of_bits - 1
		its_bpos_of_rot = num_of_bits - level;
	}else{//level = (num_of_bits + 1)
		its_is_diagonal = true;
		its_bpos_of_rot = max_ushort;
	}

	//level=1, its_num_of_d_mats = 1
	//level=num_of_bits + 1 , its_num_of_d_mats = 2^num_of_bits	
	its_num_of_d_mats = (1<<(level-1));

	//level=1,	num_of_bits_in_d_mat = num_of_bits
	//level=num_of_bits + 1, num_of_bits_in_d_mat = 0
	USHORT	num_of_bits_in_d_mat = (num_of_bits + 1) - level;
	its_d_mats_p_p = new D_MAT  * [its_num_of_d_mats];
	for(USHORT i=0; i<its_num_of_d_mats; i++){
		its_d_mats_p_p[i]= new D_MAT(num_of_bits_in_d_mat);
	}
}
//******************************************
CENTRAL_MAT::~CENTRAL_MAT()
{
	if(its_d_mats_p_p!=0){
		for(USHORT i=0; i<its_num_of_d_mats; i++){
			delete its_d_mats_p_p[i];
			its_d_mats_p_p[i]=0;		
		}
		delete [] its_d_mats_p_p;
		its_d_mats_p_p = 0;
	}
}
#pragma mark	--simple accessors--
//******************************************
LONG		CENTRAL_MAT::get_cum_num_of_elem_ops()
{
	//its_cum_num_of_elem_ops
	//counts the cumulative number of elementary operations written.
	//It does not count the cum overall phase as one operation.

	return its_cum_num_of_elem_ops;
}
//******************************************
VOID		CENTRAL_MAT::set_cum_num_of_elem_ops(
LONG	num)	//in
{
	its_cum_num_of_elem_ops = num;
}
//******************************************
BOOLEAN		CENTRAL_MAT::is_identity()
const
{
	return its_is_identity;
}
//******************************************
VOID		CENTRAL_MAT::set_identity_flag(
BOOLEAN		flag)	//in
{
	its_is_identity = flag;
}
//******************************************
BOOLEAN		CENTRAL_MAT::is_croty90(
USHORT &	control_bpos,	//out
BOOLEAN	&	req_bval,		//out
USHORT &	rot_bpos)		//out
const
{
	//croty90 = controlled rotation along Y axis by 90 degrees (just 1 control)
	//= exp[i\sigma_y(rot_bpos) 90^o  P_bval(control_bpos)]
	//where bval=req_bval
	//One can show that croty90 =
	//=\sigma_x(rot_bpos)^{P_bval(control_bpos)}*(-1)^{nbar(rot_bpos) P_bval(control_bpos)}
	
	
	//Don't use this method if "this" is diagonal central matrix
	ThrowIf_(its_d_mats_p_p[0]->get_num_of_bits() == 0);
	
	if(!all_cs_angles_are_0_or_90_degs())return false;

	rot_bpos = its_bpos_of_rot;	

	USHORT			full_num_of_bits = TREE::get_full_num_of_bits();
	BIT_VECTOR		bvec(full_num_of_bits, 0);
	USHORT			d_mat_num_of_cs_angles = its_d_mats_p_p[0]->get_num_of_cs_angles();
	control_bpos=0;
	//Look at
	//all possible control bit positions (except its_bpos_of_rot)
	//and all possible bit values (0 and 1) 
	while(control_bpos<full_num_of_bits){
		if(control_bpos != its_bpos_of_rot){
			for(USHORT bval=0; bval<=1; bval++){
				req_bval = bval;				
				USHORT	col = 0; 
				for(USHORT i=0; i<its_num_of_d_mats; i++){
					D_MAT *  d_mat_p = its_d_mats_p_p[i];
					for(USHORT	a=0; a<d_mat_num_of_cs_angles; a++){
						bvec.set_dec_rep(col);
						if(bvec.bit_is_ON(control_bpos)==req_bval){
							if(!is_zero(d_mat_p->get_cs_angle(a) - my_half_pi)) goto next_hypothesis;	
						}else{
							if(!is_zero(d_mat_p->get_cs_angle(a))) goto next_hypothesis;		
						}
						col++;					
					}
					col += d_mat_num_of_cs_angles;	
				}
				return true;
				next_hypothesis:;
			}
		}
		control_bpos++;
	}
	
	return false;
}
//******************************************
D_MAT  &	CENTRAL_MAT::get_d_mat(
USHORT	block)	//in
{
	 return *its_d_mats_p_p[block];
}
//******************************************
BOOLEAN		CENTRAL_MAT::all_cs_angles_are_zero(
VECTOR<DOUBLE>  & 	angles)	//out
{
	//This method returns a vector with the cs angles
	//plus it tells whether they are all zero.
	USHORT	d_mat_num_of_cs_angles = its_d_mats_p_p[0]->get_num_of_cs_angles();
	USHORT	len = d_mat_num_of_cs_angles*its_num_of_d_mats;
	
	angles.resize(0/*default*/, len);
	if(!its_is_identity){
		DOUBLE 		ang;
		BOOLEAN		so_far_zeros = true;
		USHORT		big = 0;
		for(USHORT	i=0; i< its_num_of_d_mats; i++){
			for(USHORT a=0; a < d_mat_num_of_cs_angles; a++){
				ang = its_d_mats_p_p[i]->get_cs_angle(a);
				angles[big] = ang;
				if(so_far_zeros && !is_zero(ang)) so_far_zeros = false;
				big++;
			}
		}
		its_is_identity = so_far_zeros;
	}
	return its_is_identity;	
}
//******************************************
BOOLEAN		CENTRAL_MAT::all_cs_angles_are_0_or_90_degs()
const
{		
	if(its_is_identity) return true;
	USHORT	d_mat_num_of_cs_angles = its_d_mats_p_p[0]->get_num_of_cs_angles();
	
	DOUBLE 		ang;
	for(USHORT	i=0; i< its_num_of_d_mats; i++){
		for(USHORT a=0; a < d_mat_num_of_cs_angles; a++){
			ang = its_d_mats_p_p[i]->get_cs_angle(a);
			if(!is_zero(ang) && !is_zero(ang - my_half_pi))return false;
		}
	}
	return true;	
}
//******************************************
USHORT	CENTRAL_MAT::alias(
USHORT 	bpos)	//in
{
	USHORT	new_bpos;
	if(bpos < its_bpos_of_rot){
		new_bpos = bpos;
	}else if(bpos==(TREE::get_full_num_of_bits() - 1)){
		new_bpos = its_bpos_of_rot;
	}else{
		new_bpos = (bpos + 1);
	}
	return new_bpos;
}
#pragma mark	--writers--
//******************************************
VOID	CENTRAL_MAT::write(
W_SPEC & 	w_spec)	//io
{
	if(its_is_diagonal){
		write_if_diagonal(w_spec);
	}else{
		write_if_not_diagonal(w_spec);
	}
}
//******************************************
VOID	CENTRAL_MAT::write_cs_angles(
W_SPEC & 					w_spec,	//io
const VECTOR<DOUBLE>  &		angles)	//in
{
	//this method is mainly for debugging
	if(w_spec.its_engl_strm_p!=0){
		USHORT	d_mat_num_of_cs_angles = its_d_mats_p_p[0]->get_num_of_cs_angles();
		USHORT	num_of_cs_angles = angles.get_len();
		CHAR	ch=((its_d_mats_p_p[0]->get_num_of_bits()==0)?'^':'&');
		DOUBLE	ang;
		*w_spec.its_engl_strm_p<< "{ angles:";
		USHORT	k=0;
		while(k<num_of_cs_angles){
			ang = angles[k]*180/my_pi;
			//round off very small ang to zero
			if(is_zero(ang)) ang = 0; 
			*w_spec.its_engl_strm_p<<" "<<ang;
			k++;
			if(k%d_mat_num_of_cs_angles==0 && k!=num_of_cs_angles){
				*w_spec.its_engl_strm_p<<" "<<ch;
			}
		}	
		*w_spec.its_engl_strm_p<<k_endline;
	}
	if(w_spec.its_pict_strm_p!=0){
		*w_spec.its_pict_strm_p
			<< "{"
			<<k_endline;
	}
}
#pragma mark ----writers of single gate
//******************************************
VOID	CENTRAL_MAT::write_bit_rot(
W_SPEC & 	w_spec,				//io
ROT_AXIS	axis,				//in
USHORT		bpos,				//in
const DOUBLE  &		angle)		//in
{
	its_cum_num_of_elem_ops++;
	ThrowIf_(TREE::get_full_num_of_bits()==0);

	//overall permutation
	if(w_spec.its_pmut_p!=0){
		bpos =  (*(w_spec.its_pmut_p))[bpos];
	}
	
	if(w_spec.its_engl_strm_p!=0){
		*w_spec.its_engl_strm_p
			<< (axis==y_ax?"ROTY":"ROTZ")
			<<'\t'
			<<bpos
			<<'\t'
			<<angle*180/my_pi
			<<k_endline;
	}
	
	if(w_spec.its_pict_strm_p!=0){
		SHORT	i;
		for(i=TREE::get_full_num_of_bits()-1 ; i>bpos ; i--){
			*w_spec.its_pict_strm_p<<'|';
		}
		*w_spec.its_pict_strm_p<< (axis==y_ax? 'Y':'Z');
		for(i=(SHORT)bpos-1 ; i>=0 ; i--){
			*w_spec.its_pict_strm_p<<'|';
		}
		*w_spec.its_pict_strm_p<<k_endline;
	}			
}
//******************************************
VOID	CENTRAL_MAT::write_sigma_x(
W_SPEC & 	w_spec,		//io
USHORT	flipper_bpos)	//in
{
	its_cum_num_of_elem_ops++;
	ThrowIf_(TREE::get_full_num_of_bits()==0);

	//overall permutation
	if(w_spec.its_pmut_p!=0){		
		flipper_bpos =  (*(w_spec.its_pmut_p))[flipper_bpos];
	}
	
	if(w_spec.its_engl_strm_p!=0){
		*w_spec.its_engl_strm_p 
			<< "SIGX"
			<<'\t'
			<<flipper_bpos
			<<k_endline;
	}

	if(w_spec.its_pict_strm_p!=0){
		SHORT 	i;		
		for(i=TREE::get_full_num_of_bits()-1 ; i>flipper_bpos ; i--){
			*w_spec.its_pict_strm_p<<'|';
		}
		*w_spec.its_pict_strm_p<< 'X';
		for(i=(SHORT)flipper_bpos-1 ; i>=0 ; i--){
			*w_spec.its_pict_strm_p<<'|';
		}
		*w_spec.its_pict_strm_p<<k_endline;
	}			
}
//******************************************
VOID	CENTRAL_MAT::write_controlled_gate(
W_SPEC & 					w_spec,				//io
const VECTOR<USHORT> &		control_bpos,		//in
const BIT_VECTOR &			req_control_bval,	//in
CGATE_TYPE					type,				//in
const DOUBLE &				gate_param)			//in
{
	its_cum_num_of_elem_ops++;
	ThrowIf_(TREE::get_full_num_of_bits()==0);
	//req_control_bval = required control bit value
		
	USHORT	flipper_bpos;
	DOUBLE	phase;
	if(type==k_cnot){
		flipper_bpos = (USHORT)gate_param;
	}else{//type==k_cpha
		phase = gate_param;
	}
	//flipper_bpos(if type==k_cnot) and 
	//all elements of control_bpos
	//must be distinct
	SHORT	num_of_controls = control_bpos.get_len();
	ThrowIf_(	num_of_controls==0 || 
				num_of_controls != req_control_bval.get_len()	);
	SHORT	c;
	
	//overall permutation
	VECTOR<USHORT> 	c_bpos = control_bpos;
	if(w_spec.its_pmut_p!=0){	
		for(c=0; c<num_of_controls; c++){
			c_bpos[c] =  (*(w_spec.its_pmut_p))[control_bpos[c]];
		}
		if(type==k_cnot){
			flipper_bpos =  (*(w_spec.its_pmut_p))[flipper_bpos];
		}
	}
	
	if(w_spec.its_engl_strm_p!=0){
		if(type==k_cnot){
			*w_spec.its_engl_strm_p << "CNOT";
		}else{
			*w_spec.its_engl_strm_p << "CPHA";
		}
		for(c=num_of_controls - 1; c>=0; c--){
			*w_spec.its_engl_strm_p
				<< '\t'
				<< c_bpos[c]
				<< '\t'
				<< (req_control_bval.bit_is_ON(c)?'T':'F');
		}
		*w_spec.its_engl_strm_p<<'\t';
		if(type==k_cnot){
			*w_spec.its_engl_strm_p << flipper_bpos <<k_endline;;
		}else{
			*w_spec.its_engl_strm_p << phase*180/my_pi <<k_endline;;
		}
	}

	if(w_spec.its_pict_strm_p!=0){
		SHORT		biggest, smallest;
		if(num_of_controls!=TREE::get_full_num_of_bits()){
			biggest=0;
			smallest=TREE::get_full_num_of_bits()-1;
			for(c=0; c<num_of_controls; c++){
				if(c_bpos[c]> biggest)	biggest=c_bpos[c];
				if(c_bpos[c]< smallest)	smallest=c_bpos[c];
			}
			if(type==k_cnot){
				if(flipper_bpos> biggest)	biggest=flipper_bpos;
				if(flipper_bpos< smallest)	smallest=flipper_bpos;
			}
		}else{
			biggest = TREE::get_full_num_of_bits()-1;
			smallest = 0;		
		}
		SHORT 	i;		
		for(i=TREE::get_full_num_of_bits()-1 ; i>biggest ; i--){
			*w_spec.its_pict_strm_p<<'|';
		}
		for(i=biggest ; i>=smallest ; i--){
			BOOLEAN		is_a_control = false;
			BOOLEAN		req_control_bval_is_1 = false;
			for(c=0; c<num_of_controls; c++){
				if(i==c_bpos[c]){
					is_a_control = true;
					req_control_bval_is_1 = req_control_bval.bit_is_ON(c);
					break;
				}
			}
			if(is_a_control){
				*w_spec.its_pict_strm_p<< (req_control_bval_is_1?'@':'O');
			}else if(type==k_cnot && i==flipper_bpos){
				*w_spec.its_pict_strm_p<< 'X';
			}else{
				*w_spec.its_pict_strm_p<<'-';
			}
		}
		for(i=smallest-1 ; i>=0 ; i--){
			*w_spec.its_pict_strm_p<<'|';
		}
		*w_spec.its_pict_strm_p<<k_endline;
	}			
}
//******************************************

VOID	CENTRAL_MAT::write_cnot(
W_SPEC & 					w_spec,				//io
const VECTOR<USHORT> &		control_bpos,		//in
const BIT_VECTOR &			req_control_bval,	//in
USHORT						flipper_bpos)		//in
{
	write_controlled_gate(w_spec, control_bpos, req_control_bval, k_cnot, (DOUBLE)flipper_bpos);
}
//******************************************
VOID	CENTRAL_MAT::write_cnot(
W_SPEC & 	w_spec,					//io
USHORT		the_control_bpos,		//in
BOOLEAN		the_req_control_bval,	//in
USHORT		flipper_bpos)			//in
{	
	VECTOR<USHORT>	control_bpos(the_control_bpos/*val*/, 1 /*len*/);
	BIT_VECTOR		req_control_bval(1/*len*/, (USHORT)the_req_control_bval/*val*/);
	write_cnot(w_spec, control_bpos, req_control_bval, flipper_bpos);
}
//******************************************
VOID	CENTRAL_MAT::write_cphase(
W_SPEC & 					w_spec,				//io
const VECTOR<USHORT> &		control_bpos,		//in
const BIT_VECTOR &			req_control_bval,	//in
const DOUBLE &				phase)				//in
{
	//cphase = controlled phase
	write_controlled_gate(w_spec, control_bpos, req_control_bval, k_cpha, phase);
}
#pragma mark	----writers of many gates----
//******************************************
VOID	CENTRAL_MAT::write_ph_factors_of_d_mats(
W_SPEC & 				w_spec,		//io
PH_FACTOR_TYPE				ft)		//in
{
	//don't use this method if "this" is a diagonal central matrix
	ThrowIf_(its_d_mats_p_p[0]->get_num_of_bits() == 0);

	USHORT	full_num_of_bits = TREE::get_full_num_of_bits();
	USHORT	num_of_controls;
	VECTOR<USHORT> 	control_bpos;
	BIT_VECTOR		req_control_bval;
	USHORT			c, col, i, a;
	
	#if		_use_n_nbar_in_cphases
		num_of_controls = full_num_of_bits; 
		control_bpos.set_to_default_vec(0, num_of_controls);
		req_control_bval.set_len(num_of_controls);
		for(c=0; c<num_of_controls; c++){
			control_bpos[c] = c;
		}
	#else
		USHORT	dim =  1<< full_num_of_bits;
		VECTOR<DOUBLE>	stored_phases(0, dim);
	#endif
	
	DOUBLE		phase, gen_phase, row_phase, col_phase;
	USHORT		d_mat_num_of_cs_angles = its_d_mats_p_p[0]->get_num_of_cs_angles();
	col=0;
	BIT_VECTOR	bvec(full_num_of_bits, 0);
	for(i=0; i<its_num_of_d_mats; i++){	
		D_MAT *     d_mat_p = its_d_mats_p_p[i];
		//at this point, col=i*d_mat_num_of_cs_angles*2;
		for(a=0; a<d_mat_num_of_cs_angles; a++){
			req_control_bval.set_dec_rep(col);
			gen_phase = d_mat_p->get_gen_phase(a);
			if(its_is_croty90 && ft==k_col_pshift){
				//this puts in
				//(-1)^{nbar(rot_bpos) P_bval(control_bpos)}
				//of croty90
				bvec.set_dec_rep(col);
				if(!bvec.bit_is_ON(its_croty90_rot_bpos) && 
					bvec.bit_is_ON(its_croty90_control_bpos)==its_croty90_req_bval){
					gen_phase += my_pi;
					limited_radians(gen_phase);
				}
			}				
			if(ft==k_col_pshift && !is_zero(gen_phase)){
				#if		_use_n_nbar_in_cphases
					write_cphase(w_spec, control_bpos, req_control_bval, gen_phase);
				#else
					stored_phases[col] = gen_phase;
				#endif
			}
			col++;
		}//a
		for(a=0; a<d_mat_num_of_cs_angles; a++){
			req_control_bval.set_dec_rep(col);
			gen_phase = d_mat_p->get_gen_phase(a);
			row_phase = d_mat_p->get_row_phase(a);
			col_phase = d_mat_p->get_col_phase(a);
			phase = gen_phase + col_phase;
			if(its_is_croty90 && ft==k_col_pshift){
				//this puts in
				//(-1)^{nbar(rot_bpos) P_bval(control_bpos)}
				//of croty90
				bvec.set_dec_rep(col);
				if(!bvec.bit_is_ON(its_croty90_rot_bpos) && 
					bvec.bit_is_ON(its_croty90_control_bpos)==its_croty90_req_bval){
					phase +=my_pi;
				}
			}				
			limited_radians(phase);
			if(ft==k_col_pshift && !is_zero(phase)){
				#if		_use_n_nbar_in_cphases
					write_cphase(w_spec, control_bpos, req_control_bval, phase);
				#else
					stored_phases[col] = phase;
				#endif
			}else if(ft==k_row_pshift && !is_zero(row_phase)){
				#if		_use_n_nbar_in_cphases
					write_cphase(w_spec, control_bpos, req_control_bval, row_phase);
				#else
					stored_phases[col] = row_phase;
				#endif
			}
			col++;
		}//a
	}//i
	
	#if		!_use_n_nbar_in_cphases
		//transform stored phases from (n, nbar) to (n, 1) basis
		nu_to_n1_vec(full_num_of_bits, stored_phases);
		TREE::add_to_cum_phase(stored_phases[0]);
		for(col=1; col<dim; col++){//start at 1
			bvec.set_dec_rep(col);
			num_of_controls = bvec.get_num_of_ON_bits();// >= 1
			control_bpos.set_to_default_vec(0, num_of_controls);
			c=0;
			for(USHORT	beta=0; beta<full_num_of_bits; beta++){
				if(bvec.bit_is_ON(beta)){
					control_bpos[c] = beta;
					c++;
				}
			}
			req_control_bval.set_len(num_of_controls);
			req_control_bval.set_all_bits_ON();
			phase = stored_phases[col];
			limited_radians(phase);
			if(!is_zero(phase)){
				write_cphase(w_spec, control_bpos, req_control_bval, phase);
			}
		}
	#endif
}

#pragma mark	------do_lazy------
#if		_do_lazy_if_central_mat_not_diagonal
//******************************************
VOID	CENTRAL_MAT::write_if_not_diagonal(
W_SPEC & 	w_spec)	//io
{
	USHORT	full_num_of_bits = TREE::get_full_num_of_bits();
	ThrowIf_(full_num_of_bits==0);
	USHORT	full_num_of_bits_minus_one = full_num_of_bits - 1;
	VECTOR<DOUBLE>	angles;	
	BOOLEAN			all_zero=true;

	if(OPTIMIZATIONS::its_extract_d_mat_phases){
		USHORT	control_bpos, rot_bpos;
		BOOLEAN	req_bval;
		if(is_croty90(control_bpos, req_bval, rot_bpos)){	
			its_is_croty90 = true;
			its_croty90_control_bpos = control_bpos;
			its_croty90_req_bval = req_bval;
			its_croty90_rot_bpos = rot_bpos;
			write_ph_factors_of_d_mats(w_spec, k_col_pshift);
			write_cnot(w_spec, control_bpos, req_bval, rot_bpos);
			#ifdef	_write_verbose_engl_file
				if(w_spec.its_engl_strm_p!=0)*w_spec.its_engl_strm_p<< "{"<<k_endline;
				if(w_spec.its_pict_strm_p!=0)*w_spec.its_pict_strm_p<< "{"<<k_endline;
			#endif
			goto ending;
		}else{
			write_ph_factors_of_d_mats(w_spec, k_col_pshift);
		}	
	}
	
	all_zero = all_cs_angles_are_zero(angles);
					
	#ifdef	_write_verbose_engl_file
		write_cs_angles(w_spec, angles);
	#endif
	
	if(all_zero){
		goto ending;
	}

	if(full_num_of_bits_minus_one==0){
		write_bit_rot(w_spec, y_ax, 0, angles[0]);
		goto ending;
	}			

	{
		//this replaces angles by the inverse Hadamard Transform angles	
		inv_had_transform(full_num_of_bits_minus_one, angles);
		limited_radians(angles);

		USHORT		num_of_factors = (1 << full_num_of_bits_minus_one);
		USHORT		f=0;
		USHORT		prev_ON_bit, cur_ON_bit;//prev=previous, cur = current
		BIT_VECTOR	cur_bvec(full_num_of_bits_minus_one);//0 by default
		BIT_VECTOR	prev_active_bvec(full_num_of_bits_minus_one);//0 by default
		BIT_VECTOR	reduced_bvec(full_num_of_bits);//0 by default, one more bit than cur_bvec and prev_active_bvec
		USHORT  	alias_of_full_num_of_bits_minus_one = alias(full_num_of_bits_minus_one);	

		while(f<num_of_factors){
			DOUBLE	ang = angles[cur_bvec.get_dec_rep()];
			if(is_zero(ang)){
				//do nothing
			}else{
				//an active bvec is one for which ang is NOT zero		
				reduced_bvec.set_dec_rep( cur_bvec.get_dec_rep() ^ prev_active_bvec.get_dec_rep());			
				prev_ON_bit = full_num_of_bits_minus_one;
				while(reduced_bvec.find_ON_bit_to_my_right(prev_ON_bit, cur_ON_bit)){
					write_cnot(w_spec, alias(cur_ON_bit), true, alias_of_full_num_of_bits_minus_one);
					prev_ON_bit = cur_ON_bit;
				}
						
				write_bit_rot(w_spec, y_ax, alias_of_full_num_of_bits_minus_one, ang);			
				prev_active_bvec = cur_bvec;
			}//zero angles if()	
			f++;	
			cur_bvec.lazy_advance(f);
		}//f loop
		
		//Don't forget the leftmost c-nots:
		//reduced_bvec and prev_active_bvec don't have
		//the same length so can't just equate them.
		reduced_bvec.set_dec_rep(prev_active_bvec.get_dec_rep());
		prev_ON_bit = full_num_of_bits_minus_one;
		while(reduced_bvec.find_ON_bit_to_my_right(prev_ON_bit, cur_ON_bit)){
			write_cnot(w_spec, alias(cur_ON_bit), true, alias_of_full_num_of_bits_minus_one);
			prev_ON_bit = cur_ON_bit;
		}
	}
	
	ending:;	

	#ifdef	_write_verbose_engl_file
		if(w_spec.its_engl_strm_p!=0)*w_spec.its_engl_strm_p<< "}"<<k_endline;
		if(w_spec.its_pict_strm_p!=0)*w_spec.its_pict_strm_p<< "}"<<k_endline;
	#endif

	if(OPTIMIZATIONS::its_extract_d_mat_phases){
		write_ph_factors_of_d_mats(w_spec, k_row_pshift);
	}
			
	#ifdef	_write_verbose_engl_file
		if(w_spec.its_engl_strm_p!=0)*w_spec.its_engl_strm_p<< k_separator<<k_endline;
		if(w_spec.its_pict_strm_p!=0)*w_spec.its_pict_strm_p<< k_separator<<k_endline;
	#endif
}
#endif
#if		_do_lazy_if_central_mat_diagonal
//******************************************
VOID	CENTRAL_MAT::write_if_diagonal(
W_SPEC & 	w_spec)	//io
{
	USHORT	full_num_of_bits = TREE::get_full_num_of_bits();
//	USHORT	full_num_of_bits_minus_one = full_num_of_bits - 1;	
	
	VECTOR<DOUBLE>	angles;
	BOOLEAN			all_zero = all_cs_angles_are_zero(angles);
		
	#ifdef	_write_verbose_engl_file
		write_cs_angles(w_spec, angles);
	#endif
	
	if(all_zero){
		goto ending;
	}
	
	if(full_num_of_bits==0){
		TREE::add_to_cum_phase(angles[0]);
		goto ending;
	}
	
	{
		//this replaces angles by the inverse Hadamard Transform angles	
		inv_had_transform(full_num_of_bits, angles);
		limited_radians(angles);
		
		USHORT		num_of_factors = (1 << full_num_of_bits);
		USHORT		f=1;
		USHORT		prev_ON_bit, cur_ON_bit; //prev=previous, cur = current
		USHORT		cur_rot_bpos=0, prev_active_rot_bpos=0;//rot= rotation
		BIT_VECTOR	cur_bvec(full_num_of_bits, 1);//1 initially
		BIT_VECTOR	prev_active_bvec(full_num_of_bits);//0 by default
		BIT_VECTOR	reduced_bvec(full_num_of_bits);//0 by default
		
		//for first A factor, f = 0, just increase the cummulative phase angle
		TREE::add_to_cum_phase(angles[0]);
		while(f<num_of_factors){
			DOUBLE	ang = angles[cur_bvec.get_dec_rep()];
			if(is_zero(ang)){
				//do nothing
			}else{
				//An active bvec (or rot_bpos) is one for which ang is NOT zero.
				//If cur_rot_bpos equals (doesn't equal) prev_active_rot_bpos,
				//then there is (isn't) cancellation between:
				//(1)the c-nots sigma_x(cur_rot_bpos)^n() 
				//contributed by the right part of the current A factor
				//and
				//(2)the c-nots sigma_x(prev_active_rot_bpos)^n()
				//contributed by the left part of the previous A factor.
				if(cur_rot_bpos==prev_active_rot_bpos){
					reduced_bvec.set_dec_rep( cur_bvec.get_dec_rep() ^ prev_active_bvec.get_dec_rep());
				}else{
					prev_ON_bit = prev_active_rot_bpos;			
					while(prev_active_bvec.find_ON_bit_to_my_right(prev_ON_bit, cur_ON_bit)){
						write_cnot(w_spec, cur_ON_bit, true, prev_active_rot_bpos);
						prev_ON_bit = cur_ON_bit;
					}
					reduced_bvec = cur_bvec;				
				}
				prev_ON_bit = cur_rot_bpos;			
				while(reduced_bvec.find_ON_bit_to_my_right(prev_ON_bit, cur_ON_bit)){
					write_cnot(w_spec, cur_ON_bit, true, cur_rot_bpos);
					prev_ON_bit = cur_ON_bit;
				}

				write_bit_rot(w_spec, z_ax, cur_rot_bpos, ang);
				prev_active_bvec = cur_bvec;
				prev_active_rot_bpos = cur_rot_bpos;				
			}//zero angles if()
			f++;
			cur_bvec.lazy_advance(f);
			//Since we have excluded f=0, f always has at least one ON bit.
			cur_bvec.find_lazy_leftmost_ON_bit(f, cur_rot_bpos);			
		}//f loop
		//Don't forget the leftmost c-nots:
		prev_ON_bit = prev_active_rot_bpos;			
		while(prev_active_bvec.find_ON_bit_to_my_right(prev_ON_bit, cur_ON_bit)){
			write_cnot(w_spec, cur_ON_bit, true, prev_active_rot_bpos);
			prev_ON_bit = cur_ON_bit;
		}
	}
	
	ending:;	
			
	#ifdef	_write_verbose_engl_file
		if(w_spec.its_engl_strm_p!=0)*w_spec.its_engl_strm_p<< "}"<<k_endline<<k_separator<<k_endline;
		if(w_spec.its_pict_strm_p!=0)*w_spec.its_pict_strm_p<< "}"<<k_endline<<k_separator<<k_endline;
	#endif
}
#endif
#pragma mark	------don't_do_lazy------
#if		!(_do_lazy_if_central_mat_not_diagonal)
//******************************************
VOID	CENTRAL_MAT::write_if_not_diagonal(
W_SPEC & 	w_spec)	//io
{

	USHORT	full_num_of_bits = TREE::get_full_num_of_bits();
	ThrowIf_(full_num_of_bits==0);
	USHORT	full_num_of_bits_minus_one = full_num_of_bits - 1;	
	VECTOR<DOUBLE>	angles;

	if(OPTIMIZATIONS::its_extract_d_mat_phases){
		USHORT	control_bpos, rot_bpos;
		BOOLEAN	req_bval;
		if(is_croty90(control_bpos, req_bval, rot_bpos)){	
			its_is_croty90 = true;
			its_croty90_control_bpos = control_bpos;
			its_croty90_req_bval = req_bval;
			its_croty90_rot_bpos = rot_bpos;
			write_ph_factors_of_d_mats(w_spec, k_col_pshift);
			write_cnot(w_spec, control_bpos, req_bval, rot_bpos);
			#ifdef	_write_verbose_engl_file
				if(w_spec.its_engl_strm_p!=0)*w_spec.its_engl_strm_p<< "{"<<k_endline;
				if(w_spec.its_pict_strm_p!=0)*w_spec.its_pict_strm_p<< "{"<<k_endline;
			#endif
			goto ending;
		}else{
			write_ph_factors_of_d_mats(w_spec, k_col_pshift);
		}	
	}
	
	BOOLEAN			all_zero = all_cs_angles_are_zero(angles);
					
	#ifdef	_write_verbose_engl_file
		write_cs_angles(w_spec, angles);
	#endif
	
	if(all_zero){
		goto ending;
	}

	if(full_num_of_bits_minus_one==0){
		write_bit_rot(w_spec, y_ax, 0, angles[0]);
		goto ending;
	}			

	{
		//this replaces angles by the inverse Hadamard Transform angles	
		inv_had_transform(full_num_of_bits_minus_one, angles);
		limited_radians(angles);

		USHORT		num_of_factors = (1 << full_num_of_bits_minus_one);
		USHORT		f;
		USHORT		prev_ON_bit, cur_ON_bit;
		BIT_VECTOR		bvec(full_num_of_bits);//the leftmost bit will always be ON
		USHORT  alias_of_full_num_of_bits_minus_one = alias(full_num_of_bits_minus_one);

		for(f=0; f<num_of_factors; f++){
			DOUBLE	ang = angles[f];
			if(is_zero(ang)){
				//do nothing
			}else{
				//Define a BIT_VECTOR by or-ing f with a mask.
				//Mask is zero at all bpos except at full_num_of_bits_minus_one.				
				bvec.set_dec_rep(f | (1<<full_num_of_bits_minus_one));
				
				prev_ON_bit = full_num_of_bits_minus_one;
							
				while(bvec.find_ON_bit_to_my_right(prev_ON_bit, cur_ON_bit)){
					write_cnot(w_spec, alias(cur_ON_bit), true, alias_of_full_num_of_bits_minus_one);
					prev_ON_bit = cur_ON_bit;
				}
				
				write_bit_rot(w_spec, y_ax, alias_of_full_num_of_bits_minus_one, ang);

				while(bvec.find_ON_bit_to_my_left(prev_ON_bit, cur_ON_bit)){
					write_cnot(w_spec, alias(prev_ON_bit), true, alias_of_full_num_of_bits_minus_one);
					prev_ON_bit = cur_ON_bit;
				}
			}
		}
	}
	
	ending:;	

	#ifdef	_write_verbose_engl_file
		if(w_spec.its_engl_strm_p!=0)*w_spec.its_engl_strm_p<< "}"<<k_endline;
		if(w_spec.its_pict_strm_p!=0)*w_spec.its_pict_strm_p<< "}"<<k_endline;
	#endif

	if(OPTIMIZATIONS::its_extract_d_mat_phases){
		write_ph_factors_of_d_mats(w_spec, k_row_pshift, i);
	}
			
	#ifdef	_write_verbose_engl_file
		if(w_spec.its_engl_strm_p!=0)*w_spec.its_engl_strm_p<< k_separator<<k_endline;
		if(w_spec.its_pict_strm_p!=0)*w_spec.its_pict_strm_p<< k_separator<<k_endline;
	#endif
}
#endif
#if		!(_do_lazy_if_central_mat_diagonal)
//******************************************
VOID	CENTRAL_MAT::write_if_diagonal(
W_SPEC & 	w_spec)	//io
{
	USHORT	full_num_of_bits = TREE::get_full_num_of_bits();
	USHORT	full_num_of_bits_minus_one = full_num_of_bits - 1;	
	
	VECTOR<DOUBLE>	angles;
	BOOLEAN			all_zero = all_cs_angles_are_zero(angles);
					
	#ifdef	_write_verbose_engl_file
		write_cs_angles(w_spec, angles);
	#endif
	
	if(all_zero){
		goto ending;
	}
	
	if(full_num_of_bits==0){
		TREE::add_to_cum_phase(angles[0]);
		goto ending;
	}

	{
		//this replaces angles by the inverse Hadamard Transform angles	
		inv_had_transform(full_num_of_bits, angles);
		limited_radians(angles);
		
		USHORT		num_of_factors = (1 << full_num_of_bits);
		USHORT		f;
		USHORT		prev_ON_bit, cur_ON_bit; //prev=previous, cur = current
		USHORT		leftmost_ON_bit, rot_bpos;
		BIT_VECTOR	bvec(full_num_of_bits);
		
		//for first factor, f = 0, just increase the cummulative phase angle
		TREE::add_to_cum_phase(angles[0]);
		for(f=1; f<num_of_factors; f++){
			DOUBLE	ang = angles[f];
			if(is_zero(ang)){
				//do nothing
			}else{
				bvec.set_dec_rep(f);		
				prev_ON_bit = full_num_of_bits_minus_one;
				//Since we have excluded f=0, f always has at least one ON bit.
				if(!bvec.bit_is_ON(prev_ON_bit)){
					bvec.find_ON_bit_to_my_right(prev_ON_bit, cur_ON_bit);
					prev_ON_bit = cur_ON_bit;
				}		
				leftmost_ON_bit = prev_ON_bit;
				
				while(bvec.find_ON_bit_to_my_right(prev_ON_bit, cur_ON_bit)){
					prev_ON_bit = cur_ON_bit;
				}
				
				rot_bpos = prev_ON_bit;

				prev_ON_bit = leftmost_ON_bit;
				
				while(bvec.find_ON_bit_to_my_right(prev_ON_bit, cur_ON_bit)){
					write_cnot(w_spec, prev_ON_bit, true, rot_bpos);
					prev_ON_bit = cur_ON_bit;
				}

				write_bit_rot(w_spec, z_ax, rot_bpos, ang);

				while(bvec.find_ON_bit_to_my_left(prev_ON_bit, cur_ON_bit)){
					write_cnot(w_spec, cur_ON_bit, true, rot_bpos);
					prev_ON_bit = cur_ON_bit;
				}
			}		
		}
	}
	
	ending:;	
			
	#ifdef	_write_verbose_engl_file
		if(w_spec.its_engl_strm_p!=0)*w_spec.its_engl_strm_p<< "}"<<k_endline<<k_separator<<k_endline;
		if(w_spec.its_pict_strm_p!=0)*w_spec.its_pict_strm_p<< "}"<<k_endline<<k_separator<<k_endline;
	#endif
}
#endif
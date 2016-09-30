#pragma once
#include "prefix2.h"

class D_MAT;
#include "VECTOR.h"
#include "Qbtr_globals.h"
#include "W_SPEC.h"
class BIT_VECTOR;

//mat = matrix
//cum_num_of_elem_ops = cummulative number of elementary operations
//bpos = bit position (0, 1, ..., full_num_of_bits-1)
//	In a bit string, bpos = 0 is the rightmost bit.
//bval = bit value (either 0 or 1)
//rot = rotation
//croty90 = controlled rotation along Y axis by 90 degrees
//req = required

//******************************************
class CENTRAL_MAT
{
private:
	static	LONG	its_cum_num_of_elem_ops;
	BOOLEAN			its_is_identity;
	BOOLEAN			its_is_diagonal;
	USHORT			its_bpos_of_rot;	
	USHORT			its_num_of_d_mats;
	D_MAT  *  *	 	its_d_mats_p_p;

	BOOLEAN			its_is_croty90;
	USHORT			its_croty90_control_bpos;
	BOOLEAN			its_croty90_req_bval;
	USHORT			its_croty90_rot_bpos;
public:
	CENTRAL_MAT(USHORT	level);
	~CENTRAL_MAT();

	static 	LONG	get_cum_num_of_elem_ops();
	static 	VOID	set_cum_num_of_elem_ops(LONG	num);
	BOOLEAN		is_identity() const;
	VOID		set_identity_flag(BOOLEAN  flag);	
	BOOLEAN		is_croty90(USHORT &	control_bpos, BOOLEAN & req_bval, USHORT &	rot_bpos) const;
	D_MAT  &	get_d_mat(USHORT	block);
	BOOLEAN		all_cs_angles_are_zero(VECTOR<DOUBLE>  & 	angles);
	BOOLEAN		all_cs_angles_are_0_or_90_degs() const;
	USHORT		alias(USHORT 	bpos);
	
	VOID	write(W_SPEC &  w_spec);
	VOID	write_cs_angles(W_SPEC &  w_spec, const VECTOR<DOUBLE>  & angles);		

	VOID	write_bit_rot(W_SPEC &  w_spec,
				ROT_AXIS  axis, USHORT	bpos, const DOUBLE  & angle);
	VOID	write_sigma_x(W_SPEC &  w_spec, USHORT flipper_bpos);
	VOID	write_controlled_gate(W_SPEC &  w_spec,
				const VECTOR<USHORT> & control_bpos, const BIT_VECTOR & req_control_bval,
				CGATE_TYPE  type, const DOUBLE &	gate_param);				
	VOID	write_cnot(W_SPEC &  w_spec,
				const VECTOR<USHORT> & control_bpos, const BIT_VECTOR & req_control_bval,
				USHORT flipper_bpos);
	VOID	write_cnot(W_SPEC &  w_spec,
				USHORT the_control_bpos, BOOLEAN the_req_control_bval,
				USHORT flipper_bpos);
	VOID	write_cphase(W_SPEC &  w_spec,
				const VECTOR<USHORT> & control_bpos, const BIT_VECTOR & req_control_bval,
				const DOUBLE &  phase);
				
	VOID	write_ph_factors_of_d_mats(W_SPEC &  w_spec, PH_FACTOR_TYPE ft);	

	VOID	write_if_diagonal(W_SPEC &  w_spec);
	VOID	write_if_not_diagonal(W_SPEC &  w_spec);
		
};	

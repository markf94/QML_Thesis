#include "D_MAT.h"
#include "Qbtr_global_funs.h"
#include "OPTIMIZATIONS.h"

#pragma mark	--creation/destruction--
//******************************************
D_MAT::D_MAT(
USHORT 		num_of_bits)			//in
:its_num_of_bits(num_of_bits)
{
	if(num_of_bits==0){
		its_num_of_cs_angles=1;
	}else{ //num_of_bits >0
		its_num_of_cs_angles= (1 << (num_of_bits-1) );
	}
	
	its_cs_angles.set_to_default_vec(0, its_num_of_cs_angles);	
	
	if(OPTIMIZATIONS::its_extract_d_mat_phases && its_num_of_bits>0){
		its_gen_phases.set_to_default_vec(0, its_num_of_cs_angles);
		its_col_phases.set_to_default_vec(0, its_num_of_cs_angles);
		its_row_phases.set_to_default_vec(0, its_num_of_cs_angles);
	}
}
//******************************************
D_MAT::~D_MAT()
{
	its_num_of_bits=0;
	its_num_of_cs_angles=0;
}
#pragma mark	--simple accessors--
//******************************************
USHORT   D_MAT::get_num_of_bits()
const
{
	return its_num_of_bits;
}
//******************************************
USHORT   D_MAT::get_num_of_cs_angles()
const
{
	return its_num_of_cs_angles;
}
//******************************************
const DOUBLE  &		D_MAT::get_cs_angle(
USHORT	pos)	//in
const
{
	return its_cs_angles[pos];
}
//******************************************
VOID	D_MAT::set_cs_angle(
USHORT	pos,			//in
const DOUBLE  &	 ang)	//in
{
	//pos = position
	its_cs_angles[pos] = ang;
	limited_radians(its_cs_angles[pos]);
}
//******************************************
const DOUBLE  &		D_MAT::get_gen_phase(
USHORT	pos)	//in
const
{
	return its_gen_phases[pos];
}
//******************************************
VOID	D_MAT::set_gen_phase(
USHORT	pos,			//in
const DOUBLE  &	 phase)	//in
{
	//pos = position
	its_gen_phases[pos] = phase;
	limited_radians(its_gen_phases[pos]);
}
//******************************************
const DOUBLE  &		D_MAT::get_col_phase(
USHORT	pos)	//in
const
{
	return its_col_phases[pos];
}
//******************************************
VOID	D_MAT::set_col_phase(
USHORT	pos,			//in
const DOUBLE  &	 phase)	//in
{
	//pos = position
	its_col_phases[pos] = phase;
	limited_radians(its_col_phases[pos]);	
}
//******************************************
const DOUBLE  &		D_MAT::get_row_phase(
USHORT	pos)	//in
const
{
	return its_row_phases[pos];
}
//******************************************
VOID	D_MAT::set_row_phase(
USHORT	pos,			//in
const DOUBLE  &	 phase)	//in
{
	//pos = position
	its_row_phases[pos] = phase;
	limited_radians(its_row_phases[pos]);
}

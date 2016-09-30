#pragma once
#include "prefix2.h"

#include "VECTOR.h"
#include "Qbtr_globals.h"

//For zero bits, the D_MAT is just exp(i*ang)
//so for num_of_bits=0: dim=1, num_of_cs_angles = 1

//Most general complex d matrix:
//D=		[D00   D01]
//			[D10   D11]	
//where D00, D01, D10, D11 are diagonal unitary matrices.


//abbreviations:
//rr = row_phase
//cc = col_phase
//gg = gen_phase

//We express dmats as:
//	
//1 bit case:
//D = diag(1, e^(i*rr[0])) *
//	  [ C0, S0] *
//	  [-S0, C0]
//    e^(i*gg[0]) * 
//    diag(1, e^(i*cc[0]))
//where C0^2 + S0^2 =1, and 
//C0, S0>=0.
//
//2 bit case:
//D = diag[ 1, 1, e^(i*rr[0]), e^(i*rr[1]) ]*
//	  [diag( C0, C1), diag(S0, S1)] *
//	  [diag(-S0,-S1), diag(C0, C1)]
//	  diag[ e^(i*gg[0]), e^(i*gg[1]), e^(i*gg[0]+i*cc[0]), e^(i*gg[1]+ i*cc[1]) ]
//where C0^2 + S0^2 =1, C1^2 + S1^2 =1, and
//C0, C1, S0, S1>=0.


//******************************************
class	D_MAT
{
private:
	USHORT		its_num_of_bits;
	USHORT		its_num_of_cs_angles;
	VECTOR<DOUBLE> 	its_cs_angles; //in radians
	
	VECTOR<DOUBLE> 	its_gen_phases;//in radians
	VECTOR<DOUBLE>	its_col_phases;//in radians
	VECTOR<DOUBLE>  its_row_phases;//in radians

public:
	D_MAT(USHORT  num_of_bits);
	~D_MAT();

	USHORT   			get_num_of_bits() const;
	USHORT   			get_num_of_cs_angles() const;

	const DOUBLE  &			get_cs_angle(USHORT pos) const;
	VOID	 				set_cs_angle(USHORT  pos, const DOUBLE &  ang);
	const DOUBLE  &			get_gen_phase(USHORT pos) const;
	VOID	 				set_gen_phase(USHORT  pos, const DOUBLE & phase);
	const DOUBLE  &			get_col_phase(USHORT pos) const;
	VOID	 				set_col_phase(USHORT  pos, const DOUBLE & phase);
	const DOUBLE  &			get_row_phase(USHORT pos) const;
	VOID	 				set_row_phase(USHORT  pos, const DOUBLE & phase);
};	

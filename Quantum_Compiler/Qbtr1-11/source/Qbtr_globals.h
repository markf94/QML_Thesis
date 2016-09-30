#pragma once


const USHORT	max_ushort = 65535;
const LONG		max_long = 0x7FFFFFFF;  
const DOUBLE	my_pi = 4*atan(1);
const DOUBLE	my_two_pi = 2*my_pi;
const DOUBLE	my_half_pi = my_pi/2;


//alternative:  k_endline = '\r'
const CHAR		k_endline = '\n';
const CHAR  	k_separator[] = "====================";

const DOUBLE	k_norm_delta = 1E-6;

const COMPLEX	k_complex0 = {0,0};
//const COMPLEX	k_complex0(0,0);

enum 	SIDE {left_sd, right_sd};
enum 	ROT_AXIS {y_ax, z_ax};

//cgate = controlled gate
//cnot = controlled not
//cpha = controlled phase
enum 	CGATE_TYPE {k_cnot, k_cpha};
//PH = phase
//pshift = phase shift
enum PH_FACTOR_TYPE {k_row_pshift, k_col_pshift};

//sign adjustments
#define 	_adjust_QR_decompo_signs		1
#if	(_adjust_QR_decompo_signs<0 || _adjust_QR_decompo_signs>2)
	#error	invalid value for adjust_QR_decompo_signs
#endif 


//mainly for debugging:
#define 	_write_verbose_engl_file
#define		_write_cs_decompo_log
#define		_use_n_nbar_in_cphases	0
#pragma once
#include "prefix2.h"

class D_MAT;
#include "Qbtr_globals.h"
#include "VECTOR.h"
class	BIT_VECTOR;
class	PERMUTATION;
class	TRANSPOSITION;


//prototypes for Clapack subroutines
/*
int zggsvd_(char *jobu, char *jobv, char *jobq, integer *m, 
	integer *n, integer *p, integer *k, integer *l, doublecomplex *a, 
	integer *lda, doublecomplex *b, integer *ldb, doublereal *alpha, 
	doublereal *beta, doublecomplex *u, integer *ldu, doublecomplex *v, 
	integer *ldv, doublecomplex *q, integer *ldq, doublecomplex *work, 
	doublereal *rwork, integer *iwork, integer *info);
*/
int zggsvd_(char *jobu, char *jobv, char *jobq, __CLPK_integer *m, 
	__CLPK_integer *n, __CLPK_integer *p, __CLPK_integer *k, __CLPK_integer *l, __CLPK_doublecomplex *a, 
	__CLPK_integer *lda, __CLPK_doublecomplex *b, __CLPK_integer *ldb, __CLPK_doublereal *alpha, 
	__CLPK_doublereal *beta, __CLPK_doublecomplex *u, __CLPK_integer *ldu, __CLPK_doublecomplex *v, 
	__CLPK_integer *ldv, __CLPK_doublecomplex *q, __CLPK_integer *ldq, __CLPK_doublecomplex *work, 
	__CLPK_doublereal *rwork, __CLPK_integer *iwork, __CLPK_integer *info);

/*
int zgemm_(char *transa, char *transb, integer *m, integer * n, 
	integer *k, doublecomplex *alpha, doublecomplex *a, integer *lda, 
	doublecomplex *b, integer *ldb, doublecomplex *beta, doublecomplex *c,
	integer *ldc);
*/

int zgemm_(char *transa, char *transb, __CLPK_integer *m, __CLPK_integer * n, 
	__CLPK_integer *k, __CLPK_doublecomplex *alpha, __CLPK_doublecomplex *a, __CLPK_integer *lda, 
	__CLPK_doublecomplex *b, __CLPK_integer *ldb, __CLPK_doublecomplex *beta, __CLPK_doublecomplex *c,
	__CLPK_integer *ldc);



/*
int zgeqrf_(integer *m, integer *n, doublecomplex *a, 
	integer *lda, doublecomplex *tau, doublecomplex *work, integer *lwork,
	 integer *info);
*/
int zgeqrf_(__CLPK_integer *m, __CLPK_integer *n, __CLPK_doublecomplex *a, 
	__CLPK_integer *lda, __CLPK_doublecomplex *tau, __CLPK_doublecomplex *work, __CLPK_integer *lwork,
	 __CLPK_integer *info);
/*
int zunmqr_(char *side, char *trans, integer *m, integer *n, 
	integer *k, doublecomplex *a, integer *lda, doublecomplex *tau, 
	doublecomplex *c, integer *ldc, doublecomplex *work, integer *lwork, 
	integer *info);
*/
int zunmqr_(char *side, char *trans, __CLPK_integer *m, __CLPK_integer *n, 
	__CLPK_integer *k, __CLPK_doublecomplex *a, __CLPK_integer *lda, __CLPK_doublecomplex *tau, 
	__CLPK_doublecomplex *c__, __CLPK_integer *ldc, __CLPK_doublecomplex *work, __CLPK_integer *lwork,
	 __CLPK_integer *info);

//******************************************
class UNITARY_MAT
{
private:
	USHORT				its_num_of_bits;
	USHORT				its_dim;
	USHORT				its_dim_sq;
	
	COMPLEX	 *			its_array_p;
public:
	VOID	clear();
	VOID	init(USHORT	num_of_bits);
	UNITARY_MAT();
	UNITARY_MAT(USHORT 	num_of_bits);
	~UNITARY_MAT();
	
	USHORT		get_num_of_bits() const;
	USHORT		get_dim() const;
	COMPLEX  & 	operator[](USHORT i);
	COMPLEX  &	entry_at(USHORT row, USHORT col);

	BOOLEAN		is_identity() const;
	VOID		set_to_identity();
//	BOOLEAN		is_permutation(VECTOR<USHORT>  col_to_row_map) const;
	BOOLEAN		is_d_mat(D_MAT *  d_mat_p = 0) const;

	VOID	fill_one_dim_d_mat(D_MAT  &	 d_mat);
	VOID	allocate_and_fill_quadrant_mats(
		COMPLEX  * 	& u00_p,	
		COMPLEX  * 	& u01_p,	
		COMPLEX  *	& u10_p,		
		COMPLEX  *	& u11_p);	
	VOID	limit_cs_angles_to_1st_quad(
			UNITARY_MAT	 &			left1,
			UNITARY_MAT	 &			right1,
			DOUBLE *				ss_p);
	VOID	lighten_right_mats(
		UNITARY_MAT	 &			left0,
		UNITARY_MAT	 &			left1,
		UNITARY_MAT  &			right0,	
		UNITARY_MAT  &			right1,
		const VECTOR<USHORT> & 	degens);
	VOID	write_cs_decompo_log(
		const UNITARY_MAT	 &		left0,
		const UNITARY_MAT	 &		left1,
		const UNITARY_MAT  &		right0,
		const UNITARY_MAT  &		right1,
		const D_MAT  &	 			d_mat) const;	
	VOID	do_cs_decompo(
		UNITARY_MAT	 &		left0,
		UNITARY_MAT	 &		left1,
		UNITARY_MAT  &		right0,
		UNITARY_MAT  &		right1,
		D_MAT  &	 		d_mat);

	VOID	absorb_left_bit_rot(ROT_AXIS axis, USHORT rot_bpos, const DOUBLE  &	angle);
	VOID	absorb_left_sigma_x(USHORT flipper_bpos);
	VOID	absorb_left_controlled_gate(
				const VECTOR<USHORT> & control_bpos, const BIT_VECTOR & req_control_bval,
				CGATE_TYPE  type, const DOUBLE & act_param);
	VOID	absorb_left_cnot(
				const VECTOR<USHORT> & control_bpos, const BIT_VECTOR & req_control_bval,
				USHORT flipper_bpos);
	VOID	absorb_left_cnot(USHORT the_control_bpos, BOOLEAN the_req_control_bval, USHORT flipper_bpos);
	VOID	absorb_phase(const DOUBLE  &  angle);
	VOID	absorb_left_cphase(
				const VECTOR<USHORT> & control_bpos, const BIT_VECTOR &  req_control_bval,
				const DOUBLE  &  phase);	

	VOID	read_controlled_gate_in_english_file(IFSTREAM  *  engl_strm_p, CGATE_TYPE  type);
	VOID	read_english_file(IFSTREAM  *  engl_strm_p);
	VOID	read_components_file(IFSTREAM  *  comp_strm_p);
	VOID	read_decrements_file(IFSTREAM  *  comp_strm_p);
	VOID	write_components_file(OFSTREAM  *  comp_strm_p) const;


	VOID	permute_cols(const PERMUTATION	&	pmut);
	VOID	permute_rows(const PERMUTATION	&	pmut);	
	VOID	permute_bits(const PERMUTATION  &	pmut);
	VOID	transpose_bits(const TRANSPOSITION  &	transp);

};	

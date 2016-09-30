#include 	"UNITARY_MAT.h"
#include 	"Qbtr_globals.h"
#include 	"Qbtr_global_funs.h"
#include 	"D_MAT.h"
#include 	"STRINGY.h"
#include 	"BIT_VECTOR.h"
#include	"PERMUTATION.h"	
#include 	"OPTIMIZATIONS.h"
#include	"DBL_SORTER.h"
#include 	<ctype.h>

extern	STRINGY 	g_mat_name;

#pragma mark	--creation/destruction--
//******************************************
VOID  UNITARY_MAT::clear()
{
	delete [] its_array_p;
	its_array_p=0;	

	its_num_of_bits=0;
	its_dim=0;
	its_dim_sq=0;
}
//******************************************
VOID  UNITARY_MAT::init(
USHORT	num_of_bits)	//in
{
	if(num_of_bits!=its_num_of_bits)clear();
	its_num_of_bits = num_of_bits;

	//For now, we will only admit matrices
	//whose dim is a power of 2.
	//note: if num_of_bits=0, dim=1
	its_dim = (1<<its_num_of_bits);
	its_dim_sq = (1<< 2*its_num_of_bits);		 
	its_array_p = new COMPLEX [its_dim_sq];
}
//******************************************
UNITARY_MAT::UNITARY_MAT()
:its_num_of_bits(0),
its_dim(0),
its_dim_sq(0),
its_array_p(0)
{
}
//******************************************
UNITARY_MAT::UNITARY_MAT(
USHORT 		num_of_bits)			//in
:its_num_of_bits(num_of_bits)
{
	init(num_of_bits);
}	
//******************************************
UNITARY_MAT::~UNITARY_MAT()
{
	clear();
}
#pragma mark	--simple accessors--
//******************************************
USHORT	UNITARY_MAT::get_num_of_bits()
const
{
	return its_num_of_bits;
}
//******************************************
USHORT	UNITARY_MAT::get_dim()
const
{
	return its_dim;
}
//******************************************
COMPLEX  &  UNITARY_MAT::operator[](
USHORT	 i)		//in
{
	ThrowIf_(i>=its_dim_sq);
	return its_array_p[i];
}
//******************************************
COMPLEX  &  	UNITARY_MAT::entry_at(
USHORT	row,	//in
USHORT	col)	//in
{
	USHORT	index = col*its_dim + row;
	ThrowIf_(index>=its_dim_sq);
	return its_array_p[index];
}
#pragma mark	--matrix types--
//******************************************
BOOLEAN		UNITARY_MAT::is_identity()
const
{
	USHORT	col, row, big=0;
	for(col=0; col<its_dim; col++){
		for(row=0; row<its_dim; row++){
			DOUBLE	x = (row==col?1:0);		
			if(	!is_zero(its_array_p[big].real()-x) ||
				!is_zero(its_array_p[big].imag()))return false;
			big++;
		}
	}
	return true;
}
//******************************************
VOID	UNITARY_MAT::set_to_identity()
{
	USHORT	 	col, row, big=0;
	for(col=0; col<its_dim; col++){
		for(row=0; row<its_dim; row++){		
			if(row==col){
				its_array_p[big].real()= 1;
			}else{
				its_array_p[big].real()= 0;
			}
			its_array_p[big].imag()= 0;
			big++;
		}
	}
}	
/*
//******************************************	
BOOLEAN		UNITARY_MAT::is_permutation(
VECTOR<USHORT>	col_to_row_map)	//out
const
{
	col_to_row_map.resize(max_ushort, its_dim);
	USHORT	col, row, big=0;
	for(col=0; col<its_dim; col++){
		for(row=0; row<its_dim; row++){
			DOUBLE	x = its_array_p[big].real();
			DOUBLE	y = its_array_p[big].imag();
			if(is_zero(y)){ //y==0
				if(is_zero(x-1)){//x==1
					if(col_to_row_map[col]==max_ushort){//col not mapped yet
						col_to_row_map[col] = row;
					}else{
						return false;
					}
				}else if(is_zero(x)){//x==0
					//do nothing
				}else{//x!=1, 0
					return false;
				}
			}else{//y!=0
				return false;
			}
			big++;
		}
		if(col_to_row_map[col]==max_ushort){//all col entries are zero
			return false;
		}
	}
	return true;
}
*/
//******************************************
BOOLEAN		UNITARY_MAT::is_d_mat(
D_MAT  *  d_mat_p /* =0 */)		//io
const
{
	//hdim = half of its_dim.	
	USHORT	hdim = (its_dim >> 1);
	ThrowIf_(d_mat_p != 0 && d_mat_p->get_num_of_cs_angles()!=hdim);
	LONG	hdim_sq = hdim*hdim;	

	COMPLEX  * 	u00_p = its_array_p;
	COMPLEX  * 	u10_p = u00_p + hdim;
	COMPLEX  * 	u01_p = its_array_p + 2*hdim_sq;
	COMPLEX  * 	u11_p = u01_p + hdim;

	USHORT	row, col;
	for(col=0; col<hdim; col++){
		for(row=0; row<hdim; row++){
			if(row != col){
				if(	!is_zero(*u00_p) ||
					!is_zero(*u01_p) ||
					!is_zero(*u10_p) ||
					!is_zero(*u11_p)) return false;
			}
			u00_p++;
			u01_p++;
			u10_p++;
			u11_p++;			
		}//row
		u00_p += hdim;
		u01_p += hdim;
		u10_p += hdim;
		u11_p += hdim;
	}//col

	//omit rest of method if d_mat_p==0
	if(d_mat_p==0)return true;
		
	u00_p = its_array_p;
	u10_p = u00_p + hdim;
	u01_p = its_array_p + 2*hdim_sq;
	u11_p = u01_p + hdim;
	
	DOUBLE		mag00, mag01;
	DOUBLE		angle;
	USHORT		dim_plus_1 = its_dim + 1;				
	DOUBLE		ph00, ph01, ph10, ph11;
	DOUBLE		gen_ph, row_ph, col_ph;
	for(row=0; row<hdim; row++){
		mag00 = zmag(*u00_p);
		mag01 = zmag(*u01_p);
		//mag10 = mag01, mag11 = mag00 and mag00^2 + mag01^2 = 1
		BOOLEAN		mag00_is_zero = is_zero(mag00);
		BOOLEAN		mag01_is_zero = is_zero(mag01);
		if(!mag00_is_zero){
			cs_to_radians(u00_p->real()/mag00, u00_p->imag()/mag00, ph00);
			cs_to_radians(u11_p->real()/mag00, u11_p->imag()/mag00, ph11);
		}		
		if(!mag01_is_zero){
			cs_to_radians(u01_p->real()/mag01, u01_p->imag()/mag01, ph01);
			cs_to_radians(u10_p->real()/mag01, u10_p->imag()/mag01, ph10);
		}
		if(mag00_is_zero){
			gen_ph = ph10 + my_pi;
			col_ph = ph01 - gen_ph;
			row_ph = 0;
		}else if(mag01_is_zero){
			gen_ph = ph00;
			col_ph = ph11 - gen_ph;
			row_ph = 0;
		}else{
			gen_ph = ph00;
			col_ph = ph01 - gen_ph;
			row_ph = ph10 + my_pi - gen_ph;
		}
		d_mat_p->set_gen_phase(row, gen_ph);//d_mat call
		d_mat_p->set_row_phase(row, row_ph);//d_mat call
		d_mat_p->set_col_phase(row, col_ph);//d_mat call
		
		cs_to_radians(mag00, mag01, angle);
		d_mat_p->set_cs_angle(row, angle);//d_mat call
		
		u00_p += dim_plus_1;
		u01_p += dim_plus_1;
		u10_p += dim_plus_1;
		u11_p += dim_plus_1;
	}//row		
	return true;
}
#pragma mark	--cs decomposition--
//******************************************
VOID  UNITARY_MAT::fill_one_dim_d_mat(
D_MAT  &	 d_mat)		//out
{
	//The do_cs_decompo() method 
	//degenerates into this method when "this" is 1-dim
	ThrowIf_(d_mat.get_num_of_bits()!=0);
	ThrowIf_(its_num_of_bits!=0);
	DOUBLE	angle;
	cs_to_radians(its_array_p[0].real(), its_array_p[0].imag(), angle);
	d_mat.set_cs_angle(0, angle);
	
}
//******************************************
VOID	UNITARY_MAT::allocate_and_fill_quadrant_mats(
COMPLEX  * 	& u00_p,		//out
COMPLEX  * 	& u01_p,		//out
COMPLEX  *	& u10_p,		//out	
COMPLEX  *	& u11_p)		//out	
{
	ThrowIf_(u00_p!=0 || u10_p!=0 || u01_p!=0 || u11_p!=0);
	ThrowIf_(its_dim==1);	
	//hdim = half of its_dim.	
	USHORT	hdim = (its_dim >> 1);
	USHORT	hdim_sq = hdim*hdim;	
	
	u00_p = new COMPLEX [hdim_sq];
	u10_p = new COMPLEX [hdim_sq];
	u01_p = new COMPLEX [hdim_sq];	
	u11_p = new COMPLEX [hdim_sq];	

	COMPLEX  * uxx_ptr = u00_p;
	COMPLEX  * u_ptr = its_array_p;
	USHORT col, row;
	for(col=0; col<hdim; col++){
		for(row=0; row<hdim; row++){
			*uxx_ptr = *u_ptr;
			uxx_ptr++;
			u_ptr++;
		}
		u_ptr += hdim;
	}

	uxx_ptr = u10_p;
	u_ptr = its_array_p + hdim;
	for(col=0; col<hdim; col++){
		for(row=0; row<hdim; row++){
			*uxx_ptr = *u_ptr;
			uxx_ptr++;
			u_ptr++;
		}
		u_ptr += hdim;
	}

	uxx_ptr = u01_p;
	u_ptr = its_array_p + 2*hdim_sq;
	for(col=0; col<hdim; col++){
		for(row=0; row<hdim; row++){
			*uxx_ptr = *u_ptr;
			uxx_ptr++;
			u_ptr++;
		}
		u_ptr += hdim;
	}

	uxx_ptr = u11_p;
	u_ptr = its_array_p + 2*hdim_sq + hdim;
	for(col=0; col<hdim; col++){
		for(row=0; row<hdim; row++){
			*uxx_ptr = *u_ptr;
			uxx_ptr++;
			u_ptr++;
		}
		u_ptr += hdim;
	}
}
//******************************************
VOID	UNITARY_MAT::limit_cs_angles_to_1st_quad(
UNITARY_MAT	 &			left1,	//io
UNITARY_MAT	 &			right1,	//io
DOUBLE *				ss_p)	//io
{
	//Assume cc_p[i]>=0 for all i.
	//For each i, the i'th angle is in
	//either the 1st(i.e., ss_p[i]>=0)
	//or 4th quadrant(i.e., ss_p[i]<0).
	//This method makes ss_p[i]>=0 for all i.
	USHORT	row, col;
	USHORT	dim = left1.get_dim();
	VECTOR<USHORT>	angle_is_neg(0, dim);
	for(row=0; row<dim; row++){
		if(ss_p[row]<0){
			angle_is_neg[row] = 1;
			change_sign(ss_p[row]);
		}
	}

	for(col=0; col<dim; col++){
		if(angle_is_neg[col]){
			for(row=0; row<dim; row++){
				change_sign(left1.entry_at(row, col));
			}
		}
	} 

	for(row=0; row<dim; row++){
		if(angle_is_neg[row]){
			for(col=0; col<dim; col++){
				change_sign(right1.entry_at(row, col));
			}
		}
	} 
}
//******************************************
VOID	UNITARY_MAT::lighten_right_mats(
UNITARY_MAT	 &			left0,				//io
UNITARY_MAT	 &			left1,				//io
UNITARY_MAT  &			right0,				//io
UNITARY_MAT  &			right1,				//io
const VECTOR<USHORT> & 	degens) 			//in
{
	//degens = cs angle degeneracies
	//Say G = diag(G_0, G_1, ..., G_{M-1})
	//where G_i is a d_i by d_i matrix, 
	//and d_i is the degeneracy of the i-th cs angle.
	//G_i is the Q matrix obtained by doing
	//a QR decomposition on the d_i rows of right0
	//that correspond to the ith cs angle.
	//This method replaces
	//	right0 by G*right0
	//	right1 by G*right1
	//	left0 by left0*G^H
	//	left1 by left1*G^H
	//The diagonal elements of the R in 
	//each QR decomposition are real,
	//but possibly negative. 
	//If _adjust_QR_decompo_signs==0, then they
	//are left like that.
	//If _adjust_QR_decompo_signs==1, then they
	//are made all non-negative.
	//If _adjust_QR_decompo_signs==2, then they
	//are adjusted so that the real parts of the 
	//diagonal elements of right0 
	//are all non-negative.
	
	//Read the comments at the beginning of "zgeqrf.c" and "zunmqr". 


	USHORT	degen_len = degens.get_len();

	//arguments of zgeqrf_()
	LONG			degen;//in (takes place of m in clapack)
	LONG			dim = right0.get_dim();//in (takes place of n in clapack)
	LONG			dim_sq = dim*dim;
	COMPLEX *		a_p = new COMPLEX [dim_sq];//io
	LONG			lda;//in
	COMPLEX	*		tau_p =  new COMPLEX [dim];//out
	COMPLEX *		work_p = new COMPLEX [dim_sq];//worksp, out
	LONG			lwork = dim_sq;//in
	LONG			info;//out
	
	//arguments of zunmqr_()
	CHAR			side;//in  (L or R)
	CHAR			trans;//in  (N or C)
	//LONG			m;//in
	//LONG			n;//in
	LONG			k;//in
	//COMPLEX *		a_p;//in
	//LONG			lda;//in
	//COMPLEX *		tau_p;//in
	COMPLEX *		c_p = new COMPLEX [dim_sq];//io
	LONG			ldc;//in
	//COMPLEX *		work_p;//worksp, out
	//LONG			lwork;//in
	//LONG			info;//out
	
	LONG	i, row, col, big;
	LONG 	first_row = 0;
	LONG	next_first_row = 0;
	degen=0;
	COMPLEX	*	uu_p;
	#if	_adjust_QR_decompo_signs != 0
		VECTOR<USHORT> row_is_neg(0, dim);
	#endif
	BOOLEAN		change_row_sign = false;	
	for(i=0; i<degen_len; i++){
		first_row = next_first_row;
		degen = lda = degens[i];
		next_first_row += degen;
		big = 0;
		for(col=0; col<dim; col++){
			for(row=first_row; row<next_first_row; row++){
				a_p[big] = right0.entry_at(row, col);
				c_p[big] = right1.entry_at(row, col);
				big++;
			}
		}
		zgeqrf_(&degen, &dim, a_p, &lda, tau_p, work_p, &lwork, &info);
		#if	_adjust_QR_decompo_signs != 0
			#if	_adjust_QR_decompo_signs==1
				big = 0;
			#else if _adjust_QR_decompo_signs==2
				big = first_row*degen;
				//example:
				//--i=0--
				//	0  	2	4
				//	1	3	5
				//--i=1--
				//	0	3	6
				//	1	4	7
				//	2	5	8
				//--i=2--
				//suppose i=1, first_row = 2, degen=3
				//big = 2*3 = 6
			#endif
			for(row=first_row; row<next_first_row; row++){
				if(a_p[big].real()<0){
					row_is_neg[row]=1;
				}else{
					row_is_neg[row]=0;
				}
				big +=(degen + 1);
			}
		#endif
		k = degen;
		side = 'L';
		trans = 'C';
		ldc = degen;
		zunmqr_(&side, &trans, &degen, &dim, &k, a_p, &lda, tau_p, 
				c_p, &ldc, work_p, &lwork, &info);
		big=0;
		for(col=0; col<dim; col++){
			for(row=first_row; row<next_first_row; row++){
				#if	_adjust_QR_decompo_signs != 0
					change_row_sign = row_is_neg[row];
				#endif
				if(row>(col + first_row)){
					right0.entry_at(row, col) = k_complex0;
				}else{
					if(!change_row_sign){
						right0.entry_at(row, col) = a_p[big];
					}else{
						right0.entry_at(row, col).real()= -a_p[big].real();
						right0.entry_at(row, col).imag()= -a_p[big].imag();
					}
				}
				if(!change_row_sign){
					right1.entry_at(row, col) = c_p[big];
				}else{
					right1.entry_at(row, col).real()= -c_p[big].real();
					right1.entry_at(row, col).imag()= -c_p[big].imag();
				}
				big++;
			}
		}
		side = 'R';
		trans = 'N';
		ldc = dim;
		uu_p = left0.its_array_p + first_row*dim;
		zunmqr_(&side, &trans, &dim, &degen, &k, a_p, &lda, tau_p, 
				uu_p, &ldc, work_p, &lwork, &info);
		
		uu_p = left1.its_array_p + first_row*dim;
		zunmqr_(&side, &trans, &dim, &degen, &k, a_p, &lda, tau_p, 
				uu_p, &ldc, work_p, &lwork, &info);
	}

	#if	_adjust_QR_decompo_signs != 0
		big=0;
		for(col=0; col<dim; col++){
			BOOLEAN		change_col_sign = row_is_neg[col];
			for(row=0; row<dim; row++){
				if(change_col_sign){
					change_sign(left0.its_array_p[big]);
					change_sign(left1.its_array_p[big]);
				}
				big++;
			}
		}
	#endif
	
	delete [] a_p;
	delete [] tau_p;
	delete [] work_p;
	delete [] c_p;
}
//******************************************
VOID	UNITARY_MAT::write_cs_decompo_log(
const UNITARY_MAT	 &		left0,		//in
const UNITARY_MAT	 &		left1,		//in
const UNITARY_MAT  &		right0,		//in
const UNITARY_MAT  &		right1,		//in
const D_MAT  &	 			d_mat)		//in
const
{
	//this method is mainly for debugging
	
	OFSTREAM  		cs_strm;
	const CHAR *	fname = (g_mat_name && "-log.out").get_string();
	//Open a new log file the first time this method is called.
	//For subsequent calls, append to the log file.
	static	BOOLEAN		first_time = true;
	if(first_time){
		cs_strm.open(fname);
		first_time = false;
	}else{
		cs_strm.open(fname, ios::out | ios::app);
	}
	
	cs_strm<<fixed<<showpoint<<setprecision(9);
	cs_strm<<"//------------------------------------------------"<<k_endline;
	
	cs_strm<<"//-----------input matrix"<<k_endline;
	this->write_components_file(&cs_strm);
	
	cs_strm<<"//-----------left0"<<k_endline;
	left0.write_components_file(&cs_strm);
	
	cs_strm<<"//-----------left1"<<k_endline;
	left1.write_components_file(&cs_strm);

	cs_strm<< "//-----------angles:"<<k_endline;
	for(USHORT k=0; k<d_mat.get_num_of_cs_angles(); k++){
		cs_strm<<'\t'<<d_mat.get_cs_angle(k)*180/my_pi;
	}	
	cs_strm<<k_endline;
	
	cs_strm<<"//-----------right0"<<k_endline;
	right0.write_components_file(&cs_strm);
	
	cs_strm<<"//-----------right1"<<k_endline;
	right1.write_components_file(&cs_strm);

	cs_strm.close();
}
//******************************************
VOID	UNITARY_MAT::do_cs_decompo(
UNITARY_MAT	 &		left0,		//out
UNITARY_MAT	 &		left1,		//out
UNITARY_MAT  &		right0,		//out
UNITARY_MAT  &		right1,		//out
D_MAT  &	 		d_mat)		//out
{
	//decompo = decomposition
	//cs = cosine sine
	
	//		[u00	u01]   [left0		 ] [cc     ss] [right0         ]
	//	u=  [          ] = [			 ] [		 ] [			   ]
	//		[u10	u11]   [		left1] [-ss    cc] [         right1]

	//Read the comments at the beginning of "zggsvd.c"

	ThrowIf_(its_dim==1);	
	//hdim = half of its_dim.	
	USHORT	hdim = (its_dim >> 1);
	USHORT	hdim_sq = hdim*hdim;	
	
	//This function assumes that memory of the correct size
	//has been allocated for all the outputs. 
	ThrowIf_(left0.get_dim()!=hdim);
	ThrowIf_(left1.get_dim()!=hdim);
	ThrowIf_(right0.get_dim()!=hdim);
	ThrowIf_(right1.get_dim()!=hdim);
	ThrowIf_(d_mat.get_num_of_cs_angles()!=hdim);

	COMPLEX  * 	u00_p = 0;
	COMPLEX  * 	u01_p = 0;
	COMPLEX  *	u10_p = 0;	
	COMPLEX  *	u11_p = 0;	
	
	allocate_and_fill_quadrant_mats(u00_p, u01_p, u10_p, u11_p);

	CHAR  			jobu = 'U';		//in
	CHAR  			jobv = 'V';		//in	
	CHAR 			jobq = 'Q';		//in
	LONG			m;				//in  
	LONG			n;				//in
	LONG			p;				//in
	LONG			k=0;		//out
	LONG			l=0;		//out
	COMPLEX  *		a_p=0; 			//in
	LONG			lda;			//in
	COMPLEX  *		b_p=0;			//in
	LONG			ldb;			//in
	DOUBLE  *		cc_p=0;		//out 		called alpha in clapack
	DOUBLE  *		ss_p=0;		//out		called beta in clapack
	COMPLEX  *		uu_p=0;		//out
	LONG			ldu;			//in
	COMPLEX  *		vv_p=0;		//out
	LONG			ldv;			//in
	COMPLEX  *		q_p=0;		//out
	LONG			ldq;			//in
	COMPLEX  *		work_p=0;	//worksp
	DOUBLE  *		rwork_p=0;	//worksp
	LONG  *			iwork_p=0;	//worksp
	LONG			info;		//out
	
	m = n = p = lda = ldb = ldu = ldv = ldq = hdim;
	
	a_p = u00_p;
	b_p = u10_p;	
	cc_p = new DOUBLE [hdim];	
	ss_p = new DOUBLE [hdim];	
	uu_p = left0.its_array_p;
	vv_p = left1.its_array_p;	
	q_p = new COMPLEX [hdim_sq];
	work_p = new COMPLEX [4*hdim];	
	rwork_p = new DOUBLE [2*hdim];	
	iwork_p = new LONG [hdim];
			
	zggsvd_(
		&jobu, &jobv, &jobq,
	   	&m, &n, &p,
	   	&k, &l,
	   	a_p, &lda,
	   	b_p, &ldb,
	   	cc_p, ss_p,
		uu_p, &ldu,
		vv_p, &ldv,
		q_p, &ldq,
		work_p, rwork_p, iwork_p,
		&info);
	//My sign convention is different from zggsvd.
	//For me, bottom-left of D matrix is -S matrix.
	//Therefore, ss_p as given by zggsvd must be patched up.
	USHORT row;
	for(row=0; row<hdim; row++){
		change_sign(ss_p[row]);
	}
	//My convention for the ordering of the rows of D2 is different from zggsvd.
	//For me, the S matrix is at bottom-right corner of D2 instead of top-right.
	//Therefore, left1 as given by zggsvd must be patched up.
	//Rearrange its columns by moving the last k columns to front.
	
	//First save current left1. Save it in u10, 
	//since u10's original data is not going to be used anymore.
	USHORT	col;
	COMPLEX * 	uxx_ptr = u10_p;
	COMPLEX * 	l_ptr = left1.its_array_p;
	for(col=0; col<hdim; col++){
		for(row=0; row<hdim; row++){
			*uxx_ptr = *l_ptr;
			uxx_ptr++;
			l_ptr++;
		}
	}
	//Now permute columns of left1.
	for(col=0; col<hdim; col++){
		LONG 	new_col = (col + k< hdim ? col + k: (col + k) - hdim);
		l_ptr = left1.its_array_p + col*hdim;
		uxx_ptr = u10_p + new_col*hdim;
		for(row=0; row<hdim; row++){
			*l_ptr = *uxx_ptr;
			uxx_ptr++;
			l_ptr++;
		}
	}
	

	//Calculate right0 as times R q^{H}.

	CHAR Stransa = 'N';				//in
	CHAR Stransb = 'N';				//in
	LONG Sm;						//in
	LONG Sn;						//in
	LONG Sk;						//in
	COMPLEX Salpha= {1,0};			//in
//	COMPLEX Salpha(1,0);			//in
	COMPLEX  *	Sa_p = 0;			//in
	LONG Slda;						//in 
	COMPLEX  * Sb_p = 0;			//in
	LONG Sldb;						//in
	COMPLEX Sbeta = {0,0};			//in
//	COMPLEX Sbeta(0,0);				//in
	COMPLEX  * Sc_p = 0;		//out
	LONG Sldc;						//in

	Sm = Sn = Sk = Slda = Sldb = Sldc = hdim;
	//zggsvd() put into u00 the upper triangular matrix R.
	Sa_p = u00_p; 
	//Use u10 since u10's original data is not going to be used anymore.
	Sb_p = u10_p; 

	//Insert into Sb_p the Hermitian of q_p
	for(col=0; col<hdim; col++){
		for(row=0; row<hdim; row++){
			Sb_p[hdim*row+col].real()= q_p[hdim*col+row].real();
			Sb_p[hdim*row+col].imag()= -q_p[hdim*col+row].imag();
		}
	}
	Sc_p = right0.its_array_p;

	zgemm_(
		&Stransa, &Stransb,
		&Sm, &Sn, &Sk,
		&Salpha,
		Sa_p, &Slda, 
		Sb_p, &Sldb,
		&Sbeta,
		Sc_p, &Sldc);
		
	//Can calculate right1 as 
	//(ss^{-1})(left0^{H}) u01  if ss!=0
	//or (cc^{-1})(left1^{H}) u11  if cc!=0

	Sa_p = q_p;
	//insert into Sa_p the hermitian of left0
	for(col=0; col<hdim; col++){
		for(row=0; row<hdim; row++){
			Sa_p[hdim*row+col].real()= left0.its_array_p[hdim*col+row].real();
			Sa_p[hdim*row+col].imag()= -left0.its_array_p[hdim*col+row].imag();
		}
	}
	Sb_p = u01_p;
	//use u00 to store (left0^{H}) u01
	Sc_p = u00_p;	

	zgemm_(
		&Stransa, &Stransb,
		&Sm, &Sn, &Sk,
		&Salpha,
		Sa_p, &Slda, 
		Sb_p, &Sldb,
		&Sbeta,
		Sc_p, &Sldc);	

	Sa_p = q_p;
	//insert into Sa_p the Hermitian of left1
	for(col=0; col<hdim; col++){
		for(row=0; row<hdim; row++){
			Sa_p[hdim*row+col].real()= left1.its_array_p[hdim*col+row].real();
			Sa_p[hdim*row+col].imag()= -left1.its_array_p[hdim*col+row].imag();
		}
	}
	Sb_p = u11_p;
	//use u10 to store (left1^{H}) u11
	Sc_p = u10_p;	

	zgemm_(
		&Stransa, &Stransb,
		&Sm, &Sn, &Sk,
		&Salpha,
		Sa_p, &Slda, 
		Sb_p, &Sldb,
		&Sbeta,
		Sc_p, &Sldc);	

	for(row=0; row<hdim; row++){
		COMPLEX  *  r1_ptr = right1.its_array_p + row;
		COMPLEX  *  top_ptr = u00_p + row;
		COMPLEX  *  bot_ptr = u10_p + row;
		DOUBLE c = cc_p[row];
		DOUBLE s = ss_p[row];
		if(s*s > c*c){
			//calculate this row of right1 as (ss^{-1})(left0^{H}) u01 
			for(col=0; col<hdim; col++){
				(*r1_ptr).real()= (*top_ptr).real()/s;
				(*r1_ptr).imag()= (*top_ptr).imag()/s;
				r1_ptr += hdim;
				top_ptr += hdim;
			}

		}else{
			//calculate this row of right1 as (cc^{-1})(left1^{H}) u11 
			for(col=0; col<hdim; col++){
				(*r1_ptr).real()= (*bot_ptr).real()/c;
				(*r1_ptr).imag()= (*bot_ptr).imag()/c;
				r1_ptr += hdim;
				bot_ptr += hdim;
			}			
		}						
	}

	//check assumptions about zggsvd()
	for(row=0; row<hdim; row++){
		//Should have cc_p >=0
		SignalIf_(cc_p[row]<0);
	}

	//this makes all ss_p >=0 while keeping cc_p signs the same
	limit_cs_angles_to_1st_quad(left1, right1,	ss_p);

	VECTOR<DOUBLE>	cs_angles(0, hdim);
	for(row=0; row<hdim; row++){
		cs_to_radians(cc_p[row], ss_p[row], cs_angles[row]);
	}

	if(OPTIMIZATIONS::its_lighten_right_mats){	
		DBL_SORTER		sorter(&cs_angles);
		PERMUTATION		pmut(hdim);
		sorter.sort(pmut);//sort cs_angles in increasing order
		
		if(!pmut.is_identity()){
			left0.permute_cols(pmut);
			left1.permute_cols(pmut);
			right0.permute_rows(pmut);
			right1.permute_rows(pmut);
		}
		
		VECTOR<USHORT>	degens;
		find_num_of_distinct_entries(cs_angles, &degens);
		lighten_right_mats(left0, left1, right0, right1, degens);
	}	
	 
	for(row=0; row<hdim; row++){
		d_mat.set_cs_angle(row, cs_angles[row]);
	}
	
			
	delete [] u00_p;
	delete [] u10_p;	
	delete [] u01_p;	
	delete [] u11_p;
	delete [] cc_p;
	delete [] ss_p;	
	delete [] q_p;
	delete [] work_p;	
	delete [] rwork_p;	
	delete [] iwork_p;


	#ifdef _write_cs_decompo_log			
		write_cs_decompo_log(left0, left1, right0, right1, d_mat);
	#endif

}	
	
#pragma mark --multiplication by elementary gates--
//******************************************
VOID	UNITARY_MAT::absorb_left_bit_rot(
ROT_AXIS			axis,		//in
USHORT				rot_bpos,	//in
const DOUBLE &		angle)		//in
{
	//rot_bpos = rotation bit position
	
	UNITARY_MAT   small_mat(1);
	DOUBLE	cc = cos(angle);
	DOUBLE	ss = sin(angle);
	if(axis==y_ax){
		small_mat[0].real()= small_mat[3].real()= cc;
		small_mat[1].real()= -ss;
		small_mat[2].real()= ss;
		for(USHORT i=0; i<4;i++){
			small_mat[i].imag()= 0;
		}
	}else if(axis==z_ax){
		small_mat[0].real()= small_mat[3].real()= cc;
		small_mat[0].imag()= ss;
		small_mat[3].imag()= -ss;
		small_mat[1].real()= small_mat[1].imag()=0;
		small_mat[2].real()= small_mat[2].imag()=0;
	}else{
		ThrowIf_(true);
	}

	USHORT	mask = (1<<rot_bpos);
	
	USHORT		small_row;
	USHORT		col, row, row1, row2;
	
	COMPLEX  * 	col_vec_p = new COMPLEX[its_dim];
	ThrowIfNil_(col_vec_p);
	//deleted at end of this method
	
	for(col = 0; col<its_dim; col++){
		for(row = 0; row<its_dim; row++){
			if((row & mask) == 0){ //row has 0 at rot_bpos
		 		//row =...0...
		 		small_row = 0;
	 			row1 = row; //row1 =...0...
		 		row2 = (row1 | mask); //row2 =...1...
			}else{ //row has 1 at rot_bpos
		 		//row =...1...
		 		small_row = 1;
		 		row1 = (row & ~mask); //row1 =...0...		
		 		row2 = row; //row2 =...1...
		 	}
		 	col_vec_p[row] = 	small_mat.entry_at(small_row, 0)*entry_at(row1, col)  
								+ small_mat.entry_at(small_row, 1)*entry_at(row2, col);
							
		}//row loop
		for(row = 0; row<its_dim; row ++){
			entry_at(row, col) = col_vec_p[row];
		}//row loop
	}//col loop
		
	delete [] col_vec_p;
}
//******************************************
VOID	UNITARY_MAT::absorb_left_sigma_x(
USHORT		flipper_bpos)	//in
{
	//sigma_x is a degenerate case of cnot
	USHORT	mask_for_flipper = (1<<flipper_bpos);
	
	USHORT 	col, row;
			
	COMPLEX  * 	col_vec_p = new COMPLEX[its_dim];
	ThrowIfNil_(col_vec_p);
	//deleted at end of this method
	
	for(col = 0; col<its_dim; col ++){
		for(row = 0; row<its_dim; row ++){
			col_vec_p[row] = entry_at(row ^ mask_for_flipper, col);
		}
		for(row = 0; row<its_dim; row ++){
			entry_at(row, col) = col_vec_p[row];
		}
	}
	
	delete [] col_vec_p;
}
//******************************************
VOID	UNITARY_MAT::absorb_left_controlled_gate(
const VECTOR<USHORT> &		control_bpos,		//in
const BIT_VECTOR  & 		req_control_bval,	//in
CGATE_TYPE					type,				//in
const DOUBLE &				gate_param)			//in
{
	//bpos = bit position
	//bval = bit value
	//req = required
	//param = parameter
	USHORT		flipper_bpos;
	USHORT		mask_for_flipper;
	DOUBLE		phase;
	COMPLEX		z;
	if(type==k_cnot){
		flipper_bpos = (USHORT)gate_param;
		mask_for_flipper = (1<<flipper_bpos);
	}else if(type==k_cpha){
		phase = gate_param;
		z.real()= cos(phase);
		z.imag()= sin(phase);
	}else{
		ThrowIf_(true);
	}
		
	USHORT	num_of_controls = control_bpos.get_len();
	ThrowIf_(num_of_controls!=req_control_bval.get_len());
	ThrowIf_(num_of_controls==0);

	USHORT 		col, row;
	BOOLEAN	 	do_flip;
			
	COMPLEX  * 	col_vec_p = new COMPLEX[its_dim];
	ThrowIfNil_(col_vec_p);
	//deleted at end of this method
	
	for(col = 0; col<its_dim; col ++){
		for(row = 0; row<its_dim; row ++){
			do_flip = true;
			for(USHORT	c=0; c<num_of_controls; c++){
				if(req_control_bval.bit_is_ON(c)!=((row>>control_bpos[c])&1)){
					do_flip = false;
					break;
				}
			}
			if(do_flip){
				if(type==k_cnot){
					col_vec_p[row] = entry_at(row ^ mask_for_flipper, col);
				}else{//type==k_cpha
					col_vec_p[row] = z*entry_at(row, col);
				}	
			}else{
				col_vec_p[row] = entry_at(row, col);				
			}
		}
		for(row = 0; row<its_dim; row ++){
			entry_at(row, col) = col_vec_p[row];
		}
	}
	
	delete [] col_vec_p;
}
//******************************************
VOID	UNITARY_MAT::absorb_left_cnot(
const VECTOR<USHORT> &		control_bpos,		//in
const BIT_VECTOR  & 		req_control_bval,	//in
USHORT						flipper_bpos)		//in
{
	absorb_left_controlled_gate(control_bpos, req_control_bval,
		k_cnot, (DOUBLE)flipper_bpos);
}
//******************************************
VOID	UNITARY_MAT::absorb_left_cnot(
USHORT		the_control_bpos,		//in
BOOLEAN		the_req_control_bval,	//in
USHORT		flipper_bpos)			//in
{
	VECTOR<USHORT>	control_bpos(the_control_bpos/*val*/, 1 /*len*/);
	BIT_VECTOR		req_control_bval(1/*len*/, (USHORT)the_req_control_bval/*val*/);
	absorb_left_cnot(control_bpos, req_control_bval, flipper_bpos);
}
//******************************************
VOID	UNITARY_MAT::absorb_phase(
const DOUBLE   &  angle)		//in
{
	COMPLEX	zz;
	zz.real()= cos(angle);
	zz.imag()= sin(angle);
	
	for(USHORT	index=0; index<its_dim_sq; index++){
		its_array_p[index] = zz*its_array_p[index];
	}	
}		
//******************************************
VOID	UNITARY_MAT::absorb_left_cphase(
const VECTOR<USHORT> &		control_bpos,		//in
const BIT_VECTOR  & 		req_control_bval,	//in
const DOUBLE &				phase)				//in
{
	absorb_left_controlled_gate(control_bpos, req_control_bval,
		k_cpha, phase);
}
#pragma mark --i/o--	
//******************************************
VOID  UNITARY_MAT::read_controlled_gate_in_english_file(
IFSTREAM  *  		engl_strm_p,	//io
CGATE_TYPE			type)			//in
{
	USHORT			c;
	CHAR 			ch;
	STRINGY			sgy;
	VECTOR<USHORT>	control_bpos;
	BIT_VECTOR		req_control_bval;	
	USHORT			flipper_bpos;
	DOUBLE			phase;
	
	c=0;
	control_bpos.resize(0, BIT_VECTOR::max_len);				
	req_control_bval.set_len(BIT_VECTOR::max_len);
	*engl_strm_p>>phase; 
	control_bpos[0] = (USHORT)phase;
	my_get(*engl_strm_p, ch);		
	while(ch!=k_endline){
		if(isspace(ch)){
			//do nothing
		}else{
			engl_strm_p->putback(ch);
			*engl_strm_p>>sgy;
			if(sgy=="T"){
				req_control_bval.set_bit_ON(c);
			}else if(sgy=="F"){
				req_control_bval.set_bit_OFF(c);
			}
			c++;
			*engl_strm_p>> phase; 
			control_bpos[c] = (USHORT)phase;	
		}
		my_get(*engl_strm_p, ch);
	}
	//There should be at least one control.
	ThrowIf_(c==0);
	if(type==k_cnot){
		flipper_bpos = control_bpos[c];
	}
	req_control_bval.set_len(c);
	control_bpos.resize(0, c);
	if(type==k_cnot){				
		absorb_left_cnot(control_bpos, req_control_bval, flipper_bpos);
	}else{//type==k_cpha
		absorb_left_cphase(control_bpos, req_control_bval, phase*my_pi/180);
	}
}
//******************************************
VOID  UNITARY_MAT::read_english_file(
IFSTREAM  *  engl_strm_p)	//io
{
	USHORT	num_of_bits; 
	*engl_strm_p>>num_of_bits; engl_strm_p->ignore(500, k_endline); 
	init(num_of_bits);
	set_to_identity();
	
	STRINGY			gate_name;
	BOOLEAN			read_endline;	
	USHORT			flipper_bpos;	
	DOUBLE 			angle;
	ROT_AXIS		axis;
	USHORT			rot_bpos;

	engl_strm_p->exceptions(ios::badbit | ios::failbit);
	try{
		while(engl_strm_p->peek()!=EOF){
			*engl_strm_p>>gate_name;
			//all except CNOT and CPHA require read_endline
			read_endline=true;
			if(gate_name=="ROTY"){
				axis = y_ax;
				*engl_strm_p>>rot_bpos>>angle;
				absorb_left_bit_rot(axis, rot_bpos, angle*my_pi/180);
			}else if(gate_name=="ROTZ"){
				axis = z_ax;
				*engl_strm_p>>rot_bpos>>angle;
				absorb_left_bit_rot(axis, rot_bpos, angle*my_pi/180);				
			}else if(gate_name=="SIGX"){
				*engl_strm_p>>flipper_bpos;
				absorb_left_sigma_x(flipper_bpos);
			}else if(gate_name=="CNOT"){
				read_controlled_gate_in_english_file(engl_strm_p, k_cnot);
				read_endline=false;
			}else if(gate_name=="PHAS"){
				*engl_strm_p>>angle;
				absorb_phase(angle*my_pi/180);
			}else if(gate_name=="CPHA"){
				read_controlled_gate_in_english_file(engl_strm_p, k_cpha);
				read_endline=false;
			}else if(gate_name=="{" || gate_name=="}" || gate_name==k_separator){
				//do nothing
			}else{
				break;
			}
			if(read_endline)engl_strm_p->ignore(500, k_endline);
		}		
	}
	
	catch(END_OF_FILE){}	

	catch(const ios::failure  &  io_exc){
		cerr<<"'mat_name-engl.out' file is illegal.";
		exit(-1);
	}
}
//******************************************
VOID  UNITARY_MAT::read_components_file(
IFSTREAM  *  comp_strm_p)	//io
{
	USHORT	num_of_bits; 
	comp_strm_p->ignore(500, k_endline);
	*comp_strm_p>>num_of_bits; 
	comp_strm_p->ignore(500, k_endline);	
	comp_strm_p->ignore(500, k_endline);
	init(num_of_bits);	

	USHORT	 col, row, big=0;
	DOUBLE	 x, y;
	comp_strm_p->exceptions(ios::badbit | ios::failbit);
	try{
		for(col=0; col<its_dim; col++){
			for(row=0; row<its_dim; row++){
				*comp_strm_p>> x >> y ; 
				its_array_p[big].real()= x;
				its_array_p[big].imag()= y;
				big++;
			}
		}
	}
	catch(const ios::failure  &  io_exc){
		cerr<<"'mat_name.in' file is illegal.";
		exit(-1);
	}
}
//******************************************
VOID  UNITARY_MAT::read_decrements_file(
IFSTREAM  *  comp_strm_p)	//io
{
	comp_strm_p->ignore(500, k_endline);
	comp_strm_p->ignore(500, k_endline);	
	comp_strm_p->ignore(500, k_endline);
	
	USHORT	 col, row, big=0;
	DOUBLE	 x, y;
	comp_strm_p->exceptions(ios::badbit | ios::failbit);
	try{
		for(col=0; col<its_dim; col++){
			for(row=0; row<its_dim; row++){
				*comp_strm_p>> x >> y ; 
				its_array_p[big].real()-= x;
				its_array_p[big].imag()-= y;
				big++;
			}
		}
	}
	catch(const ios::failure  &  io_exc){
		cerr<<"'mat_name-chk.in' file is illegal.";
		exit(-1);
	}
}
//******************************************
VOID  UNITARY_MAT::write_components_file(
OFSTREAM  *  comp_strm_p)	//io
const
{
	*comp_strm_p<<"//number of bits:"	<<k_endline; 	
	*comp_strm_p<<its_num_of_bits <<k_endline;			
	*comp_strm_p<<"//matrix U, as a string of columns:" <<k_endline;
		
	USHORT	 col, row, big=0;
	for(col=0; col<its_dim; col++){
		for(row=0; row<its_dim; row++){
			*comp_strm_p<< setprecision(9);
			*comp_strm_p<< setw(20) <<its_array_p[big].real()		
						<< '\t'
						<< its_array_p[big].imag()						<<k_endline;
			big++;
		}
	}
}
#pragma mark --permutations--
//******************************************
VOID	UNITARY_MAT::permute_cols(
const PERMUTATION	&	pmut)	//in
{
	ThrowIf_(its_dim != pmut.get_len());
	COMPLEX * new_array_p = new COMPLEX [its_dim_sq];
	COMPLEX * new_p;
	COMPLEX * old_p;	
	for(USHORT col=0; col<its_dim; col++){
		old_p = its_array_p + col*its_dim;
		new_p = new_array_p + pmut[col]*its_dim;
		for(USHORT	row=0; row<its_dim; row++){
			*new_p = *old_p;
			new_p++;
			old_p++;
		}
	}
	delete [] its_array_p;
	its_array_p = new_array_p;
}
//******************************************
VOID	UNITARY_MAT::permute_rows(
const PERMUTATION	&	pmut)	//in
{
	ThrowIf_(its_dim != pmut.get_len());
	COMPLEX * new_array_p = new COMPLEX [its_dim_sq];
	COMPLEX * new_p;
	COMPLEX * old_p;	
	for(USHORT row=0; row<its_dim; row++){
		old_p = its_array_p + row;
		new_p = new_array_p + pmut[row];
		for(USHORT	col=0; col<its_dim; col++){
			*new_p = *old_p;
			new_p += its_dim;
			old_p += its_dim;
		}
	}
	delete [] its_array_p;
	its_array_p = new_array_p;
}	
//******************************************
VOID	UNITARY_MAT::permute_bits(
const PERMUTATION  &	pmut)		//in
{
	ThrowIf_(its_num_of_bits != pmut.get_len());
	if(!pmut.is_identity()){
		COMPLEX	 *	new_array_p = new COMPLEX [its_dim_sq];
		USHORT	col, row;
		USHORT	big=0, new_big;
		BIT_VECTOR	rr(its_num_of_bits);
		BIT_VECTOR	cc(its_num_of_bits);
		for(col=0; col<its_dim; col++){
			for(row=0; row<its_dim; row++){
				rr.set_dec_rep(row);
				cc.set_dec_rep(col);
				new_big = cc.permute_bits(pmut)*its_dim + rr.permute_bits(pmut);	
				new_array_p[new_big] = its_array_p[big];
				big++;
			}
		}
		delete its_array_p;
		its_array_p = new_array_p;
	}	
}
//******************************************
VOID	UNITARY_MAT::transpose_bits(
const TRANSPOSITION  &	transp)		//in
{
	if(transp.x != transp.y){
		PERMUTATION 	pmut(its_num_of_bits);
		pmut.swap_entries(transp.x, transp.y);
		permute_bits(pmut);
	}
}
	
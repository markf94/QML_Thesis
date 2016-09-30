#include "nu_n1_transforms.h"
#include "BIT_VECTOR.h"

//******************************************
VOID	nu_to_n1_vec(
USHORT 					num_of_bits,		//in
VECTOR<DOUBLE>  &		in_vec)				//io
{
	//As in Latex, let _beta mean a subscript of beta.
	//For bit beta, define
	//n(beta) = diag(0,1)_beta, 
	//u(beta) = nbar(beta) = 1 - n(beta) = diag(1,0)_beta
	//1_beta = diag(1,1)_beta
	//This method replaces in_vec (a vector from the n,u basis) by 
	//its equivalent in the n,1 basis
	//example:
	//2 bits
	//A00 u(1)u(0) = A00 [ ( 1)*1 + (-1)*n(0) + (-1)*n(1) + ( 1)*n(1)n(0) ]
	//A01 u(1)n(0) = A01 [ ( 0)*1 + ( 1)*n(0) + ( 0)*n(1) + (-1)*n(1)n(0) ]
	//A10 n(1)u(0) = A10 [ ( 0)*1 + ( 0)*n(0) + ( 1)*n(1) + (-1)*n(1)n(0) ]
	//A11 n(1)n(0) = A11 [ ( 0)*1 + ( 0)*n(0) + ( 0)*n(1) + ( 1)*n(1)n(0) ]
	//vector in n,u basis: [A00, A01, A10, A11]
	//vector in n,1 basis: [B00, B01, B10, B11]
	//where
	//B00 = A00*( 1)
	//B01 = A00*(-1) + A01*( 1)
	//B10 = A00*(-1) + A01*( 0) + A10*( 1)
	//B11 = A00*( 1) + A01*(-1) + A10*(-1) + A11*( 1)
	

	if(num_of_bits==0)return;//do nothing since only one component

	USHORT	num_of_comps = (1 << num_of_bits);
	ThrowIf_(in_vec.get_len()!=num_of_comps);
	
	VECTOR<DOUBLE>	n1_vec(0, num_of_comps);
	BIT_VECTOR		bvec(num_of_bits, 0);
	for(USHORT i_n1=0; i_n1<num_of_comps; i_n1++){
		for(USHORT i_nu=0; i_nu<=i_n1; i_nu++){
			if( (i_nu & i_n1)==i_nu ){
				//remember that i^j is bitwise mod2 addition of i and j
				bvec.set_dec_rep(i_nu ^ i_n1);
				if(bvec.get_num_of_ON_bits()%2){//bvec.num_of_ON_bits is odd
					n1_vec[i_n1] -= in_vec[i_nu];
				}else{//bvec.num_of_ON_bits is even
					n1_vec[i_n1] += in_vec[i_nu];
				}
			}
		}
	}
	in_vec = n1_vec;
}

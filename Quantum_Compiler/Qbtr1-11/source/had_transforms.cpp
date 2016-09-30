#include "had_transforms.h"

//******************************************
VOID	had_transform(
USHORT 					num_of_bits,		//in
VECTOR<DOUBLE>  &		in_vec)				//io
{
	//This method replaces in_vec by its Hadamard transform. 
	if(num_of_bits==0)return;//do nothing since only one component

	USHORT	num_of_comps = (1 << num_of_bits);
	ThrowIf_(in_vec.get_len()!=num_of_comps);
	
	VECTOR<DOUBLE>	prev_vec;
	LONG	half_num_of_comps = (1 << (num_of_bits - 1));	
	for(USHORT	beta=0; beta < num_of_bits; beta++){
		USHORT	j = 0;
		prev_vec = in_vec;	
		for(USHORT  i=0; i < half_num_of_comps; i++){
			DOUBLE	x = prev_vec[j];
			DOUBLE	y = prev_vec[j + 1];	
			in_vec[i]= x + y;
			in_vec[half_num_of_comps + i] = x - y;
			j +=2;
		}			
	}
}
//******************************************
VOID	inv_had_transform(
USHORT 					num_of_bits,		//in
VECTOR<DOUBLE>  &		in_vec)				//io
{
	//This method replaces in_vec by its inverse Hadamard transform. 
	if(num_of_bits==0)return;//do nothing since only one component

	had_transform(num_of_bits, in_vec);
	
	USHORT	num_of_comps = (1 << num_of_bits);
	for(USHORT i=0; i<num_of_comps; i++){
		in_vec[i] /= num_of_comps;
	}
}

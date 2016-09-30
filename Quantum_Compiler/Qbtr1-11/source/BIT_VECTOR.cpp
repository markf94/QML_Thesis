#include "BIT_VECTOR.h"
#include "PERMUTATION.h"
#pragma mark --creation/destruction--
//******************************************
BIT_VECTOR::BIT_VECTOR(
USHORT	len /*=1*/,			//in
USHORT	dec_rep /*=0*/)		//in
:its_len(len),
its_dec_rep(dec_rep)
{
	ThrowIf_(len>max_len);
	ThrowIf_(len<1);
}
//******************************************
BIT_VECTOR  & 	BIT_VECTOR::operator= (
const BIT_VECTOR  &	rhs)	//in
{
	if(this != &rhs){
		its_len = rhs.its_len;
		its_dec_rep = rhs.its_dec_rep;
	}
	return *this;
}
#pragma mark --simple accessors--
//******************************************
USHORT	BIT_VECTOR::get_len()
const
{
	return its_len;
}
//******************************************
VOID 	BIT_VECTOR::set_len(
USHORT 	len)				//in
{
	ThrowIf_(len>max_len);
	ThrowIf_(len<1);
	its_len = len;
}
//******************************************
USHORT	BIT_VECTOR::get_dec_rep()
const
{
	return its_dec_rep;
}
//******************************************
BIT_VECTOR &  BIT_VECTOR::set_dec_rep(
USHORT 	dec_rep)			//in
{
	its_dec_rep = dec_rep;
	return 	*this;
}
#pragma mark --ON/OFF bit methods--
//******************************************
BOOLEAN 	BIT_VECTOR::bit_is_ON(
USHORT 	bpos)					//in
const
{
	ThrowIf_(bpos>=its_len);
	USHORT	mask = (1<<bpos);
	return (its_dec_rep & mask)==mask;
}
//******************************************
VOID	BIT_VECTOR::set_bit_ON(
USHORT 	bpos)					//in
{
	ThrowIf_(bpos>=its_len);
	its_dec_rep |=(1<<bpos);
}
//******************************************
VOID	BIT_VECTOR::set_bit_OFF(
USHORT 	bpos)					//in
{
	ThrowIf_(bpos>=its_len);
	its_dec_rep &= ~(1<<bpos);
}
//******************************************
VOID	BIT_VECTOR::set_all_bits_ON()
{
	for(USHORT bpos=0; bpos<its_len; bpos++){
		its_dec_rep |=(1<<bpos);
	}
}
//******************************************
USHORT	BIT_VECTOR::get_num_of_ON_bits()
const
{
	USHORT	count = 0;	
	for(USHORT bpos=0; bpos<its_len; bpos++){
		if(bit_is_ON(bpos))count++;
	}
	return count;
}
//******************************************
BOOLEAN 	BIT_VECTOR::find_ON_bit_to_my_right(
USHORT 		me_bit,				//in
USHORT  &	right_ON_bit)		//out
{
	ThrowIf_(me_bit>=its_len);
	if(me_bit==0)return false;
	
	right_ON_bit = me_bit;
	USHORT		mask = (1<<right_ON_bit);
	BOOLEAN		found_it = false;  
	do{
		right_ON_bit--;
		mask >>= 1;
		found_it = ((its_dec_rep & mask) == mask);
	}while( (right_ON_bit!=0)  &&  !found_it );
	return 	found_it;
}
//******************************************
BOOLEAN 	BIT_VECTOR::find_ON_bit_to_my_left(
USHORT 		me_bit,				//in
USHORT  &	left_ON_bit)		//out
{
	ThrowIf_(me_bit>=its_len);
	if(me_bit==(its_len-1))return false;
	
	left_ON_bit = me_bit;
	USHORT		mask = (1<<left_ON_bit);
	BOOLEAN		found_it = false;  
	do{
		left_ON_bit++;
		mask <<= 1;
		found_it = ((its_dec_rep & mask) == mask);
	}while( (left_ON_bit!=(its_len-1))  &&  !found_it );
	return 	found_it;
}
//******************************************
BOOLEAN 	BIT_VECTOR::find_leftmost_ON_bit(
USHORT  &	leftmost_ON_bit)		//out
{
	if(bit_is_ON(its_len-1)){
		leftmost_ON_bit = its_len-1;
		return true;
	}else{
		return find_ON_bit_to_my_right(its_len-1, leftmost_ON_bit);
	}
}
//******************************************
BOOLEAN 	BIT_VECTOR::find_rightmost_ON_bit(
USHORT  &	rightmost_ON_bit)		//out
{
	if(bit_is_ON(0)){
		rightmost_ON_bit = 0;
		return true;
	}else{
		return find_ON_bit_to_my_left(0, rightmost_ON_bit);
	}
}  
#pragma mark --about lazy ordering--

//Refs: look under "gray code"
//(1)Martin Gardener, "Knotted DoughNuts and Other 
//Mathematical Entertainments", chapt. 2, "The Binary Gray Code"
//(2)"Numerical Recipies in C"
//(3)Many books on Discrete Mathematics for CompSci types
//(4)On the web, in Eric's Treasure Trove/Math/Gray Codes

//Normal and lazy sequences both start at 0
//One has normal (dictionary) order, the other has lazy order.

//For illustration purposes, suppose N_B = 3
//The lazy sequence 000, 100, 110, 010, 011, 111, 101, 001
//is easily obtained from
//the "standard" lazy sequence 000, 001, 011, 010, 110, 111, 101, 100
//by "reflecting" each sequence term. 
//We will use the second sequence because
//it is more common in the literature.

//******************************************
USHORT		lazy_from_normal(
USHORT		normal,		//in
USHORT		bit_len)	//in
{	
	ThrowIf_(normal>= (1<<bit_len));
	ThrowIf_(bit_len>BIT_VECTOR::max_len);
	USHORT	 lazy = normal;
	for(SHORT m = (SHORT)bit_len-2; m >= 0; m--){
		//Look at bpos = m+1, if it's ON, then flip bpos=m.
		//Remember that ^ is same as a mod2 sum.
		lazy ^= ( (((1 << m+1) & normal)?1:0) << m );		
	}
	
	return lazy;
}
//******************************************
VOID	BIT_VECTOR::normal_to_lazy(
const BIT_VECTOR &	normal_bvec,	//in
BIT_VECTOR &		lazy_bvec)		//out
{
	ThrowIf_(lazy_bvec.its_len != normal_bvec.its_len);
	lazy_bvec.its_dec_rep = lazy_from_normal(normal_bvec.its_dec_rep,  normal_bvec.its_len);
}
//******************************************
VOID	BIT_VECTOR::lazy_advance(
USHORT 	new_normal)					//in
{

	//This method takes bit vector "lazy" (which corresponds to bit vector "normal"),  and 
	//changes it to the next lazy bit vector, "new_lazy" (which corresponds to "new_normal").
	ThrowIf_(new_normal<1);
	its_dec_rep ^= ((new_normal) & ~(new_normal-1));
	//example:  000, 001, 011, 010, 110, 111, 101, 100
	//its_dec_rep = 011, normal = 2 = 010 initially
	//new_normal = 3 = 011
	//(new_normal & ~normal) = 011 & 101 = 001 = mask for the bit that changed
	//its_dec_rep = 011 ^ 001 = 010 finally

}
//******************************************
BOOLEAN 	BIT_VECTOR::find_lazy_leftmost_ON_bit(
USHORT		new_normal,				//in
USHORT  &	leftmost_ON_bit)		//out
{
	//This method works only for bit vectors in the standard lazy sequence.
	//example:  000, 001, 011, 010, 110, 111, 101, 100
	//if new_normal >= 4, leftmost_ON_bit = 2
	//else if new_normal >= 2, leftmost_ON_bit = 1
	//else if new_normal >= 1, leftmost_ON_bit = 0
	ThrowIf_(new_normal<1);
	BOOLEAN 	found_it = true;
	if(its_dec_rep == 0){
		found_it = false;
	}else{
		for(SHORT n=its_len-1; n>=0; n--){ 
		 	if(new_normal >= (1<< n)){
		 		leftmost_ON_bit = n;
		 		break;
		 	}
		}
	}
	return 	found_it;
} 
#pragma mark	--permuting bits--
//******************************************
USHORT	BIT_VECTOR::permute_bits(
const PERMUTATION  &	pmut)		//in
{
	ThrowIf_(its_len!=pmut.get_len());
	USHORT	dec=0;
	for(USHORT i=0; i<its_len; i++){
		if( ((its_dec_rep>>i)&1)==1 ){
			 dec |= (1<<pmut[i]);
		}
	}
	its_dec_rep = dec;
	return 	dec;
}
//******************************************
USHORT	BIT_VECTOR::transpose_bits(
const TRANSPOSITION  &	transp)		//in
{
	if(transp.x != transp.y){
		PERMUTATION		pmut(its_len);
		pmut.swap_entries(transp.x, transp.y);
		permute_bits(pmut);
	}
	return 	its_dec_rep;
}

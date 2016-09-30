#pragma once
#include "prefix2.h"

class	PERMUTATION;
class   TRANSPOSITION;
//dec_rep = decimal representation
//bvec = bit vector
//******************************************
class BIT_VECTOR
{
private:
	USHORT	its_dec_rep;
	USHORT	its_len;
public:
	enum 	{max_len=16};
	BIT_VECTOR(USHORT len = 1, USHORT  dec_rep = 0);	
	BIT_VECTOR  &	operator= (const BIT_VECTOR  &	rhs);

	USHORT	get_len() const;	
	VOID	set_len(USHORT  len);
	USHORT	get_dec_rep() const;
	BIT_VECTOR &  set_dec_rep(USHORT  dec_rep);

	BOOLEAN		bit_is_ON(USHORT  bpos) const;
	VOID		set_bit_ON(USHORT bpos);
	VOID		set_bit_OFF(USHORT bpos);
	VOID		set_all_bits_ON();
	USHORT		get_num_of_ON_bits() const;
	BOOLEAN		find_ON_bit_to_my_right(USHORT  me_bit, USHORT  &  right_ON_bit);
	BOOLEAN		find_ON_bit_to_my_left(USHORT  me_bit, USHORT  &   left_ON_bit);
	BOOLEAN		find_leftmost_ON_bit(USHORT  &	leftmost_ON_bit);
	BOOLEAN		find_rightmost_ON_bit(USHORT  &	rightmost_ON_bit);
	
	friend USHORT	lazy_from_normal(USHORT	normal, USHORT	bit_len);
	VOID		normal_to_lazy(const BIT_VECTOR & normal_bvec, BIT_VECTOR & lazy_bvec);
	VOID		lazy_advance(USHORT  new_normal);
	BOOLEAN		find_lazy_leftmost_ON_bit(USHORT new_normal, USHORT  &	leftmost_ON_bit);
	
	USHORT		permute_bits(const PERMUTATION  &	pmut);
	USHORT		transpose_bits(const TRANSPOSITION  & transp);
};



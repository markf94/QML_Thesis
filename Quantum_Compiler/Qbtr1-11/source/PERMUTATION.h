#pragma once
#include "prefix2.h"

#include "VECTOR.h"
//******************************************
class	TRANSPOSITION
{
public:
	USHORT	x;
	USHORT	y;
	TRANSPOSITION(){x=0; y=0;}
};
//******************************************
class PERMUTATION: public VECTOR<USHORT>
{
private:
	BOOLEAN		its_more_pmuts;
public:
	PERMUTATION();
	PERMUTATION(USHORT	len);

	VOID		set_to_identity();
	VOID		set_to_identity(USHORT	len);
	BOOLEAN		is_identity() const;

	friend PERMUTATION	 operator *(const PERMUTATION & p2,	const PERMUTATION & p1);
	VOID	pre_multiply_by(const PERMUTATION  &  p);
	
	VOID		get_inverse(PERMUTATION  &  inv_pmut) const;
	
	VOID		swap_entries(USHORT	 i, USHORT	j);
	BOOLEAN		dict_advance();
	BOOLEAN		rev_dict_advance();

	VOID		prepare_for_lazy_advance();
	BOOLEAN		lazy_advance(TRANSPOSITION  &	transp);
};

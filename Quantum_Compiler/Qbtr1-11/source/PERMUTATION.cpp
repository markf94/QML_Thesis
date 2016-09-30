#include 	"PERMUTATION.h"
#include	"nexper1.h"

#pragma mark	--creation/destruction--
//******************************************
PERMUTATION::PERMUTATION()
{}
//******************************************
PERMUTATION::PERMUTATION(
USHORT		len)				//in
{
	set_to_identity(len);
}
#pragma mark	--identity--
//******************************************
VOID	PERMUTATION::set_to_identity()
{
	for(USHORT i=0; i<its_len; i++){
		its_array_p[i] = i;
	}
}
//******************************************
VOID	PERMUTATION::set_to_identity(
USHORT	len)
{
	ThrowIf_(len==0);
	if(len != its_len){
		delete its_array_p;
		its_array_p= new USHORT [len];//new[]
		its_len = len;
	}
	set_to_identity();
}
//******************************************
BOOLEAN		PERMUTATION::is_identity()
const
{
	for(USHORT i=0; i<its_len; i++){
		if(its_array_p[i] != i)return false;
	}
	return true;
}
#pragma mark	--multiplication--
//******************************************
PERMUTATION		operator *(
const PERMUTATION	&  	p2,			//in
const PERMUTATION	&   p1)			//in
{
	//permutation product is function composition
	ThrowIf_(p1.its_len != p2.its_len);
	USHORT	len = p1.its_len;
	PERMUTATION		p(len);
	for(USHORT j=0; j<len; j++){
		p.its_array_p[j] = 	p2.its_array_p[p1.its_array_p[j]];	
	}
	return p;
}
//******************************************
VOID	PERMUTATION::pre_multiply_by(
const PERMUTATION	&   p)			//in
{
	//this is similar to the operation *=
	//except that * for permutations is not commutative
	ThrowIf_(p.its_len != its_len);
	for(USHORT j=0; j<its_len; j++){
		its_array_p[j] = p.its_array_p[its_array_p[j]];	
	}
}
//******************************************
/*
The following won't work:

VOID	PERMUTATION::post_multiply_by(
const PERMUTATION	&   p)			//in
{
	for(USHORT j=0; j<its_len; j++){
		its_array_p[j] = its_array_p[p.its_array_p[j]];	
	}	
}

because its_array_p[4] might depend on its_array_p[3]
which has already been changed. Use * operator if 
post multiplying "this" by p
(*this) = (*this) * p;
*/
#pragma mark	--inverse--
//******************************************
VOID	PERMUTATION::get_inverse(
PERMUTATION 	& 	inv_pmut)	//out
const
{
	inv_pmut.resize(0, its_len);
	for(USHORT i=0; i<its_len; i++){
		inv_pmut.its_array_p[its_array_p[i]]=i;
	}
}
#pragma mark	--advance--	
//******************************************
VOID	PERMUTATION::swap_entries(
USHORT	 i,		//in 
USHORT	j)		//in
{
	SignalIf_(i>=its_len || j>=its_len);
	USHORT	 temp;
	temp = its_array_p[i];
	its_array_p[i] = its_array_p[j];
	its_array_p[j] = temp;
}
//******************************************
BOOLEAN		PERMUTATION::dict_advance()
{
	//dict = dictionary
	//In dictionary ordering,
	//first permutation is the identity permutation
	//(pmut[0]=0, pmut[1]=1, etc. ).
	//This method advances the permutation to
	//the next permutation in dictionary ordering.
	//It returns false if we've reached the last one.
	//Otherwise it returns true.
	//Ref:book "Combinatorial Generation", by Joe Sawada
	/*
	Example
	04321
	     step:14320
	     step:10324
	     step:10234
	*/
		
	SHORT	 k, j;
	SHORT	 s, r;

	ThrowIf_(its_len<=1); 
	k = its_len - 2;
	while(its_array_p[k] > its_array_p[k+1]){
	 	k--;
	 	if(k==-1)break;
	}
	if (k == -1){
		return false;
	}else{
		j = its_len - 1;
		while(its_array_p[k] > its_array_p[j]){
			j--;
		}
		swap_entries(j, k);
		s = k+1; r = its_len - 1;
		while(s<r){
			swap_entries(r, s);
			s++; r--;
		}
	}
	return true;
}
//******************************************
BOOLEAN		PERMUTATION::rev_dict_advance()
{
	//rev_dict = reverse dictionary
	//In reverse dictionary ordering,
	//last permutation is the identity permutation
	//(pmut[0]=0, pmut[1]=1, etc. ).
	//This method advances the permutation to
	//the next permutation in reverse dictionary ordering.
	//It returns false if we've reached the last one.
	//Otherwise it returns true.
	//see PERMUTATION::dict_advance()		
	SHORT	 k, j;
	SHORT	 s, r;

	ThrowIf_(its_len<=1); 
	k = its_len - 2;
	while(its_array_p[its_len -1 - k] > its_array_p[its_len -2 - k]){
	 	k--;
	 	if(k==-1)break;
	}
	if (k == -1){
		return false;
	}else{
		j = its_len - 1;
		while(its_array_p[its_len -1 - k] > its_array_p[its_len -1 - j]){
			j--;
		}
		swap_entries(its_len -1 - j, its_len -1 - k);
		s = k+1; r = its_len - 1;
		while(s<r){
			swap_entries(its_len -1 - r, its_len -1 - s);
			s++; r--;
		}
	}
	return true;
}
//******************************************
VOID		PERMUTATION::prepare_for_lazy_advance()
{
	its_more_pmuts = false;
}
//******************************************
BOOLEAN		PERMUTATION::lazy_advance(
TRANSPOSITION  &		transp)	//out
{
	//advance one transposition at a time
	nexper(its_len, its_array_p, its_more_pmuts, transp.x, transp.y);
	return its_more_pmuts;
}

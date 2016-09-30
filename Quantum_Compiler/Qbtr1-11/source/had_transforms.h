#pragma once
#include "prefix2.h"

#include "VECTOR.h"

//had = Hadamard, inv = inverse
//These methods perform fast Hadamard and inverse Hadamard transforms.
//Ref:  Hadamard Matrix Analysis and Synthesis, by
//Yarlagadda and Hershey
//******************************************

VOID	had_transform(USHORT  num_of_bits, VECTOR<DOUBLE>  & in_vec);
VOID	inv_had_transform(USHORT  num_of_bits, VECTOR<DOUBLE>  & in_vec);

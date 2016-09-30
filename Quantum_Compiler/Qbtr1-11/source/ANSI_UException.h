//Mac CodeWarrior PowerPlant users can replace this by UException.h 
//to increase functionality.
#pragma once

#include "ANSI_UDebugging.h"

typedef long	ExceptionCode;

enum {
	err_NilPointer		= 'nilP',
	err_AssertFailed	= 'asrt'
};

#define	ThrowIfNil_(ptr)											\
	do {															\
		if ((ptr) == 0) Throw_(err_NilPointer);						\
	} while (false)

#define	ThrowIf_(test)												\
	do {															\
		if (test) Throw_(err_AssertFailed);							\
	} while (false)

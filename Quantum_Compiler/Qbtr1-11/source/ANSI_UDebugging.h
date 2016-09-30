//Mac CodeWarrior PowerPlant users can replace this by UDebugging.h
//to increase functionality.
#pragma once
#include <iostream>

//********************Throw Debugging
#define Throw_Err(err)		throw (ExceptionCode)(err)
#ifdef Debug_Throw
	#define SetDebugThrow_(inAction)	//do nothing
	#define Throw_(err)														\
		do {																\
			cerr<<"Exception Thrown"<<endl;									\
			if(err=='nilP'){												\
				cerr<<"   Reason: Nil Pointer"<<endl;						\
			}else if(err=='asrt'){											\
				cerr<<"   Reason: Assertion Failed"<<endl;					\
			}																\
			cerr<<"   File: "<<__FILE__<<endl;								\
			cerr<<"   Line: "<<__LINE__<<endl;								\
			Throw_Err(err);													\
		} while (false)

#else
	#define SetDebugThrow_(inAction)	//do nothing
	#define Throw_(err)		Throw_Err(err)
#endif // Debug_Throw
//********************Signal Debugging
#ifdef Debug_Signal
	#define SetDebugSignal_(inAction)	//do nothing
	#define SignalCStr_(cstr)												\
		do {																\
			cerr<<"Signal Raised"<<endl;									\
			cerr<<"   Message: "<<cstr<<endl;								\
			cerr<<"   File: "<<__FILE__<<endl;								\
			cerr<<"   Line: "<<__LINE__<<endl;								\
		} while (false)
														
	#define SignalIf_(test)						\
	    do {									\
	        if (test) SignalCStr_(#test);		\
	    } while (false)
#else
	#define SetDebugSignal_(inAction)		//do nothing
	#define	SignalCStr_(cstr)				//do nothing
	#define SignalIf_(test)					//do nothing
#endif // Debug_Signal

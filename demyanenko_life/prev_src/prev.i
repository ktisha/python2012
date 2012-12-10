%module prev
%{
#include "prev.h"
%}

%include stl.i
%include prev.h
namespace std
{
	%template(vec) vector<bool>;
	%template(dvec) vector< vector<bool> >;
}
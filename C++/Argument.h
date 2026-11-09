#ifndef _ARGUMENT_H_
#define _ARGUMENT_H_

#include <string>

#include "Entity.h"

struct Argument {
	Entity* parent;
	Entity* child;
	size_t index;

	Argument(const Entity* parent,const Entity* child,const size_t index);
};

#endif
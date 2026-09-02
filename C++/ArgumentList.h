#ifndef _ARGUMENT_LIST_H_
#define _ARGUMENT_LIST_H_

#include <vector>

#include "Argument.h"
#include "Entity.h"

struct ArgumentList {
	Entity* entity;
	std::vector<Argument*> values;

	Argument(const Entity* entity,const std::vector<Argument*>& values);
};

#endif
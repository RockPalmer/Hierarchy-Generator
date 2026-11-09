#ifndef _RETURNS_H_
#define _RETURNS_H_

#include "Entity.h"

struct Returns {
	Entity* parent;
	Entity* child;

	Returns(const Entity* parent,const Entity* child);
};

#endif
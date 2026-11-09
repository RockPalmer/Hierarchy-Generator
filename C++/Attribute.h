#ifndef _ATTRIBUTE_H_
#define _ATTRIBUTE_H_

#include "Entity.h"

struct Attribute {
	Entity* parent;
	Entity* child;

	Attribute(const Entity* parent,const Entity* child);
};

#endif
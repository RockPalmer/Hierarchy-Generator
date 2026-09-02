#ifndef _ATTRIBUTE_SET_H_
#define _ATTRIBUTE_SET_H_

#include <vector>

#include "Entity.h"

struct AttributeSet {
	Entity* entity;
	std::vector<Entity*> values;

	AttributeSet(const Entity* entity,const std::vector<Entity*>& values);
};

#endif
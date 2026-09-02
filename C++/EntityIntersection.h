#ifndef _ENTITY_INTERSECTION_H_
#define _ENTITY_INTERSECTION_H_

#include <cstddef>
#include <set>

#include "Entity.h"

struct EntityIntersection: Entity {
	std::set<Entity*> values;

	EntityIntersection(const std::set<Entity*>& values);
};

#endif
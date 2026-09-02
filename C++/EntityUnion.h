#ifndef _ENTITY_UNION_H_
#define _ENTITY_UNION_H_

#include <cstddef>
#include <set>

#include "Entity.h"

struct EntityUnion: Entity {
	std::set<Entity*> values;

	EntityUnion(const std::set<Entity*>& values);
};

#endif
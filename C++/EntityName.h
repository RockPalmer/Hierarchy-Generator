#ifndef _ENTITY_NAME_H_
#define _ENTITY_NAME_H_

#include <string>

#include "Entity.h"

struct EntityName {
	Entity* entity;
	std::string name;

	EntityName(const Entity* entity,const std::string name);
};

#endif
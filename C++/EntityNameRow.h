#ifndef _ENTITY_NAME_ROW_H_
#define _ENTITY_NAME_ROW_H_

#include <string>

#include "EntityRow.h"

struct EntityNameRow {
	EntityRow* entity;
	std::string name;

	EntityNameRow(EntityRow* entity,const std::string name);
};

bool operator<(const EntityNameRow& v1,const EntityNameRow& v2);
bool operator>(const EntityNameRow& v1,const EntityNameRow& v2);
bool operator<=(const EntityNameRow& v1,const EntityNameRow& v2);
bool operator>=(const EntityNameRow& v1,const EntityNameRow& v2);
bool operator==(const EntityNameRow& v1,const EntityNameRow& v2);
bool operator!=(const EntityNameRow& v1,const EntityNameRow& v2);

#endif
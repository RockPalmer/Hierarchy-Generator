#ifndef _ENTITY_ARGUMENT_LIST_ROW_H_
#define _ENTITY_ARGUMENT_LIST_ROW_H_

#include <string>

#include "EntityRow.h"

struct EntityArgumentListRow {
	EntityRow* entity;
	bool hasArguments;

	EntityArgumentListRow(EntityRow* entity,const bool hasArguments);
};

bool operator<(const EntityArgumentListRow& v1,const EntityArgumentListRow& v2);
bool operator>(const EntityArgumentListRow& v1,const EntityArgumentListRow& v2);
bool operator<=(const EntityArgumentListRow& v1,const EntityArgumentListRow& v2);
bool operator>=(const EntityArgumentListRow& v1,const EntityArgumentListRow& v2);
bool operator==(const EntityArgumentListRow& v1,const EntityArgumentListRow& v2);
bool operator!=(const EntityArgumentListRow& v1,const EntityArgumentListRow& v2);

#endif
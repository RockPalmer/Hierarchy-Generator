#ifndef _ENTITY_GROUP_ROW_H_
#define _ENTITY_GROUP_ROW_H_

#include "EntityRow.h"

struct EntityGroupRow {
	EntityRow* parent;
	EntityRow* child;

	EntityGroupRow(EntityRow* parent,EntityRow* child);
};

bool operator<(const EntityGroupRow& v1,const EntityGroupRow& v2);
bool operator>(const EntityGroupRow& v1,const EntityGroupRow& v2);
bool operator<=(const EntityGroupRow& v1,const EntityGroupRow& v2);
bool operator>=(const EntityGroupRow& v1,const EntityGroupRow& v2);
bool operator==(const EntityGroupRow& v1,const EntityGroupRow& v2);
bool operator!=(const EntityGroupRow& v1,const EntityGroupRow& v2);

#endif
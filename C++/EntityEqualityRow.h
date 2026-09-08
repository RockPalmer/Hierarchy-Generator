#ifndef _ENTITY_EQUALITY_ROW_H_
#define _ENTITY_EQUALITY_ROW_H_

#include <set>

#include "EntityRow.h"

struct EntityEqualityRow {
	std::set<EntityRow*> values;

	EntityEqualityRow(const std::set<EntityRow*>& values);
};

bool operator<(const EntityEqualityRow& v1,const EntityEqualityRow& v2);
bool operator>(const EntityEqualityRow& v1,const EntityEqualityRow& v2);
bool operator<=(const EntityEqualityRow& v1,const EntityEqualityRow& v2);
bool operator>=(const EntityEqualityRow& v1,const EntityEqualityRow& v2);
bool operator==(const EntityEqualityRow& v1,const EntityEqualityRow& v2);
bool operator!=(const EntityEqualityRow& v1,const EntityEqualityRow& v2);

#endif
#ifndef _ENTITY_ROW_H_
#define _ENTITY_ROW_H_

#include <string>

struct EntityRow {
	void* value;
	size_t type;

	EntityRow(void* id,const size_t type);
};

bool operator<(const EntityRow& v1,const EntityRow& v2);
bool operator>(const EntityRow& v1,const EntityRow& v2);
bool operator<=(const EntityRow& v1,const EntityRow& v2);
bool operator>=(const EntityRow& v1,const EntityRow& v2);
bool operator==(const EntityRow& v1,const EntityRow& v2);
bool operator!=(const EntityRow& v1,const EntityRow& v2);

#endif
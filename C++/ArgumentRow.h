#ifndef _ARGUMENT_ROW_H_
#define _ARGUMENT_ROW_H_

#include <string>

#include "EntityRow.h"

struct ArgumentRow {
	EntityRow* entity;
	void* value;
	size_t index;
	size_t type;

	ArgumentRow(EntityRow* entity,void* value,const size_t index,const size_t type);
};

bool operator<(const ArgumentRow& v1,const ArgumentRow& v2);
bool operator>(const ArgumentRow& v1,const ArgumentRow& v2);
bool operator<=(const ArgumentRow& v1,const ArgumentRow& v2);
bool operator>=(const ArgumentRow& v1,const ArgumentRow& v2);
bool operator==(const ArgumentRow& v1,const ArgumentRow& v2);
bool operator!=(const ArgumentRow& v1,const ArgumentRow& v2);

#endif
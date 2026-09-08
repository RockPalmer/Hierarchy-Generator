#ifndef _ARGUMENT_GROUP_ROW_H_
#define _ARGUMENT_GROUP_ROW_H_

#include "EntityRow.h"
#include "ArgumentRow.h"

struct ArgumentGroupRow {
	ArgumentRow* argument;
	EntityRow* entity;

	ArgumentGroupRow(ArgumentRow* argument,EntityRow* entity);
};

bool operator<(const ArgumentGroupRow& v1,const ArgumentGroupRow& v2);
bool operator>(const ArgumentGroupRow& v1,const ArgumentGroupRow& v2);
bool operator<=(const ArgumentGroupRow& v1,const ArgumentGroupRow& v2);
bool operator>=(const ArgumentGroupRow& v1,const ArgumentGroupRow& v2);
bool operator==(const ArgumentGroupRow& v1,const ArgumentGroupRow& v2);
bool operator!=(const ArgumentGroupRow& v1,const ArgumentGroupRow& v2);

#endif
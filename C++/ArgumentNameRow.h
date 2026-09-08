#ifndef _ARGUMENT_NAME_ROW_H_
#define _ARGUMENT_NAME_ROW_H_

#include "ArgumentRow.h"

struct ArgumentNameRow {
	ArgumentRow* argument;
	std::string name;

	ArgumentNameRow(ArgumentRow* argument,const std::string name);
};

bool operator<(const ArgumentNameRow& v1,const ArgumentNameRow& v2);
bool operator>(const ArgumentNameRow& v1,const ArgumentNameRow& v2);
bool operator<=(const ArgumentNameRow& v1,const ArgumentNameRow& v2);
bool operator>=(const ArgumentNameRow& v1,const ArgumentNameRow& v2);
bool operator==(const ArgumentNameRow& v1,const ArgumentNameRow& v2);
bool operator!=(const ArgumentNameRow& v1,const ArgumentNameRow& v2);

#endif
#ifndef _NAME_LIST_H_
#define _NAME_LIST_H_

#include <string>
#include <set>

#include "Entity.h"

struct NameList {
	Entity* entity;
	std::set<std::string> names;

	NameList(const Entity* entity,const std::set<std::string>& names);
};

#endif
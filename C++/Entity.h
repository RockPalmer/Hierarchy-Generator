#ifndef _ENTITY_H_
#define _ENTITY_H_

struct Entity {
	size_t id;
	size_t isArgument;
	bool hasArguments;

	Entity(const size_t id,const bool isArgument,const bool hasArguments);
};

bool operator<(const Entity& v1,const Entity& v2);
bool operator<=(const Entity& v1,const Entity& v2);
bool operator>(const Entity& v1,const Entity& v2);
bool operator>=(const Entity& v1,const Entity& v2);
bool operator==(const Entity& v1,const Entity& v2);
bool operator!=(const Entity& v1,const Entity& v2);

#endif
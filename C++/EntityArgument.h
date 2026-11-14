#ifndef _ENTITY_ARGUMENT_H_
#define _ENTITY_ARGUMENT_H_

struct EntityArgument {
	size_t id1;
	size_t id2;
	size_t index;

	EntityArgument(const size_t id1,const size_t id2,const size_t index);
};

bool operator<(const EntityArgument& v1,const EntityArgument& v2);
bool operator<=(const EntityArgument& v1,const EntityArgument& v2);
bool operator>(const EntityArgument& v1,const EntityArgument& v2);
bool operator>=(const EntityArgument& v1,const EntityArgument& v2);
bool operator==(const EntityArgument& v1,const EntityArgument& v2);
bool operator!=(const EntityArgument& v1,const EntityArgument& v2);

#endif
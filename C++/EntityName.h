#ifndef _ENTITY_NAME_H_
#define _ENTITY_NAME_H_

struct EntityName {
	size_t id;
	std::string name;

	EntityName(const size_t id,const std::string name);
};

bool operator<(const EntityName& v1,const EntityName& v2);
bool operator<=(const EntityName& v1,const EntityName& v2);
bool operator>(const EntityName& v1,const EntityName& v2);
bool operator>=(const EntityName& v1,const EntityName& v2);
bool operator==(const EntityName& v1,const EntityName& v2);
bool operator!=(const EntityName& v1,const EntityName& v2);

#endif
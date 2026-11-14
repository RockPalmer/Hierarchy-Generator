#ifndef _ENTITY_PAIR_H_
#define _ENTITY_PAIR_H_

struct EntityPair {
	size_t id1;
	size_t id2;

	EntityPair(const size_t id1,const size_t id2);
};

bool operator<(const EntityPair& v1,const EntityPair& v2);
bool operator<=(const EntityPair& v1,const EntityPair& v2);
bool operator>(const EntityPair& v1,const EntityPair& v2);
bool operator>=(const EntityPair& v1,const EntityPair& v2);
bool operator==(const EntityPair& v1,const EntityPair& v2);
bool operator!=(const EntityPair& v1,const EntityPair& v2);

#endif
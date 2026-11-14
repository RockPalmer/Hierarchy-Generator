#include "EntityPair.h"

EntityPair::EntityPair(const size_t id1,const size_t id2):
	id1(id1),
	id2(id2) {};

bool operator<(const EntityPair& v1,const EntityPair& v2) {
	if (v1.id1 < v2.id1) return true;
	if (v1.id1 > v2.id1) return false;
	if (v1.id2 < v2.id2) return true;
	if (v1.id2 > v2.id2) return false;
	return false;
};
bool operator<=(const EntityPair& v1,const EntityPair& v2) {
	if (v1.id1 < v2.id1) return true;
	if (v1.id1 > v2.id1) return false;
	if (v1.id2 < v2.id2) return true;
	if (v1.id2 > v2.id2) return false;
	return true;
};
bool operator>(const EntityPair& v1,const EntityPair& v2) {
	if (v1.id1 > v2.id1) return true;
	if (v1.id1 < v2.id1) return false;
	if (v1.id2 > v2.id2) return true;
	if (v1.id2 < v2.id2) return false;
	return false;
};
bool operator>=(const EntityPair& v1,const EntityPair& v2) {
	if (v1.id1 > v2.id1) return true;
	if (v1.id1 < v2.id1) return false;
	if (v1.id2 > v2.id2) return true;
	if (v1.id2 < v2.id2) return false;
	return true;
};
bool operator==(const EntityPair& v1,const EntityPair& v2) {
	return (
		v1.id1 == v2.id1 &&
		v1.id2 == v2.id2
	);
};
bool operator!=(const EntityPair& v1,const EntityPair& v2) {
	return !(v1 == v2);
};
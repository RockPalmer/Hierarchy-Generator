#include "EntityArgument.h"

EntityArgument::EntityArgument(const size_t id1,const size_t id2,const size_t index):
	id1(id1),
	id2(id2),
	index(index) {};

bool operator<(const EntityArgument& v1,const EntityArgument& v2) {
	if (v1.id1 < v2.id1) return true;
	if (v1.id1 > v2.id1) return false;
	if (v1.id2 < v2.id2) return true;
	if (v1.id2 > v2.id2) return false;
	if (v1.index < v2.index) return true;
	if (v1.index > v2.index) return false;
	return false;
};
bool operator<=(const EntityArgument& v1,const EntityArgument& v2) {
	if (v1.id1 < v2.id1) return true;
	if (v1.id1 > v2.id1) return false;
	if (v1.id2 < v2.id2) return true;
	if (v1.id2 > v2.id2) return false;
	if (v1.index < v2.index) return true;
	if (v1.index > v2.index) return false;
	return true;
};
bool operator>(const EntityArgument& v1,const EntityArgument& v2) {
	if (v1.id1 > v2.id1) return true;
	if (v1.id1 < v2.id1) return false;
	if (v1.id2 > v2.id2) return true;
	if (v1.id2 < v2.id2) return false;
	if (v1.index > v2.index) return true;
	if (v1.index < v2.index) return false;
	return false;
};
bool operator>=(const EntityArgument& v1,const EntityArgument& v2) {
	if (v1.id1 > v2.id1) return true;
	if (v1.id1 < v2.id1) return false;
	if (v1.id2 > v2.id2) return true;
	if (v1.id2 < v2.id2) return false;
	if (v1.index > v2.index) return true;
	if (v1.index < v2.index) return false;
	return true;
};
bool operator==(const EntityArgument& v1,const EntityArgument& v2) {
	return (
		v1.id1 == v2.id1 &&
		v1.id2 == v2.id2 &&
		v1.index == v2.index
	);
};
bool operator!=(const EntityArgument& v1,const EntityArgument& v2) {
	return !(v1 == v2);
};
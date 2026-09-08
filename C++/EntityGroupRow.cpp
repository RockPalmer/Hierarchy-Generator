#include "EntityGroupRow.h"

EntityGroupRow::EntityGroupRow(EntityRow* parent,EntityRow* child):
	parent(parent),
	child(child) {};

bool operator<(const EntityGroupRow& v1,const EntityGroupRow& v2) {
	return v1.parent < v2.parent || v1.parent == v2.parent && v1.child < v2.child;
};
bool operator>(const EntityGroupRow& v1,const EntityGroupRow& v2) {
	return v1.parent > v2.parent || v1.parent == v2.parent && v1.child > v2.child;
};
bool operator<=(const EntityGroupRow& v1,const EntityGroupRow& v2) {
	return v1.parent <= v2.parent || v1.parent == v2.parent && v1.child <= v2.child;
};
bool operator>=(const EntityGroupRow& v1,const EntityGroupRow& v2) {
	return v1.parent >= v2.parent || v1.parent == v2.parent && v1.child >= v2.child;
};
bool operator==(const EntityGroupRow& v1,const EntityGroupRow& v2) {
	return v1.parent == v2.parent && v1.child == v2.child;
};
bool operator!=(const EntityGroupRow& v1,const EntityGroupRow& v2) {
	return v1.parent != v2.parent || v1.child != v2.child;
};
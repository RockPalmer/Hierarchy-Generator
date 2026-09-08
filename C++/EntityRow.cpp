#include "EntityRow.h"

EntityRow::EntityRow(void* value,const size_t type):
	value(value),
	type(type) {};

bool operator<(const EntityRow& v1,const EntityRow& v2) {
	return v1.value < v2.value || v1.value == v2.value && v1.type < v2.type;
};
bool operator>(const EntityRow& v1,const EntityRow& v2) {
	return v1.value > v2.value || v1.value == v2.value && v1.type > v2.type;
};
bool operator<=(const EntityRow& v1,const EntityRow& v2) {
	return v1.value <= v2.value || v1.value == v2.value && v1.type <= v2.type;
};
bool operator>=(const EntityRow& v1,const EntityRow& v2) {
	return v1.value >= v2.value || v1.value == v2.value && v1.type >= v2.type;
};
bool operator==(const EntityRow& v1,const EntityRow& v2) {
	return v1.value == v2.value && v1.type == v2.type;
};
bool operator!=(const EntityRow& v1,const EntityRow& v2) {
	return v1.value != v2.value || v1.type != v2.type;
};
#include "ArgumentRow.h"

ArgumentRow::ArgumentRow(EntityRow* entity,void* value,const size_t index,const size_t type):
	entity(entity),
	value(value),
	index(index),
	type(type) {};

bool operator<(const ArgumentRow& v1,const ArgumentRow& v2) {
	return 
		v1.entity < v2.entity || 
		v1.entity == v2.entity && v1.index < v2.index ||
		v1.entity == v2.entity && v1.index == v2.index && v1.type < v2.type;
};
bool operator>(const ArgumentRow& v1,const ArgumentRow& v2) {
	return 
		v1.entity > v2.entity || 
		v1.entity == v2.entity && v1.index > v2.index ||
		v1.entity == v2.entity && v1.index == v2.index && v1.type > v2.type;
};
bool operator<=(const ArgumentRow& v1,const ArgumentRow& v2) {
	return 
		v1.entity <= v2.entity || 
		v1.entity == v2.entity && v1.index <= v2.index ||
		v1.entity == v2.entity && v1.index == v2.index && v1.type <= v2.type;
};
bool operator>=(const ArgumentRow& v1,const ArgumentRow& v2) {
	return 
		v1.entity >= v2.entity || 
		v1.entity == v2.entity && v1.index >= v2.index ||
		v1.entity == v2.entity && v1.index == v2.index && v1.type >= v2.type;
};
bool operator==(const ArgumentRow& v1,const ArgumentRow& v2) {
	return v1.entity == v2.entity && v1.index == v2.index && v1.type == v2.type;
};
bool operator!=(const ArgumentRow& v1,const ArgumentRow& v2) {
	return v1.entity != v2.entity || v1.index != v2.index || v1.type != v2.type;
};
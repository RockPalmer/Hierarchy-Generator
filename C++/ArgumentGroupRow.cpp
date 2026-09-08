#include "ArgumentGroupRow.h"

ArgumentGroupRow::ArgumentGroupRow(ArgumentRow* argument,Entity* entity):
	argument(argument),
	entity(entity) {};

bool operator<(const ArgumentGroupRow& v1,const ArgumentGroupRow& v2) {
	return v1.argument < v2.argument || v1.argument == v2.argument && v1.entity < v2.entity;
};
bool operator>(const ArgumentGroupRow& v1,const ArgumentGroupRow& v2) {
	return v1.argument > v2.argument || v1.argument == v2.argument && v1.entity > v2.entity;
};
bool operator<=(const ArgumentGroupRow& v1,const ArgumentGroupRow& v2) {
	return v1.argument <= v2.argument || v1.argument == v2.argument && v1.entity <= v2.entity;
};
bool operator>=(const ArgumentGroupRow& v1,const ArgumentGroupRow& v2) {
	return v1.argument >= v2.argument || v1.argument == v2.argument && v1.entity >= v2.entity;
};
bool operator==(const ArgumentGroupRow& v1,const ArgumentGroupRow& v2) {
	return v1.argument == v2.argument && v1.entity == v2.entity;
};
bool operator!=(const ArgumentGroupRow& v1,const ArgumentGroupRow& v2) {
	return v1.argument != v2.argument || v1.entity != v2.entity;
};
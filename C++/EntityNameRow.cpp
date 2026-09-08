#include "EntityNameRow.h"

EntityNameRow::EntityNameRow(EntityRow* entity,const std::string name):
	entity(entity),
	name(name) {};

bool operator<(const EntityNameRow& v1,const EntityNameRow& v2) {
	return v1.entity < v2.entity || v1.entity == v2.entity && v1.name < v2.name;
};
bool operator>(const EntityNameRow& v1,const EntityNameRow& v2) {
	return v1.entity > v2.entity || v1.entity == v2.entity && v1.name > v2.name;
};
bool operator<=(const EntityNameRow& v1,const EntityNameRow& v2) {
	return v1.entity <= v2.entity || v1.entity == v2.entity && v1.name <= v2.name;
};
bool operator>=(const EntityNameRow& v1,const EntityNameRow& v2) {
	return v1.entity >= v2.entity || v1.entity == v2.entity && v1.name >= v2.name;
};
bool operator==(const EntityNameRow& v1,const EntityNameRow& v2) {
	return v1.entity == v2.entity && v1.name == v2.name;
};
bool operator!=(const EntityNameRow& v1,const EntityNameRow& v2) {
	return v1.entity != v2.entity || v1.name != v2.name;
};
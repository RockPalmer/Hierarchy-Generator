#include "EntityName.h"

EntityName::EntityName(const size_t id,const std::string name):
	id(id),
	name(name) {};

bool operator<(const EntityName& v1,const EntityName& v2) {
	if (v1.id < v2.id) return true;
	if (v1.id > v2.id) return false;
	if (v1.name < v2.name) return true;
	if (v1.name > v2.name) return false;
	return false;
};
bool operator<=(const EntityName& v1,const EntityName& v2) {
	if (v1.id < v2.id) return true;
	if (v1.id > v2.id) return false;
	if (v1.name < v2.name) return true;
	if (v1.name > v2.name) return false;
	return true;
};
bool operator>(const EntityName& v1,const EntityName& v2) {
	if (v1.id > v2.id) return true;
	if (v1.id < v2.id) return false;
	if (v1.name > v2.name) return true;
	if (v1.name < v2.name) return false;
	return false;
};
bool operator>=(const EntityName& v1,const EntityName& v2) {
	if (v1.id > v2.id) return true;
	if (v1.id < v2.id) return false;
	if (v1.name > v2.name) return true;
	if (v1.name < v2.name) return false;
	return true;
};
bool operator==(const EntityName& v1,const EntityName& v2) {
	return (
		v1.id == v2.id &&
		v1.name == v2.name
	);
};
bool operator!=(const EntityName& v1,const EntityName& v2) {
	return !(v1 == v2);
};
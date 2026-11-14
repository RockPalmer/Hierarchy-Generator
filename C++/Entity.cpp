#include "Entity.h"

Entity::Entity(const size_t id,const bool isArgument,const bool hasArguments):
	id(id),
	isArgument(isArgument),
	hasArguments(hasArguments) {};

bool operator<(const Entity& v1,const Entity& v2) {
	if (v1.id < v2.id) return true;
	if (v1.id > v2.id) return false;
	if ((int)v1.hasArguments < (int)v2.hasArguments) return true;
	if ((int)v1.hasArguments > (int)v2.hasArguments) return false;
	if ((int)v1.isArgument < (int)v2.isArgument) return true;
	if ((int)v1.isArgument > (int)v2.isArgument) return false;
	return false;
};
bool operator<=(const Entity& v1,const Entity& v2) {
	if (v1.id < v2.id) return true;
	if (v1.id > v2.id) return false;
	if ((int)v1.hasArguments < (int)v2.hasArguments) return true;
	if ((int)v1.hasArguments > (int)v2.hasArguments) return false;
	if ((int)v1.isArguments < (int)v2.isArguments) return true;
	if ((int)v1.isArguments > (int)v2.isArguments) return false;
	return true;
};
bool operator>(const Entity& v1,const Entity& v2) {
	if (v1.id > v2.id) return true;
	if (v1.id < v2.id) return false;
	if ((int)v1.hasArguments > (int)v2.hasArguments) return true;
	if ((int)v1.hasArguments < (int)v2.hasArguments) return false;
	if ((int)v1.isArguments > (int)v2.isArguments) return true;
	if ((int)v1.isArguments < (int)v2.isArguments) return false;
	return false;
};
bool operator>=(const Entity& v1,const Entity& v2) {
	if (v1.id > v2.id) return true;
	if (v1.id < v2.id) return false;
	if ((int)v1.hasArguments > (int)v2.hasArguments) return true;
	if ((int)v1.hasArguments < (int)v2.hasArguments) return false;
	if ((int)v1.isArguments > (int)v2.isArguments) return true;
	if ((int)v1.isArguments < (int)v2.isArguments) return false;
	return true;
};
bool operator==(const Entity& v1,const Entity& v2) {
	return (
		v1.id == v2.id &&
		v1.hasArguments == v2.hasArguments &&
		v1.isArguments == v2.isArguments
	);
};
bool operator!=(const Entity& v1,const Entity& v2) {
	return !(v1 == v2);
};
#include "EntityArgumentListRow.h"

EntityArgumentListRow::EntityArgumentListRow(EntityRow* entity,const bool hasArguments):
	entity(entity),
	hasArguments(hasArguments) {};

bool operator<(const EntityArgumentListRow& v1,const EntityArgumentListRow& v2) {
	return v1.entity < v2.entity || v1.entity == v2.entity && (int)v1.hasArguments < (int)v2.hasArguments;
};
bool operator>(const EntityArgumentListRow& v1,const EntityArgumentListRow& v2) {
	return v1.entity > v2.entity || v1.entity == v2.entity && (int)v1.hasArguments > (int)v2.hasArguments;
};
bool operator<=(const EntityArgumentListRow& v1,const EntityArgumentListRow& v2) {
	return v1.entity <= v2.entity || v1.entity == v2.entity && (int)v1.hasArguments <= (int)v2.hasArguments;
};
bool operator>=(const EntityArgumentListRow& v1,const EntityArgumentListRow& v2) {
	return v1.entity >= v2.entity || v1.entity == v2.entity && (int)v1.hasArguments >= (int)v2.hasArguments;
};
bool operator==(const EntityArgumentListRow& v1,const EntityArgumentListRow& v2) {
	return v1.entity == v2.entity && (int)v1.hasArguments == (int)v2.hasArguments;
};
bool operator!=(const EntityArgumentListRow& v1,const EntityArgumentListRow& v2) {
	return v1.entity != v2.entity || (int)v1.hasArguments != (int)v2.hasArguments;
};
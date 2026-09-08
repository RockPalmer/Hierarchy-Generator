#include "ArgumentNameRow.h"

ArgumentNameRow::ArgumentNameRow(ArgumentRow* argument,const std::string name):
	argument(argument),
	name(name) {};

bool operator<(const ArgumentNameRow& v1,const ArgumentNameRow& v2) {
	return v1.argument < v2.argument || v1.argument == v2.argument && v1.name < v2.name;
};
bool operator>(const ArgumentNameRow& v1,const ArgumentNameRow& v2) {
	return v1.argument > v2.argument || v1.argument == v2.argument && v1.name > v2.name;
};
bool operator<=(const ArgumentNameRow& v1,const ArgumentNameRow& v2) {
	return v1.argument <= v2.argument || v1.argument == v2.argument && v1.name <= v2.name;
};
bool operator>=(const ArgumentNameRow& v1,const ArgumentNameRow& v2) {
	return v1.argument >= v2.argument || v1.argument == v2.argument && v1.name >= v2.name;
};
bool operator==(const ArgumentNameRow& v1,const ArgumentNameRow& v2) {
	return v1.argument == v2.argument && v1.name == v2.name;
};
bool operator!=(const ArgumentNameRow& v1,const ArgumentNameRow& v2) {
	return v1.argument != v2.argument || v1.name != v2.name;
};
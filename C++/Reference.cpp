#include <iostream>

#include "Reference.h"

Argument::Argument(const std::string name):
	Argument(name,{},{}) {};
Argument::Argument(const std::string name,const std::set<Reference>& returns,const std::set<Reference>& inherits):
	name(name),
	hasDefaultValue(false),
	returns(returns),
	inherits(inherits) {};

std::string Argument::to_string() const {
	std::string block = "",result = name;
	if (returns.size() > 0) {
		result += ":";
	};
	for (const Reference& r : returns) {
		block += "|" + r.to_string();
	};
	result += block.substr(1);
	if (inherits.size() > 0) {
		result += "<";
	};
	block = "";
	for (const Reference& r : inherits) {
		block += "&" + r.to_string();
	};
	result += block.substr(1);
	if (hasDefaultValue) {
		result += "=" + defaultValue;
	};
	return result;
};

ArgumentList::ArgumentList(const std::vector<Argument>& values):
	values(values) {};

Argument& ArgumentList::operator[](const size_t index) {
	return values[index];
};
const Argument& ArgumentList::operator[](const size_t index) const {
	return values[index];
};

size_t ArgumentList::size() const {
	return values.size();
};

std::vector<Argument>::iterator ArgumentList::begin() {
	return values.begin();
};
std::vector<Argument>::iterator ArgumentList::end() {
	return values.end();
};

std::vector<Argument>::const_iterator ArgumentList::begin() const {
	return values.begin();
};
std::vector<Argument>::const_iterator ArgumentList::end() const {
	return values.end();
};

std::string ArgumentList::to_string() const {
	std::string result = "";
	if (size() > 0) {
		result += values[0].to_string();
	};
	for (size_t i = 1; i < size(); ++i) {
		result += "," + values[i].to_string();
	};
	return "(" + result + ")";
};

Identifier::Identifier(const std::string name):
	hasArguments(false),
	names{name},
	arguments({}) {};
Identifier::Identifier(const std::vector<std::string>& names):
	hasArguments(false),
	names(names),
	arguments({}) {};
Identifier::Identifier(const std::string name,const ArgumentList& arguments):
	hasArguments(true),
	names{name},
	arguments(arguments) {};
Identifier::Identifier(const std::vector<std::string>& names,const ArgumentList& arguments):
	hasArguments(true),
	names(names),
	arguments(arguments) {};

std::string Identifier::to_string() const {
	std::string result = names[0];
	for (size_t i = 1; i < names.size(); ++i) {
		result += "," + names[i];
	};
	if (names.size() > 1) {
		result = "(" + result + ")";
	};
	if (hasArguments) {
		result += arguments.to_string();
	};
	return result;
};

Reference::Reference(const std::vector<Identifier>& values):
	values(values) {};
Reference::Reference(const std::vector<Identifier>::iterator start,const std::vector<Identifier>::iterator stop):
	values(start,stop) {};
Reference::Reference(const std::vector<Identifier>::const_iterator start,const std::vector<Identifier>::const_iterator stop):
	values(start,stop) {};

Identifier& Reference::operator[](const size_t index) {
	return values[index];
};
const Identifier& Reference::operator[](const size_t index) const {
	return values[index];
};

size_t Reference::size() const {
	return values.size();
};

std::vector<Identifier>::iterator Reference::begin() {
	return values.begin();
};
std::vector<Identifier>::iterator Reference::end() {
	return values.end();
};

std::vector<Identifier>::const_iterator Reference::begin() const {
	return values.begin();
};
std::vector<Identifier>::const_iterator Reference::end() const {
	return values.end();
};

std::string Reference::to_string() const {
	std::string result = values[0].to_string();
	for (size_t i = 1; i < size(); ++i) {
		result += "." + values[i].to_string();
	};
	return result;
};
void Reference::push_back(const Identifier& identifier) {
	values.push_back(identifier);
};
void Reference::insert(const std::vector<Identifier>::iterator i1,const std::vector<Identifier>::iterator i2,const std::vector<Identifier>::iterator i3) {
	values.insert(i1,i2,i3);
};

bool operator<(const Reference& v1,const Reference& v2) {
	return v1.to_string() < v2.to_string();
};
bool operator<=(const Reference& v1,const Reference& v2) {
	return v1.to_string() <= v2.to_string();
};
bool operator>(const Reference& v1,const Reference& v2) {
	return v1.to_string() > v2.to_string();
};
bool operator>=(const Reference& v1,const Reference& v2) {
	return v1.to_string() >= v2.to_string();
};
bool operator==(const Reference& v1,const Reference& v2) {
	return v1.to_string() == v2.to_string();
};
bool operator!=(const Reference& v1,const Reference& v2) {
	return v1.to_string() != v2.to_string();
};
#ifndef _REFERENCE_H_
#define _REFERENCE_H_

#include <string>
#include <vector>
#include <set>

#include "AST.h"
#include "characters.h"

struct Reference;

struct Argument {
	std::string name;
	std::set<Reference> returns;
	std::set<Reference> inherits;

	Argument(const std::string name);
	Argument(const std::string name,const std::set<Reference>& returns,const std::set<Reference>& inherits);

	std::string to_string() const;
};

struct ArgumentList {
	std::vector<Argument> values;

	ArgumentList();
	ArgumentList(const Argument& argument);
	ArgumentList(const std::vector<Argument>& values);

	Argument& operator[](const size_t index);
	const Argument& operator[](const size_t index) const;

	size_t size() const;

	std::vector<Argument>::iterator begin();
	std::vector<Argument>::iterator end();

	std::vector<Argument>::const_iterator begin() const;
	std::vector<Argument>::const_iterator end() const;

	std::string to_string() const;
};

struct Identifier {
	bool hasArguments;
	std::set<std::string> names;
	ArgumentList arguments;

	Identifier();
	Identifier(const std::string name);
	Identifier(const std::set<std::string>& names);
	Identifier(const std::string name,const ArgumentList& arguments);
	Identifier(const std::set<std::string>& names,const ArgumentList& arguments);

	std::string to_string() const;
};

struct Reference {
	std::vector<Identifier> values;
	bool hasArgument;
	Identifier argumentIdentifier;

	Reference();
	Reference(const Reference& reference,const Identifier& argumentIdentifier);
	Reference(const Identifier& value);
	Reference(const Identifier& value,const Identifier& argumentIdentifier);
	Reference(const std::vector<Identifier>& values);
	Reference(const std::vector<Identifier>& values,const Identifier& argumentIdentifier);
	Reference(const std::vector<Identifier>::iterator startVals,const std::vector<Identifier>::iterator stopVals);
	Reference(const std::vector<Identifier>::iterator startVals,const std::vector<Identifier>::iterator stopVals,const Identifier& argumentIdentifier);
	Reference(const std::vector<Identifier>::const_iterator startVals,const std::vector<Identifier>::const_iterator stopVals);
	Reference(const std::vector<Identifier>::const_iterator startVals,const std::vector<Identifier>::const_iterator stopVals,const Identifier& argumentIdentifier);

	Identifier& operator[](const size_t index);
	const Identifier& operator[](const size_t index) const;

	size_t size() const;

	std::vector<Identifier>::iterator begin();
	std::vector<Identifier>::iterator end();

	std::vector<Identifier>::const_iterator begin() const;
	std::vector<Identifier>::const_iterator end() const;

	std::string to_string() const;

	void push_back(const Identifier& identifier);
	void insert(const std::vector<Identifier>::iterator i1,const std::vector<Identifier>::iterator i2,const std::vector<Identifier>::iterator i3);
};

bool operator<(const Reference& v1,const Reference& v2);
bool operator<=(const Reference& v1,const Reference& v2);
bool operator>(const Reference& v1,const Reference& v2);
bool operator>=(const Reference& v1,const Reference& v2);
bool operator==(const Reference& v1,const Reference& v2);
bool operator!=(const Reference& v1,const Reference& v2);

bool canBeReference(const AST& ast);
bool canBeIdentifier(const AST& ast);
bool canBeArgumentList(const AST& ast);
bool canBeArgument(const AST& ast);

#endif
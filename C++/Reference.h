#ifndef _REFERENCE_H_
#define _REFERENCE_H_

#include <string>
#include <vector>

struct Reference;

struct Argument {
	std::string name;
	bool hasDefaultValue;
	std::string defaultValue;
	std::vector<Reference> returns;
	std::vector<Reference> inherits;

	Argument(const std::string name);
	Argument(const std::string name,const std::string defaultValue);
	Argument(const std::string name,const std::vector<Reference>& returns,const std::vector<Reference>& inherits);
	Argument(const std::string name,const std::string defaultValue,const std::vector<Reference>& returns,const std::vector<Reference>& inherits);

	std::string to_string() const;
};

struct ArgumentList {
	std::vector<Argument> values;

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
	std::vector<std::string> names;
	ArgumentList arguments;

	Identifier(const std::string name);
	Identifier(const std::vector<std::string>& names);
	Identifier(const std::string name,const ArgumentList& arguments);
	Identifier(const std::vector<std::string>& names,const ArgumentList& arguments);

	std::string to_string() const;
};

struct Reference {
	std::vector<Identifier> values;

	Reference(const std::vector<Identifier>& values);
	Reference(const std::vector<Identifier>::iterator start,const std::vector<Identifier>::iterator stop);
	Reference(const std::vector<Identifier>::const_iterator start,const std::vector<Identifier>::const_iterator stop);

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

#endif
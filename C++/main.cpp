#include <vector>

#include <string>
#include <vector>
#include <set>
#include <cctype>
#include <iostream>

#include "EntityRow.h"
#include "EntityNameRow.h"
#include "EntityGroupRow.h"
#include "EntityArgumentListRow.h"
#include "EntityEqualityRow.h"
#include "ArgumentRow.h"
#include "ArgumentNameRow.h"
#include "ArgumentGroupRow.h"
#include "AST.h"
/*
g++ -o ArgumentGroupRow.cpp ArgumentNameRow.cpp ArgumentRow.cpp AST.cpp EntityArgumentListRow.cpp EntityEqualityRow.cpp EntityGroupRow.cpp EntityNameRow.cpp EntityRow.cpp main.cpp
*/

std::set<EntityRow> ENTITIES;
std::set<EntityNameRow> ENTITY_NAMES;
std::set<EntityArgumentListRow> ENTITY_ARGUMENT_LISTS;
std::set<EntityGroupRow> ENTITY_INTERSECTIONS;
std::set<EntityGroupRow> ENTITY_UNIONS;
std::set<EntityGroupRow> ATTRIBUTION;
std::set<EntityGroupRow> INHERITANCE;
std::set<EntityGroupRow> TYPES;
std::set<ArgumentRow> ARGUMENTS;
std::set<ArgumentNameRow> ARGUMENT_NAMES;
std::set<ArgumentGroupRow> ARGUMENT_TYPES;
std::set<ArgumentGroupRow> ARGUMENT_INHERITANCE;
std::set<ArgumentGroupRow> ARGUMENT_CONTAINERS;
std::set<EntityEqualityRow> EQUALITIES;

std::vector<char> BINOPS = {
	',',
	'<',
	'>',
	'=',
	':',
	'|',
	'&',
	'.'
};

AST parse(const std::string expression);
std::string lstrip(const std::string value);
std::string rstrip(const std::string value);
std::string strip(const std::string value);
std::vector<size_t> getIndices(const std::string subject,const char value);
std::vector<size_t> filter(const std::vector<size_t>& values,const size_t bottom,const size_t top);
int main();

//---------------------

std::string lstrip(const std::string value) {
	if (value.length() > 0 && std::isspace(value[0]))
		for (size_t i = 0;i < value.length();i++)
			if (!std::isspace(value[i]))
				return value.substr(i - 1);
	return value;
};
std::string rstrip(const std::string value) {
	if (value.length() > 0 && std::isspace(value[value.length() - 1]))
		for (size_t i = 0;i < value.length();i++)
			if (!std::isspace(value[value.length() - i - 1]))
				return value.substr(0,value.length() - i - 1);
	return value;
};
std::string strip(const std::string value) {
	return lstrip(rstrip(value));
};
std::vector<size_t> getIndices(const std::string subject,const char value) {
	std::vector<size_t> values;
	for (size_t i = 0;i < subject.length();i++)
		if (subject[i] == value)
			values.push_back(i);
	return values;
};
std::vector<size_t> filter(const std::vector<size_t>& values,const size_t bottom,const size_t top) {
	std::vector<size_t> vals;
	for (const size_t v : values)
		if (bottom > v || v > top)
			vals.push_back(v);
	return vals;
};
AST parse(const std::string expression) {
	if (
		expression.length() > 0 && (
			std::isspace(expression[0]) ||
			std::isspace(expression[expression.length() - 1])
		)
	) return parse(strip(expression));
	std::vector<size_t> left,right;

	for (size_t i = 0;i < expression.length();i++) {
		switch (expression[i]) {
			case '(':
			case '{':
				left.push_back(i);
				right.push_back(std::string::npos);
				break;
			case ')':
			case '}':
				for (size_t j = 0;j < left.size();i++)
					if (right[right.size() - j - 1] == std::string::npos) {
						right[right.size() - j - 1] = i;
						break;
					};
				break;
		};
	};
	if (left.size() > 0 && left[0] == 0 && right[0] == expression.length() - 1) return AST(
		expression[left[0]] + expression[right[0]],
		{parse(expression.substr(left[0] + 1,right[0] - left[0] - 1))}
	);
	std::vector<size_t> indices;
	if (left.size() > 0) {
		for (const charcl op : BINOPS) {
			indices = filter(getIndices(expression,op),left[0],right[0]);
			if (indices.size() > 0) {
				return AST(
					"" + op,{
						parse(expression.substr(0,indices[0])),
						parse(expression.substr(indices[0] + 1,expression.length() - indices[0]))
					}
				);
			};
		};
	};
	for (size_t i = 0;i < expression.length();i++) {
		if (std::isspace(expression[i])) {
			return AST(
				' ',{
					parse(expression.substr(0,i)),
					parse(expression.substr(i + 1,expression.length() - i))
				}
			);
		};
	};
	if (left.size() > 0)
		return AST(
			' ',{
				parse(expression.substr(0,left[0])),
				parse(expression.substr(left[0],expression.length() - left[0]))
			}
		);
	return AST(expression,{});
};
int main() {
	std::cout << parse("type1 < type2,type1 : type2,type1 = type2,{type1},type1(type2)")
};
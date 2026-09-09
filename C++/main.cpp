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
g++ ArgumentGroupRow.cpp ArgumentNameRow.cpp ArgumentRow.cpp AST.cpp EntityArgumentListRow.cpp EntityEqualityRow.cpp EntityGroupRow.cpp EntityNameRow.cpp EntityRow.cpp main.cpp -o main
*/

size_t iter = 0;

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

std::vector<std::string> BINOPS = {
	";",
	",",
	"<",
	">",
	"=",
	":",
	"*",
	"|",
	"&",
	"^",
	"@",
	".",
	"!",
};
std::vector<std::string> UNOPS = {
	"+",
	"-",
	"#",
	"~"
};

AST parse(const std::string expression);
std::string lstrip(const std::string value);
std::string rstrip(const std::string value);
std::string strip(const std::string value);
std::vector<size_t> getIndices(const std::string& a,const std::string& b);
std::vector<size_t> filter(const std::vector<size_t>& values,const size_t bottom,const size_t top);
void prt(const std::string value);
void up();
void dn();
int main();

//---------------------

void prt(const std::string value) {
	for (size_t i = 0;i < iter;i++) std::cout << " ";
	std::cout << value << std::endl;
};
void up() {
	++iter;
};
void dn() {
	--iter;
};
std::string lstrip(const std::string value) {
	if (value.length() > 0 && std::isspace(value[0]))
		for (size_t i = 0;i < value.length();i++)
			if (!std::isspace(value[i]))
				return value.substr(i);
	return value;
};
std::string rstrip(const std::string value) {
	if (value.length() > 0 && std::isspace(value[value.length() - 1]))
		for (size_t i = 0;i < value.length();i++)
			if (!std::isspace(value[value.length() - i - 1]))
				return value.substr(0,value.length() - i);
	return value;
};
std::string strip(const std::string value) {
	return lstrip(rstrip(value));
};
std::vector<size_t> getIndices(const std::string& a,const std::string& b) {
    std::vector<size_t> indices;

    if (b.empty()) return indices;

    size_t pos = a.find(b);
    while (pos != std::string::npos) {
        indices.push_back(pos);
        pos = a.find(b,pos + 1);
    };

    return indices;
}
std::vector<size_t> filter(const std::vector<size_t>& values,const size_t bottom,const size_t top) {
	std::vector<size_t> vals;
	for (const size_t v : values)
		if (bottom > v || v > top)
			vals.push_back(v);
	return vals;
};
AST parse(const std::string expression) {
	prt("parse(\"" + expression + "\") {");
	up();
	if (
		expression.length() > 0 && (
			std::isspace(expression[0]) ||
			std::isspace(expression[expression.length() - 1])
		)
	) {
		AST x = parse(strip(expression));
		dn();
		prt("} -> " + to_string(x));
		return AST(x);
	};
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
	if (left.size() > 0 && left[0] == 0 && right[0] == expression.length() - 1) {
		prt(">>" + expression.substr(left[0],1));
		prt(">>" + expression.substr(right[0],1));
		AST x = AST(
			expression.substr(left[0],1) + expression.substr(right[0],1),
			{parse(expression.substr(left[0] + 1,right[0] - left[0] - 1))}
		);
		dn();
		prt("} -> " + to_string(x));
		return AST(x);
	};
	std::vector<size_t> indices;
	for (const std::string op : BINOPS) {
		if (left.size() > 0)
			indices = filter(getIndices(expression,op),left[0],right[0]);
		else
			indices = getIndices(expression,op);
		if (indices.size() > 0) {
			AST x = AST(
				op,{
					parse(expression.substr(0,indices[0])),
					parse(expression.substr(indices[0] + op.length()))
				}
			);
			dn();
			prt("} -> " + to_string(x));
			return AST(x);
		};
	};
	for (const std::string op : UNOPS) {
		if (left.size() > 0)
			indices = filter(getIndices(expression,op),left[0],right[0]);
		else
			indices = getIndices(expression,op);
		if (indices.size() > 0 && indices[0] == 0) {
			AST x = AST(
				op,{
					parse(expression.substr(op.length()))
				}
			);
			dn();
			prt("} -> " + to_string(x));
			return AST(x);
		};
	};
	for (size_t i = 0;i < expression.length();i++) {
		if (std::isspace(expression[i])) {
			AST x = AST(
				"",{
					parse(expression.substr(0,i)),
					parse(expression.substr(i + 1,expression.length() - i))
				}
			);
			dn();
			prt("} -> " + to_string(x));
			return AST(x);
		};
	};
	if (left.size() > 0) {
		AST x = AST(
			"",{
				parse(expression.substr(0,left[0])),
				parse(expression.substr(left[0],expression.length() - left[0]))
			}
		);
		dn();
		prt("} -> " + to_string(x));
		return AST(x);
	};
	AST x = AST(expression,{});
	dn();
	prt("} -> " + to_string(x));
	return AST(x);
};
int main() {
	std::cout << parse("type1 < type2,type1 : type2,type1 = type2,{type1},type1(type2)");
};
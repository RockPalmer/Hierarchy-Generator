#include <string>
#include <vector>
#include <set>
#include <map>
#include <sstream>
#include <iostream>
#include <regex>
#include <cctype>

#include "AST.h"
#include "Reference.h"
#include "Entity.h"
#include "EntityName.h"
#include "EntityPair.h"
#include "EntityArgument.h"

// g++ -o main main.cpp AST.cpp Reference.cpp Entity.cpp EntityName.cpp EntityPair.cpp EntityArgument.cpp

size_t CURRENT = 0;

std::set<Entity> ENTITIES = {
	{0,false,false}
};
std::set<EntityName> ENTITY_NAMES;
std::set<EntityPair> PARENTS;
std::set<EntityPair> RETURNS;
std::set<EntityPair> ATTRIBUTES;
std::set<EntityArgument> ARGUMENTS;

int main();
AST parse(const AST& ast);
AST parseGroupers(const AST& tokens);
AST tokenize(const AST& ast);
AST combine(const AST& ast);
AST parseBinary(const AST& ast,const size_t index);
AST parseUnary(const AST& ast);
AST parseNoSpace(const AST& ast);
AST squash(const AST& ast);
bool isName(const std::string value);
bool containsName(const AST& ast);
bool isUnaryOperator(const AST& ast);
std::string ltrim(const std::string value);
std::string rtrim(const std::string value);
std::string trim(const std::string value);
std::string uppercase(const std::string value);
void handleCommand(const std::string value);
//------------------------------------------------------------------------------
size_t itera = 0;
void prt(std::string value) {
	std::string result = "";
	for (size_t i = 0; i < itera; ++i) result += "  ";
	std::cout << result + value << std::endl;
};
void up() {
	++itera;
};
void dn() {
	--itera;
};
std::vector<std::string> BINOPS = {
	",",
	"=",
	":",
	"<",
	">",
	"&",
	"|",
	"-",
	"*",
	"."
};
AST tokenize(const AST& ast) {
	std::string str = ast.to_string();
	std::vector<AST> a;
	std::string item = "";
	for (size_t i = 0; i < str.length(); ++i) {
		switch (str[i]) {
			case '\t':
			case '\n':
			case ' ':
				if (item.length() > 0) {
					a.push_back(AST(item));
				};
				item = "";
				break;
			case '(':
			case ')':
			case '{':
			case '}':
			case '=':
			case ',':
			case '.':
			case '&':
			case '|':
			case '-':
			case '*':
			case '<':
			case '>':
			case ':':
				if (item.length() > 0) {
					a.push_back(AST(item));
				};
				item = "";
				a.push_back(AST(str[i]));
				break;
			default:
				item += str[i];
				break;
		};
	};
	if (item.length() > 0) {
		a.push_back(AST(item));
	};
	if (a.size() == 1) {
		return AST(a[0].to_string());
	};
	return AST(a);
};
AST parse(const AST& ast) {
	AST a = tokenize(ast);
	a = combine(a);
	a = parseGroupers(a);
	a = parseBinary(a,0);
	return a;
};
bool isName(const AST& value) {
	std::regex pattern1("[a-zA-Z_][a-zA-Z0-9_]*");
	std::regex pattern2("[a-zA-Z]");
	std::string str = value.to_string();
	std::smatch match;
	return (
		std::regex_match(str,match,pattern1) && std::regex_search(str,match,pattern2) ||
		value.type == GROUPER
	);
};
bool containsName(const AST& ast) {
	for (const AST& a : ast) if (isName(a)) return true;
	return false;
};
bool isUnaryOperator(const AST& ast) {
	return (
		ast.to_string() == "*" ||
		ast.to_string() == "**"
	);
};
AST combine(const AST& ast) {
	if (ast.type != BINARY) {
		return ast;
	};
	std::vector<AST> arguments;
	for (size_t i = 0; i < ast.size(); ++i) {
		if (
			i + 2 < ast.size() &&
			ast[i].to_string() == "*" &&
			ast[i + 1].to_string() == "*"
		) {
			arguments.push_back(AST("**"));
			++i;
		} else {
			arguments.push_back(ast[i]);
		};
	};
	return AST(arguments);
};
AST parseGroupers(const AST& tokens) {
	AST arguments = tokens;
	AST arguments2;

	bool found = true;
	size_t start,end;
	std::string start_c,end_c;
	while (found) {
		found = false;
		for (size_t i = 0; i < arguments.size(); ++i) {
			if (
				arguments[i].to_string() == "(" ||
				arguments[i].to_string() == "{"
			) {
				start = i;
				start_c = arguments[i].to_string();
			} else if (
				arguments[i].to_string() == ")" ||
				arguments[i].to_string() == "}"
			) {
				found = true;
				end = i;
				end_c = arguments[i].to_string();
				break;
			};
		};
		if (found) {
			arguments2.insert(
				arguments2.end(),
				arguments.begin(),
				arguments.begin() + start
			);
			if (start + 1 == end) {
				arguments2.push_back(AST(
					GROUPER,{},{start_c,end_c}
				));
			} else {
				arguments2.push_back(AST(
					GROUPER,{
						parse(AST(
							arguments.begin() + start + 1,
							arguments.begin() + end
						))
					},{
						start_c,end_c
					}
				));
			};
			arguments2.insert(
				arguments2.end(),
				arguments.begin() + end + 1,
				arguments.end()
			);
			arguments.clear();
			arguments.insert(
				arguments.end(),
				arguments2.begin(),
				arguments2.end()
			);
			arguments2.clear();
		};
	};
	return AST(arguments);
};
AST parseBinary(const AST& ast,const size_t index) {
	if (index >= BINOPS.size()) {
		return parseNoSpace(ast);
	};
	for (size_t idx = index; idx < BINOPS.size(); ++idx) {
		for (size_t i = 0; i < ast.size(); ++i) {
			if (
				ast[i].to_string() == BINOPS[idx] &&
				i > 0 &&
				i < ast.size() - 1 &&
				containsName(AST(ast.begin(),ast.begin() + i)) &&
				containsName(AST(ast.begin() + i + 1,ast.end()))
			) {
				std::vector<AST> args;
				if (i == 1) {
					args.push_back(parseBinary(ast[0],idx));
				} else {
					args.push_back(parseBinary(AST(ast.begin(),ast.begin() + i),idx));
				};
				if (i == ast.size() - 2) {
					args.push_back(parseBinary(ast[i + 1],idx));
				} else {
					args.push_back(parseBinary(AST(ast.begin() + i + 1,ast.end()),idx));
				};
				return parseNoSpace(AST(
					BINARY,
					args,
					{ast[i].to_string()}
				));
			};
		};
	};
	return parseNoSpace(ast);
};
AST parseUnary(const AST& ast) {
	for (size_t i = 0; i < ast.size(); ++i) {
		if (
			isUnaryOperator(ast[i].to_string()) &&
			i < ast.size() - 1 &&
			containsName(AST(ast.begin() + i + 1,ast.end()))
		) {
			std::vector<AST> args;
			if (i == ast.size() - 2) {
				args.push_back(parseUnary(ast[i + 1]));
			} else {
				args.push_back(parseUnary(AST(ast.begin() + i + 1,ast.end())));
			};
			return AST(
				UNARY,
				args,
				{ast[i].to_string()}
			);
		};
	};
	return ast;
};
AST parseNoSpace(const AST& ast) {
	AST a;
	std::vector<AST> args;
	switch (ast.type) {
		case GROUPER:
			return AST(
				GROUPER,
				{parseNoSpace(ast.arguments[0])},
				{ast.op[0],ast.op[1]}
			);
		case BINARY:
			if (ast.size() > 2) {
				for (size_t i = 1; i < ast.size(); ++i) {
					if (
						containsName(AST(ast.begin(),ast.begin() + i)) &&
						containsName(AST(ast.begin() + i,ast.end()))
					) {
						if (i == 1) {
							args.push_back(parseNoSpace(ast[0]));
						} else {
							args.push_back(parseNoSpace(AST(ast.begin(),ast.begin() + i)));
						};
						if (i == ast.size() - 1) {
							args.push_back(parseNoSpace(ast[ast.size() - 1]));
						} else {
							args.push_back(parseNoSpace(AST(ast.begin() + i,ast.end())));
						};
						return AST(
							BINARY,
							args,
							{""}
						);
					};
				};
			};
			return parseUnary(ast);
	};
	return ast;
};
AST squash(const AST& ast) {
	std::vector<AST> args1,args2;
	switch (ast.type) {
		case NONE: return ast;
		case GROUPER:
		case UNARY:
			return AST(
				ast.type,
				{squash(ast[0])},
				ast.op
			);
		case BINARY:
			args1 = {
				squash(ast[0]),
				squash(ast[1])
			};
			if (
				args1[0].type == BINARY &&
				args1[0].op.size() == 1 &&
				args1[0].op[0] == ast.op[0] &&
				args1[1].type == BINARY &&
				args1[1].op.size() == 1 &&
				args1[1].op[0] == ast.op[0]
			) {
				args2.insert(
					args2.end(),
					args1[0].begin(),
					args1[0].end()
				);
				args2.insert(
					args2.end(),
					args1[1].begin(),
					args1[1].end()
				);
				args1.clear();
				args1.insert(
					args1.end(),
					args2.begin(),
					args2.end()
				);
			};
			return AST(
				BINARY,
				args1,
				ast.op
			);
	};
	return ast;
};
std::string ltrim(const std::string value) {
	size_t index = 0;
	for (; index < value.length(); ++index) {
		if (!std::isspace(value[index])) break;
	};
	return value.substr(index);
};
std::string rtrim(const std::string value) {
	size_t index = value.length() - 1;
	for (; index >= 0; --index) {
		if (!std::isspace(value[index])) break;
	};
	return value.substr(0,index + 1);
};
std::string trim(const std::string value) {
	return ltrim(rtrim(value));
};
std::string uppercase(const std::string value) {
	std::string result = "";
	for (const char& c : value) {
		result += std::toupper(static_cast<unsigned char>(c));
	};
	return result;
};
void handleCommand(const std::string value) {
	std::string command,arguments,line = trim(value);
	size_t index = 0;
	for (; index < line.length(); ++index) {
		if (std::isspace(line[index])) break;
	};
	command = trim(line.substr(0,index));	
	arguments = trim(line.substr(index));
};
size_t getArgumentAt(const size_t id,const size_t index) {
	for (const EntityArgument& argument : ARGUMENTS)
		if (argument.id1 == id && argument.index > max_v)
			return argument.id2;
	return std::string::npos;
};
std::vector<size_t> getArguments(const size_t id) {
	size_t max_v = 0;
	for (const EntityArgument& argument : ARGUMENTS)
		if (argument.id1 == id && argument.index > max_v)
			max_v = argument.index;
	std::vector<size_t> results(max_v + 1);
	for (size_t i = 0; i <= max_v; ++i)
		results[i] = getArgumentAt(id,i);
	return results;
};
bool hasArguments(const size_t id,const ArgumentList& arguments) {
	std::vector<size_t> args = getArguments(id);
	if (arguments.size() != args.size()) return false;
	for (const size_t i = 0; i < arguments.size(); ++i)
		if (!argumentMatches(args[i],arguments[i]))
			return false;
	return true;
};
std::set<size_t> getAttributes(const size_t id) {
	std::set<size_t> results;
	for (const EntityPair& pair : ATTRIBUTES) {
		if (pair.id1 == id)
			results.insert(pair.id2);
	};
	return results;
};
std::set<size_t> getByName(const std::string name,const size_t id) {
	std::set<size_t> results;
	for (const size_t attribute_id : getAttributes(id)) {
		EntityName n(attribute_id,name);
		if (ENTITY_NAMES.find(n) != ENTITY_NAMES.end())
			results.insert(attribute_id);
	};
	return results;
};
std::set<size_t> getByNames(const std::set<std::string>& names,const size_t id) {
	std::set<size_t> results;
	for (const std::string name : names)
		for (const size_t i : getByName(name,id))
			results.insert(i);
	return results;
};
std::set<size_t> getByIdentifier(const Identifier& identifier,const size_t id) {
	if (identifier.hasArguments) {
		std::set<size_t> results;
		for (const size_t i : getByNames(identifier.names,id))
			if (hasArguments(i,identifier.arguments))
				results.insert(i);
		return results;
	};
	return getByName(identifier.name,id);
};
std::set<size_t> getByReference(const Reference& reference,const size_t id) {
	std::set<size_t> ids = getByIdentifier(reference[0],id);
	if (reference.size() == 1) return ids;
	std::set<size_t> result;
	Reference ref = Reference(reference.begin() + 1,reference.end());
	for (const size_t i : ids)
		for (const size_t j : getByIdentifier(ref,i))
			result.insert(j);
	return result;
};
int main() {
	Reference ref = Reference({
		Identifier(
			"type1",
			ArgumentList({
				Argument("/"),
				Argument("arg1","45"),
				Argument("arg2",{},{Reference({Identifier("parent1")}),Reference({Identifier("parent2")})}),
				Argument("arg3",{Reference({Identifier("return1")}),Reference({Identifier("return2")})},{Reference({Identifier("parent1")}),Reference({Identifier("parent2")})})
			})
		),
		Identifier(
			"type2"
		)
	});
	std::cout << ref.to_string() << std::endl;
};

/*

BINARY("=")[
	BINARY("")[
		UNARY("*")[
			NONE("a")
		],
		GROUPER(
			NONE("b")
		)
	],
	BINARY(":")[
		NONE("c"),
		NONE("d")
	]
]

*/
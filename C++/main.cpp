#include <string>
#include <vector>
#include <set>
#include <map>
#include <sstream>
#include <iostream>
#include <regex>
#include <cctype>
#include <tuple>
#include <algorithm>

#include "AST.h"
#include "Reference.h"

// g++ -o main main.cpp AST.cpp Reference.cpp

const std::string PARENT_REFERENCE = "^";
const std::string TOP_REFERENCE = "~";
const std::vector<std::string> BINOPS = {
	",",
	"=",
	":",
	"<",
	">",
	"&",
	"|",
	"-",
	">-",
	"-<",
	"><",
	"--",
	"*",
	"."
};
const std::vector<std::tuple<std::string,std::string>> GROUPING_SYMBOLS = {
	{"(",")"},
	{"{","}"}
};
const std::vector<std::string> SPECIAL_TOKENS = {
	PARENT_REFERENCE,
	TOP_REFERENCE
};

size_t CURRENT = 0;

std::vector<std::tuple<size_t,bool,bool>> ENTITIES = {
	{0,false,false}
};
std::vector<std::tuple<size_t,std::string>> ENTITY_NAMES = {
	{0,TOP_REFERENCE}
};
std::vector<std::tuple<size_t,std::string>> DEFAULT_VALUES;
std::vector<std::tuple<size_t,size_t>> PARENTS;
std::vector<std::tuple<size_t,size_t>> RETURNS;
std::vector<std::tuple<size_t,size_t>> ATTRIBUTES;
std::vector<std::tuple<size_t,size_t,size_t>> ARGUMENTS;

int main();
AST parse(const AST& ast);
AST parseGroupers(const AST& tokens);
AST tokenize(const AST& ast);
AST parseBinary(const AST& ast,const size_t index);
AST parseUnary(const AST& ast);
AST parseNoSpace(const AST& ast);
AST squash(const AST& ast);
bool isName(const std::string value);
bool containsName(const AST& ast);
bool isUnaryOperator(const AST& ast);
bool defined(const std::string name);
std::string ltrim(const std::string value);
std::string rtrim(const std::string value);
std::string trim(const std::string value);
std::string uppercase(const std::string value);
void addEntityName(const size_t id,const std::string name);
void handleCommand(const std::string value);
size_t tokenMaxLength();
size_t addEntity();
std::vector<std::string> tokensOfLength(const size_t length);
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
size_t tokenMaxLength() {
	size_t max_length_token = 0;
	for (const std::string& binop : BINOPS)
		if (binop.length() > max_length_token)
			max_length_token = binop.length();
	for (const auto [ left , right ] : GROUPING_SYMBOLS) {
		if (left.length() > max_length_token)
			max_length_token = left.length();
		if (right.length() > max_length_token)
			max_length_token = right.length();
	};
	for (const std::string& token : SPECIAL_TOKENS)
		if (token.length() > max_length_token)
			max_length_token = token.length();
	return max_length_token;
};
std::vector<std::string> tokensOfLength(const size_t length) {
	std::vector<std::string> tokens;
	for (const std::string& binop : BINOPS)
		if (binop.length() == length)
			tokens.push_back(binop);
	for (const auto [ left , right ] : GROUPING_SYMBOLS) {
		if (left.length() == length)
			tokens.push_back(left);
		if (right.length() == length)
			tokens.push_back(right);
	};
	for (const std::string& token : SPECIAL_TOKENS)
		if (token.length() == length)
			tokens.push_back(token);
	return tokens;
};
AST tokenize(const AST& ast) {
	std::string str = ast.to_string();
	std::vector<AST> a;
	std::string item = "";
	std::vector<std::string> tokens;
	size_t max_length_token = tokenMaxLength();
	size_t index = std::string::npos;
	for (size_t i = 0; i < str.length(); ++i) {
		switch (str[i]) {
			case '\t':
			case '\n':
			case ' ':
				if (item.length() > 0)
					a.push_back(AST(item));
				item = "";
				break;
			default:
				for (size_t j = max_length_token; j > 0; --j) {
					tokens = tokensOfLength(j);
					for (const std::string& token : tokens) {
						if (str.substr(i,j) == token) {
							index = j;
							break;
						};
					};
					if (index != std::string::npos)
						break;
				};
				if (index == std::string::npos)
					item += str[i];
				else {
					if (item.length() > 0)
						a.push_back(AST(item));
					item = "";
					a.push_back(AST(str.substr(i,index)));
					index = std::string::npos;
				};
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
	a = parseGroupers(a);
	a = parseBinary(a,0);
	a = squash(a);
	return a;
};
bool isName(const AST& value) {
	std::regex pattern1("[a-zA-Z_][a-zA-Z0-9_]*");
	std::regex pattern2("[a-zA-Z]");
	std::string str = value.to_string();
	std::smatch match;
	for (const std::string& token : SPECIAL_TOKENS)
		if (token == str)
			return true;
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
			if (ast.size() > 0) {
				return AST(
					GROUPER,
					{parseNoSpace(ast.arguments[0])},
					{ast.op[0],ast.op[1]}
				);
			};
			return ast;
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
		case UNARY:
			return AST(
				ast.type,
				{squash(ast[0])},
				ast.op
			);
		case GROUPER:
			if (ast.size() > 0)
				return AST(
					ast.type,
					{squash(ast[0])},
					ast.op
				);
			return ast;
		case BINARY:
			args1 = {
				squash(ast[0]),
				squash(ast[1])
			};
			if (
				args1[0].type == BINARY &&
				args1[0].op.size() == 1 &&
				args1[0].op[0] == ast.op[0]
			) {
				args2.insert(
					args2.end(),
					args1[0].begin(),
					args1[0].end()
				);
			} else {
				args2.push_back(args1[0]);
			};
			if (
				args1[1].type == BINARY &&
				args1[1].op.size() == 1 &&
				args1[1].op[0] == ast.op[0]
			) {
				args2.insert(
					args2.end(),
					args1[1].begin(),
					args1[1].end()
				);
			} else {
				args2.push_back(args1[1]);
			};
			args1.clear();
			args1.insert(
				args1.end(),
				args2.begin(),
				args2.end()
			);
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
//--------------------------------------------------------------------
std::set<size_t> getAttributeIds(const size_t id) {
	std::set<size_t> ids;
	for (const auto [ parentid , childid ] : ATTRIBUTES)
		if (parentid == id)
			ids.insert(id);
	return ids;
};
std::set<std::string> getNames(const size_t id) {
	std::set<std::string> names;
	for (const auto [ entityid , name ] : ENTITY_NAMES)
		if (entityid == id)
			names.insert(name);
	return names;
};
bool defined(const size_t id,const Reference& reference) {
	size_t current = id;
	char c;
	for (size_t i = 0; i < reference.size(); ++i) {
		c = i == 0 ? '.' : reference.ops[i - 1];
		if (!defined())
	};
};
size_t addEntity() {
	size_t max_id = 0;
	for (const auto [ entityid , isArgument , hasArguments ] : ENTITIES)
		if (entityid > max_id)
			max_id = entityid + 1;
	ENTITIES.emplace_back(max_id,false,false);
	return max_id;
};
void addEntityName(const size_t id,const std::string name) {
	ENTITY_NAMES.emplace_back(id,name);
};
void cmd_define(const AST& ast) {
	if (ast.type == NONE) {
		std::string name = ast.to_string();
		if (!defined(CURRENT,Reference(Identifier(name)))) {
			size_t entityid = addEntity();
			addAttribute(CURRENT,entityid);
			addEntityName(entityid,name);
		};
	};
	switch (ast.type) {
		case NONE:
			if (!defined(ast.to)) {
				size_t entityid = addEntity();
				addEntityName(entityid,name);
			};
			break;
		case BINARY:
			if (ast.op[0] == ".") {

			};
	};
};
int main() {
	std::cout << parse(AST("type1: type2 = {} < type3")).repr() << std::endl;
};
/*
",",
"=",
":",
"<",
">",
"&",
"|",
"-",
">-",
"-<",
"><",
"--",
"*",
"."
bool hasArguments(const size_t id) {
	for (const auto& [ entityid , isArgument , hasArguments ] : ENTITIES)
		if (id == entityid)
			return hasArguments;
	return false;
};
std::set<std::string> getNames(const size_t id) {
	std::set<std::string> names;
	for (const auto& [ entityid , name ] : ENTITY_NAMES)
		if (id == entityid)
			names.insert(name);
	return names;
};
size_t getMaxIndex(const size_t id) {
	size_t max_v = 0;
	for (const auto& [ entityid , argumentid , index ] : ARGUMENTS)
		if (max_v < index)
			max_v = index;
	return max_v;
};
size_t getArgumentIdAt(const size_t id,const size_t index) {
	for (const auto& [ entityid , argumentid , idx ] : ARGUMENTS)
		if (entityid == id && idx == index)
			return argumentid;
	return std::string::npos;
};
std::string getName(const size_t id) {
	for (const auto& [ entityid , name ] : ENTITY_NAMES)
		if (entityid == id)
			return name;
	return "";
};
Reference getReference(const size_t id) {
	std::vector<Identifier> values = {
		getIdentifier(id)
	};
	if (hasContainer(id)) {
		size_t containerid = getContainerId(id);
		if (containerid == 0) {
			return Reference(values);
		};
		Reference ref = getReference(containerid);
		ref.push_back(values[0]);
		return ref;
	};
	return Reference(values);
};
std::set<Reference> getReturnValues(const size_t id) {
	std::set<Reference> returnValues;
	for (const auto& [ parentid , childid ] : RETURNS)
		if (parentid == id)
			returnValues.insert(getReference(childid));
	return returnValues;
};
std::set<Reference> getParents(const size_t id) {
	std::set<Reference> parents;
	for (const auto& [ childid , parentid ] : RETURNS)
		if (childid == id)
			parents.insert(getReference(parentid));
	return parents;
};
Argument getArgument(const size_t id) {
	return Argument(
		getName(id),
		getReturnValues(id),
		getParents(id)
	);
};
std::vector<Argument> getArguments(const size_t id) {
	size_t numberOfArguments = getMaxIndex(id) + 1;
	std::vector<size_t> argumentids;
	for (size_t i = 0; i < numberOfArguments; ++i)
		argumentids.push_back(getArgumentIdAt(id,i));
	std::vector<Argument> arguments;
	for (size_t i = 0; i < numberOfArguments; ++i)
		arguments.push_back(getArgument(argumentids[i]));
	return arguments;
};
ArgumentList getArgumentList(const size_t id) {
	return ArgumentList(
		getArguments(id)
	);
};
Identifier getIdentifier(const size_t id) {
	if (hasArguments(id))
		return Identifier(
			getNames(id),
			getArgumentList(id)
		);
	return Identifier(
		getNames(id)
	);
};
std::map<size_t,Identifier> getAttributes(const size_t id) {
	std::map<size_t,Identifier> values;
	for (const auto& [ containerid , attributeid ] : ATTRIBUTES)
		if (id == containerid)
			values[attributeid] = getIdentifier(attributeid);
	return values;
};
bool areDisjoint(const std::set<size_t>& a, const std::set<size_t>& b) {
    std::vector<size_t> intersection;
    std::set_intersection(a.begin(),a.end(),b.begin(),b.end(),std::back_inserter(intersection));
    return intersection.empty();
};
bool referenceListContains(const std::set<Reference>& list,const Reference& reference) {
	std::set<size_t> mainList = getByReference(reference);
	for (const Reference& ref : list) {
		std::set<size_t> argList = getByReference(ref);
		if (!areDisjoint(argList,mainList))
			return true;
	};
	return false;
};
bool referenceListIncludes(const std::set<Reference>& list1,const std::set<Reference>& list2) {
	for (const Reference& reference : list1)
		if (!referenceListContains(list2,reference))
			return false;
	return true;
};
bool argumentsMatch(const ArgumentList& arguments1,const ArgumentList& arguments2) {
	if (arguments1.size() != arguments2.size())
		return false;
	for (size_t i = 0; i < arguments1.size(); ++i) {
		if (arguments1[i].name != arguments2[i].name)
			return false;
		if (arguments1[i].returns.size() == 0 || referenceListIncludes(arguments1[i].returns,arguments2[i].returns))
			return false;
		if (arguments1[i].inherits.size() == 0 || referenceListIncludes(arguments1[i].inherits,arguments2[i].inherits))
			return false;
	};
	return true;
};
std::set<size_t> getByIdentifier(const size_t id,const Identifier& identifier) {
	std::map<size_t,Identifier> attrs1 = getAttributes(id);
	std::map<size_t,Identifier> attrs2;
	std::set<size_t> ids;
	for (const auto& [ key , value ] : attrs1)
		if (std::includes(value.names.begin(),value.names.end(),identifier.names.begin(),identifier.names.end()))
			attrs2[key] = value;
	if (!identifier.hasArguments) {
		if (attrs2.size() == 1)
			for (const auto& [ key , value ] : attrs2)
				return key;
		for (const auto& [ key , value ] : attrs2)
			ids.insert(key);
		return ids;
	};
	attrs1.clear();
	for (const auto& [ key , value ] : attrs2)
		if (value.hasArguments && argumentsMatch(identifier.arguments,value.arguments))
			attrs1[key] = value;
	for (const auto& [ key , value ] : attrs1)
		ids.insert(key);
	return ids;
};
std::set<size_t> getByReference(const size_t id,const Reference& reference) {
	std::set<size_t> newids = getByIdentifier(id,reference[0]);
	if (newids.size() == 0)
		return getByReference(0,reference);
	if (reference.size() > 1) {
		std::set<size_t> ids;
		for (const size_t newid : newids)
			for (const size_t i : getByReference(newid,Reference(reference.begin(),reference.end())))
				ids.insert(i);
		if (ids.size() == 0)
			return getByReference(0,reference);
		return ids;
	};
	return newids;
};
*/
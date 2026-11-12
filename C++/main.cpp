#include <string>
#include <vector>
#include <sstream>
#include <iostream>
#include <regex>

#include "AST.h"

int main();
AST parse(const AST& ast);
AST parseGroupers(const AST& tokens);
AST tokenize(const AST& ast);
AST combine(const AST& ast);
AST parseBinary(const AST& ast,const size_t index);
bool isName(const std::string value);
bool containsName(const AST& ast);
//------------------------------------------------------------------------------
std::vector<std::string> BINOPS = {
	",",
	"=",
	":",
	"<",
	"&",
	"|",
	"-",
	"*",
	"."
};
std::regex OPERATOR_PATTERN("[,=:<&|\\-*.(){}]|**");
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
			case '<':
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
	//a = parseBinary(a,0);
	return a;
};
bool isName(const AST& value) {
	std::regex pattern1("[a-zA-Z_][a-zA-Z0-9_]*");
	std::regex pattern2("[a-zA-Z]");
	std::string str = value.to_string();
	std::smatch match;
	return std::regex_match(str,match,pattern1) && std::regex_search(str,match,pattern2);
};
bool containsName(const AST& ast) {
	for (const AST& a : ast) if (isName(a)) return true;
	return false;
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
				arguments2.begin(),
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
			std::cout << ">>" << AST(arguments).repr() << std::endl;
		};
	};
	return AST(arguments);
};
AST parseBinary(const AST& ast,const size_t index) {
	std::cout << ast.to_string() << std::endl;
	if (index >= BINOPS.size()) {
		return ast;
	};
	for (size_t idx = index; idx < BINOPS.size(); ++idx) {
		for (size_t i = 0; i < ast.size(); ++i) {
			//std::cout << (ast[i].to_string() == BINOPS[index]) << (i > 0) << (i < ast.size() - 1) << containsName(AST(ast.begin(),ast.begin() + i)) << containsName(AST(ast.begin() + i + 1,ast.end())) << std::endl;
			//std::cout << ast[i].to_string() << " == " << BINOPS[index] << std::endl;
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
				std::cout << ast.to_string() << " -> " << ast[i].to_string() << std::endl;
				return AST(
					BINARY,
					args,
					{ast[i].to_string()}
				);
			};
		};
	};
	return ast;
};

int main() {
	std::cout << parse(AST("a (b) = c : d")).repr() << std::endl;
};

/*

AST(
	NONE,[
		AST(NONE,[],["this"]),
		AST(NONE,[],["is"]),
		AST(NONE,[],["a"]),
		AST(
			GROUPER,[
				AST(
					BINARY,
					[
						AST(NONE,[],["test"])
					],[""]
				)
			],["(",")"])],[""])

*/
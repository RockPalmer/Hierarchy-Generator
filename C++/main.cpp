#include <string>
#include <vector>
#include <sstream>
#include <iostream>

#include "AST.h"

int main();
AST splitWhitespace(const AST& str);
AST parse(const AST& ast);
AST parseGroupers(const AST& tokens);
AST tokenize(const AST& ast);

//------------------------------------------------------------------------------

AST splitWhitespace(const AST& str) {
	std::vector<AST> result;
	std::istringstream iss(str.to_string());
	std::string word;

	while (iss >> word) result.emplace_back(word);

	return AST(result);
};
AST tokenize(const AST& ast) {
	std::string str = ast.to_string();
	AST a;
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
	return a;
};
AST parse(const AST& ast) {
	return parseGroupers(tokenize(ast));
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
			arguments = arguments2;
			arguments2.clear();
		};
	};
	return AST(arguments);
};

int main() {
	AST ast = parse(AST("this is a (test)"));
	std::cout << "THERE" << std::endl;
	std::cout << ast.repr() << std::endl;
};

/*

AST(
	NONE,[
		AST(NONE,[],["this"]),
		AST(NONE,[],["is"]),
		AST(NONE,[],["a"]),
		AST(
			GROUPER,[
				AST(NONE,[],[""])
			],["(",")"])],[""])

*/
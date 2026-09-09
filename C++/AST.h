#ifndef _AST_H_
#define _AST_H_

#include <string>
#include <vector>
#include <ostream>

struct AST {
	std::string op;
	std::vector<AST> args;

	AST(const std::string op,const std::vector<AST>& args);
	AST(const char op,const std::vector<AST>& args);
};

std::string to_string(const AST& value);
std::ostream& operator<<(std::ostream& v1,const AST v2);

#endif
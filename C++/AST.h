#ifndef _AST_H_
#define _AST_H_

#include <string>
#include <vector>

#include "ASTType.h"

struct AST {
	ASTType type;
	std::vector<AST> arguments;
	std::vector<std::string> op;

	AST();
	AST(const char op);
	AST(const std::string op);
	AST(const ASTType type,const std::vector<AST>& arguments,const std::vector<std::string>& op);
	AST(const std::vector<AST>& arguments);
	AST(const std::vector<AST>::iterator start,const std::vector<AST>::iterator end);

	size_t size() const;

	AST& operator[](size_t index);
	const AST& operator[](size_t index) const;

	std::vector<AST>::iterator begin();
	std::vector<AST>::iterator end();

	std::vector<AST>::const_iterator begin() const;
	std::vector<AST>::const_iterator end() const;

	std::string to_string() const;
	std::string repr() const;

	void insert(const std::vector<AST>::iterator i1,const std::vector<AST>::iterator i2,const std::vector<AST>::iterator i3);
	void push_back(const AST& ast);
	void clear();
};

#endif
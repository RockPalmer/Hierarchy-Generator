#include "AST.h"

AST::AST():
	AST("") {};
AST::AST(const char op):
	AST(std::string(1,op)) {};
AST::AST(const std::string op):
	AST(NONE,{},{op}) {};
AST::AST(const ASTType type,const std::vector<AST>& arguments,const std::vector<std::string>& op):
	type(type),
	arguments(arguments),
	op(op) {};
AST::AST(const std::vector<AST>& arguments):
	AST(BINARY,arguments,{""}) {};
AST::AST(const std::vector<AST>::iterator start,const std::vector<AST>::iterator end):
	AST(std::vector<AST>(start,end)) {};
AST::AST(const std::vector<AST>::const_iterator start,const std::vector<AST>::const_iterator end):
	AST(std::vector<AST>(start,end)) {};

size_t AST::size() const {
	return arguments.size();
};

AST& AST::operator[](size_t index) {
	return arguments[index];
};
const AST& AST::operator[](size_t index) const {
	return arguments[index];
};

std::vector<AST>::iterator AST::begin() {
	return arguments.begin();
};
std::vector<AST>::iterator AST::end() {
	return arguments.end();
};

std::vector<AST>::const_iterator AST::begin() const {
	return arguments.begin();
};
std::vector<AST>::const_iterator AST::end() const {
	return arguments.end();
};

std::string AST::to_string() const {
	std::string r;
	switch (type) {
		case NONE: return op[0];
		case GROUPER: return op[0] + arguments[0].to_string() + op[1];
		case UNARY: return op[0] + arguments[0].to_string();
		case BINARY:
			r = arguments[0].to_string();
			for (size_t i = 1; i < arguments.size(); ++i) {
				r += op[0] + arguments[i].to_string();
			};
			return r;
	};
	return r;
};
std::string AST::repr() const {
	std::string r = "AST(";
	switch (type) {
		case NONE: return "NONE(\"" + op[0] + "\")";
		case GROUPER: return "GROUPER" + op[0] + arguments[0].repr() + op[1];
		case UNARY: return "UNARY(\"" + op[0] + "\")[" + arguments[0].repr() + "]";
		case BINARY:
			r = "BINARY(\"" + op[0] + "\")[";
			if (arguments.size() > 0) {
				r += arguments[0].repr();
			};
			for (size_t i = 1; i < arguments.size(); ++i) {
				r += "," + arguments[i].repr();
			};
			r += "]";
			break;
	};
	return r;
};

void AST::insert(const std::vector<AST>::iterator i1,const std::vector<AST>::iterator i2,const std::vector<AST>::iterator i3) {
	arguments.insert(i1,i2,i3);
};
void AST::push_back(const AST& ast) {
	arguments.push_back(ast);
};
void AST::clear() {
	arguments.clear();
};
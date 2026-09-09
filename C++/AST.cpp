#include "AST.h"

AST::AST(const std::string op,const std::vector<AST>& args):
	op(op),
	args(args) {};
AST::AST(const char op,const std::vector<AST>& args):
	op("" + op),
	args(args) {};

std::string to_string(const AST& value) {
	if (value.args.size() == 0) return value.op;
	if (value.op.length() == 2) return value.op[0] + to_string(value.args[0]) + value.op[1];
	return to_string(value.args[0]) + value.op + to_string(value.args[1]);
};
std::ostream& operator<<(std::ostream& v1,const AST v2) {
	return v1 << to_string(v2);
};
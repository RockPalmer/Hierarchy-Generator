#include "AST.h"

AST::AST(const std::string op,const std::vector<AST>& args):
	op(op),
	args(args) {};
AST::AST(const char op,const std::vector<AST>& args):
	op("" + op),
	args(args) {};

std::string to_string(const AST& value) {
	/*std::string result = "('" + value.op + "',[";
	if (value.args.size() > 0)
		result += to_string(value.args[0]);
	for (size_t i = 1;i < value.args.size();++i)
		result += "," + to_string(value.args[i]);
	return result + "])";*/
	switch (value.args.size()) {
		case 0: return value.op;
		case 1:
			if (value.op == "{}" || value.op == "()") return value.op[0] + to_string(value.args[0]) + value.op[1];
			return value.op + to_string(value.args[0]);
		default: return to_string(value.args[0]) + value.op + to_string(value.args[1]);
	};
};
std::ostream& operator<<(std::ostream& v1,const AST v2) {
	return v1 << to_string(v2);
};
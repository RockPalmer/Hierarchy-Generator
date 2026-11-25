#include "characters.h"

namespace Characters {
	const std::string PARENT_REFERENCE = "^";
	const std::string TOP_REFERENCE = "~";
	const std::string POSITIONAL_DELIMITER = "/";
	const std::string KEYWORD_DELIMITER = "*";
	const std::string REFERENCE_DELIMITER = ".";
	const std::string ARGUMENT_REFERENCE_DELIMITER = "!";
	const std::string INTERSECTION_OPERATOR = "&";
	const std::string UNION_OPERATOR = "!";
	const std::string BEQUEATH_OPERATOR = ">";
	const std::string INHERIT_OPERATOR = "<";
	const std::string INSTANCE_OPERATOR = ":";
	const std::string DIFFERENCE_OPERATOR = "-";
	const std::string LEFT_JOIN_OPERATOR = ">-";
	const std::string RIGHT_JOIN_OPERATOR = "-<";
	const std::string OUTER_JOIN_OPERATOR = "><";
	const std::string INNER_JOIN_OPERATOR = "--";
	const std::string PRODUCT_OPERATOR = "*";
	const std::string EQUALITY_OPERATOR = "=";
	const std::string ARGUMENT_OPERATOR = "";
	const std::string GENERAL_DELIMITER = ",";
	const std::string ARGUMENT_LIST_OPEN = "(";
	const std::string ARGUMENT_LIST_CLOSE = ")";
	const std::string ATTRIBUTE_LIST_OPEN = "{";
	const std::string ATTRIBUTE_LIST_CLOSE = "}";
	const std::string LIST_ARGUMENT_OPERATOR = "*";
	const std::string DICT_ARGUMENT_OPERATOR = "**";
	const std::vector<std::string> BINOPS = {
		GENERAL_DELIMITER,
		BEQUEATH_OPERATOR,
		INHERIT_OPERATOR,
		EQUALITY_OPERATOR,
		INSTANCE_OPERATOR,
		INTERSECTION_OPERATOR,
		UNION_OPERATOR,
		DIFFERENCE_OPERATOR,
		LEFT_JOIN_OPERATOR,
		RIGHT_JOIN_OPERATOR,
		OUTER_JOIN_OPERATOR,
		INNER_JOIN_OPERATOR,
		PRODUCT_OPERATOR,
		ARGUMENT_REFERENCE_DELIMITER,
		REFERENCE_DELIMITER
	};
	const std::vector<std::string> UNOPS = {
		LIST_ARGUMENT_OPERATOR,
		DICT_ARGUMENT_OPERATOR
	};
	const std::vector<std::tuple<std::string,std::string>> GROUPING_SYMBOLS = {
		{ARGUMENT_LIST_OPEN,ARGUMENT_LIST_CLOSE},
		{ATTRIBUTE_LIST_OPEN,ATTRIBUTE_LIST_CLOSE},
		{GENERAL_OPEN,GENERAL_CLOSE},
	};
	const std::vector<std::string> SPECIAL_TOKENS = {
		PARENT_REFERENCE,
		TOP_REFERENCE,
		POSITIONAL_DELIMITER,
		KEYWORD_DELIMITER
	};
	const std::regex NAME_PATTERN1("[a-zA-Z_][a-zA-Z0-9_]*");
	const std::regex NAME_PATTERN2("[a-zA-Z]");
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
	bool isOpenGrouper(const std::string op) {
		for (const auto [ open , close ] : GROUPING_SYMBOLS)
			if (op == open) return true;
		return false;
	};
	bool isCloseGrouper(const std::string op) {
		for (const auto [ open , close ] : GROUPING_SYMBOLS)
			if (op == close) return true;
		return false;
	};
	bool isUnaryOperator(const std::string op) {
		for (const std::string value : UNOPS)
			if (op == value) return true;
		return false;
	};
	bool canBeName(const std::string value) {
		std::smatch match;
		return (
			std::regex_match(value,match,NAME_PATTERN1) &&
			std::regex_search(value,match,NAME_PATTERN2)
		);
	};
};
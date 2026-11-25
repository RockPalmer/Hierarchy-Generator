#pragma once

#include <string>
#include <vector>
#include <tuple>
#include <regex>

namespace Characters {
	extern const std::string PARENT_REFERENCE;
	extern const std::string TOP_REFERENCE;
	extern const std::string POSITIONAL_DELIMITER;
	extern const std::string KEYWORD_DELIMITER;
	extern const std::string REFERENCE_DELIMITER;
	extern const std::string ARGUMENT_REFERENCE_DELIMITER;
	extern const std::string INTERSECTION_OPERATOR;
	extern const std::string UNION_OPERATOR;
	extern const std::string BEQUEATH_OPERATOR;
	extern const std::string INHERIT_OPERATOR;
	extern const std::string INSTANCE_OPERATOR;
	extern const std::string DIFFERENCE_OPERATOR;
	extern const std::string LEFT_JOIN_OPERATOR;
	extern const std::string RIGHT_JOIN_OPERATOR;
	extern const std::string OUTER_JOIN_OPERATOR;
	extern const std::string INNER_JOIN_OPERATOR;
	extern const std::string PRODUCT_OPERATOR;
	extern const std::string EQUALITY_OPERATOR;
	extern const std::string ARGUMENT_OPERATOR;
	extern const std::string GENERAL_DELIMITER;
	extern const std::string GENERAL_OPEN;
	extern const std::string GENERAL_CLOSE;
	extern const std::string ARGUMENT_LIST_OPEN;
	extern const std::string ARGUMENT_LIST_CLOSE;
	extern const std::string ATTRIBUTE_LIST_OPEN;
	extern const std::string ATTRIBUTE_LIST_CLOSE;
	extern const std::string LIST_ARGUMENT_OPERATOR;
	extern const std::string DICT_ARGUMENT_OPERATOR;
	extern const std::vector<std::string> BINOPS;
	extern const std::vector<std::string> UNOPS;
	extern const std::vector<std::tuple<std::string,std::string>> GROUPING_SYMBOLS;
	extern const std::vector<std::string> SPECIAL_TOKENS;
	extern const std::regex NAME_PATTERN1;
	extern const std::regex NAME_PATTERN2;
	size_t tokenMaxLength();
	std::vector<std::string> tokensOfLength(const size_t length);
	bool isOpenGrouper(const std::string op);
	bool isCloseGrouper(const std::string op);
	bool isUnaryOperator(const std::string op);
	bool canBeName(const std::string value);
};
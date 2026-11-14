#include "global.h"

std::string join_with(const std::string delimiter,const std::vector<std::string>& values) {
	if (values.size() == 0) return "";
	std::string result = values[0];
	for (size_t i = 1; i < values.size(); ++i) {
		result += delimiter + values[i];
	};
	return result;
};
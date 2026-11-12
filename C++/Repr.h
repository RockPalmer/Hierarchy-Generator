#ifndef _REPR_H_
#define _REPR_H_

#include <string>
#include <vector>

std::string repr(const std::string& value) {
	return value;
};
std::string repr(const int value) {
	return std::to_string(value);
};
std::string repr(const bool value) {
	return value ? "true" : "false";
};
std::string repr(const float value) {
	return std::to_string(value);
};
std::string repr(const std::vector<std::string>& value) {
	std::string result = "[";
	
};

#endif
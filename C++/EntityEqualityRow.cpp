#include <vector>
#include <string>

#include "EntityEqualityRow.h"

EntityEqualityRow::EntityEqualityRow(const std::set<EntityRow*>& values):
	values(values) {};

bool operator<(const EntityEqualityRow& v1,const EntityEqualityRow& v2) {
	std::vector<EntityRow*> vals1(v1.values.begin(),v1.values.end());
	std::vector<EntityRow*> vals2(v2.values.begin(),v2.values.end());
	size_t
		s1 = v1.values.size(),
		s2 = v2.values.size();
	size_t s3 = s1 < s2 ? s1 : s2;
	for (size_t i = 0;i < s3;i++) {
		if (vals1[i] < vals2[i]) return true;
		if (vals1[i] > vals2[i]) return false;
	};
	return s1 < s2;
};
bool operator>(const EntityEqualityRow& v1,const EntityEqualityRow& v2) {
	std::vector<EntityRow*> vals1(v1.values.begin(),v1.values.end());
	std::vector<EntityRow*> vals2(v2.values.begin(),v2.values.end());
	size_t
		s1 = v1.values.size(),
		s2 = v2.values.size();
	size_t s3 = s1 < s2 ? s1 : s2;
	for (size_t i = 0;i < s3;i++) {
		if (vals1[i] > vals2[i]) return true;
		if (vals1[i] < vals2[i]) return false;
	};
	return s1 > s2;
};
bool operator<=(const EntityEqualityRow& v1,const EntityEqualityRow& v2) {
	std::vector<EntityRow*> vals1(v1.values.begin(),v1.values.end());
	std::vector<EntityRow*> vals2(v2.values.begin(),v2.values.end());
	size_t
		s1 = v1.values.size(),
		s2 = v2.values.size();
	size_t s3 = s1 < s2 ? s1 : s2;
	for (size_t i = 0;i < s3;i++) {
		if (vals1[i] < vals2[i]) return true;
		if (vals1[i] > vals2[i]) return false;
	};
	return s1 <= s2;
};
bool operator>=(const EntityEqualityRow& v1,const EntityEqualityRow& v2) {
	std::vector<EntityRow*> vals1(v1.values.begin(),v1.values.end());
	std::vector<EntityRow*> vals2(v2.values.begin(),v2.values.end());
	size_t
		s1 = v1.values.size(),
		s2 = v2.values.size();
	size_t s3 = s1 < s2 ? s1 : s2;
	for (size_t i = 0;i < s3;i++) {
		if (vals1[i] > vals2[i]) return true;
		if (vals1[i] < vals2[i]) return false;
	};
	return s1 >= s2;
};
bool operator==(const EntityEqualityRow& v1,const EntityEqualityRow& v2) {
	std::vector<EntityRow*> vals1(v1.values.begin(),v1.values.end());
	std::vector<EntityRow*> vals2(v2.values.begin(),v2.values.end());
	if (vals1.size() != vals2.size()) return false;
	for (size_t i = 0;i < v1.values.size();i++) if (vals1[i] != vals2[i]) return false;
	return true;
};
bool operator!=(const EntityEqualityRow& v1,const EntityEqualityRow& v2) {
	return !(v1 == v2);
};
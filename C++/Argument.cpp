#include "Argument.h"

Argument::Argument(const Entity* parent,const Entity* child,const size_t index):
	parent(parent),
	child(child),
	index(index) {};
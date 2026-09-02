#ifndef _INHERITANCE_H_
#define _INHERITANCE_H_

struct Inheritance {
	Entity* parent;
	Entity* child;

	Inheritance(const Entity* parent,const Entity* child);
};

#endif
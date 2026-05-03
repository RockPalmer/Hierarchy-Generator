from __future__ import annotations
from typing import (
	Iterable,
	Any,
	KeysView,
	ValuesView,
	ItemsView
)
from collections.abc import (
	Mapping,
	Iterable
)

CONDITIONS_ORDER = [
	':',
	'<',
	'>',
	'='
]

def get_at(index : Any,values : Mapping) -> Any:
	match_values = [get_match_value(index,v) for v in values]
	max_match = max(match_values)
	if max_match == 0:
		raise KeyError
	vals = [m for m,v in zip(match_values,values) if m == max_match]
	if len(vals) == 1:
		return vals[0]
	return set(vals)
def set_at(index : Any,other : Any,values : Mapping) -> None:
	match_values = [get_match_value(index,v) for v in values]
	max_match = max(match_values)
	if max_match == 0:
		raise KeyError
	indices = [i for i,m in enumerate(match_values) if m == max_match]
	first_index = min(indices)
	indices.remove(first_index)
	for i in reversed(sorted(indices)):
		del values[i]
	values[first_index] = other
def insert_at(index : Any,other : Any,values : Mapping) -> None:
	match_values = [get_match_value(index,v) for v in values]
	max_match = max(match_values)
	if max_match == 0:
		raise KeyError
	indices = [i for i,m in enumerate(match_values) if m == max_match]
	first_index = 
	values.insert(min(indices),other)
def del_at(index : Any,values : Mapping) -> None:
	match_values = [get_match_value(index,v) for v in values]
	max_match = max(match_values)
	if max_match == 0:
		raise KeyError
	indices = [i for i,m in enumerate(match_values) if m == max_match]
	if len(indices) != 1:
		raise KeyError(type(values).__name__ + '[' + type(index).__name__ + ']')
	for i in reversed(sorted(indices)):
		del values[i]
def contains_close(values : Iterable,other : Any) -> bool:
	match_values = [get_match_value(index,v) for v in values]
	return max(match_values) > 0
def contains_exact(values : Iterable,other : Any) -> bool:
	match_values = [get_match_value(index,v) for v in values]
	max_match = max(match_values)
	if max_match == 0:
		return False
	vals = [m for m,v in zip(match_values,values) if m == max_match]
	return len(vals) == 1
def set_parent(value,parent) -> None:
	if hasattr(value,'parent'):
		value.parent = parent

class All:
	def __repr__(self) -> str:
		return str(self)
	def __hash__(self) -> int:
		return hash(str(self))
class ParentRef(All):
	def __init__(self):
		pass
	def __str__(self) -> str:
		return '<-'
class Reference(All):
	def __init__(self,*values : tuple[Any...]) -> None:
		self.values = tuple([value for value in values])
	def __iter__(self) -> iter:
		return iter(self.values)
	def __len__(self) -> int:
		return len(self.values)
	def __getitem__(self,index : int | slice | Reference) -> Any:
		if isinstance(index,int):
			return self.values[index]
		if isinstance(index,slice):
			return Reference(*self.values[index])
		if isinstance(index,Reference):
			if len(index) == 0:
				return self
			return self[index[0]][index[1:]]
		raise KeyError('Reference[' + type(index).__name__ + ']')
	def __setitem__(self,index : int | Reference,other : Any) -> None:
		if isinstance(index,int):
			self[index] = other
		elif isinstance(index,Reference):
			if len(index) == 1:
				self.values[index[0]] = other
			else:
				self[index[0]][index[1:]] = other
		else:
			raise KeyError('Reference[' + type(index).__name__ + ']')
	def __delitem__(self,index : int | Reference) -> None:
		if isinstance(index,int):
			del self[index]
		elif isinstance(index,Reference):
			if len(index) == 1:
				del self.values[index[0]]
			else:
				del self[index[0]][index[1:]]
		else:
			raise KeyError('Reference[' + type(index).__name__ + ']')
	def __contains__(self,other : Any) -> bool:
		return other in self.values
	def __add__(self,other : Any) -> Reference:
		if isinstance(other,Reference):
			return Reference(*(self.values + other.values))
		return Reference(*(self.values + (other,)))
	def __radd__(self,other : Any) -> Reference:
		if isinstance(other,Reference):
			return NotImplemented
		return Reference(*((other,) + self.values))
	def __str__(self) -> str:
		return ''.join(str(v for v in self))
	def append(self,other : Any) -> None:
		self.values.append(other)
class Clause(All):
	def top(self):
		x = self
		while not isinstance(x,Hierarchy):
			x = self.parent
		return x
	def reference(self) -> Reference:
		if isinstance(self,Hierarchy):
			return Reference()
		return self.parent.reference() + self.header()

class ContainerClause(Clause):
	def __len__(self) -> int:
		return len(self.elements)
	def __setitem__(self,index : int,other : Any) -> None:
		self.elements[index] = other
	def __delitem__(self,index : int) -> None:
		del self.elements[index]
	def __contains__(self,other : Any) -> bool:
		return other in self.elements
	def __iter__(self) -> iter:
		return iter(self.elements)
	def __reversed__(self) -> iter:
		return reversed(self.elements)
	def clear(self) -> None:
		self.elements.clear()
	def copy(self) -> ContainerClause:
		return self.__class__(self.elements.copy())
class CollectionClause(ContainerClause):
	def __init__(self,iterable = (),/) -> None:
		self.elements = [value for value in iterable]
		for value in self.elements:
			set_parent(value,self)
	def __getitem__(self,index : int | slice) -> Any:
		if isinstance(index,int):
			return self.elements[index]
		return self.__class__(self.elements[index])
	def __str__(self) -> str:
		return self.delimiter.join(str(value) for value in self)
	def __eq__(self,other : Any) -> bool:
		return (
			len(self) == len(other) and all(
				value in other for value in self
			) and all(
				value in self for value in other
			)
		)
	def __ne__(self,other : Any) -> bool:
		return not (self == other)
	def __le__(self,other : Any) -> bool:
		return self.issubset(other)
	def __lt__(self,other : Any) -> bool:
		return self <= other and self != other
	def __ge__(self,other : Any) -> bool:
		return self.issuperset(other)
	def __gt__(self,other : Any) -> bool:
		return self >= other and self != other
	def __or__(self,other : Any) -> Any:
		return self.union(other)
	def __ior__(self,other : Any) -> Any:
		self.elements = (self | other).values
	def __ror__(self,other : Any) -> Any:
		if isinstance(other,CollectionClause):
			return NotImplemented
		return self | other
	def __and__(self,other : Any) -> Any:
		return self.intersection(other)
	def __iand__(self,other : Any) -> Any:
		self.elements = (self & other).values
	def __rand__(self,other : Any) -> Any:
		if isinstance(other,CollectionClause):
			return NotImplemented
		return self & other
	def __sub__(self,other : Any) -> Any:
		return self.difference(other)
	def __isub__(self,other : Any) -> Any:
		self.elements = (self - other).values
	def __rsub__(self,other : Any) -> Any:
		if isinstance(other,CollectionClause):
			return NotImplemented
		return self.__class__([
			value for value in other if value not in self
		])
	def __xor__(self,other : Any) -> Any:
		return self.symmetric_difference(other)
	def __ixor__(self,other : Any) -> Any:
		self.elements = (self ^ other).values
	def __rxor__(self,other : Any) -> Any:
		if isinstance(other,CollectionClause):
			return NotImplemented
		return self ^ other
	def __add__(self,value : Any) -> CollectionClause:
		return self.__class__(list(self) + list(value))
	def __radd__(self,value : Any) -> CollectionClause:
		if isinstance(value,CollectionClause):
			return NotImplemented
		return self.__class__(list(value) + list(self))
	def __mul__(self,value : int) -> CollectionClause:
		return self.__class__(list(self) * value)
	def __rmul__(self,value : int) -> CollectionClause:
		return self * value
	def __squash__(self) -> tuple:
		return (type(self).__name__,squash(self.elements))
	def add(self,elem : Any,/) -> None:
		if elem not in self:
			self.elements.append(elem)
	def append(self,value : Any,/) -> None:
		self.elements.append(value)
	def count(self,value : Any,/) -> int:
		return self.elements.count(value)
	def difference(self,*others : tuple[Any...]) -> Any:
		if len(others) == 1 and isinstance(others[0],Iterable):
			others = others[0]
		return self.__class__([
			value for value in self.elements if all(
				value not in other for other in others
			)
		])
	def discard(self,elem : Any,/) -> None:
		if elem in self:
			self.remove(elem)
	def extend(self,iterable : Iterable,/) -> None:
		self.elements.extend(iterable)
	def intersection(self,*others : tuple[Any...]) -> Any:
		if len(others) == 1 and isinstance(others[0],Iterable):
			others = others[0]
		return self.__class__([
			value for value in self.elements if all(
				value in other for other in others
			)
		])
	def isdisjoint(self,other : Any,/) -> bool:
		return all(
			value not in other for value in self
		) and all(
			value not in self for value in other
		)
	def issubset(self,other : Any,/) -> bool:
		return all(
			value in other for value in self
		)
	def issuperset(self,other : Any,/) -> bool:
		return all(
			value in self for value in other
		)
	def pop(self,index : int = -1,/) -> Any:
		return self.pop(index)
	def remove(self,value : Any,/) -> None:
		self.elements.remove(value)
	def reverse(self) -> None:
		self.elements.reverse()
	def sort(self,*,key = None,reverse = False) -> None:
		self.elements.sort(key = key,reverse = reverse)
	def symmetric_difference(self,*others : tuple[Any...]) -> Any:
		if len(others) == 1 and isinstance(others[0],Iterable):
			others = others[0]
		arr = [self.elements] + list(others)
		values = []
		for i in range(len(arr)):
			values += [
				value for value in arr[i] if all(
					value not in a for a in arr[:i] + arr[i + 1:]
				)
			]
		return self.__class__(values)
	def union(self,*others : tuple[Any...]) -> Any:
		if len(others) == 1 and isinstance(others[0],Iterable):
			others = others[0]
		values = [value for value in self.elements]
		for other in others:
			for value in other:
				if value not in values:
					values.append(value)
		return self.__class__(values)
class SequenceClause(ContainerClause):
	def __init__(self,iterable = (),/) -> None:
		self.elements = [value for value in iterable]
		for value in self.elements:
			set_parent(value,self)
	def __getitem__(self,index : int | slice) -> Any:
		if isinstance(index,int):
			return self.elements[index]
		return self.__class__(self.elements[index])
	def __str__(self) -> str:
		return self.delimiter.join(str(value) for value in self)
	def __eq__(self,other : Any) -> bool:
		return (
			len(self) == len(other) and all(
				value in other for value in self
			) and all(
				value in self for value in other
			)
		)
	def __ne__(self,other : Any) -> bool:
		return not (self == other)
	def __add__(self,value : Any) -> CollectionClause:
		return self.__class__(list(self) + list(value))
	def __radd__(self,value : Any) -> CollectionClause:
		if isinstance(value,CollectionClause):
			return NotImplemented
		return self.__class__(list(value) + list(self))
	def __mul__(self,value : int) -> CollectionClause:
		return self.__class__(list(self) * value)
	def __rmul__(self,value : int) -> CollectionClause:
		return self * value
	def __squash__(self) -> tuple:
		return (type(self).__name__,squash(self.elements))
	def add(self,elem : Any,/) -> None:
		if elem not in self:
			self.elements.append(elem)
	def append(self,value : Any,/) -> None:
		self.elements.append(value)
	def count(self,value : Any,/) -> int:
		return self.elements.count(value)
	def discard(self,elem : Any,/) -> None:
		if elem in self:
			self.remove(elem)
	def extend(self,iterable : Iterable,/) -> None:
		self.elements.extend(iterable)
	def pop(self,index : int = -1,/) -> Any:
		return self.pop(index)
	def remove(self,value : Any,/) -> None:
		self.elements.remove(value)
	def reverse(self) -> None:
		self.elements.reverse()
	def sort(self,*,key = None,reverse = False) -> None:
		self.elements.sort(key = key,reverse = reverse)
class MappingClause(ContainerClause):
	def __init__(self,*args,**kwargs) -> None:
		self.elements = dict(*args,**kwargs)
	def __getitem__(self,index : Any) -> Any:
		return self.elements[index]
	def __or__(self,other : Any) -> MappingClause:
		return MappingClause(self.elements | dict(other))
	def __ror__(self,other : Any) -> MappingClause:
		if isinstance(other,MappingClause):
			return NotImplemented
		return MappingClause(dict(other) | self.elements)
	def __ior__(self,other : Any) -> None:
		self.elements |= dict(other)
	def get(self,key : Any,default : Any = None,/) -> Any:
		self.elements.get(key,default)
	def items(self) -> ItemsView:
		return self.elements.items()
	def keys(self) -> KeysView:
		return self.elements.keys()
	def pop(self,*args,/) -> Any:
		if len(args) not in {1,2}:
			raise KeyError
		return self.elements.pop(*args)
	def popitem(self) -> tuple[Any,Any]:
		return self.elements.popitem()
	def setdefault(self,key : Any,default : Any = None,/) -> None:
		self.elements.setdefault(key,default)
	def values(self) -> ValuesView:
		return self.elements.values()
class CommaSeparatedClause(SequenceClause):
	def __init__(self,iterable = (),/) -> None:
		super().__init__(values)
		self.delimiter = ','
class GroupedClause(Clause):
	def __str__(self) -> str:
		return self.left + super().__str__() + self.right

class Hierarchy(CommaSeparatedClause):
	def __init__(self,*args,**kwargs) -> None:
		super().__init__(*args,**kwargs)
class NameList(CommaSeparatedClause):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
class Entity(Clause):
	def __init__(
		self,
		*,
		name = None,
		names = [],
		arguments = None,
		order = None,
		conditions = {}
	) -> None:
		if name is not None:
			self.names = NameList(name)
		else:
			self.names = NameList(names)
		if arguments is not None:
			self.arguments = ArgumentList(arguments)
		else:
			self.arguments = None
		if order is not None:
			self.order = Ordering(order)
		else:
			self.order = None
		self.conditions = ConditionSet(conditions)
		set_parent(self.names,self)
		set_parent(self.arguments,self)
		set_parent(self.order,self)
		set_parent(self.conditions,self)
	def __str__(self) -> str:
		result = str(self.names)
		if self.arguments is not None:
			result += str(self.arguments)
		if self.order is not None:
			result += '/' + str(self.order)
		if self.conditions is not None:
			for k,v in self.conditions.items():
				result += ' ' + k + ' ' + str(v)
		return result
class ConditionSet(Clause):
	def __init__(self,*args,**kwargs) -> None:
		super().__init__(*args,**kwargs)
	def __str__(self) -> str:
		global CONDITIONS_ORDER

		vals = []
		for k in CONDITIONS_ORDER:
			if k not in self:
				continue
			vals.append(k + ' ' + str(self[k]))
		return ' '.join(vals)
class ArgumentList(GroupedClause):
	def __init__(self,*args,**kwargs) -> None:
		super().__init__(*args,**kwargs)
		(self.left,self.right) = ('(',')')
class AttributeList(GroupedClause):
	def __init__(self,*args,**kwargs) -> None:
		super().__init__(*args,**kwargs)
		(self.left,self.right) = ('{','}')
class Argument(Clause):
	pass
class PositionalDelimiter(Argument):
	def __init__(self) -> None:
		pass
	def __str__(self) -> str:
		return '<-'
	def __squash__(self) -> tuple[str]:
		return ('PositionalDelimiter',)
class RealArgument(Argument):
	def __init__(name,conditions = {}) -> None:
		self.name = name
		self.conditions = ConditionSet(conditions)
	def __str__(self) -> str:
		result = self.prefix + str(self.name)
		if len(self.conditions) > 0:
			result += ' ' + str(self.conditions)
		return result
	def __squash__(self):
		return (
			type(self).__name__,
			squash(self.name),
			squash(self.conditions)
		)
class BasicArgument(RealArgument):
	def __init__(name,conditions = {}) -> None:
		super().__init__(name,conditions)
		self.prefix = ''
class ComplexArgument(Argument):
	pass
class ListArgument(ComplexArgument):
	def __init__(name,conditions = {}) -> None:
		super().__init__(name,conditions)
		self.prefix = '*'
class DictArgument(ComplexArgument):
	def __init__(name,conditions = {}) -> None:
		super().__init__(name,conditions)
		self.prefix = '**'
class Union(CollectionClause):
	def __init__(self,*values) -> None:
		super().__init__(*values)
		self.delimiter = '|'
class Intersection(CollectionClause):
	def __init__(self,*values) -> None:
		super().__init__(*values)
		self.delimiter = '&'
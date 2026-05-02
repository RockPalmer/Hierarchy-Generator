from __future__ import annotations
from typing import (
	Iterable,
	Any,
	KeysView,
	ValuesView,
	ItemsView
)
from collections.abc import Mapping

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
class CollectionClause(Clause):
	def __init__(self,*values):
		if len(values) == 1:
			if type(values[0]) == type(self):
				self.values = [value for value in values[0].values]
			elif isinstance(values[0],set | frozenset | list | tuple):
				self.values = [value for value in values[0]]
			else:
				self.values = [values[0]]
		else:
			self.values = [value for value in values]
		for value in self.values:
			set_parent(value,self)
	def __iter__(self) -> iter:
		return iter(self.values)
	def __len__(self) -> int:
		return len(self.values)
	def __getitem__(self,index : int | slice) -> Any:
		if isinstance(index,int):
			return self.values[index]
		return self.__class__(*self.values[index])
	def __setitem__(self,index : int,other : Any) -> None:
		self.values[index] = other
	def __delitem__(self,index : int) -> None:
		del self.values[index]
	def __contains__(self,other : Any) -> bool:
		return other in self.values
	def __squash__(self) -> tuple:
		return (type(self).__name__,squash(self.values))
	def __str__(self) -> str:
		return self.delimiter.join(str(value) for value in self)
class ListClause(CollectionClause):
	def __init__(self,*values) -> None:
		super().__init__(*values)
		self.delimiter = ','
class GroupedClause(ListClause):
	def __str__(self) -> str:
		return self.left + super().__str__() + self.right

class Hierarchy(ListClause):
	def __init__(self,*values) -> None:
		super().__init__(*values)
class NameList(ListClause):
	def __init__(self,*values):
		super().__init__(*values)
class Entity(Clause):
	def __init__(self,**kargs : dict[str,Any]) -> None:
		self.names = NameList(
			kargs.get(
				'names',
				kargs.get(
					'name',
					[]
				)
			)
		)
		self.arguments = ArgumentList(
				kargs.get(
				'arguments',
				None
			)
		)
		self.order = Ordering(
			kargs.get(
				'order',
				None
			)
		)
		self.conditions = Conditions(
			kargs.get(
				'conditions',
				[]
			)
		)
		set_parent(self.names,self)
		set_parent(self.arguments,self)
		set_parent(self.order,self)
		set_parent(self.conditions,self)
	def __getitem__(self,index : str | Reference) -> Any:
		if isinstance(index,str):
			match index:
				case '.':
					return self.conditions['=']
				case '!':
					return self.arguments
				case _:
					return self.conditions[index]
		if isinstance(index,Reference):
			if len(index) == 0:
				return self
			return self[index[0]][index[1:]]
		raise KeyError('Entity[' + type(index).__name__ + ']')
	def __setitem__(self,index : str | Reference,other : Any) -> None:
		if isinstance(index,str):
			match index:
				case '.':
					self.conditions['='] = other
				case '!':
					self.arguments = other
				case _:
					self.conditions[index] = other
		elif isinstance(index,Reference) and len(index) > 1:
			self[index[0]][index[1:]] = other
		else:
			raise KeyError('Entity[' + type(index).__name__ + ']')
	def __delitem__(self,index : str | Reference) -> None:
		if isinstance(index,str):
			match index:
				case '.':
					del self.conditions['=']
				case '!':
					self.arguments = None
				case _:
					del self.conditions[index]
		elif isinstance(index,Reference) and len(index) > 1:
			del self[index[0]][index[1:]]
		else:
			raise KeyError('Entity[' + type(index).__name__ + ']')
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
class Conditions(Clause):
	def __init__(self,args : dict[str,Any] = {}) -> None:
		self.values = {k : v for k,v in args.items()}
		for v in self.conditions.values():
			set_parent(v,self)
	def __iter__(self) -> iter:
		return iter(self.values)
	def __len__(self) -> int:
		return len(self.values)
	def __getitem__(self,index : str | Reference) -> Any:
		if isinstance(index,str):
			return self.values[index]
		if isinstance(index,Reference):
			if len(index) == 0:
				return self
			return self[index[0]][index[1:]]
		raise KeyError('Conditions[' + type(index).__name__ + ']')
	def __setitem__(self,index : str | Reference,other : Any) -> None:
		if isinstance(index,str):
			self.values[index] = other
		elif isinstance(index,Reference):
			if len(index) == 1:
				self.values[index[0]] = other
			else:
				self[index[0]][index[1:]] = other
		else:
			raise KeyError('Conditions[' + type(index).__name__ + ']')
	def __delitem__(self,index : str | Reference) -> None:
		if isinstance(index,str):
			del self.values[index]
		elif isinstance(index,Reference):
			if len(index) == 1:
				del self.values[index[0]]
			else:
				del self[index[0]][index[1:]]
		else:
			raise KeyError('Conditions[' + type(index).__name__ + ']')
	def __contains__(self,other : Any) -> bool:
		return other in self.values
	def __str__(self) -> str:
		global CONDITIONS_ORDER

		vals = []
		for k in CONDITIONS_ORDER:
			if k not in self:
				continue
			vals.append(k + ' ' + str(self[k]))
		return ' '.join(vals)
	def keys(self) -> KeysView:
		return self.values.keys()
	def values(self) -> ValuesView:
		return self.values.values()
	def items(self) -> ItemsView:
		return self.values.items()
class ArgumentList(GroupedClause):
	def __init__(self,*values) -> None:
		super().__init__(*values)
		(self.left,self.right) = ('(',')')
class AttributeList(GroupedClause):
	def __init__(self,*values) -> None:
		super().__init__(*values)
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
		self.conditions = Conditions(conditions)
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
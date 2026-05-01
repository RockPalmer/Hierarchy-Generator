from __future__ import annotations
from typing import (
	Iterable,
	Any,
	KeysView,
	ValuesView,
	ItemsView
)
from collections.abc import Mapping

'''
define entity
define entity(arguments)
define entity = ?pattern?
define entity = attributes
define entity < reference
define any > reference
define reference : any
define (arguments)
define operator/(order)
'''

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
	if value is not None:
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

class Hierarchy(Clause):
	def __init__(self,*values : tuple[Any...]) -> None:
		self.values = {value for value in values}
		for value in self.values:
			set_parent(value,self)
	def __iter__(self) -> iter:
		return iter(self.values)
	def __len__(self) -> int:
		return len(self.values)
	def __getitem__(self,index : Any) -> Any:
		if isinstance(index,Reference):
			if len(index) == 0:
				return self
			return self[index[0]][index[1:]]
		return get_at(index,self)
	def __setitem__(self,index : Any,other : Any) -> None:
		if isinstance(index,Reference):
			if len(index) == 1:
				self.values[index[0]] = other
			else:
				self[index[0]][index[1:]] = other
		else:
			set_at(index,other,self)
	def __delitem__(self,index : Any) -> None:
		if isinstance(index,Reference):
			if len(index) == 1:
				self.values[index[0]] = other
			else:
				self[index[0]][index[1:]] = other
		else:
			del_at(index,other,self)
	def __str__(self) -> str:
		return ','.join(str(value) for value in self)
	def __squash__(self) -> tuple[str,Any]:
		return ('Hierarchy',squash(self.values))
	def add(self,other : Any) -> None:
		if not contains_close(self,other):
			self.values.append(other)
	def cd(self,index : Reference):
		match len(index):
			case 0:
				return self
			case 1:
				return self[index[0]]
			case _:
				return self[index[0]][index[1:]]
	def remove(self,other : Any) -> None:
		del self[other]
class NameList(Clause):
	def __init__(self,*names) -> None:
		match len(names):
			case 0:
				raise TypeError
			case 1:
				if isinstance(names[0],NameList):
					self.values = names[0].values
				else:
					self.values = {names[0]}
			case _:
				self.values = set(names)
	def __str__(self) -> str:
		return ','.join(sorted(list(str(value) for value in self.values)))
	def __iter__(self) -> iter:
		return iter(self.values)
	def __len__(self) -> int:
		return len(self.values)
	def __contains__(self,other : Any) -> bool:
		return other in self.values
	def __or__(self,other : NameList) -> NameList:
		return NameList(*(self.values | other.values))
	def __and__(self,other : NameList) -> NameList:
		return NameList(*(self.values & other.values))
	def __sub__(self,other : NameList) -> NameList:
		return NameList(*(self.values - other.values))
	def __xor__(self,other : NameList) -> NameList:
		return NameList(*(self.values ^ other.values))
	def add(self,other) -> None:
		self.values.add(other)
	def remove(self,other) -> None:
		self.values.remove(other)
class Entity(Clause):
	def __init__(self,**kargs : dict[str,Any]) -> None:
		self.names = NameList(
			kargs.get(
				'names',
				kargs.get(
					'name',
					None
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
				None
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
	def __init__(self,args : dict[str,Any]) -> None:
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
class ArgumentList(Clause):
	def __init__(self,*values) -> None:
		self.values = tuple([value for value in values])
	def __iter__(self) -> iter:
		return iter(self.values)
	def __len__(self,index : int) -> int:
		return len(self.values)
	def __getitem__(self,index : int | Argument | Reference) -> Argument:
		if isinstance(index,int):
			return self.values[index]
		if isinstance(index,Reference):
			if len(index) == 0:
				return self
			return self[index[0]][index[1:]]
		if isinstance(index,Argument):
			return get_at(index,self)
		raise KeyError('ArgumentList[' + type(index).__name__ + ']')
	def __setitem__(self,index : int | Argument | Reference,other : Any) -> None:
		if isinstance(index,int):
			self.values[index] = other
		elif isinstance(index,Reference):
			if len(index) == 1:
				self[index[0]] = other
			else:
				self[index[0]][index[1:]] = other
		elif isinstance(index,Argument):
			set_at(index,other,self)
		else:
			raise KeyError('ArgumentList[' + type(index).__name__ + ']')
	def __delitem__(self,index : int | Argument | Reference) -> None:
		if isinstance(index,int):
			del self.values[index]
		elif isinstance(index,Reference):
			if len(index) == 1:
				del self.values[index]
			else:
				del self[index[0]][index[1:]]
		elif isinstance(index,Argument):
			del_at(index,self)
		else:
			raise KeyError('ArgumentList[' + type(index).__name__ + ']')
	def __contains__(self,other : Any) -> bool:
		return contains_close(self,other)
	def __str__(self) -> str:
		return '(' + ','.join(str(value) for value in self) + ')'
	def insert(self,index : int | Argument | Reference,other : Argument) -> None:
		if isinstance(index,int):
			self.values.insert(index,other)
		elif isinstance(index,Reference):
			if len(index) == 1:
				self.insert(index[0],other)
			else:
				self[index[0]].insert(index[1:],other)
		elif isinstance(index,Argument):
			insert_at(index,other,self)
		else:
			raise KeyError('ArgumentList[' + type(index).__name__ + ']')
	def add(self,other : Argument) -> None:
		self.values.append(other)
class AttributeList(Clause):
	def __init__(self,*values : tuple[Any...]) -> None:
		self.values = {value for value in values}
	def __iter__(self) -> iter:
		return iter(self.values)
	def __len__(self) -> int:
		return len(self.values)
	def __getitem__(self,index : Any) -> Any:
		if isinstance(index,Reference):
			if len(index) == 0:
				return self
			return self[index[0]][index[1:]]
		return get_at(index,self)
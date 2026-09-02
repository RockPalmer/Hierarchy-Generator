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
from enum import Enum,auto
from token_types import symbol_of
from clause_operators import *

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
def squash(value : Any) -> Any:
	if isinstance(value,int | float | str | frozenset):
		return value
	if isinstance(value,tuple | list):
		return tuple([squash(v) for v in value])
	if isinstance(value,set):
		return frozenset({squash(v) for v in value})
	if isinstance(value,dict):
		return frozenset({squash((k,v)) for k,v in value.items()})
	return value.__squash__()
def matches(x : Any,y : Any) -> bool:
	if hasattr(x,'__matches__'):
		return x.__matches__(y)
	return x == y

class Parse_Grouped:
	def __init__(self,left : str,*args) -> None:
		match len(args):
			case 1:
				self.left = left
				self.empty = True
				self.body = None
				self.right = args[0]
			case 2:
				self.left = left
				self.empty = False
				self.body = args[0]
				self.right = args[1]
			case _:
				raise TypeError
class Parse_Delimited:
	def __init__(self,delimiter : str,*values : tuple[Any,...],/) -> None:
		self.delimiter = delimiter
		self.values = [value for value in values]

class All:
	def __repr__(self) -> str:
		return str(self)
	def __hash__(self) -> int:
		return hash(squash(self))
class Symbol(All):
	def __squash__(self) -> tuple[str]:
		return (self.__class__.__name__,)
	def __str__(self) -> str:
		return symbol_of(self.__class__.__name__)
class ParentReference(Symbol):
	def __init__(self) -> None:
		pass
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
class CollectionClause(All):
	def __iter__(self) -> iter:
		return iter(self.elements)
	def __len__(self) -> int:
		return len(self.elements)
	def __setitem__(self,index : Any,value : Any) -> None:
		self.elements[index] = value
	def __delitem__(self,index : Any) -> None:
		del self.elements[index]
	def __contains__(self,value : Any) -> bool:
		return value in self.elements
class SequenceClause(CollectionClause):
	def __init__(self,iterable = (),/) -> None:
		self.elements = [self.element_func(value) for value in iterable]
		for value in self.elements:
			set_parent(value,self)
		self.delimiter = symbol_of(self.__class__.__name__ + '.DELIMITER')
	def __getitem__(self,index : int | slice) -> Any:
		if isinstance(index,slice):
			return self.__class__(self.elements[index])
		return self.elements[index]
	def __str__(self) -> str:
		return self.delimiter.join(str(value) for value in self)
	def __squash__(self) -> tuple:
		return (
			type(self).__name__,
			squash(self.elements)
		)
	def add(self,value : Any) -> None:
		if value not in self:
			self.elements.append(value)
	def remove(self,value : Any) -> None:
		self.elements.remove(value)
	def discard(self,value : Any) -> None:
		if value int self:
			self.remove(value)
class GroupedClause(SequenceClause):
	def __str__(self) -> str:
		
		return op[0] + super().__str__() + op[1]
class RelationalAlgebraClause(Clause):
	def __init__(self,left : Any,right : Any,/) -> None:
		self.left = left
		self.right = right
		set_parent(self.left,self)
		set_parent(self.right,self)
	def __str__(self) -> str:
		return str(self.left) + str(self.delimiter()) + str(self.right)
	def operator_name(self) -> str:
		return self.__class__.__name__.split('_')[0]
class ParseMode(Enum):
	ENTITY = auto()
	ARGUMENT = auto()

def genElement(value):
	return value
def genAttribute(value):
	return value

class Reference(SequenceClause):
	def __init__(self,iterable = (),/) -> None:
		self.element_func = lambda x : x
		super().__init__(iterable)
	def __add__(self,value : Reference) -> Reference:
		return Reference(list(self) + list(value))
	def __radd__(self,value : Reference) -> Reference:
		if isinstance(value,Reference):
			return NotImplemented
		return Reference(list(value) + list(self))
	def __str__(self) -> str:
		return ''.join(str(value) for value in self)
class Hierarchy(SequenceClause):
	def __init__(self,iterable = (),/) -> None:
		self.element_func = genElement
		super().__init__(iterable)
	def getindices(self,value : Any) -> list[int]:
		return [
			i for i,e in enumerate(self) if matches(value,e)
		]
	def getindex(self,value : Any) -> int:
		indices = self.getindices(value)
		if len(indices) != 1:
			raise KeyError
		return indices[0]
	def contains(self,value : Any) -> bool:
		try:
			x = self.getindex(value)
			return True
		except KeyError:
			return False
	def get_at(self,index : Reference) -> Any:
		match len(index):
			case 0:
				return self
			case 1:

	def __define(self,fact : Any) -> None:
		if not isinstance(fact,Entity):
			raise TypeError
		if not self.contains(fact.header()):
			self.append(fact.header())
		if len(fact.conditions) > 1:
			raise TypeError
		operator = list(fact.conditions.keys())[0]
		clause = list(fact.conditions.values())[0]
class Identifier(All):
	def __init__(self,value : str,/) -> None:
		self.value = value
	def __eq__(self,value : Any) -> bool:
		if isinstance(value,str):
			return self.value == value
		if isinstance(value,Identifier):
			return self.value == value.value
		return False
	def __ne__(self,value : Any) -> bool:
		return not (self == value)
	def __squash__(self) -> tuple[str,str]:
		return ('Identifier',self.value)
class NameList(SequenceClause):
	def __init__(self,iterable = (),/) -> None:
		self.element_func = Identifier
		super().__init__(iterable)
	def __str__(self) -> str:
		match len(self):
			case 0:
				return ''
			case 1:
				return str(self[0])
			case _:
				return '(' + ','.join(str(value) for value in self) + ')'
	def __le__(self,value : Any) -> bool:
		return all(
			v in value for v in self
		)
	def __ge__(self,value : Any) -> bool:
		return all(
			v in self for v in value
		)
class Entity(Clause):
	def __init__(
		self,
		name = None,
		*,
		names = [],
		arguments = None,
		order = None,
		conditions = {}
	) -> None:
		if name is not None:
			self.names = NameList([name])
		else:
			self.names = NameList(names)
		if arguments is not None:
			self.arguments = ArgumentList(arguments)
		else:
			self.arguments = None
		if order is not None:
			self.ordering = Ordering(order)
		else:
			self.ordering = None
		self.conditions = ConditionSet(conditions)
		set_parent(self.names,self)
		set_parent(self.arguments,self)
		set_parent(self.ordering,self)
		set_parent(self.conditions,self)
	def __str__(self) -> str:
		result = str(self.names)
		if self.arguments is not None:
			result += str(self.arguments)
		if self.ordering is not None:
			result += '/' + str(self.ordering)
		if self.conditions is not None:
			for k,v in self.conditions.items():
				result += ' ' + k + ' ' + str(v)
		return result
	def __matches__(self,value : Any) -> bool:
		return (
			isinstance(value,Entity) and
			value.ordering is None and
			value.conditions is None and
			value.names <= self.names and
			matches(self.arguments,value.arguments)
		)
	def header(self) -> Entity:
		return Entity(
			names = self.names,
			arguments = self.arguments
		)
class ConditionSet(CollectionClause):
	def __init__(self,*args,**kwargs) -> None:
		self.elements = dict(*args,**kwargs)
	def __getitem__(self,index : Any) -> Any:
		return self.elements[index]
	def __str__(self) -> str:
		global CONDITIONS_ORDER

		vals = []
		for k in CONDITIONS_ORDER:
			if k not in self:
				continue
			vals.append(k + ' ' + str(self[k]))
		return ' '.join(vals)
	def __squash__(self) -> tuple:
		global CONDITIONS_ORDER

		vals = ['ConditionSet']
		for k in CONDITIONS_ORDER:
			if k not in self:
				continue
			vals.append((k,self[k]))
		return squash(vals)
class ArgumentList(GroupedClause):
	def __init__(self,iterable = (),/) -> None:
		self.element_func = Argument
		super().__init__(iterable)
	def __eq__(self,value : Any) -> bool:
		return (
			isinstance(value,ArgumentList) and
			self.elements == value.elements
		)
	def __ne__(self,value : Any) -> bool:
		return not (self == value)
class AttributeList(GroupedClause):
	def __init__(self,iterable = (),/) -> None:
		self.element_func = genAttribute
		super().__init__(iterable)
class Argument(Clause):
	pass
class ArgumentSymbol(Argument,Symbol):
	def is_defaulted(self) -> bool:
		return False
class PositionalDelimiter(ArgumentSymbol):
	def __init__(self) -> None:
		pass
class KeywordDelimiter(ArgumentSymbol):
	def __init__(self) -> None:
		pass
class RealArgument(Argument):
	def __init__(name,conditions = {}) -> None:
		self.name = Identifier(name)
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
	def is_defaulted(self) -> bool:
		return '=' in self.conditions
class BasicArgument(RealArgument):
	def __init__(name,conditions = {}) -> None:
		super().__init__(name,conditions)
		self.prefix = ''
class ComplexArgument(Argument):
	pass
class VarPositionalArgument(ComplexArgument):
	def __init__(name,conditions = {}) -> None:
		super().__init__(name,conditions)
		self.prefix = '*'
class VarKeywordArgument(ComplexArgument):
	def __init__(name,conditions = {}) -> None:
		super().__init__(name,conditions)
		self.prefix = '**'
class Union(SequenceClause):
	def __init__(self,iterable = (),/) -> None:
		self.element_func = lambda x : x
		super().__init__(iterable)
class Intersection(SequenceClause):
	def __init__(self,iterable = (),/) -> None:
		self.element_func = lambda x : x
		super().__init__(iterable)
class Difference(SequenceClause):
	def __init__(self,iterable = (),/) -> None:
		self.element_func = lambda x : x
		super().__init__(iterable)
class SymmetricDifference(SequenceClause):
	def __init__(self,iterable = (),/) -> None:
		self.element_func = lambda x : x
		super().__init__(iterable)
class InnerJoin(SequenceClause):
	def __init__(self,iterable = (),/) -> None:
		self.element_func = lambda x : x
		super().__init__(iterable)
class LeftJoin(SequenceClause):
	def __init__(self,iterable = (),/) -> None:
		self.element_func = lambda x : x
		super().__init__(iterable)
class RightJoin(SequenceClause):
	def __init__(self,iterable = (),/) -> None:
		self.element_func = lambda x : x
		super().__init__(iterable)
class FullJoin(SequenceClause):
	def __init__(self,iterable = (),/) -> None:
		self.element_func = lambda x : x
		super().__init__(iterable)
class CartesianProduct(SequenceClause):
	def __init__(self,iterable = (),/) -> None:
		self.element_func = lambda x : x
		super().__init__(iterable)
class Rename(RelationalAlgebraClause):
	def __init__(self,*args,**kwargs) -> None:
		super().__init__(*args,**kwargs)
class Select(RelationalAlgebraClause):
	def __init__(self,*args,**kwargs) -> None:
		super().__init__(*args,**kwargs)
class Projection(RelationalAlgebraClause):
	def __init__(self,*args,**kwargs) -> None:
		super().__init__(*args,**kwargs)
class Alias(RelationalAlgebraClause):
	def __init__(self,*args,**kwargs) -> None:
		super().__init__(*args,**kwargs)
class RenameWith(RelationalAlgebraClause):
	def __init__(self,*args,**kwargs) -> None:
		super().__init__(*args,**kwargs)
class RenameBody(GroupedClause):
	def __init__(self,iterable = (),/) -> None:
		self.element_func = RenameWith
		super().__init__(iterable)
class ProjectionBody(GroupedClause):
	def __init__(self,iterable = (),/) -> None:
		self.element_func = lambda x : x
		super().__init__(iterable)
from __future__ import annotations
from typing import Any,Iterable
from functools import reduce
from operator import (
	or_,
	and_
)
from glb import *
'''
<value> : None 		=> (None)
<value> : bool		=> (bool_<value>)
<value> : int 		=> (int_<value>)
<value> : float		=> (float_<value>)
<value> : str 		=> (str_<value>)
<value> : list 		=> (list_<i>_<v> for i,v in value)
<value> : tuple		=> (list_<i>_<v> for i,v in value)
<value> : set 		=> (list_<i>_<v> for i,v in value)
<value> : frozenset	=> (list_<i>_<v> for i,v in value)
<value> : dict		=> (dict_<k>_<v> for k,v in value)

<value> = ('None') => None
<value> = ('bool',...) => <value>[1] == 'True'
<value> = ('int',...) => int(<value>[1])
<value> = ('float',...) => float(<value>[1])
<value> = ('str',...) => '_'.join(<value>[1:])
<value> = ('list',...) => 
'''

class Clause:
	def __repr__(self) -> str:
		return str(self)
class Fact(Clause):
	def __init__(self,key : str,value : str) -> None:
		self.key = key
		self.value = value
	def needs_par(self) -> bool:
		return False
	def __str__(self) -> str:
		return self.key + '_' + self.value
	def __invert__(self) -> Not:
		return Not(self)
	def __and__(self,other : Clause) -> Binary:
		if isinstance(other,Fact | Not):
			return Binary('&&',self,other)
		if isinstance(other,Binary):
			match other.operator:
				case '&&':
					return other + Binary('&&',self)
				case '||':
					return Binary('&&',self,other)
				case _:
					raise TypeError('Invalid Binary op: ' + str(other.operator))
		return NotImplemented
	def __or__(self,other : Clause) -> Binary:
		if isinstance(other,Fact | Not):
			return Binary('||',self,other)
		if isinstance(other,Binary):
			match other.operator:
				case '||':
					return other + Binary('||',self)
				case '&&':
					return Binary('||',self,other)
				case _:
					raise TypeError('Invalid Binary op: ' + str(other.operator))
		return NotImplemented
class Binary(Clause):
	def __init__(self,op,*values) -> None:
		self.operator = op
		self.values = [value for value in values]
	def __str__(self) -> str:
		str_values = []
		for v in self:
			if v.needs_par():
				str_values.append('(' + str(v) + ')')
			else:
				str_values.append(str(v))
		return self.operator.join(str_values)
	def __iter__(self) -> iter:
		return iter(self.values)
	def __getitem__(self,index : int | slice):
		if isinstance(index,int):
			return self.values[index]
		return Binary(self.operator,*self.values[index])
	def __len__(self) -> int:
		return len(self.values)
	def __invert__(self) -> Binary:
		return Not(self)
	def __add__(self,other : Binary) -> Binary:
		if self.operator != other.operator:
			return NotImplemented
		return Binary(self.operator,*(self.values + other.values))
	def __and__(self,other):
		match self.operator:
			case '&&':
				if isinstance(other,Binary) and other.operator == '&&':
					return self + other
				return self + Binary('&&',other)
			case '||':
				if isinstance(other,Binary) and other.operator == '&&':
					return Binary('&&',self) + other
				return Binary('&&',self,other)
			case _:
				return NotImplemented
	def __or__(self,other):
		match self.operator:
			case '&&':
				if isinstance(other,Binary) and other.operator == '||':
					return Binary('||',self) + other
				return Binary('||',self,other)
			case '||':
				if isinstance(other,Binary) and other.operator == '||':
					return self + other
				return self + Binary('||',other)
			case _:
				return NotImplemented
	def needs_par(self) -> bool:
		return True
class Not(Clause):
	def __init__(self,value) -> None:
		self.value = value
	def __str__(self) -> str:
		return '!(' + str(self.value) + ')'
	def __invert__(self):
		return self.value
	def __and__(self,other : Clause) -> Binary:
		if isinstance(other,Fact | Not):
			return Binary('&&',self,other)
		if isinstance(other,Binary):
			match other.op:
				case '&&':
					return other + Binary('&&',self)
				case '||':
					return Binary('&&',self,other)
				case _:
					raise TypeError('Invalid Binary op: ' + str(other.op))
		return NotImplemented
	def __or__(self,other : Clause) -> Binary:
		if isinstance(other,Fact | Not):
			return Binary('||',self,other)
		if isinstance(other,Binary):
			match other.op:
				case '||':
					return other + Binary('||',self)
				case '&&':
					return Binary('||',self,other)
				case _:
					raise TypeError('Invalid Binary op: ' + str(other.op))
		return NotImplemented
	def needs_par(self) -> bool:
		return not isinstance(self.value,Fact)
def q(key : str,op : str,value : Any,value2 : Any = None) -> str:
	if op == '!=':
		return Not(q(key,'=',value))
	match op:
		case '=' | '==':
			ks = key.split('[')
			key = ks[0]
			indices = []
			for i in range(1,len(ks)):
				indices.append(ks[i][:-1])
			nkey = 'dict_' + key
			for index in indices:
				try:
					nkey += '_list_' + str(int(index))
				except:
					nkey += '_dict_' + index
			value = type_to_properties(value)
			if len(value) == 1:
				return Fact(nkey,value[0])
			return reduce(
				and_,
				[Fact(nkey,v) for v in value]
			)
		case 'in':
			return reduce(
				or_,
				[q(key,'=',v) for v in value]
			)
		case 'between':
			if not isinstance(value,int) or not isinstance(value2,int):
				raise TypeError
			return reduce(
				or_,
				[q(key,'=',v) for v in range(value,value2 + 1)]
			)
		case _:
			raise TypeError
def type_to_properties(value : Any) -> tuple[str,...]:
	if value is None:
		return ('None',)
	if isinstance(value,bool | int | float | str):
		return (type(value).__name__ + '_' + str(value),)
	if isinstance(value,list | tuple | set | frozenset):
		vals = []
		for i,v in enumerate(value):
			r = type_to_properties(v)
			for p in r:
				vals.append('list_' + str(i) + '_' + p)
		return tuple(vals)
	if isinstance(value,dict):
		vals = []
		for k,v in value.items():
			r = type_to_properties(v)
			for p in r:
				vals.append('dict_' + str(k) + '_' + p)
		return tuple(vals)
	raise TypeError(type(value).__name__)
def properties_to_type(values : Iterable[str]) -> Any:
	return list_list_to_any([
		value.split('_') for value in values
	])
def list_list_to_any(values : list[list[str]]) -> Any:
	if (
		len(values) == 1 and
		values[0][0] in {
			'None',
			'int',
			'float',
			'bool',
			'str',
		}
	):
		match values[0][0]:
			case 'None':
				return None
			case 'str':
				return '_'.join(values[0][1:])
			case 'bool':
				return values[0][1] == 'True'
			case 'int' | 'float':
				return {
					'int' : int,
					'float' : float,
				}[values[0][0]](values[0][1])
			case _:
				raise TypeError(values[0][0])
	match values[0][0]:
		case 'list':
			length = max(int(value[1]) for value in values) + 1
			vals = [None for i in range(length)]
			for i in range(length):
				vals[i] = list_list_to_any([
					v[2:] for v in values if v[1] == str(i)
				])
			return vals
		case 'dict':
			keys = {value[1] for value in values}
			vals = {}
			for key in keys:
				vals[key] = list_list_to_any([
					v[2:] for v in values if v[1] == key
				])
			return vals
		case _:
			raise TypeError(values[0][0])
def TAGS_(arg = None,**kargs) -> tuple[str,...]:
	if len(kargs) > 0:
		return type_to_properties(kargs)
	return str(arg)
from dataclasses import dataclass

@dataclass
class Entity:
  pass
@dataclass
class Type(Entity):
  name : str
  attributes : set[Attribute]
@dataclass
class Attribute(Entity):
  name : str
@dataclass
class Operation:
  pass
@dataclass
class Function(Operation):
  pass
@dataclass
class Projection(Function):
  directional : bool = False
  parameter = list[str] # length > 0
  input = Type
  returns = Type
@dataclass
class Selection(Function):
  directional : bool = False
  parameter = Callable[[],bool]
  input = Type
  returns = Type
@dataclass
class Rename(Function):
  directional : bool = False
  parameter : dict[str,str] # length > 0
  input = Type
  returns = Type
@dataclass
class Alias(Function):
  directional : bool = False
  parameter = str
  input = Type
  returns = Type
@dataclass
class Union(Function):
  directional : bool = False
  input = set[Type]
  returns = Type
@dataclass
class Intersection(Function):
  directional : bool = False
  input = set[Type]
  returns = Type
@dataclass
class SymmetricDifference(Function):
  directional : bool = False
  input = set[Type]
  returns = Type
@dataclass
class Difference(Function):
  directional : bool = True
  input = list[Type]
  returns = Type
@dataclass
class Product(Function):
  directional : bool = True
  input = list[Type]
  returns = Type
@dataclass
class Relationship(Operation):
  pass
@dataclass
class Inheritance(Relationship):
  directional : bool = True
  input : tuple[Type,Type]
@dataclass
class Instance(Relationship):
  directional : bool = True
  input : tuple[Attribute,Type]

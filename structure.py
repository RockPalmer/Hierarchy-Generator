class Entity:
  pass
class Type(Entity):
  name : str
  attributes : set[Attribute]
class Attribute(Entity):
  name : str
class Operation:
  pass
class Function(Operation):
  pass
class Projection(Function):
  directional : bool = False
  parameter = list[str] # length > 0
  input = Type
  returns = Type
class Selection(Function):
  directional : bool = False
  parameter = Callable[[],bool]
  input = Type
  returns = Type
class Rename(Function):
  directional : bool = False
  parameter : dict[str,str] # length > 0
structure = {
  "operator" : {
    "function" : {
      "rename" : {
        "directional" : false,
        "parameter" : "MAPPING[STRING,STRING]{>0}",
        "input" : "TYPE"
      },
      "alias" : {
        "directional" : false,
        "parameter" : "STRING",
        "input" : "TYPE"
      },
      "union" : {
        "directional" : false,
        "input" : "TYPE..."
      },
      "intersection" : {
        "directional" : false,
        "input" : "TYPE..."
      },
      "symmetric difference" : {
        "directional" : false,
        "input" : "TYPE..."
      },
      "difference" : {
        "directional" : true,
        "input" : "TYPE..."
      },
      "product" : {
        "directional" : true,
        "input" : "TYPE..."
      }
    },
    "relationship" : {
      "inheritance" : {
        "directional" : true,
        "input" : [
          "TYPE",
          "TYPE"
        ]
      },
      "instance" : {
        "directional" : true,
        "input" : [
          "ATTRIBUTE",
          "TYPE"
        ]
      }
    }
  }
}

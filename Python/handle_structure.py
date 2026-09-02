def try_create_type(name : str):
  global TYPES

  if any(name == n for _,n in TYPES.values()):
    raise TypeError

  TYPES[len(TYPES)] = ('LITERAL',name)
def try_create_projection(type_id : int,*attribute_indices : tuple[int,...]):
  global TYPES,PROJECTIONS

  PROJECTION_ID = len(TYPES)
  TYPES[PROJECTION_ID] = ('PROJECTION',type_id)
  PROJECTIONS[PROJECTION_ID] = attribute_indices
def try_create_selection(type_id : int,condition_id : int):
  global TYPES

  TYPES[len(TYPES)] = ('SELECTION',condition_id,type_id)
def try_create_renames(type_id : int,*renames : tuple[tuple[str,int],...]):
  global TYPES,RENAMES

  RENAME_ID = len(TYPES)
  TYPES[RENAME_ID] = ('RENAME',type_id)
  RENAMES[RENAME_ID] = set(renames)
def try_create_alias(type_id : int,new_type_name : str):
  global TYPES

  if any(new_type_name == n for _,n in TYPES.values()):
    raise TypeError
  TYPES[len(TYPES)] = ('ALIAS',new_type_name,type_id)
def try_create_union(type_id_1 : int,type_id_2 : int,*type_ids : tuple[int,...]):
  global TYPES,UNIONS

  UNION_ID = len(TYPES)
  TYPES[UNION_ID] = {type_id_1,type_id_2} | set(type_ids)

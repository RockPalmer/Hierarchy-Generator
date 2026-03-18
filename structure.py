ATTRIBUTES : int,int,str                        # TYPE_ID,INDEX,ATTRIBUTE_NAME
INHERITANCES : int,int                          # CHILD_TYPE_ID,PARENT_TYPE_ID
INSTANCES : int,int,int                         # CHILD_TYPE_ID,ATTRIBUTE_INDEX,PARENT_TYPE_ID
TYPES : {
  (int,'LITERAL',str),                          # TYPE_NAME
  (int,'PROJECTION',int),                       # TYPE_ID
  (int,'SELECTION',int,int),                    # CONDITION_ID,TYPE_ID
  (int,'RENAME',int),                           # TYPE_ID
  (int,'ALIAS',str,int),                        # NEW_TYPE_NAME,TYPE_ID
  (int,'UNION',frozenset[int]),                 # frozenset[TYPE_ID]
  (int,'INTERSECTION',frozenset[int]),          # frozenset[TYPE_ID]
  (int,'SYMMETRIC_DIFFERENCE',frozenset[int]),  # frozenset[TYPE_ID]
  (int,'DIFFERENCE',int,...),                   # TYPE_ID...
  (int,'PRODUCT',int,...),                      # TYPE_ID...
}
PROJECTIONS : int,int,int,int                   # PROJECTION_ID,NEW_COLUMN_INDEX,ATTRIBUTE_INDEX
RENAMES : int,str,int                           # RENAME_ID,NEW_ATTRIBUTE_NAME,ATTRIBUTE_INDEX

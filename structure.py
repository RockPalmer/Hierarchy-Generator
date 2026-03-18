ENTITIES : set[tuple[int,str,str]] # ENTITY_ID,TYPE,NAME
PROJECTIONS : set[tuple[int,index,str,int]] # PROJECTION_ID,INDEX,ATTRIBUTE_NAME,ENTITY_ID
SELECTIONS : set[tuple[int,int,int]] # SELECTION_ID,CONDITION_ID,ENTITY_ID
RENAMES : dict[tuple[int,str,str,int,int]] # RENAME_ID,PREVIOUS_ATTRIBUTE_NAME,NEW_ATTRIBUTE_NAME,INDEX,ENTITY_ID
ALIASES : 

{
  "function" : {
    "projection" : {
      "directional" : false,
      "parameter" : "STRING{>0}",
      "input" : "TYPE"
    },
    "selection" : {
      "directional" : false,
      "parameter" : "(INSTANCE) => BOOLEAN",
      "input" : "TYPE"
    },
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

# step 8. Only Extract these entities and these relationships.
ENTITY_TYPES = [
    "Pod",
    "Deployment",
    "ReplicaSet",
    "Node",
    "Service",
    "Container",
    "Component",
    "Resource",
]

RELATIONSHIP_TYPES = [
    "CREATES",
    "MANAGES",
    "RUNS_ON",
    "USES",
    "ROUTES_TO",
    "DEPENDS_ON",
    "CONTAINS",
    "COMMUNICATES_WITH",
]
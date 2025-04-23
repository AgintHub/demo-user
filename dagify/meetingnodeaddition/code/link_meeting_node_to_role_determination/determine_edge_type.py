def determine_edge_type(node_types: str) -> str:
 """
 Determines the type of edge based on the given node types.

 Args:
 node_types: Input parameter of type str

 Returns:
 str: Output of type str
 """
 # Pure implementation based on Node PRD requirements
 node_type_mapping = {
 'meeting': 'contains',
 'role_determination': 'determines'
 # Add more mappings as needed
 }

 try:
 node_types_list = node_types.split(',')
 edge_types = []
 for node_type in node_types_list:
 node_type = node_type.strip().lower()
 edge_type = node_type_mapping.get(node_type, 'unknown')
 edge_types.append(edge_type)
 return ','.join(edge_types)
 except Exception as e:
 raise ValueError(f"Failed to determine edge type: {e}") from e
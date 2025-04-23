def validate_node_creation(node_id: str, label: str) -> bool:
	"""
	Validates the creation of a node with a given ID and label.

	Args:
	node_id: Input parameter of type str
	label: Input parameter of type str

	Returns:
	bool: Output of type bool
	"""

	import re
	existing_node_ids = set()
	existing_labels = set()

	if not node_id or not label:
		return False

	if not re.match("^[a-zA-Z0-9_]+$", node_id) or not re.match("^[a-zA-Z0-9_]+$", label):
		return False

	if node_id in existing_node_ids or label in existing_labels:
		return False

	existing_node_ids.add(node_id)
	existing_labels.add(label)

	return True
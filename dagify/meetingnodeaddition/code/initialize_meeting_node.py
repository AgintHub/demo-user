from initialize_meeting_node.generate_uuid import generate_uuid
from initialize_meeting_node.create_node_with_label import create_node_with_label
from initialize_meeting_node.validate_node_creation import validate_node_creation

from pydantic import BaseModel, Field


class InitializeMeetingNodeOutput(BaseModel):
    """Pydantic model for initialize_meeting_node node outputs."""
    node_id: str = Field(..., description="Unique ID of the newly created meeting node")
    node_label: str = Field(..., description="Label of the meeting node")


def initialize_meeting_node_fx(general_input: str, **kwargs) -> InitializeMeetingNodeOutput:
    """Create a new node for the meeting with senior managers

    Args:
        general_input: General input string for the root node.
        **kwargs: Additional keyword arguments.

    Returns:
        InitializeMeetingNodeOutput: Object containing outputs for this node.
    """
    unique_id: str = generate_uuid()
    labeled_node: str = create_node_with_label(node_id=unique_id, label='Senior Managers Meeting')
    validation_result: bool = validate_node_creation(node_id=unique_id, label='Senior Managers Meeting')
    if validation_result:
        return InitializeMeetingNodeOutput(node_id=unique_id, node_label=labeled_node)
    else:
        return InitializeMeetingNodeOutput(node_id='Failed to create node', node_label='Node creation failed')

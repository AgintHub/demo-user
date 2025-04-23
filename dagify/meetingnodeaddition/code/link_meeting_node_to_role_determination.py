from link_meeting_node_to_role_determination.extract_relevant_info import extract_relevant_info
from link_meeting_node_to_role_determination.generate_unique_id import generate_unique_id
from link_meeting_node_to_role_determination.determine_edge_type import determine_edge_type
from link_meeting_node_to_role_determination.create_edge import create_edge
from link_meeting_node_to_role_determination.handle_error import handle_error

from pydantic import BaseModel, Field
from typing import List


class SpecifyMeetingDetailsOutput(BaseModel):
    """Pydantic model for specify_meeting_details node outputs."""
    meeting_date: str = Field(..., description="Date of the meeting in ISO format (YYYY-MM-DD)")
    meeting_time: str = Field(..., description="Time of the meeting in ISO format (HH:MM)")
    meeting_location: str = Field(..., description="Location of the meeting")
    attendees: List[str] = Field(..., description="List of attendees for the meeting")


class LinkMeetingNodeToRoleDeterminationOutput(BaseModel):
    """Pydantic model for link_meeting_node_to_role_determination node outputs."""
    edge_id: str = Field(..., description="Unique ID of the edge linking the meeting node to the role determination node")
    edge_type: str = Field(..., description="Type of the edge (e.g., 'precedence')")


def link_meeting_node_to_role_determination_fx(specify_meeting_details_input: SpecifyMeetingDetailsOutput, **kwargs) -> LinkMeetingNodeToRoleDeterminationOutput:
    """Link the meeting node to the user role determination process

    Args:
        specify_meeting_details_input: Input from the 'specify_meeting_details' node.
        **kwargs: Additional keyword arguments.

    Returns:
        LinkMeetingNodeToRoleDeterminationOutput: Object containing outputs for this node.
    """
    # Extract necessary information from the input
    meeting_details: dict = extract_relevant_info(input_data=specify_meeting_details_input)
    
    # Generate a unique edge ID using a UUID library
    edge_id: str = generate_unique_id()
    
    # Determine the edge type based on the node types
    edge_type: str = determine_edge_type(node_types=__get_node_types(meeting_details=meeting_details))
    
    # Implement error handling for edge creation
    try:
        # Attempt to create the edge
        create_edge(edge_id=edge_id, edge_type=edge_type, meeting_details=meeting_details)
    except Exception as e:
        # Handle any exceptions that occur during edge creation
        handle_error(exception=e)
    
    # Return the output in the required format
    return LinkMeetingNodeToRoleDeterminationOutput(edge_id=edge_id, edge_type=edge_type)

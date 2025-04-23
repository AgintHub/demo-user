from specify_meeting_details.get_available_dates import get_available_dates
from specify_meeting_details.select_meeting_date import select_meeting_date
from specify_meeting_details.schedule_meeting_time import schedule_meeting_time
from specify_meeting_details.determine_meeting_location import determine_meeting_location
from specify_meeting_details.identify_meeting_attendees import identify_meeting_attendees

from pydantic import BaseModel, Field
from typing import List


class InitializeMeetingNodeOutput(BaseModel):
    """Pydantic model for initialize_meeting_node node outputs."""
    node_id: str = Field(..., description="Unique ID of the newly created meeting node")
    node_label: str = Field(..., description="Label of the meeting node")


class SpecifyMeetingDetailsOutput(BaseModel):
    """Pydantic model for specify_meeting_details node outputs."""
    meeting_date: str = Field(..., description="Date of the meeting in ISO format (YYYY-MM-DD)")
    meeting_time: str = Field(..., description="Time of the meeting in ISO format (HH:MM)")
    meeting_location: str = Field(..., description="Location of the meeting")
    attendees: List[str] = Field(..., description="List of attendees for the meeting")


def specify_meeting_details_fx(initialize_meeting_node_input: InitializeMeetingNodeOutput, **kwargs) -> SpecifyMeetingDetailsOutput:
    """Specify details of the meeting with senior managers

    Args:
        initialize_meeting_node_input: Input from the 'initialize_meeting_node' node.
        **kwargs: Additional keyword arguments.

    Returns:
        SpecifyMeetingDetailsOutput: Object containing outputs for this node.
    """
    proposed_dates: List[str] = get_available_dates()
    chosen_date: str = select_meeting_date(dates=proposed_dates)
    meeting_time: str = schedule_meeting_time(date=chosen_date)
    location: str = __determine_meeting_location(date=chosen_date, time=meeting_time)
    attendees_list: List[str] = identify_meeting_attendees(node_id=initialize_meeting_node_input.node_id)
    
    return SpecifyMeetingDetailsOutput(
        meeting_date=chosen_date,
        meeting_time=meeting_time,
        meeting_location=location,
        attendees=attendees_list
    )
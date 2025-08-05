from pydantic import BaseModel, Field
from typing import List


class CalculateThrustRequirementsOutput(BaseModel):
    """Pydantic model for calculate_thrust_requirements node outputs."""
    thrust_values: List[float] = Field(..., description="List of necessary thrust values for each stage")
    payload_capacity: float = Field(..., description="Maximum payload capacity of the rocket")
    mission_duration: float = Field(..., description="Duration of the mission in seconds")
    gravitational_forces: List[float] = Field(..., description="List of gravitational forces acting on the rocket at each stage")
    num_stages: int = Field(..., description="Number of stages in the rocket")


class SelectPropulsionSystemOutput(BaseModel):
    """Pydantic model for select_propulsion_system node outputs."""
    propulsion_system_type: str = Field(..., description="The type of propulsion system selected (e.g., solid, liquid, hybrid)")
    thrust_vector: float = Field(..., description="The thrust vector of the selected propulsion system")
    specific_impulse: float = Field(..., description="The specific impulse of the selected propulsion system")
    fuel_efficiency: float = Field(..., description="The fuel efficiency of the selected propulsion system")
    is_alternative_propulsion: bool = Field(..., description="Whether an alternative propulsion method is used")


def select_propulsion_system(calculate_thrust_requirements_input: CalculateThrustRequirementsOutput, **kwargs) -> SelectPropulsionSystemOutput:
    """Choose a propulsion system that meets the rocket's performance requirements

    Args:
        calculate_thrust_requirements_input: Input from the 'calculate_thrust_requirements' node.
        **kwargs: Additional keyword arguments.

    Returns:
        SelectPropulsionSystemOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return SelectPropulsionSystemOutput(
        propulsion_system_type="",
        thrust_vector=0.0,
        specific_impulse=0.0,
        fuel_efficiency=0.0,
        is_alternative_propulsion=False,
    )
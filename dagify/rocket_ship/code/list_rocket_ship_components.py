from pydantic import BaseModel, Field
from typing import List


class DefineRocketShipOutput(BaseModel):
    """Pydantic model for define_rocket_ship node outputs."""
    rocket_name: str = Field(..., description="Name of the rocket ship")
    propulsion_system: str = Field(..., description="Type of propulsion system used")
    cargo_capacity: List[str] = Field(..., description="List of cargo types and capacities")
    guidance_system: str = Field(..., description="Type of guidance system used")
    functionality: List[str] = Field(..., description="List of functionalities of the rocket ship")


class ListRocketShipComponentsOutput(BaseModel):
    """Pydantic model for list_rocket_ship_components node outputs."""
    component_names: List[str] = Field(..., description="List of names of the rocket ship components")


def list_rocket_ship_components(define_rocket_ship_input: DefineRocketShipOutput, **kwargs) -> ListRocketShipComponentsOutput:
    """Enumerate and describe each major component of a rocket ship

    Args:
        define_rocket_ship_input: Input from the 'define_rocket_ship' node.
        **kwargs: Additional keyword arguments.

    Returns:
        ListRocketShipComponentsOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return ListRocketShipComponentsOutput(
        component_names=[],
    )
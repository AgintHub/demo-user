from pydantic import BaseModel, Field
from typing import List


class DefineRocketShipOutput(BaseModel):
    """Pydantic model for define_rocket_ship node outputs."""
    rocket_name: str = Field(..., description="Name of the rocket ship")
    propulsion_system: str = Field(..., description="Type of propulsion system used")
    cargo_capacity: List[str] = Field(..., description="List of cargo types and capacities")
    guidance_system: str = Field(..., description="Type of guidance system used")
    functionality: List[str] = Field(..., description="List of functionalities of the rocket ship")


def define_rocket_ship(general_input: str, **kwargs) -> DefineRocketShipOutput:
    """Identify the key components and purposes of a rocket ship

    Args:
        general_input: General input string for the root node.
        **kwargs: Additional keyword arguments.

    Returns:
        DefineRocketShipOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return DefineRocketShipOutput(
        rocket_name="",
        propulsion_system="",
        cargo_capacity=[],
        guidance_system="",
        functionality=[],
    )
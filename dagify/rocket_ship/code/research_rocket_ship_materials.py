from pydantic import BaseModel, Field
from typing import List


class DefineRocketShipOutput(BaseModel):
    """Pydantic model for define_rocket_ship node outputs."""
    rocket_name: str = Field(..., description="Name of the rocket ship")
    propulsion_system: str = Field(..., description="Type of propulsion system used")
    cargo_capacity: List[str] = Field(..., description="List of cargo types and capacities")
    guidance_system: str = Field(..., description="Type of guidance system used")
    functionality: List[str] = Field(..., description="List of functionalities of the rocket ship")


class ResearchRocketShipMaterialsOutput(BaseModel):
    """Pydantic model for research_rocket_ship_materials node outputs."""
    material_type: str = Field(..., description="Type of material used in rocket ship construction")
    material_description: str = Field(..., description="Description of the material used in rocket ship construction")


def research_rocket_ship_materials(define_rocket_ship_input: DefineRocketShipOutput, **kwargs) -> ResearchRocketShipMaterialsOutput:
    """Identify and describe the materials typically used in rocket ship construction

    Args:
        define_rocket_ship_input: Input from the 'define_rocket_ship' node.
        **kwargs: Additional keyword arguments.

    Returns:
        ResearchRocketShipMaterialsOutput: Object containing outputs for this node.
    """
    # TODO: Implement this function

    # Return stub output with placeholder values
    return ResearchRocketShipMaterialsOutput(
        material_type="",
        material_description="",
    )
from pydantic import BaseModel, Field
from typing import List


class ExtractCriticalConstraintsOutput(BaseModel):
    """Pydantic model for extract_critical_constraints node outputs."""
    constraints: List[str] = Field(..., description="Individual statements of technical, business, regulatory, or design constraints relevant to the product requirements.")


def extract_critical_constraints_fx(general_input: str, **kwargs) -> ExtractCriticalConstraintsOutput:
    """List all technical, business, or regulatory constraints inferred or stated in the workflow requirements.

    Args:
        general_input: General input string for the root node.
        **kwargs: Additional keyword arguments.

    Returns:
        ExtractCriticalConstraintsOutput: Object containing outputs for this node.
    """
    pass
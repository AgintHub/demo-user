from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class assess_major_risks_output(BaseModel):
    risk_descriptions: List[str]  # Short descriptions of major risks for the workflow/project.

class assign_feature_priorities_output(BaseModel):
    core_feature_priorities: List[str]  # Relative priority label (Must Have, Should Have, Nice to Have) for each feature (same order as core_feature_names).

class define_stakeholder_roles_output(BaseModel):
    stakeholder_roles: List[str]  # List of unique user or stakeholder roles relevant to the workflow.

class extract_acceptance_criteria_output(BaseModel):
    acceptance_criteria_texts: List[str]  # All acceptance criteria, grouped by order to associated user stories.
    user_story_indices: List[int]  # Index of the user story each set of acceptance criteria belongs to (same order as acceptance_criteria_texts).

class extract_workflow_overview_output(BaseModel):
    workflow_overview: str  # Concise summary of the workflows purpose and business value.

class formulate_user_stories_output(BaseModel):
    user_stories: List[str]  # User stories, each following the format: As a [role], I want to [action] so that [goal].

class identify_core_features_output(BaseModel):
    core_feature_names: List[str]  # Names or short descriptions of each core feature required for the workflow.

class identify_project_constraints_output(BaseModel):
    constraint_descriptions: List[str]  # Descriptions of all project constraints, each as a brief sentence.


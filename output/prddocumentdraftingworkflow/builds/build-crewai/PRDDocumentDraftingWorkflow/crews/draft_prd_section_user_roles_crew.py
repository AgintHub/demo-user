from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import draft_prd_section_user_roles_output

@CrewBase
class draft_prd_section_user_roles_crew:
    """Crew for draft_prd_section_user_roles operations."""


    @agent
    def draft_prd_section_user_roles_agent(self):
        return Agent(
            role="Draft Prd Section User Roles Specialist",
            goal="""Execute draft_prd_section_user_roles task accurately.
PRD Requirements:
""",
            backstory="You are a specialized worker focused on Format the identified user roles as the User Roles & Personas section for the PRD.",
            verbose=True
        )



    @task
    def draft_prd_section_user_roles_task(self):
        """Task for draft_prd_section_user_roles."""
        agent = self.draft_prd_section_user_roles_agent()
        return Task(
            description="""Using {identify_primary_user_roles_output}, Format the identified user roles as the User Roles & Personas section for the PRD.""",
            agent=agent,
            expected_output="""{
    role_names: list of strs  # List of user role or persona names included in the PRD section
    role_descriptions: list of strs  # List of brief descriptions for each user role or persona, matching the order of role_names
    section_text: str  # The full 'User Roles & Personas' section as formatted text for the PRD
}""",
            output_pydantic=draft_prd_section_user_roles_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.draft_prd_section_user_roles_agent()],
            tasks=[self.draft_prd_section_user_roles_task()],
            verbose=True
        )

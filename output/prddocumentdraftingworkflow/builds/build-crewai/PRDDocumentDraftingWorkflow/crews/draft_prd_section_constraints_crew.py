from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import draft_prd_section_constraints_output

@CrewBase
class draft_prd_section_constraints_crew:
    """Crew for draft_prd_section_constraints operations."""


    @agent
    def draft_prd_section_constraints_agent(self):
        return Agent(
            role="Draft Prd Section Constraints Specialist",
            goal="""Execute draft_prd_section_constraints task accurately.
PRD Requirements:
""",
            backstory="You are a specialized worker focused on Format the extracted constraints into a Constraints section for the PRD.",
            verbose=True
        )



    @task
    def draft_prd_section_constraints_task(self):
        """Task for draft_prd_section_constraints."""
        agent = self.draft_prd_section_constraints_agent()
        return Task(
            description="""Using {extract_critical_constraints_output}, Format the extracted constraints into a Constraints section for the PRD.""",
            agent=agent,
            expected_output="""{
    constraints_section_heading: str  # Section heading for the Constraints section in the PRD.
    constraints_list: list of strs  # A list of formal, clearly stated constraints relevant to the product requirements.
}""",
            output_pydantic=draft_prd_section_constraints_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.draft_prd_section_constraints_agent()],
            tasks=[self.draft_prd_section_constraints_task()],
            verbose=True
        )

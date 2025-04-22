from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import draft_prd_section_objectives_output

@CrewBase
class draft_prd_section_objectives_crew:
    """Crew for draft_prd_section_objectives operations."""


    @agent
    def draft_prd_section_objectives_agent(self):
        return Agent(
            role="Draft Prd Section Objectives Specialist",
            goal="""Execute draft_prd_section_objectives task accurately.
PRD Requirements:
""",
            backstory="You are a specialized worker focused on Format the extracted objectives as the Objectives section for the PRD.",
            verbose=True
        )



    @task
    def draft_prd_section_objectives_task(self):
        """Task for draft_prd_section_objectives."""
        agent = self.draft_prd_section_objectives_agent()
        return Task(
            description="""Using {extract_objectives_from_workflow_requirements_output}, Format the extracted objectives as the Objectives section for the PRD.""",
            agent=agent,
            expected_output="""{
    objectives_section_heading: str  # The section heading for objectives, e.g. 'Objectives'.
    objective_statements: list of strs  # A list of individual, formal objective statements for inclusion in the PRD Objectives section.
}""",
            output_pydantic=draft_prd_section_objectives_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.draft_prd_section_objectives_agent()],
            tasks=[self.draft_prd_section_objectives_task()],
            verbose=True
        )

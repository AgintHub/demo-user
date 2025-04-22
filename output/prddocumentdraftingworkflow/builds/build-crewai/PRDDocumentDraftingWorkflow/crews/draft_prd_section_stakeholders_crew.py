from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import draft_prd_section_stakeholders_output

@CrewBase
class draft_prd_section_stakeholders_crew:
    """Crew for draft_prd_section_stakeholders operations."""


    @agent
    def draft_prd_section_stakeholders_agent(self):
        return Agent(
            role="Draft Prd Section Stakeholders Specialist",
            goal="""Execute draft_prd_section_stakeholders task accurately.
PRD Requirements:
""",
            backstory="You are a specialized worker focused on Format the stakeholder summaries into a PRD Stakeholders section.",
            verbose=True
        )



    @task
    def draft_prd_section_stakeholders_task(self):
        """Task for draft_prd_section_stakeholders."""
        agent = self.draft_prd_section_stakeholders_agent()
        return Task(
            description="""Using {summarize_key_stakeholders_output}, Format the stakeholder summaries into a PRD Stakeholders section.""",
            agent=agent,
            expected_output="""{
    stakeholder_names: list of strs  # List of the stakeholder names or titles included in the PRD Stakeholders section.
    stakeholder_roles: list of strs  # List of short descriptions for each stakeholder's role in the project. Aligned by index with stakeholder_names.
    stakeholder_significance: list of strs  # List of brief statements of each stakeholder's significance or interest in the project outcome. Aligned by index with stakeholder_names.
    prd_stakeholders_section_text: str  # The fully formatted 'Stakeholders' section text, ready to be inserted directly into the PRD document.
}""",
            output_pydantic=draft_prd_section_stakeholders_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.draft_prd_section_stakeholders_agent()],
            tasks=[self.draft_prd_section_stakeholders_task()],
            verbose=True
        )

from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import compile_final_prd_document_output

@CrewBase
class compile_final_prd_document_crew:
    """Crew for compile_final_prd_document operations."""


    @agent
    def compile_final_prd_document_agent(self):
        return Agent(
            role="Compile Final Prd Document Specialist",
            goal="""Execute compile_final_prd_document task accurately.
PRD Requirements:
""",
            backstory="You are a specialized worker focused on Combine all previously drafted sections into a single coherent PRD document, maintaining logical order and structure.",
            verbose=True
        )



    @task
    def compile_final_prd_document_task(self):
        """Task for compile_final_prd_document."""
        agent = self.compile_final_prd_document_agent()
        return Task(
            description="""Using {draft_prd_section_objectives_output}, {draft_prd_section_user_roles_output}, {draft_prd_section_features_output}, {draft_prd_section_constraints_output}, {draft_prd_section_success_metrics_output}, {draft_prd_section_stakeholders_output}, {draft_prd_section_user_journeys_output}, Combine all previously drafted sections into a single coherent PRD document, maintaining logical order and structure.""",
            agent=agent,
            expected_output="""{
    prd_title: str  # Title of the Product Requirements Document
    objectives_section: str  # The full formatted Objectives section text
    user_roles_and_personas_section: str  # The full formatted User Roles & Personas section text
    features_section: str  # The full formatted Features section text
    constraints_section: str  # The full formatted Constraints section text
    success_metrics_section: str  # The full formatted Success Metrics section text
    stakeholders_section: str  # The full formatted Stakeholders section text
    user_journeys_section: str  # The full formatted User Journeys section text
    full_prd_document: str  # The complete combined PRD document as a single string, with all sections in proper order and headings
}""",
            output_pydantic=compile_final_prd_document_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.compile_final_prd_document_agent()],
            tasks=[self.compile_final_prd_document_task()],
            verbose=True
        )

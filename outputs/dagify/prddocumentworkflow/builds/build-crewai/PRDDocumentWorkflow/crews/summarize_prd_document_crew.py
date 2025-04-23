from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import summarize_prd_document_output

@CrewBase
class summarize_prd_document_crew:
    """Crew for summarize_prd_document operations."""


    @agent
    def summarize_prd_document_agent(self):
        return Agent(
            role="Summarize Prd Document Specialist",
            goal="Execute summarize_prd_document task accurately",
            backstory="You are a specialized worker focused on Produces a coherent, structured PRD summary from all extracted and organized data.",
            verbose=True
        )



    @task
    def summarize_prd_document_task(self):
        """Task for summarize_prd_document."""
        agent = self.summarize_prd_document_agent()
        return Task(
            description="""Using {extract_product_name_output}, {extract_primary_objective_output}, {determine_target_users_output}, {identify_user_problems_output}, {extract_user_stories_output}, {extract_feature_requirements_output}, {classify_feature_priorities_output}, {determine_technical_constraints_output}, {extract_success_metrics_output}, Produces a coherent, structured PRD summary from all extracted and organized data.""",
            agent=agent,
            expected_output="""{
    prd_summary: str  # The full, structured PRD summary as plain text.
}""",
            output_pydantic=summarize_prd_document_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.summarize_prd_document_agent()],
            tasks=[self.summarize_prd_document_task()],
            verbose=True
        )

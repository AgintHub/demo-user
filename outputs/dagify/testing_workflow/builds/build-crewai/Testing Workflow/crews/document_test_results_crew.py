from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import document_test_results_output

@CrewBase
class document_test_results_crew:
    """Crew for document_test_results operations."""


    @agent
    def document_test_results_agent(self):
        return Agent(
            role="Document Test Results Specialist",
            goal="Execute document_test_results task accurately",
            backstory="You are a specialized worker focused on Document the test results",
            verbose=True
        )



    @task
    def document_test_results_task(self):
        """Task for document_test_results."""
        agent = self.document_test_results_agent()
        return Task(
            description="""Using {analyze_test_results_output}, Document the test results""",
            agent=agent,
            expected_output="""{
    document_id: str  # Document ID
    document_url: str  # Document URL
}""",
            output_pydantic=document_test_results_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.document_test_results_agent()],
            tasks=[self.document_test_results_task()],
            verbose=True
        )

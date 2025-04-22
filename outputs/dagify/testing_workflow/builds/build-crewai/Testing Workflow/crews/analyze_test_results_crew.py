from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import analyze_test_results_output

@CrewBase
class analyze_test_results_crew:
    """Crew for analyze_test_results operations."""


    @agent
    def analyze_test_results_agent(self):
        return Agent(
            role="Analyze Test Results Specialist",
            goal="Execute analyze_test_results task accurately",
            backstory="You are a specialized worker focused on Analyze the test results",
            verbose=True
        )



    @task
    def analyze_test_results_task(self):
        """Task for analyze_test_results."""
        agent = self.analyze_test_results_agent()
        return Task(
            description="""Using {perform_test_cases_output}, Analyze the test results""",
            agent=agent,
            expected_output="""{
    analysis_results: str  # Analysis results
}""",
            output_pydantic=analyze_test_results_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.analyze_test_results_agent()],
            tasks=[self.analyze_test_results_task()],
            verbose=True
        )

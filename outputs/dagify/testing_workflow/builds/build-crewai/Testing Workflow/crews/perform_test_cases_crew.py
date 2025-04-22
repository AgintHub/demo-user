from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import perform_test_cases_output

@CrewBase
class perform_test_cases_crew:
    """Crew for perform_test_cases operations."""


    @agent
    def perform_test_cases_agent(self):
        return Agent(
            role="Perform Test Cases Specialist",
            goal="Execute perform_test_cases task accurately",
            backstory="You are a specialized worker focused on Perform the selected test cases",
            verbose=True
        )



    @task
    def perform_test_cases_task(self):
        """Task for perform_test_cases."""
        agent = self.perform_test_cases_agent()
        return Task(
            description="""Using {select_test_cases_output}, Perform the selected test cases""",
            agent=agent,
            expected_output="""{
    test_results: list of strs  # List of test results
}""",
            output_pydantic=perform_test_cases_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.perform_test_cases_agent()],
            tasks=[self.perform_test_cases_task()],
            verbose=True
        )

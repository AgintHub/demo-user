from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import select_test_cases_output

@CrewBase
class select_test_cases_crew:
    """Crew for select_test_cases operations."""


    @agent
    def select_test_cases_agent(self):
        return Agent(
            role="Select Test Cases Specialist",
            goal="Execute select_test_cases task accurately",
            backstory="You are a specialized worker focused on Select the relevant test cases",
            verbose=True
        )



    @task
    def select_test_cases_task(self):
        """Task for select_test_cases."""
        agent = self.select_test_cases_agent()
        return Task(
            description="""Using {get_testing_environment_output}, Select the relevant test cases""",
            agent=agent,
            expected_output="""{
    selected_test_cases: list of strs  # List of selected test cases
}""",
            output_pydantic=select_test_cases_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.select_test_cases_agent()],
            tasks=[self.select_test_cases_task()],
            verbose=True
        )

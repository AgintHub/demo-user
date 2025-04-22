from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import get_testing_environment_output

@CrewBase
class get_testing_environment_crew:
    """Crew for get_testing_environment operations."""


    @agent
    def get_testing_environment_agent(self):
        return Agent(
            role="Get Testing Environment Specialist",
            goal="Execute get_testing_environment task accurately",
            backstory="You are a specialized worker focused on Get the testing environment details",
            verbose=True
        )



    @task
    def get_testing_environment_task(self):
        """Task for get_testing_environment."""
        agent = self.get_testing_environment_agent()
        return Task(
            description="""Using {input}, Get the testing environment details""",
            agent=agent,
            expected_output="""{
    environment_type: str  # Type of the testing environment
    test_cases: list of strs  # List of test cases
    test_data: list of strs  # List of test data
}""",
            output_pydantic=get_testing_environment_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.get_testing_environment_agent()],
            tasks=[self.get_testing_environment_task()],
            verbose=True
        )

from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import extract_goals_output

@CrewBase
class extract_goals_crew:
    """Crew for extract_goals operations."""


    @agent
    def extract_goals_agent(self):
        return Agent(
            role="Extract Goals Specialist",
            goal="Execute extract_goals task accurately",
            backstory="You are a specialized worker focused on Extract and list the primary goals and objectives the product must achieve.",
            verbose=True
        )



    @task
    def extract_goals_task(self):
        """Task for extract_goals."""
        agent = self.extract_goals_agent()
        return Task(
            description="""Using {extract_product_context_output}, Extract and list the primary goals and objectives the product must achieve.""",
            agent=agent,
            expected_output="""{
    primary_goals: list of strs  # A list of the main goals and objectives the product or workflow must achieve, each expressed as a clear and atomic statement focused on business value.
}""",
            output_pydantic=extract_goals_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.extract_goals_agent()],
            tasks=[self.extract_goals_task()],
            verbose=True
        )

from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import extract_primary_objective_output

@CrewBase
class extract_primary_objective_crew:
    """Crew for extract_primary_objective operations."""


    @agent
    def extract_primary_objective_agent(self):
        return Agent(
            role="Extract Primary Objective Specialist",
            goal="Execute extract_primary_objective task accurately",
            backstory="You are a specialized worker focused on Identifies the main objective or goal of the product as described by the user.",
            verbose=True
        )



    @task
    def extract_primary_objective_task(self):
        """Task for extract_primary_objective."""
        agent = self.extract_primary_objective_agent()
        return Task(
            description="""Using {extract_product_name_output}, Identifies the main objective or goal of the product as described by the user.""",
            agent=agent,
            expected_output="""{
    primary_objective: str  # Main product objective or success goal.
}""",
            output_pydantic=extract_primary_objective_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.extract_primary_objective_agent()],
            tasks=[self.extract_primary_objective_task()],
            verbose=True
        )

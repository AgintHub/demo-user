from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import identify_core_objective_output

@CrewBase
class identify_core_objective_crew:
    """Crew for identify_core_objective operations."""


    @agent
    def identify_core_objective_agent(self):
        return Agent(
            role="Identify Core Objective Specialist",
            goal="Execute identify_core_objective task accurately",
            backstory="You are a specialized worker focused on Extract the single core objective of the workflow based on provided requirements.",
            verbose=True
        )



    @task
    def identify_core_objective_task(self):
        """Task for identify_core_objective."""
        agent = self.identify_core_objective_agent()
        return Task(
            description="""Using {input}, Extract the single core objective of the workflow based on provided requirements.""",
            agent=agent,
            expected_output="""{
    core_objective: str  # The primary objective statement for the workflow as described in the requirements.
}""",
            output_pydantic=identify_core_objective_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.identify_core_objective_agent()],
            tasks=[self.identify_core_objective_task()],
            verbose=True
        )

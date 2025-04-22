from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import extract_core_product_features_output

@CrewBase
class extract_core_product_features_crew:
    """Crew for extract_core_product_features operations."""


    @agent
    def extract_core_product_features_agent(self):
        return Agent(
            role="Extract Core Product Features Specialist",
            goal="""Execute extract_core_product_features task accurately.
PRD Requirements:
""",
            backstory="You are a specialized worker focused on Identify and list all core product features needed to satisfy the workflow requirements.",
            verbose=True
        )



    @task
    def extract_core_product_features_task(self):
        """Task for extract_core_product_features."""
        agent = self.extract_core_product_features_agent()
        return Task(
            description="""Using {extract_objectives_from_workflow_requirements_output}, Identify and list all core product features needed to satisfy the workflow requirements.""",
            agent=agent,
            expected_output="""{
    core_product_features: list of strs  # A list of singular, succinct descriptions of each core product feature required to achieve the stated objectives.
}""",
            output_pydantic=extract_core_product_features_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.extract_core_product_features_agent()],
            tasks=[self.extract_core_product_features_task()],
            verbose=True
        )

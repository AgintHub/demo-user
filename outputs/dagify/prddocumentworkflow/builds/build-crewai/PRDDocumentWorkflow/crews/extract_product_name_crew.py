from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import extract_product_name_output

@CrewBase
class extract_product_name_crew:
    """Crew for extract_product_name operations."""


    @agent
    def extract_product_name_agent(self):
        return Agent(
            role="Extract Product Name Specialist",
            goal="Execute extract_product_name task accurately",
            backstory="You are a specialized worker focused on Extracts the product or feature name from the user prompt.",
            verbose=True
        )



    @task
    def extract_product_name_task(self):
        """Task for extract_product_name."""
        agent = self.extract_product_name_agent()
        return Task(
            description="""Using {input}, Extracts the product or feature name from the user prompt.""",
            agent=agent,
            expected_output="""{
    product_name: str  # The concise name of the product or feature.
}""",
            output_pydantic=extract_product_name_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.extract_product_name_agent()],
            tasks=[self.extract_product_name_task()],
            verbose=True
        )

from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import identify_stakeholders_output

@CrewBase
class identify_stakeholders_crew:
    """Crew for identify_stakeholders operations."""


    @agent
    def identify_stakeholders_agent(self):
        return Agent(
            role="Identify Stakeholders Specialist",
            goal="Execute identify_stakeholders task accurately",
            backstory="You are a specialized worker focused on Identify and list all relevant stakeholders for the product or feature based on workflow requirements.",
            verbose=True
        )



    @task
    def identify_stakeholders_task(self):
        """Task for identify_stakeholders."""
        agent = self.identify_stakeholders_agent()
        return Task(
            description="""Using {extract_product_context_output}, Identify and list all relevant stakeholders for the product or feature based on workflow requirements.""",
            agent=agent,
            expected_output="""{
    stakeholder_roles: list of strs  # List of individual stakeholder roles, titles, or groups relevant to the product or workflow.
}""",
            output_pydantic=identify_stakeholders_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.identify_stakeholders_agent()],
            tasks=[self.identify_stakeholders_task()],
            verbose=True
        )

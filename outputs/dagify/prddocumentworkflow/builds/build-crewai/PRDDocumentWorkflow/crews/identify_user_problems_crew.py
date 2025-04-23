from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import identify_user_problems_output

@CrewBase
class identify_user_problems_crew:
    """Crew for identify_user_problems operations."""


    @agent
    def identify_user_problems_agent(self):
        return Agent(
            role="Identify User Problems Specialist",
            goal="Execute identify_user_problems task accurately",
            backstory="You are a specialized worker focused on Lists specific user problems or pain points that the product will address.",
            verbose=True
        )



    @task
    def identify_user_problems_task(self):
        """Task for identify_user_problems."""
        agent = self.identify_user_problems_agent()
        return Task(
            description="""Using {extract_product_name_output}, {determine_target_users_output}, Lists specific user problems or pain points that the product will address.""",
            agent=agent,
            expected_output="""{
    user_problems: list of strs  # List of the user problems or pain points the product addresses.
}""",
            output_pydantic=identify_user_problems_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.identify_user_problems_agent()],
            tasks=[self.identify_user_problems_task()],
            verbose=True
        )

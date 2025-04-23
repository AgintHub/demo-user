from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import determine_target_users_output

@CrewBase
class determine_target_users_crew:
    """Crew for determine_target_users operations."""


    @agent
    def determine_target_users_agent(self):
        return Agent(
            role="Determine Target Users Specialist",
            goal="Execute determine_target_users task accurately",
            backstory="You are a specialized worker focused on Identifies the primary intended users or user segments for the product.",
            verbose=True
        )



    @task
    def determine_target_users_task(self):
        """Task for determine_target_users."""
        agent = self.determine_target_users_agent()
        return Task(
            description="""Using {extract_product_name_output}, Identifies the primary intended users or user segments for the product.""",
            agent=agent,
            expected_output="""{
    target_user_segments: list of strs  # List of target user types or segments.
}""",
            output_pydantic=determine_target_users_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.determine_target_users_agent()],
            tasks=[self.determine_target_users_task()],
            verbose=True
        )

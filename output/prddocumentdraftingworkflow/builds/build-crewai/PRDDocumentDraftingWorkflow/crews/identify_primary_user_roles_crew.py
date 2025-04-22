from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import identify_primary_user_roles_output

@CrewBase
class identify_primary_user_roles_crew:
    """Crew for identify_primary_user_roles operations."""


    @agent
    def identify_primary_user_roles_agent(self):
        return Agent(
            role="Identify Primary User Roles Specialist",
            goal="""Execute identify_primary_user_roles task accurately.
PRD Requirements:
""",
            backstory="You are a specialized worker focused on Extract the main user roles or personas directly involved with the product based on the requirements.",
            verbose=True
        )



    @task
    def identify_primary_user_roles_task(self):
        """Task for identify_primary_user_roles."""
        agent = self.identify_primary_user_roles_agent()
        return Task(
            description="""Using {input}, Extract the main user roles or personas directly involved with the product based on the requirements.""",
            agent=agent,
            expected_output="""{
    user_role_names: list of strs  # List of primary user role or persona names directly involved with the product.
    user_role_descriptions: list of strs  # List of concise one-sentence descriptions for each user role, matched by index to user_role_names.
}""",
            output_pydantic=identify_primary_user_roles_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.identify_primary_user_roles_agent()],
            tasks=[self.identify_primary_user_roles_task()],
            verbose=True
        )

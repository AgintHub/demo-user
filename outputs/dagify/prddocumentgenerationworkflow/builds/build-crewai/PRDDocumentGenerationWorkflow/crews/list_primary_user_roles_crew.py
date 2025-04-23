from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import list_primary_user_roles_output

@CrewBase
class list_primary_user_roles_crew:
    """Crew for list_primary_user_roles operations."""


    @agent
    def list_primary_user_roles_agent(self):
        return Agent(
            role="List Primary User Roles Specialist",
            goal="Execute list_primary_user_roles task accurately",
            backstory="You are a specialized worker focused on Determine all primary user roles or personas that will interact with the workflow.",
            verbose=True
        )



    @task
    def list_primary_user_roles_task(self):
        """Task for list_primary_user_roles."""
        agent = self.list_primary_user_roles_agent()
        return Task(
            description="""Using {identify_core_objective_output}, Determine all primary user roles or personas that will interact with the workflow.""",
            agent=agent,
            expected_output="""{
    user_roles: list of strs  # List of primary user roles or personas interacting with the workflow.
}""",
            output_pydantic=list_primary_user_roles_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.list_primary_user_roles_agent()],
            tasks=[self.list_primary_user_roles_task()],
            verbose=True
        )

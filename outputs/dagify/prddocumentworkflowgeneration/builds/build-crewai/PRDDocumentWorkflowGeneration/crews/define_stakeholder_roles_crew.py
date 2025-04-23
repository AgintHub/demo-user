from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import define_stakeholder_roles_output

@CrewBase
class define_stakeholder_roles_crew:
    """Crew for define_stakeholder_roles operations."""


    @agent
    def define_stakeholder_roles_agent(self):
        return Agent(
            role="Define Stakeholder Roles Specialist",
            goal="Execute define_stakeholder_roles task accurately",
            backstory="You are a specialized worker focused on Identify and list all distinct user or stakeholder roles relevant to the workflow.",
            verbose=True
        )



    @task
    def define_stakeholder_roles_task(self):
        """Task for define_stakeholder_roles."""
        agent = self.define_stakeholder_roles_agent()
        return Task(
            description="""Using {extract_workflow_overview_output}, Identify and list all distinct user or stakeholder roles relevant to the workflow.""",
            agent=agent,
            expected_output="""{
    stakeholder_roles: list of strs  # List of unique user or stakeholder roles relevant to the workflow.
}""",
            output_pydantic=define_stakeholder_roles_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.define_stakeholder_roles_agent()],
            tasks=[self.define_stakeholder_roles_task()],
            verbose=True
        )

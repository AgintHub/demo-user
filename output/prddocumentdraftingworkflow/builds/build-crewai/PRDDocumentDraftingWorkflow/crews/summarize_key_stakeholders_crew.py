from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import summarize_key_stakeholders_output

@CrewBase
class summarize_key_stakeholders_crew:
    """Crew for summarize_key_stakeholders operations."""


    @agent
    def summarize_key_stakeholders_agent(self):
        return Agent(
            role="Summarize Key Stakeholders Specialist",
            goal="""Execute summarize_key_stakeholders task accurately.
PRD Requirements:
""",
            backstory="You are a specialized worker focused on Identify and summarize the interest and influence of key project stakeholders.",
            verbose=True
        )



    @task
    def summarize_key_stakeholders_task(self):
        """Task for summarize_key_stakeholders."""
        agent = self.summarize_key_stakeholders_agent()
        return Task(
            description="""Using {input}, Identify and summarize the interest and influence of key project stakeholders.""",
            agent=agent,
            expected_output="""{
    stakeholder_names: list of strs  # List of key stakeholder names.
    stakeholder_roles: list of strs  # List of brief descriptions of each stakeholder's role.
    stakeholder_interests: list of strs  # List of brief descriptions of each stakeholder's interest in the project outcome.
}""",
            output_pydantic=summarize_key_stakeholders_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.summarize_key_stakeholders_agent()],
            tasks=[self.summarize_key_stakeholders_task()],
            verbose=True
        )

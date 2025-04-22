from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import define_user_journeys_for_each_role_output

@CrewBase
class define_user_journeys_for_each_role_crew:
    """Crew for define_user_journeys_for_each_role operations."""


    @agent
    def define_user_journeys_for_each_role_agent(self):
        return Agent(
            role="Define User Journeys For Each Role Specialist",
            goal="""Execute define_user_journeys_for_each_role task accurately.
PRD Requirements:
""",
            backstory="You are a specialized worker focused on For each identified user role, provide a concise narrative of the main user journey(s) within the workflow.",
            verbose=True
        )



    @task
    def define_user_journeys_for_each_role_task(self):
        """Task for define_user_journeys_for_each_role."""
        agent = self.define_user_journeys_for_each_role_agent()
        return Task(
            description="""Using {identify_primary_user_roles_output}, {extract_core_product_features_output}, For each identified user role, provide a concise narrative of the main user journey(s) within the workflow.""",
            agent=agent,
            expected_output="""{
    user_role_names: list of strs  # List of user role or persona names for whom journeys are defined.
    user_role_descriptions: list of strs  # List of brief descriptions for each user role, aligned by index with user_role_names.
    user_journey_titles: list of strs  # List of main user journey titles or names for each user role, matching the order of user_role_names.
    user_journey_steps: list of strs  # List of step-by-step narratives for each user journey, one item per user role, matching the order of user_role_names. Each step-by-step narrative is a single string with steps sequenced, separated by a delimiter or in formatted text.
}""",
            output_pydantic=define_user_journeys_for_each_role_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.define_user_journeys_for_each_role_agent()],
            tasks=[self.define_user_journeys_for_each_role_task()],
            verbose=True
        )

from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import draft_prd_section_user_journeys_output

@CrewBase
class draft_prd_section_user_journeys_crew:
    """Crew for draft_prd_section_user_journeys operations."""


    @agent
    def draft_prd_section_user_journeys_agent(self):
        return Agent(
            role="Draft Prd Section User Journeys Specialist",
            goal="""Execute draft_prd_section_user_journeys task accurately.
PRD Requirements:
""",
            backstory="You are a specialized worker focused on Organize the user journeys as a distinct User Journeys section in the PRD.",
            verbose=True
        )



    @task
    def draft_prd_section_user_journeys_task(self):
        """Task for draft_prd_section_user_journeys."""
        agent = self.draft_prd_section_user_journeys_agent()
        return Task(
            description="""Using {define_user_journeys_for_each_role_output}, Organize the user journeys as a distinct User Journeys section in the PRD.""",
            agent=agent,
            expected_output="""{
    user_journey_section_heading: str  # Heading for the User Journeys section in the PRD.
    user_roles: list of strs  # List of user roles for which user journeys are documented.
    user_journey_titles: list of strs  # List of titles/names for each user journey, corresponding one-to-one with user_roles.
    user_journey_narratives: list of strs  # List of narrative descriptions for each user journey, corresponding one-to-one with user_roles.
    user_journey_step_lists: list of strs  # For each user journey, a string formatted step-by-step sequence describing the actions in that journey (bulleted or numbered).
}""",
            output_pydantic=draft_prd_section_user_journeys_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.draft_prd_section_user_journeys_agent()],
            tasks=[self.draft_prd_section_user_journeys_task()],
            verbose=True
        )

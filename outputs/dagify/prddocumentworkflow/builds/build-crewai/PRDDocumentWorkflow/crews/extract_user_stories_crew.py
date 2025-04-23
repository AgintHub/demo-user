from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import extract_user_stories_output

@CrewBase
class extract_user_stories_crew:
    """Crew for extract_user_stories operations."""


    @agent
    def extract_user_stories_agent(self):
        return Agent(
            role="Extract User Stories Specialist",
            goal="Execute extract_user_stories task accurately",
            backstory="You are a specialized worker focused on Drafts elemental user stories to capture desired end-user behaviors.",
            verbose=True
        )



    @task
    def extract_user_stories_task(self):
        """Task for extract_user_stories."""
        agent = self.extract_user_stories_agent()
        return Task(
            description="""Using {identify_user_problems_output}, Drafts elemental user stories to capture desired end-user behaviors.""",
            agent=agent,
            expected_output="""{
    user_stories: list of strs  # User stories covering key user needs, matching the order of input problems.
}""",
            output_pydantic=extract_user_stories_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.extract_user_stories_agent()],
            tasks=[self.extract_user_stories_task()],
            verbose=True
        )

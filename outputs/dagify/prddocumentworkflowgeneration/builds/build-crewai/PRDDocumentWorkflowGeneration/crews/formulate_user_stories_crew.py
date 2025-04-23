from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import formulate_user_stories_output

@CrewBase
class formulate_user_stories_crew:
    """Crew for formulate_user_stories operations."""


    @agent
    def formulate_user_stories_agent(self):
        return Agent(
            role="Formulate User Stories Specialist",
            goal="Execute formulate_user_stories task accurately",
            backstory="You are a specialized worker focused on Write user stories for each core feature from the perspective of each appropriate stakeholder.",
            verbose=True
        )



    @task
    def formulate_user_stories_task(self):
        """Task for formulate_user_stories."""
        agent = self.formulate_user_stories_agent()
        return Task(
            description="""Using {identify_core_features_output}, {define_stakeholder_roles_output}, Write user stories for each core feature from the perspective of each appropriate stakeholder.""",
            agent=agent,
            expected_output="""{
    user_stories: list of strs  # User stories, each following the format: 'As a [role], I want to [action] so that [goal]'.
}""",
            output_pydantic=formulate_user_stories_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.formulate_user_stories_agent()],
            tasks=[self.formulate_user_stories_task()],
            verbose=True
        )

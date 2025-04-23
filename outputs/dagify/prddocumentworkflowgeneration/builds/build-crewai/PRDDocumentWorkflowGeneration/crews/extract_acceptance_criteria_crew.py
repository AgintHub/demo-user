from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import extract_acceptance_criteria_output

@CrewBase
class extract_acceptance_criteria_crew:
    """Crew for extract_acceptance_criteria operations."""


    @agent
    def extract_acceptance_criteria_agent(self):
        return Agent(
            role="Extract Acceptance Criteria Specialist",
            goal="Execute extract_acceptance_criteria task accurately",
            backstory="You are a specialized worker focused on For each user story, specify clear, testable acceptance criteria.",
            verbose=True
        )



    @task
    def extract_acceptance_criteria_task(self):
        """Task for extract_acceptance_criteria."""
        agent = self.extract_acceptance_criteria_agent()
        return Task(
            description="""Using {formulate_user_stories_output}, For each user story, specify clear, testable acceptance criteria.""",
            agent=agent,
            expected_output="""{
    acceptance_criteria_texts: list of strs  # All acceptance criteria, grouped by order to associated user stories.
    user_story_indices: list of ints  # Index of the user story each set of acceptance criteria belongs to (same order as acceptance_criteria_texts).
}""",
            output_pydantic=extract_acceptance_criteria_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.extract_acceptance_criteria_agent()],
            tasks=[self.extract_acceptance_criteria_task()],
            verbose=True
        )

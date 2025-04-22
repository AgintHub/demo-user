from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import draft_prd_section_features_output

@CrewBase
class draft_prd_section_features_crew:
    """Crew for draft_prd_section_features operations."""


    @agent
    def draft_prd_section_features_agent(self):
        return Agent(
            role="Draft Prd Section Features Specialist",
            goal="""Execute draft_prd_section_features task accurately.
PRD Requirements:
""",
            backstory="You are a specialized worker focused on Compile the core features into the PRD Features section.",
            verbose=True
        )



    @task
    def draft_prd_section_features_task(self):
        """Task for draft_prd_section_features."""
        agent = self.draft_prd_section_features_agent()
        return Task(
            description="""Using {extract_core_product_features_output}, Compile the core features into the PRD Features section.""",
            agent=agent,
            expected_output="""{
    features_section_title: str  # The heading/title for the PRD Features section.
    feature_list: list of strs  # A list of core product features, each stated concisely suitable for inclusion in the PRD.
}""",
            output_pydantic=draft_prd_section_features_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.draft_prd_section_features_agent()],
            tasks=[self.draft_prd_section_features_task()],
            verbose=True
        )

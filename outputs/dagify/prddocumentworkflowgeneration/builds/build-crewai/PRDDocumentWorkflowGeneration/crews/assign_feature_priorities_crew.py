from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import assign_feature_priorities_output

@CrewBase
class assign_feature_priorities_crew:
    """Crew for assign_feature_priorities operations."""


    @agent
    def assign_feature_priorities_agent(self):
        return Agent(
            role="Assign Feature Priorities Specialist",
            goal="Execute assign_feature_priorities task accurately",
            backstory="You are a specialized worker focused on Assign a relative priority to each core feature based on its necessity and impact.",
            verbose=True
        )



    @task
    def assign_feature_priorities_task(self):
        """Task for assign_feature_priorities."""
        agent = self.assign_feature_priorities_agent()
        return Task(
            description="""Using {identify_core_features_output}, Assign a relative priority to each core feature based on its necessity and impact.""",
            agent=agent,
            expected_output="""{
    core_feature_priorities: list of strs  # Relative priority label ('Must Have', 'Should Have', 'Nice to Have') for each feature (same order as core_feature_names).
}""",
            output_pydantic=assign_feature_priorities_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.assign_feature_priorities_agent()],
            tasks=[self.assign_feature_priorities_task()],
            verbose=True
        )

from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import classify_feature_priorities_output

@CrewBase
class classify_feature_priorities_crew:
    """Crew for classify_feature_priorities operations."""


    @agent
    def classify_feature_priorities_agent(self):
        return Agent(
            role="Classify Feature Priorities Specialist",
            goal="Execute classify_feature_priorities task accurately",
            backstory="You are a specialized worker focused on Classifies each feature requirement as must-have or nice-to-have.",
            verbose=True
        )



    @task
    def classify_feature_priorities_task(self):
        """Task for classify_feature_priorities."""
        agent = self.classify_feature_priorities_agent()
        return Task(
            description="""Using {extract_feature_requirements_output}, Classifies each feature requirement as must-have or nice-to-have.""",
            agent=agent,
            expected_output="""{
    is_must_have: list of bools  # Must-have (true) or nice-to-have (false) label for each feature requirement, in the same order.
}""",
            output_pydantic=classify_feature_priorities_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.classify_feature_priorities_agent()],
            tasks=[self.classify_feature_priorities_task()],
            verbose=True
        )

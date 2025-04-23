from typing import Dict, Any, List, Optional
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from .models import extract_product_context_output

@CrewBase
class extract_product_context_crew:
    """Crew for extract_product_context operations."""


    @agent
    def extract_product_context_agent(self):
        return Agent(
            role="Extract Product Context Specialist",
            goal="Execute extract_product_context task accurately",
            backstory="You are a specialized worker focused on Extract and summarize the core product or feature context from workflow requirements.",
            verbose=True
        )



    @task
    def extract_product_context_task(self):
        """Task for extract_product_context."""
        agent = self.extract_product_context_agent()
        return Task(
            description="""Using {input}, Extract and summarize the core product or feature context from workflow requirements.""",
            agent=agent,
            expected_output="""{
    product_name: str  # The name or title of the product or feature being described.
    summary: str  # A concise summary of what is being built, capturing the high-level product or feature context.
    primary_purpose: str  # A single sentence stating the core purpose or intent of the product or feature.
    key_features: list of strs  # A list of the most important features or elements that define the product's scope, expressed broadly (not as requirements).
}""",
            output_pydantic=extract_product_context_output
        )


    @crew
    # @traceable
    def crew(self):
        """Create the crew instance."""
        return Crew(
            agents=[self.extract_product_context_agent()],
            tasks=[self.extract_product_context_task()],
            verbose=True
        )

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.75,
)

@CrewBase
class HypothesisCrew:
    """FAQ Hypothesis Crew"""
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def faq_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["faq_generator"],
            llm=llm,
        )

    @task
    def generate_faqs(self) -> Task:
        return Task(
            config=self.tasks_config["generate_faqs"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the FAQ Crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
        )

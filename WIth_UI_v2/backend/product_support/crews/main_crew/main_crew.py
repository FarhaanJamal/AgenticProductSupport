from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os
import google.generativeai as genai
from dotenv import load_dotenv
from product_support.tools.image_describer_tool import ImageDescriberTool
from product_support.tools.other_tools import other_tools

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.5,
)

pdf_tool, web_search_tool = other_tools()


@CrewBase
class MainCrew:
    """MainCrew crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def image_describer(self) -> Agent:
        return Agent(
            config=self.agents_config["image_describer"],
            llm=llm,
            tools=[ImageDescriberTool()],
        )

    @agent
    def unified_reflection_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["unified_reflection_agent"],
            llm=llm,
            tools=[pdf_tool, web_search_tool],
        )

    @task
    def describe_image(self) -> Task:
        return Task(
            config=self.tasks_config["describe_image"],
        )

    @task
    def unified_reflection_task(self) -> Task:
        return Task(
            config=self.tasks_config["unified_reflection_task"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MainCrew crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
        )

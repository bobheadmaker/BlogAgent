# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 11:04:45 2025

@author: Bob Head
"""

from crewai import Agent, Task, Crew, LLM
from langchain_community.tools import DuckDuckGoSearchRun

#ollama_llm = Ollama(model="llama2")

ollama_llm = LLM(
        base_url= "http://127.0.0.1:11434/v1",
        model= "openai/openhermes")

#from crewai_tools import tool
from crewai.tools import tool
@tool("Duck_Duck_Go_Search")
def ddgsearch(question: str) -> str:
    """Clear description for what this tool is useful for, your agent will need this information to use it."""
    # Function logic here
    return DuckDuckGoSearchRun().run(question)


blog_topic = "AI agents in 2025"

# setup first agent as researcher

researcher = Agent(
  role='Researcher',
  goal='Search the internet about {blog_topic}',
  backstory="""
  You are a researcher. Using the information in the task, you find out some of the most popular facts about the topic along with some of the trending aspects.
  You provide a lot of information thereby allowing a choice in the content selected for the final blog
  """,
  verbose=True,            # want to see the thinking behind
  allow_delegation=False,  # Not allowed to ask any of the other roles
  # tools=[DuckDuckGoSearchRun()],
  tools=[ddgsearch],        # Is allowed to use the following tools to conduct research
  llm = ollama_llm
)

#setup second agent as techincal blogger

writer = Agent(
  role='Technical blogger',
  goal='Craft compelling content on a set of information provided by the researcher.',
  backstory="""You are a technical blogger known for your simple yet informative way of explaining. 
  You transform complex concepts into compelling narratives.""",
  verbose=True,            # want to see the thinking behind
  allow_delegation=True,   # can ask the "researcher" for more information
  llm=ollama_llm           # using the local model
)

# lets define the tasks now

task1 = Task(
  agent=researcher,
  description=blog_topic,
  expected_output="A complete analysis of the {blog_topic}, presented as a concise article.",
)

task2 = Task(
  agent=writer,
  description="""Using the insights provided, develop an engaging blog
  post that highlights the most significant and trending facts information on AI agents in 2025
  Your post should be informative, catering to a tech-savvy audience.
  Make it sound simple, and avoid complex words so it doesn't sound AI generated.""",
  expected_output="""A article containing a minimum of 2 paragraphs. contains no more than 600 words but no less than 100 words.
  Use bullet points for concise view of the blog. 
  The final output will not contain any extra fluff like "Paragraph 1:" or any action the writer should do.""",
)

# initialize crew to run the tasks

crew = Crew(
  agents=[researcher, writer],
  tasks=[task1, task2],
  verbose=1, # You can set it to 1 or 2 for different logging levels
)

result = crew.kickoff()
print(result)


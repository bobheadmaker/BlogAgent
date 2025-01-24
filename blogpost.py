# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 19:49:11 2025

@author: Bob Head
"""

import os
from crewai import Agent, Task, Crew

os.environ["OPENAI_API_KEY"] = "sk-proj"
os.environ["OPENAI_MODEL_NAME"] = "gpt-4"


blog_topic = "AI agents in 2025"

# setup first agent as researcher

researcher = Agent(
  role='Researcher',
  goal='Search the internet about {blog_topic}',
  backstory="""
  You are a researcher. Using the information in the task, you find out some of the most popular facts about the topic along with some of the trending aspects.
  You provide a lot of information thereby allowing a choice in the content selected for the final blog
  """,
  verbose=True            # want to see the thinking behind
)

#setup second agent as techincal blogger

writer = Agent(
  role='Technical blogger',
  goal='Craft compelling content on a set of information provided by the researcher.',
  backstory="""You are a technical blogger known for your simple yet informative way of explaining. 
  You transform complex concepts into compelling narratives.""",
  verbose=True            # want to see the thinking behind
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
  expected_output="""A article containing a minimum of 3 paragraphs. contains no more than 800 words but no less than 200 words.
  Use bullet points for concise view of the blog. 
  The final output will not contain any extra fluff like "Paragraph 1:" or any action the writer should do.""",
)


crew = Crew(
    agents=[researcher, writer],
    tasks=[task1,task2],
    verbose=1
)

result = crew.kickoff()

print("############")
print(result)

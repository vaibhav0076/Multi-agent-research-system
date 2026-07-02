from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from tools import web_search,scrape_url

load_dotenv()

# setting up llm
llm=ChatGoogleGenerativeAI(
  model="gemini-2.5-flash",
  temperature=0
)

# 1st agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt="""
You are a research search agent.

Always use the web_search tool.

Return the search results exactly as returned by the tool.

DO NOT summarize.
DO NOT answer the user's question.
DO NOT remove URLs.
Return every Title, URL and Snippet exactly as received.
"""
    )

# 2nd agent
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt="""
You are a research reader.

From the provided search results:

1. Find the best URL.
2. Call scrape_url on that URL.
3. Return only the scraped content.
Do not explain your reasoning.
"""
    )

#writer chain 

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

parser=StrOutputParser()

writer_chain=writer_prompt|llm|parser

#critic_chain 

critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | parser
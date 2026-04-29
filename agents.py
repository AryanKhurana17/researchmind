from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search , scrape_url 
from dotenv import load_dotenv

load_dotenv()

#model setup 
llm = ChatOllama(model="mistral", temperature=0, num_ctx=8192, num_predict=4096)


#1st agent 
def build_search_agent():
    return create_agent(
        model = llm,
        tools= [web_search]
    )

#2nd agent 

def build_reader_agent():
    return create_agent(
        model = llm,
        tools = [scrape_url]
    )


#writer chain 
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured, and highly detailed analytical reports. Never treat the topic as hypothetical unless explicitly stated. Treat current events as real and factual. Always write long, comprehensive reports."),
    ("human", """Write a highly detailed, in-depth, and comprehensive research report on the topic below. The report must be at least 1500 words.

Topic: {topic}

Research Gathered:
{research}

Structure the report with ALL of the following sections (do not skip any):

1. Executive Summary (3-4 paragraphs overview)
2. Background & Context (Historical context and why this topic matters now)
3. In-Depth Analysis (Include ALL specific quantitative data, statistics, numbers, and direct quotes from the research. Break into multiple sub-sections if needed.)
4. Key Stakeholders & Their Perspectives (Who is affected and how)
5. Strategic Scenarios & Broad Impacts (Short-term vs long-term effects)
6. Potential Mitigation Strategies & Recommendations (Actionable steps to reduce negative impacts)
7. Conclusion & Future Outlook
8. Sources (List ALL URLs found in the research provided)

Be extremely detailed, analytical, factual, and professional. Expand on each point thoroughly with multiple paragraphs per section. Use the actual data from the research - do not generalize."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

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

critic_chain = critic_prompt | llm | StrOutputParser()

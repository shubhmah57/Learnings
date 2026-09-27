import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from tavily import TavilyClient
from agents import set_default_openai_client,set_tracing_disabled, Agent, function_tool, ModelSettings, Runner
import asyncio
from pathlib import Path
import sys

## We have 3 agents planner, search and report agent. Planner returns structured output according to query what should be searched, search performs actual search on internet. 
## Report agent creates report in markdown format from the search results.



QUERY = "EATHONAL BLENDING IN INDIA"
HOW_MANY_SEARCHES = 5
MODEL = "gpt-4o-mini"
settings = ModelSettings(tool_choice="required", max_tokens= 10000)


PLANNER_AGENT_INSTRUCTIONS = """
You are a research assistant. Given a user query, come up with a set of web searches
to perform to best answer the query. Output 5 terms to query for.
"""

SEARCH_AGENT_INSTRUCTIONS = """
You are a research assistant. Given a search term, you search the web for that term and 
produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 words.
Capture the main points and be succinct. Reply only with the summary.
"""

WRITER_AGENT_INSTRUCTIONS = """
You are a senior researcher tasked with writing a cohesive report for a research query.
You will be provided with the original query, and some research.
Generate a comprehensive report based on the research and the query.
The final output should be in markdown format, and it should be lengthy and detailed. Aim 
for 5-10 pages of content, at least 1000 words.
"""

class WebSearchAgents:
    def __init__(self):
        load_dotenv(override=True)
        open_router_key = os.getenv('OPEN_ROUTER_API_KEY')
        open_router_url = os.getenv('OPEN_ROUTER_BASE_URL')
        openai = AsyncOpenAI(api_key=open_router_key, base_url=open_router_url)
        set_default_openai_client(openai, use_for_tracing=False)
        set_tracing_disabled(True)


class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important for the query.")
    query: str = Field(description="The Actual Search Query to be used.")

class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of websearches to be performed to best answer the query.")

class ReportData(BaseModel):
    short_summary: str = Field(description="A short 2-3 sentence summary of the findings.")
    markdown_report: str = Field(description="The final report")
    follow_up_questions: list[str] = Field(description="Suggested topics to research further")

@function_tool
def tavily_web_search(query: str) -> str:
    """
    Search the web for the given query using Tavily.
    Use this to get accurate, clean, and up-to-date information from the web.
    """
    api_key = os.getenv('TAVILY_API_KEY')
    if not api_key:
         return "Error: TAVILY_API_KEY is missing from environment variables."

    try:
        client = TavilyClient(api_key=api_key)
        # max_results limits token usage, search_depth='basic' keeps it fast
        response = client.search(query=query, search_depth="basic", max_results=3)
        
        results = []
        for result in response.get("results", []):
            results.append(
                f"Title: {result.get('title')}\n"
                f"Content: {result.get('content')}\n"
                f"Source: {result.get('url')}"
            )
            
        return "\n\n".join(results) or "No results found."
        
    except Exception as e:
        return f"Error during Tavily search: {e}"
    


planner_agent = Agent(name="Planner Agent", instructions=PLANNER_AGENT_INSTRUCTIONS, model=MODEL, output_type = WebSearchPlan, model_settings= ModelSettings(max_tokens=10000))
search_agent = Agent(name = "Search Agent", instructions=SEARCH_AGENT_INSTRUCTIONS, model=MODEL, tools=[tavily_web_search], model_settings=settings)
writer_agent = Agent(name = "Writer Agent", instructions=WRITER_AGENT_INSTRUCTIONS,model=MODEL,output_type= ReportData,model_settings=ModelSettings(max_tokens=10000))

async def run_searches(query: str):
    print("Planing Searches....")
    result = await Runner.run(planner_agent, f"Query:{query}")
    searches = result.final_output.searches
    print(f"Will perform {len(searches)} searches")
    #[print(item) for item in searches]
    tasks = [search(item) for item in searches] # provides a coroutine of objects because search method is async
    results = await asyncio.gather(*tasks) # it concurrently executes those coroutintes.
    print("Finished Searching")
    return results


async def search(item : WebSearchItem):
    input_message = f"Search term: {item.query}\n Reason for searching: {item.reason}"
    result = await Runner.run(search_agent,input_message)
    return result.final_output

async def write_report(query: str, search_results: list[str]):
    print("Thinking about report...")
    input_message = f"Original query: {query}\nSummarized search results: {search_results}"
    result = await Runner.run(writer_agent, input_message)
    print("Finished writing report")
    return result.final_output

async def executeAgents():
    search_results = await run_searches(QUERY)
    report_data: ReportData = await write_report(QUERY, search_results)
    print("\n--- FINAL REPORT ---")
    #print(report_data.markdown_report)
    return report_data.markdown_report

async def run(query: str):
    search_results = await run_searches(query)
    report_data: ReportData = await write_report(query, search_results)
    print("\n--- FINAL REPORT ---")
    #print(report_data.markdown_report)
    return report_data.markdown_report

if __name__ == "__main__":
    object = WebSearchAgents()
    #asyncio.run(executeAgents())
    #result = asyncio.run(run_searches(QUERY))
    #report_data: ReportData = asyncio.run(write_report(QUERY,result))
    #print(report_data.markdown_report)
    #print(result)
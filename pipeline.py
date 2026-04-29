from agents import build_reader_agent , build_search_agent , writer_chain , critic_chain
from tools import scrape_url
from rich import print
def run_research_pipeline(topic : str) -> dict:

    state = {}

    #search agent working 
    print("\n"+" ="*50)
    print("step 1 - search agent is working ...")
    print("="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages" : [("system", "You are a web searcher. You MUST use the 'web_search' tool to look up the user's query. DO NOT answer from your own memory. DO NOT hallucinate search results. You MUST include the exact URLs and snippets returned by the tool in your final response."),
                      ("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    tool_messages = [m.content for m in search_result['messages'] if m.type == 'tool']
    if tool_messages:
        state["search_results"] = "\n\n".join(tool_messages)
    else:
        state["search_results"] = search_result['messages'][-1].content

    print("\n search result ",state['search_results'])

    #step 2 - reader agent 
    print("\n"+" ="*50)
    print("step 2 - Reader agent is scraping top resources ...")
    print("="*50)

    import re
    # Extract all URLs from search results
    urls = re.findall(r'https?://[^\s\n,]+', state.get("search_results", ""))
    seen = set()
    unique_urls = []
    for u in urls:
        clean = u.rstrip('.,;:)]\'"')
        if clean not in seen:
            seen.add(clean)
            unique_urls.append(clean)

    scraped_parts = []
    for url in unique_urls[:7]:  # Scrape top 7 URLs
        try:
            content = scrape_url.invoke(url)
            if content and not content.startswith("Could not scrape"):
                scraped_parts.append(f"--- Source: {url} ---\n{content}")
        except Exception:
            pass

    if scraped_parts:
        state['scraped_content'] = "\n\n".join(scraped_parts)
    else:
        state['scraped_content'] = "No content could be scraped from the URLs."

    print("\nscraped content: \n", state['scraped_content'])

    #step 3 - writer chain 

    print("\n"+" ="*50)
    print("step 3 - Writer is drafting the report ...")
    print("="*50)

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })

    print("\n Final Report\n",state['report'])

    #critic report 

    print("\n"+" ="*50)
    print("step 4 - critic is reviewing the report ")
    print("="*50)

    state["feedback"] = critic_chain.invoke({
        "report":state['report']
    })

    print("\n critic report \n", state['feedback'])

    return state



if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)


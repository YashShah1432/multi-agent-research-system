from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

def run_research_pipeline(topic: str, progress_callback=None) -> dict:
    state = {}

    #Search Agent
    if progress_callback:
        progress_callback("Search Agent", "running")

    search_agent = build_search_agent()
    search_result = search_agent.invoke({"messages": [{"role": "user", "content": f"Find recent, reliable and detailed information about: {topic}"}]})

    state["search_result"] = search_result["messages"][-1].content

    if progress_callback:
        progress_callback("Search Agent", "completed")


    #Reader Agent
    if progress_callback:
        progress_callback("Reader Agent", "running")

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({"messages": [{"role": "user", "content": f"Research topic: {topic}\n\nSearch Agent results: {search_result}\n\nExtract all relevant URLs from the Search Agent results, scrape each webpage using the available web scraping tool, and return the page titles, source URLs, and extracted content in a structured format for the Writer Agent. If a URL fails, continue processing the remaining URLs."}]})

    state["reader_result"] = reader_result["messages"][-1].content

    if progress_callback:
        progress_callback("Reader Agent", "completed")


    #Writer Agent
    if progress_callback:
        progress_callback("Writer Agent", "running")

    research_combined = (
        f"Search Result: \n{state["search_result"]}\n\n"
        f"Scrapped Content: \n{state["reader_result"]}\n\n"
    )

    writer_result = writer_chain.invoke({
        "research_topic": topic,
        "scraped_content": research_combined
        })

    state["writer_result"] = writer_result

    if progress_callback:
        progress_callback("Writer Agent", "completed")
        

    #Critic Agent
    if progress_callback:
        progress_callback("Critic Agent", "running")

    critic_result = critic_chain.invoke({
        "research_topic" : topic,
        "scraped_content" : reader_result,
        "writer_report": writer_result
        })

    state["critic_result"] = critic_result

    if progress_callback:
        progress_callback("Critic Agent", "completed")

    return state


if __name__ == "__main__":
    topic = input("Enter your topic for research: ")
    run_research_pipeline(topic)
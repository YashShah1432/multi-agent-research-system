from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

def run_research_pipeline(topic: str) -> dict:
    state = {}

    #Search Agent
    print("\n"+"="*50)
    print("step 1 - Search Agent is working")
    print("="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({"messages": [{"role": "user", "content": f"Find recent, reliable and detailed information about: {topic}"}]})

    state["search_result"] = search_result["messages"][-1].content

    print(f"\nSearch Result : \n{state["search_result"]}")

    #Reader Agent
    print("\n"+"="*50)
    print("step 2 - Reader Agent is scraping")
    print("="*50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({"messages": [{"role": "user", "content": f"Research topic: {topic}\n\nSearch Agent results: {search_result}\n\nExtract all relevant URLs from the Search Agent results, scrape each webpage using the available web scraping tool, and return the page titles, source URLs, and extracted content in a structured format for the Writer Agent. If a URL fails, continue processing the remaining URLs."}]})

    state["reader_result"] = reader_result["messages"][-1].content

    print(f"\nReader Result : \n{state["reader_result"]}")

    #Writer Agent
    print("\n"+"="*50)
    print("step 3 - Writer Agent is generating report")
    print("="*50)

    research_combined = (
        f"Search Result: \n{state["search_result"]}\n\n"
        f"Scrapped Content: \n{state["reader_result"]}\n\n"
    )

    writer_result = writer_chain.invoke({
        "research_topic": topic,
        "scraped_content": research_combined
        })

    state["writer_result"] = writer_result

    print(f"\nWriter Agent : \n{state["writer_result"]}")

    #Critic Agent
    print("\n"+"="*50)
    print("step 4 - Critic Agent is analysing and scoring the report")
    print("="*50)

    critic_result = critic_chain.invoke({
        "research_topic" : topic,
        "scraped_content" : reader_result,
        "writer_report": writer_result
        })

    state["critic_result"] = critic_result

    print(f"\nCritic Agent : \n{state["critic_result"]}")

    return state

if __name__ == "__main__":
    topic = input("Enter your topic for research: ")
    run_research_pipeline(topic)

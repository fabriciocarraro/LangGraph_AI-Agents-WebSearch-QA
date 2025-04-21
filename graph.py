import os
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langgraph.graph import START, END, StateGraph
from langgraph.types import Send
from tavily import TavilyClient

from schemas import *
from prompts import *

import streamlit as st

from dotenv import load_dotenv
load_dotenv()

base_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
    )

writer_llm = ChatOpenAI(
    model="gpt-4o",
    temperature=1.0,
    api_key=os.getenv("OPENAI_API_KEY")
    )

# Nodes
def build_first_queries(state: ReportState):
    class QueryList(BaseModel):
        queries: List[str]

    user_input = state.user_input
    
    prompt = build_queries.format(user_input=user_input)
    query_llm = base_llm.with_structured_output(QueryList)
    result = query_llm.invoke(prompt)
    
    return {"queries": result.queries}

def spawn_researchers(state: ReportState):
    return [Send("single_search", query) for query in state.queries]

def single_search(query: str):
    query_results = []
    tavily_client = TavilyClient()

    results = tavily_client.search(query, max_results=1, include_raw_content=False)
    url = results["results"][0]["url"]
    url_extraction = tavily_client.extract(url)

    if len(url_extraction["results"]) > 0:
        raw_content = url_extraction["results"][0]["raw_content"]
        prompt = resume_search.format(user_input=user_input,
                                      search_query=query,
                                      search_results=raw_content)
        
        llm_response = base_llm.invoke(prompt)

        query_results = QueryResult(title=results["results"][0]["title"],
                                    url = url,
                                    resume = llm_response.content)
        
    return {"query_results": [query_results]}
    

def final_writer(state: ReportState):
    search_results = ""
    references = []

    for i, result in enumerate(state.query_results):
        search_results += f"[{i+1}]\n\n"
        search_results += f"Title: {result.title}\n"
        search_results += f"URL: {result.url}\n"
        search_results += f"Content: {result.resume}\n"
        search_results += f"============================\n\n"

        references.append(f"[{i+1}] [{result.title}]({result.url})")

    prompt = build_final_response.format(user_input=user_input,
                                         search_results=search_results)
    
    llm_response = writer_llm.invoke(prompt)

    return {"final_response": llm_response.content, "references": references}

# Edges
builder = StateGraph(ReportState)

builder.add_node("build_first_queries", build_first_queries)
builder.add_node("single_search", single_search)
builder.add_node("final_writer", final_writer)

builder.add_edge(START, "build_first_queries")
builder.add_conditional_edges("build_first_queries",
                              spawn_researchers,
                              ["single_search"])
builder.add_edge("single_search", "final_writer")
builder.add_edge("final_writer", END)

graph = builder.compile()


if __name__ == "__main__":
    from IPython.display import Image, display
    display(Image(graph.get_graph().draw_mermaid_png()))

    st.title("Perplexity Agent")
    user_input = st.text_input("What's your question?",
                               value = "Explain the complete process of how to develop an LLM from scratch")
    
    if st.button("Search"):
        with st.status("Generating answer"):
            response = graph.invoke({"user_input": user_input})
            st.write(response)

        st.write(response["final_response"])
        st.write("### References:")
        for ref in response["references"]:
            st.write(ref)
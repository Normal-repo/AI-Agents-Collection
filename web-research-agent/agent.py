import argparse

from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from typing import Annotated, TypedDict
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from langchain_tavily import TavilySearch
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
load_dotenv()

MODEL = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.4,
)


sys_mess="""You are an expert research analyst.

Your task is to analyze the provided search results and produce a concise, well-structured research report. Base your conclusions only on the information provided. If the sources disagree, clearly identify the conflicting viewpoints instead of choosing one.

Structure your response as follows:

# Executive Summary
Provide a 2–4 paragraph overview of the topic and the most important conclusions.

# Key Findings
- List the most important facts as bullet points.
- Group related findings together where appropriate.
- Highlight trends, statistics, dates, and notable insights.

# Detailed Analysis
Explain the findings in more depth, including context, comparisons, advantages, disadvantages, and any important limitations.

# Sources
For each source, include:
- Title
- URL
- One-sentence description of what information it contributed.

Guidelines:
- Do not fabricate information.
- Do not repeat the same information from multiple sources.
- Prioritize high-confidence information supported by multiple sources.
- Clearly state when evidence is limited or uncertain.
- Use professional, neutral language.
- Format the report in clean Markdown."""






class ResearchState(TypedDict):
    messages: Annotated[list, add_messages]
    query: str
    search_result: list[dict]
    report: str



def search_web(state:ResearchState) -> ResearchState:
    tool = TavilySearch(max_results=5)
    raw_result=tool.invoke(state['query'])

    if isinstance(raw_result,dict):
        results=raw_result.get("results",[])
    elif isinstance(raw_result,list):
        results=raw_result
    else:
        results=[]

    return {"search_result": results}

def model_review(state:ResearchState) -> ResearchState:

    

    results_text = ''

    for r in state.get("search_result", []):
        results_text+=(
            f"Source: {r.get('url', 'N/A')}\n"
            f"Title: {r.get('title','N/A')}\n"
            f"Content: {r.get('content', '')[:800]}\n\n"
        )

    message = [
        SystemMessage(content=sys_mess),
        HumanMessage(content=f"Research query: {state.get('query','')}\n\nSearch results:\n{results_text}"),
    ]

    res = MODEL.invoke(message)

    # Append the model response to the messages list (preserve prior messages)
    prev_messages = state.get("messages", []) or []
    new_messages = [*prev_messages, res]

    return {"report": res.content, "messages": new_messages}



def graph() -> StateGraph:

    g = StateGraph(ResearchState)

    g.add_node("search_web",search_web)
    g.add_node("model_review",model_review)
    g.set_entry_point("search_web")
    g.add_edge("search_web","model_review")
    g.add_edge("model_review",END)

    return g.compile()



def main():
    parser = argparse.ArgumentParser(description="Web Research Agent")
    parser.add_argument("--query", default="latest advances in AI agents 2024", help="Research query")
    args = parser.parse_args()

    print(f"\n🔍 Researching: {args.query}\n")

    agent = graph()
    result = agent.invoke({"query": args.query, "messages": [], "search_result": [], "report": ""})

    print("=" * 50)
    print("📄 RESEARCH REPORT")
    print("=" * 50)
    print(result["report"])


if __name__ == "__main__":
    main()
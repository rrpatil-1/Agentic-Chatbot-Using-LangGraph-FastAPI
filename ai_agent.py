import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
# from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

#load environment variables from .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Steup llm
# groq_llm =  ChatGroq(api_key=GROQ_API_KEY, model="llama-3.3-70b-versatile")



#setup agent with search tool functionality



def get_response_from_ai(llm_id,query,allow_search,system_prompt,provider):

    if provider.lower() == "groq":
        llm = ChatGroq(api_key=GROQ_API_KEY, model=llm_id)
    # elif provider == "OpenAI":
    #     llm = ChatOpenAI(model_name=llm_id, temperature=0.7
    if system_prompt.strip() == "":
        system_prompt = "You are a helpful AI assistant that helps people find information."
        
    #set up tool
    search_tool = [TavilySearchResults(max_results=2, api_key=TAVILY_API_KEY)] if allow_search else []
    agent = create_react_agent(
        model=llm,
        tools=search_tool,
        prompt= system_prompt)


    state={"messages":query}

    response = agent.invoke(state)
    messages = response.get("messages")
    ai_messages = [message.content for message in messages if isinstance(message,AIMessage)]

    return ai_messages[-1]
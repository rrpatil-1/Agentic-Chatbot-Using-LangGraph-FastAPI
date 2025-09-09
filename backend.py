from pydantic import BaseModel
from typing import List
from fastapi import FastAPI
from ai_agent import get_response_from_ai


#set up pydantic model for schema validation
class RequestSate(BaseModel):
    model_name:str
    model_provider:str
    system_prompt:str
    messages:List[str]
    allow_search:bool

app = FastAPI(title="LangGraph AI Agent")

ALLOWED_MODELS_NAMES = ["qwen/qwen3-32b","llama-3.3-70b-versatile","llama-3.1-8b-instant"]

@app.post("/chat")
def chat_endpoint(request:RequestSate):
    """
    API endpoint to interact with Chatbot using LangGraph and search tool.
    it dynamically select model specify in request
    
    """
    if request.model_name not in ALLOWED_MODELS_NAMES:
        return {"error":"Invalid model name. Kindly select Valid AI Model "}
    
    llm_id = request.model_name
    provider = request.model_provider
    allow_search = request.allow_search
    system_prompt = request.system_prompt
    query = request.messages

    #get response from ai agent
    response = get_response_from_ai(llm_id,query,allow_search,system_prompt,provider)

    return response

# run and explore swagger doc
if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)
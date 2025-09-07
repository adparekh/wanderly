from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent.agentic_workflow import GraphBuilder
# from utils.export import export_trip
from starlette.responses import JSONResponse
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_wanderly(query: QueryRequest):
    try:
        print(query)
        graph = GraphBuilder(model_provider="openai")
        react_app = graph()

        flow_graph = react_app.get_graph().draw_mermaid_png()
        with open("langgraph_flow.png", "wb") as file:
            file.write(flow_graph)

        print(f"Graph saved as 'langgraph_flow.png' in {os.getcwd()}")

        messages = {"messages" : [query.question]}
        output = react_app.invoke(messages)

        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content
        else:
            final_output = str(output)

        return {"answer" : final_output}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error" : str(e)})
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Ensure the backend directory is in the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph import app as langgraph_app

api = FastAPI(title="Consulting Delivery Copilot API")

# Enable CORS for Vite frontend
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DiscoveryRequest(BaseModel):
    notes: str
    thread_id: str = "default_session"

@api.post("/generate-proposal")
async def generate_proposal(request: DiscoveryRequest):
    try:
        inputs = {"discovery_doc": request.notes}
        # Run the graph synchronously for the prototype
        # (In prod, use a background task or webhooks)
        config = {"configurable": {"thread_id": request.thread_id}}
        result = langgraph_app.invoke(inputs, config=config)
        
        return {
            "proposal": result.get("final_proposal", ""),
            "constraints": result.get("constraints", []),
            "steps": result.get("steps", []),
            "rag_context": result.get("rag_context", []),
            "tool_data": result.get("tool_data", {})
        }
    except Exception as e:
        print(f"❌ BACKEND ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=8000)

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from gateway.auth import verify_and_decode_agent_token
from pydantic import BaseModel
from typing import Any, Dict

app = FastAPI(title="Zero-Trust Multi-Agent Guardrail Gateway")
security_scheme = HTTPBearer()

class ToolExecutionPayload(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]

async def validate_agent_context(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme)
) -> dict:
    """
    Dependency Injection layer ensuring every single incoming request has 
    a highly authentic, non-expired cryptographic payload context.
    """
    try:
        token = credentials.credentials
        agent_context = verify_and_decode_agent_token(token)
        return agent_context
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.post("/gateway/execute-tool")
async def execute_tool_interceptor(
    payload: ToolExecutionPayload, 
    agent_ctx: dict = Depends(validate_agent_context)
):
    """
    The zero-trust guardrail validation point. Decouples decisions 
    from raw agent execution runtimes.
    """
    requested_tool = payload.tool_name
    allowed_tools = agent_ctx.get("allowed_tools", [])

    # Strict structural comparison check
    if requested_tool not in allowed_tools:
        raise HTTPException(
            status_code=403,
            detail=f"Security Violation: Agent '{agent_ctx['sub']}' with Session '{agent_ctx['session_id']}' "
                   f"attempted to call unauthorized tool '{requested_tool}'. Access Denied."
        )

    # In Phase 2, this will route out to Open Policy Agent (OPA) for granular parsing
    return {
        "status": "APPROVED",
        "authorized_by": "Zero-Trust-Gateway-v1",
        "execution_context": {
            "agent_id": agent_ctx["sub"],
            "session_id": agent_ctx["session_id"],
            "tool_executed": requested_tool,
            "payload_echo": payload.arguments
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


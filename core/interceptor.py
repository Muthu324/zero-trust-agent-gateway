import time
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Any, Dict
from services.auth_service import CryptographicAuthService
from tools.mock_system import InternalCorporateTools

app = FastAPI(title="Zero-Trust Multi-Agent Guardrail Gateway")
security_scheme = HTTPBearer()

class ToolExecutionPayload(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]

async def validate_agent_token_context(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme)
) -> dict:
    """Dependency Injection layer ensuring every single incoming request has a valid token."""
    try:
        token = credentials.credentials
        return CryptographicAuthService.decode_and_validate_token(token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.post("/gateway/execute-tool")
async def proxy_tool_execution(
    payload: ToolExecutionPayload, 
    agent_ctx: dict = Depends(validate_agent_context)
):
    """The explicit zero-trust gatekeeping logic layer."""
    requested_tool = payload.tool_name
    allowed_tools = agent_ctx.get("allowed_tools", [])
    current_time = time.time()

    # 1. Enforcement Check: Lifespan Check
    if agent_ctx.get("exp", 0) < current_time:
        raise HTTPException(status_code=403, detail="Security Token Violation: Context Pass Expired.")

    # 2. Enforcement Check: Cryptographic Scope Matrix Validation
    if requested_tool not in allowed_tools:
        raise HTTPException(
            status_code=403,
            detail=f"Security Matrix Breach: Agent '{agent_ctx.get('sub')}' is not authorized "
                   f"to access operation '{requested_tool}'. Connection Severed."
        )

    # 3. Dynamic Execution Router Path (Protected Route)
    if requested_tool == "fetch_user_profile":
        execution_result = InternalCorporateTools.fetch_user_profile(payload.arguments)
    elif requested_tool == "delete_system_database":
        execution_result = InternalCorporateTools.delete_system_database(payload.arguments)
    else:
        raise HTTPException(status_code=404, detail="Target system tool signature mapping missing.")

    return {
        "status": "APPROVED",
        "verified_by": "Zero-Trust-Proxy-v1",
        "execution_meta": {
            "agent_id": agent_ctx["sub"],
            "session_id": agent_ctx["session_id"],
            "payload_response": execution_result
        }
    }

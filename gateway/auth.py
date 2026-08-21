import time
from typing import List
from jose import jwt, JWTError

# In production, load this securely via environment variables or HashiCorp Vault
SECRET_KEY = "enterprise_level_super_secure_signing_key_change_in_production"
ALGORITHM = "HS256"

def generate_ephemeral_agent_token(agent_id: str, session_id: str, allowed_tools: List[str]) -> str:
    """
    Mints a short-lived (60 seconds) token bound tightly to an agent task context.
    """
    payload = {
        "iss": "agent_orchestrator",
        "sub": agent_id,
        "session_id": session_id,
        "allowed_tools": allowed_tools,
        "exp": time.time() + 60,  # Strict 60-second expiration window
        "iat": time.time()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_and_decode_agent_token(token: str) -> dict:
    """
    Validates signature, expiration, and returns the structural context payload.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise ValueError(f"Token verification failed: {str(e)}")


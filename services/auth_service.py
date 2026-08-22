import time
from typing import List
from jose import jwt, JWTError
from config.secure_env import GatewayConfig

class CryptographicAuthService:
    """Mints and verifies short-lived, context-bound cryptographic access tokens for agents."""
    
    @staticmethod
    def mint_agent_token(agent_id: str, session_id: str, allowed_tools: List[str]) -> str:
        """Binds an agent tightly to a specific, sandboxed operational task window."""
        payload = {
            "iss": "agent_orchestrator",
            "sub": agent_id,
            "session_id": session_id,
            "allowed_tools": allowed_tools,
            "exp": time.time() + GatewayConfig.TOKEN_EXPIRY_SECONDS,
            "iat": time.time()
        }
        return jwt.encode(payload, GatewayConfig.SECRET_KEY, algorithm=GatewayConfig.ALGORITHM)

    @staticmethod
    def decode_and_validate_token(token: str) -> dict:
        """Validates structural context payload integrity, signature, and expiration parameters."""
        try:
            return jwt.decode(token, GatewayConfig.SECRET_KEY, algorithms=[GatewayConfig.ALGORITHM])
        except JWTError as e:
            raise ValueError(f"Token verification failed: {str(e)}")

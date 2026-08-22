import os

class GatewayConfig:
    """Isolates signing key parameters and server listening environments."""
    # In live enterprise deployments, pull these from HashiCorp Vault or AWS Secrets Manager
    SECRET_KEY: str = "enterprise_level_super_secure_signing_key_change_in_production"
    ALGORITHM: str = "HS256"
    TOKEN_EXPIRY_SECONDS: int = 60  # Strict 60-second execution window

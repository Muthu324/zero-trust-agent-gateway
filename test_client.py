import requests
from services.auth_service import CryptographicAuthService

BASE_URL = "http://127.0.0"

def execute_zero_trust_evaluation():
    print("="*75)
    print("=== STARTING DECOUPLED ZERO-TRUST GATEWAY PIPELINE EVALUATION ===")
    print("="*75 + "\n")
    
    # Simulate central control plane minting a short-lived token for an agent
    agent_id = "support_agent_01"
    session_id = "session_usr_9921"
    authorized_scopes = ["fetch_user_profile"] # Explicitly sandboxed
    
    print(f"[*] Minting Ephemeral Token with strict allowed tool scopes: {authorized_scopes}")
    token = CryptographicAuthService.mint_agent_token(agent_id, session_id, authorized_scopes)
    headers = {"Authorization": f"Bearer {token}"}
    
    # ----------------------------------------------------
    # TEST CASE A: Authorized Path (Should Pass 200 OK)
    # ----------------------------------------------------
    valid_payload = {
        "tool_name": "fetch_user_profile",
        "arguments": {"user_id": "usr_772"}
    }
    print("\n[TEST A] Sending AUTHORIZED tool execution request...")
    res_a = requests.post(BASE_URL, json=valid_payload, headers=headers)
    print(f"↳ Gateway Response Status: {res_a.status_code}")
    print(f"↳ Gateway Payload Data:   {res_a.json()}")

    # ----------------------------------------------------
    # TEST CASE B: Out-of-Scope Execution (Should Block 403 Forbidden)
    # ----------------------------------------------------
    malicious_payload = {
        "tool_name": "delete_system_database",
        "arguments": {"confirmed": "true"}
    }
    print("\n[TEST B] Sending UNAUTHORIZED privilege escalation request...")
    res_b = requests.post(BASE_URL, json=malicious_payload, headers=headers)
    print(f"↳ Gateway Response Status: {res_b.status_code}")
    print(f"↳ Gateway Payload Data:   {res_b.json()}")
    
    print("\n" + "="*75)
    print("=== ZERO-TRUST SYSTEM GATEWAY PIPELINE VALIDATION COMPLETE ===")
    print("="*75)

if __name__ == "__main__":
    try:
        execute_zero_trust_evaluation()
    except requests.exceptions.ConnectionError:
        print("\n[Error] System connection link failed. Ensure the server module is running first:")
        print("python main.py")

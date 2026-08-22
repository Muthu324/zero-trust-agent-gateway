# 🛡️ Zero-Trust Multi-Agent Guardrail Gateway

[![Security: Zero Trust Architecture](https://shields.io)](#)
[![Design Pattern: API Proxy Interceptor](https://shields.io)](#)

## 🚀 Overview

Autonomous multi-agent ecosystems (e.g., LangGraph, CrewAI) present severe security vectors if given direct, unmediated access to system tools or organizational API channels. If an agent is hijacked via prompt injection, its access keys can be used to execute arbitrary actions.

This repository implements a production-grade, asynchronous **Zero-Trust Guardrail Gateway**. By forcing a decoupled proxy abstraction tier between your agent workers and enterprise microservices, every execution step requires context-bound, short-lived cryptographic identity validation via ephemeral tokens.

---

## 🏗️ Folder Architecture Blueprint

```text
zero-trust-gateway/
├── config/
│   └── secure_env.py    # Master Signing Keys & Expiry Configurations
├── core/
│   └── interceptor.py   # FastAPI Security Gateway Routing Engine
├── services/
│   └── auth_service.py  # Cryptographic JWT Minting & Structural Verification
├── tools/
│   └── mock_system.py   # Actual Restricted Corporate Tools / Databases
├── main.py              # Application Ingress Server Setup
└── test_client.py       # Simulated Agent Framework Execution Vector
```

---

## ⚙️ How It Works (The 0.1% Differentiation)

1. **Context-Bound Single-Use Tokens:** The orchestrator mints short-lived (60-second) JWTs containing the exact array of authorized tool scopes allowed for the agent's current atomic sub-task.
2. **Decoupled Verification Engine:** Core system endpoints are locked behind an ingress gateway middleware layer (`core/interceptor.py`). The tool code never runs unless the proxy layer confirms the signature matches.
3. **Strict Parameter Validation:** If an agent attempts an action outside its cryptographic token context, the gateway severs the request path instantly with a `403 Forbidden` error.

---

## 💻 Running the Security Matrix

1. Launch the security gateway backend server process:
   ```bash
   python main.py
   ```
2. Open a separate terminal pane and execute the validation suite:
   ```bash
   python test_client.py
   ```

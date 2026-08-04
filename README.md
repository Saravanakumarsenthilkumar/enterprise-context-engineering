# Enterprise Context Engineering - Generative AI Landing Zone

[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-brightgreen.svg)](.github/workflows/ci-cd.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)


An enterprise-ready **Context Engineering Engine** for Generative AI Landing Zones. Designed to govern, sanitize, optimize, and inject enterprise context into Large Language Model (LLM) prompts dynamically with built-in PII redaction, Role-Based Access Control (RBAC), context window truncation, semantic chunking, and full telemetry.

---

## 🌟 Core Architecture & Features

1. **Dynamic Context Building**: Intelligently assembles system prompts, user queries, retrieved vector chunks, and conversation history within tight token constraints.
2. **PII Masking & Guardrails**: Automatic detection and redaction of SSNs, Emails, Credit Cards, API Keys, and custom sensitive patterns before context leaves the enterprise boundary.
3. **Enterprise RBAC**: Ensures retrieved documents respect strict user access control lists (ACLs) and security clearance tiers.
4. **Semantic Chunking & Embedding**: Efficient text splitting with configurable overlap and metadata injection for RAG pipelines.
5. **Infrastructure as Code (IaC)**: Production-grade Terraform modules to provision secure AWS/Azure GenAI landing zones (Key Vaults, Vector DB Endpoints, API Gateways, Private Links).
6. **Observability & Audit**: Structured JSON logging and OpenTelemetry metrics for every context assembly request.

---

## 📁 Repository Structure

```
enterprise-context-engineering/
├── README.md                  # Master documentation & quickstart
├── Dockerfile                 # Multi-stage container definition
├── requirements.txt           # Python dependencies
├── docs/                      # Technical specification & deployment guides
│   ├── architecture.md
│   ├── deployment.md
│   └── context_engineering_guide.md
├── terraform/                 # Terraform IaC for GenAI Landing Zone
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── providers.tf
│   └── terraform.tfvars.example
├── src/                       # Production Python microservice source code
│   ├── config.py              # Configuration & Environment management
│   ├── api/
│   │   └── main.py            # FastAPI REST endpoints
│   ├── pipeline/
│   │   ├── chunking.py        # Document chunking logic
│   │   ├── embedding.py       # Embeddings generator
│   │   ├── retriever.py       # Vector retrieval interface
│   │   └── context_builder.py # Token-aware prompt context constructor
│   ├── security/
│   │   ├── pii_redactor.py    # Sanitization & PII masking
│   │   ├── rbac.py            # Document access control enforcement
│   │   └── guardrails.py      # Input/Output policy checks
│   └── utils/
│       ├── logger.py          # Structured JSON logging
│       └── telemetry.py       # OpenTelemetry metrics helper
├── tests/                     # Automated test suites (pytest)
│   ├── test_api.py
│   ├── test_chunking.py
│   ├── test_context_builder.py
│   └── test_guardrails.py
└── .github/
    └── workflows/
        └── ci-cd.yml          # GitHub Actions workflow for linting, testing & IaC validate
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.11+
- Docker (optional)
- Terraform >= 1.5.0 (for infrastructure deployment)

### Local Setup

#### **On Windows (PowerShell)**

1. **Clone & Create Virtual Environment**
   ```powershell
   git clone https://github.com/enterprise/context-engineering.git
   cd context-engineering
   python -m venv .venv
   ```

2. **Activate Virtual Environment**
   ```powershell
   # Unblock execution policy for current session if needed:
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   
   # Activate:
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install Dependencies & Run API Server**
   ```powershell
   python -m pip install -r requirements.txt
   python -m uvicorn src.api.main:app --reload --port 8000
   ```

---

#### **On Linux / macOS (Bash / Zsh)**

1. **Clone & Setup Environment**
   ```bash
   git clone https://github.com/enterprise/context-engineering.git
   cd context-engineering
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run API Server**
   ```bash
   uvicorn src.api.main:app --reload --port 8000
   ```

---

### 🌐 Access API Endpoints

Once the server is running, open your browser:

- **Interactive Swagger Docs (Test Endpoints)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Root Welcome Endpoint**: [http://localhost:8000/](http://localhost:8000/)
- **Health Check Endpoint**: [http://localhost:8000/health](http://localhost:8000/health)


---

## 🔒 Security & Compliance

- **Zero Trust Context Sanitation**: All incoming text passes through input guardrails and regex/heuristic PII sanitization.
- **Least Privilege Access**: User security tokens are validated against metadata tags attached to vector embeddings.
- **Audit Logging**: Fully compliant with enterprise audit standards; logs token consumption, latency, masked entities count, and tenant identifiers.

---

## 📄 License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.

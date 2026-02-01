# SimpleDiscord

### Code Architecture
```
my-project/
├── config/                  # <--- SOURCE OF TRUTH
│   └── tables.json          # Shared definition of table schemas (Keys, Attributes)
│
├── src/                     # <--- APPLICATION LOGIC (Environment Agnostic)
│   ├── my-app/              # Main application code
│   └── requirements.txt     # Python dependencies
│
├── infra/                   # <--- INFRASTRUCTURE (The "Makers")
│   ├── local/               # Tools for Local-Dev only
│   │   └── init_db.py       # Your Python script that reads tables.json & calls Boto3
│   │
│   └── terraform/           # Tools for Dev/Prod (AWS)
│       ├── main.tf          # Terraform logic (reads tables.json)
│       ├── variables.tf
│       └── envs/            # Environment specific settings
│           ├── dev.tfvars   # e.g., billing_mode = "PAY_PER_REQUEST"
│           └── prod.tfvars  # e.g., billing_mode = "PROVISIONED"
│
├── docker-compose.yml       # Defines DynamoDB-Local container
├── Taskfile.yml             # <--- THE ORCHESTRATOR (Replaces makefile)
└── .env                     # Local environment variables (GitIgnored)

my-app/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point, lifespan management
│   ├── core/
│   │   ├── config.py        # Pydantic Settings (Env vars, AWS creds)
│   │   └── exceptions.py    # Custom exception handlers
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/   # Routes (Controllers)
│   │           └── users.py
│   ├── schemas/             # Pydantic Models (Data Transfer Objects)
│   │   └── user.py          # Request/Response models
│   ├── services/            # Business Logic
│   │   └── user_service.py
│   ├── repositories/        # Database Access Layer (DynamoDB wrappers)
│   │   └── user_repo.py
│   └── db/
│       └── dynamo.py        # Aioboto3 session and client management
├── tests/
├── .env
└── pyproject.toml
```


### Setup
Dependencies:
- conda
- taskfile
```Bash
conda env create -f environment.yaml -n simple-discord
conda activate simple-discord
```
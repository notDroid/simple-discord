# Harmony Chat
A fullstack discord/slack based chat app built with FastAPI (backend) and Next.js (frontend) for learning and demonstration purposes.

### Setup
Dependencies:

1. Conda
2. Taskfile
3. Docker and Docker Compose


Create and activate the conda environment:
```bash
conda env create -f environment.yaml
conda activate harmony
python -m pip install -e backend
```

### Run and Test Locally
To run the application locally using Docker Compose, use the following commands:
```bash
task build
task run-local
```

In another terminal, run tests:
```bash
task test
```
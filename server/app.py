# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

"""
FastAPI application for the Github Triage Env Environment.
"""

from openenv.core.env_server.http_server import create_app

# IMPORTANT: use absolute imports so uvicorn can load the module
from models import GithubTriageAction, GithubTriageObservation
from server.github_triage_env_environment import GithubTriageEnvironment


# Create FastAPI app
app = create_app(
    GithubTriageEnvironment,
    GithubTriageAction,
    GithubTriageObservation,
    env_name="github_triage_env",
    max_concurrent_envs=1,
)


def main(host: str = "0.0.0.0", port: int = 8000):
    import uvicorn
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()